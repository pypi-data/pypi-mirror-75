import datetime
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize

def xnpv(rate, values, dates):
    '''Equivalent of Excel's XNPV function.

    >>> from datetime import date
    >>> dates = [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]
    >>> values = [-10000, 20, 10100]
    >>> xnpv(0.1, values, dates)
    -966.4345...
    '''
    if rate <= -1.0:
        return float('inf')
    d0 = dates[0]    # or min(dates)
    return sum([ vi / (1.0 + rate)**((di - d0).days / 365.0) for vi, di in zip(values, dates)])

def xirr(values, dates):
    '''Equivalent of Excel's XIRR function.

    >>> from datetime import date
    >>> dates = [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]
    >>> values = [-10000, 20, 10100]
    >>> xirr(values, dates)
    0.0100612...
    '''
    try:
        return scipy.optimize.brentq(lambda r: xnpv(r, values, dates), -0.999, 1e10)
    except RuntimeError:    # Failed to converge?
        return scipy.optimize.newton(lambda r: xnpv(r, values, dates),  x0=0.0, maxiter=40)

class AIPCalculator(object):

    def __init__(self, arr, start_date, end_date, stop_profit=None, strategy=None,
                 amt_bench=1000, mode='1w', mode_offset=0, purchase_rate=0.001, redeem_rate=0.001):
        self.arr = arr.dropna()
        self.start_date = max(start_date, self.arr.index[0])
        self.end_date = end_date or datetime.datetime.now().date()
        self.amt_bench = amt_bench
        self.mode = mode
        self.mode_offset = mode_offset
        self.yearly_multiplier = self.get_yearly_multiplier(mode)
        self.purchase_rate = purchase_rate
        self.redeem_rate = redeem_rate
        self.stop_profit = stop_profit
        # calc
        self.last_trade_day = None
        self.moving_average = None
        if strategy:
            if strategy.startswith('ma'):
                window_size = int(strategy[2:])
                self.moving_average = self.arr.rolling(window_size).mean().fillna(0)
                self.vol_10 = self.arr.pct_change(1).rolling(10).std().fillna(0)
                
    def get_yearly_multiplier(self, mode):
        m = None
        if mode == '1d':
            m = 365
        elif mode == '1w':
            m = 52
        elif mode == '2w':
            m = 26
        elif mode == '1m':
            m = 12
        else:
            raise Exception(f'unexpected trade mode: {mode}')
        return m

    # 判断是否当前要进行交易
    def is_to_trade(self, dt):
        if self.mode == '1d':
            return True
        elif self.mode == '1w':
            return dt.weekday() == self.mode_offset
        elif self.mode == '2w':
            return dt.weekday() == self.mode_offset and (self.last_trade_day is None or (dt - self.last_trade_day).days > 7)
        elif self.mode == '1m':
            return dt.day == self.mode_offset + 1
        else:
            raise Exception('unexpected trade mode: ' + self.mode)
    
    def convert_irr(self, irr):
        return pow(irr + 1, self.yearly_multiplier) - 1
        
    def convert_ret(self, ret):
        days = (self.end_date - self.start_date).days
        return pow(ret + 1, 365 / days) - 1

    def _mv_multiplier(self, val, ma, vol_10):
        if ma == 0:
            return 1
        diff = (val - ma) / ma
        if diff > 0:
            if diff <= 0.15:
                return 0.9
            elif diff <= 0.5:
                return 0.8
            elif diff <= 1:
                return 0.7
            else:
                return 0.6
        else:
            diff = abs(diff)
            if diff <= 0.05:
                return 0.6 if vol_10 > 0.05 else 1.6
            elif diff <= 0.1:
                return 0.7 if vol_10 > 0.05 else 1.7
            elif diff <= 0.2:
                return 0.8 if vol_10 > 0.05 else 1.8
            elif diff <= 0.3:
                return 0.9 if vol_10 > 0.05 else 1.9
            elif diff <= 0.4:
                return 1.0 if vol_10 > 0.05 else 2.0
            else:
                return 1.1 if vol_10 > 0.05 else 2.1

    def get_amt(self, cur_date):
        if self.moving_average is not None:
            ma = self.moving_average[:cur_date][-1]
            vol_10 = self.vol_10[:cur_date][-1]
            val = self.arr[:cur_date][-1]
            m = self._mv_multiplier(val, ma, vol_10)
            return self.amt_bench * m
        else:
            return self.amt_bench

    def run(self):
        self.res = []

        cur_date = self.start_date
        arr_idx = 0

        self.cur_mv = [0] # 当前基金资产市值
        self.vol = [0] # 份额
        self.tot_inv_amt = [0] # 总投资额
        self.trd_count = [0] # 总投资次数
        self.redeem_amt = []
        self.redeem_date = []
        self.redeem_ret = []
        self.redeem_gain = []
        avg_cost = 0 # 平均投资成本

        self.irr_helper = ([], [])
        amt_to_trade = 0

        last_trade_mv = 0

        while cur_date < self.end_date:
            while self.arr.index[arr_idx] < cur_date and arr_idx < len(self.arr.index) - 1:
                arr_idx += 1

            if self.is_to_trade(cur_date):
                amt_to_trade += self.get_amt(cur_date)
                self.irr_helper[0].append(amt_to_trade)
                self.irr_helper[1].append(cur_date)

            if self.arr.index[arr_idx] == cur_date:
                # 交易日
                p = self.arr[arr_idx]

                # 1. 处理正常的买入工作
                if amt_to_trade > 0:
                    # update data
                    self.trd_count[-1] += 1
                    _tot_cost = sum(self.tot_inv_amt) * avg_cost
                    self.tot_inv_amt[-1] += amt_to_trade
                    self.vol[-1] += amt_to_trade * (1 - self.purchase_rate) / p
                    avg_cost = (_tot_cost + amt_to_trade * p) / sum(self.tot_inv_amt)
                    self.res.append({'dt': cur_date, 'amt_to_trade': amt_to_trade, 'cur_mv': self.cur_mv[-1], 'tot_inv_amt': self.tot_inv_amt[-1], 'avg_cost': avg_cost, 'p': p})
                    last_trade_price = p
                    amt_to_trade = 0
                    # print(f'[{cur_date}] (tot){_tot_cost} (avg){avg_cost} (tot_inv_amt){str(self.tot_inv_amt)}')

                # 更新 当前基金资产市值
                self.cur_mv[-1] = self.vol[-1] * p

                # 止盈逻辑
                if self.stop_profit:
                    rate = self.cur_mv[-1] / self.tot_inv_amt[-1] - 1 if self.tot_inv_amt[-1] > 0 else 0
                    if rate >= self.stop_profit:
                        next_idx = arr_idx + 1 if arr_idx + 1 < len(self.arr) else arr_idx
                        next_p = self.arr[next_idx]
                        redeem_amt = self.vol[-1] * next_p * (1 - self.redeem_rate)
                        self.redeem_amt.append(redeem_amt)
                        self.redeem_date.append(cur_date)
                        #self.redeem_ret.append(rate)
                        self.redeem_ret.append(redeem_amt / self.tot_inv_amt[-1])
                        self.redeem_gain.append(redeem_amt - self.tot_inv_amt[-1])
                        self.cur_mv.append(0)
                        self.vol.append(0)
                        self.tot_inv_amt.append(0)
                        self.trd_count.append(0)
                        self.irr_helper[0].append(-1 * redeem_amt)
                        self.irr_helper[1].append(cur_date)
                        # irr_helper[1].append(self.arr.index[next_idx])

            cur_date += datetime.timedelta(days=1)

        # stat
        self.irr_helper[0].append(-1 * (self.cur_mv[-1] + amt_to_trade)) #如果终止定投前，到了月初投入一笔前，但是一直没到交易日，没有买入资产，这笔前进入了irr_helper，但是没有进入 资产里。终止定投取钱，会少最后一笔
        self.irr_helper[1].append(self.end_date)
        self.irr = xirr(self.irr_helper[0], self.irr_helper[1])
        self.tot_mv = self.cur_mv[-1] + sum(self.redeem_amt)
        self.tot_ret = (self.tot_mv) / sum(self.tot_inv_amt) - 1
        self.ret = self.convert_ret(self.tot_ret)
        self.tot_gain = self.tot_mv - sum(self.tot_inv_amt)
        #print(f'(irr){self.irr} (cur_mv){self.tot_mv} (tot_inv_amt){sum(self.tot_inv_amt)} (ret){self.ret} (cnt){sum(self.trd_count)} (tot_ret){self.tot_ret} (tot_gain){self.tot_gain}')
        '''
        if self.stop_profit:
            print('cur_mv', self.cur_mv)
            print('tot_inv_amt', self.tot_inv_amt)
            for i in range(0, len(self.redeem_amt)):
                print(f'{self.redeem_date[i]} (ret){self.redeem_ret[i]} (inv){self.tot_inv_amt[i]} (gain){self.redeem_gain[i]} (amt){self.redeem_amt[i]}')
        '''
    def get_irr(self):
        #self.res = []
        cur_date = self.start_date
        arr_idx = 0
        self.cur_mv = 0 # 当前基金资产市值
        self.vol = 0 # 份额
        self.tot_inv_amt = 0 # 总投资额
        self.irr_helper = ([], [])
        amt_to_trade = 0
        while cur_date < self.end_date:
            while self.arr.index[arr_idx] < cur_date and arr_idx < len(self.arr.index) - 1:
                arr_idx += 1

            if self.is_to_trade(cur_date):
                amt_to_trade += self.get_amt(cur_date)
                self.irr_helper[0].append(amt_to_trade)
                self.irr_helper[1].append(cur_date)

            if self.arr.index[arr_idx] == cur_date:
                # 交易日
                p = self.arr[arr_idx]

                # 1. 处理正常的买入工作
                if amt_to_trade > 0:
                    self.tot_inv_amt += amt_to_trade
                    self.vol += amt_to_trade * (1 - self.purchase_rate) / p
                    amt_to_trade = 0

                # 更新 当前基金资产市值
                self.cur_mv = self.vol * p

                # 止盈逻辑
                if self.stop_profit:
                    rate = self.cur_mv / self.tot_inv_amt - 1 if self.tot_inv_amt > 0 else 0
                    if rate >= self.stop_profit:
                        next_idx = arr_idx + 1 if arr_idx + 1 < len(self.arr) else arr_idx
                        next_p = self.arr[next_idx]
                        redeem_amt = self.vol * next_p * (1 - self.redeem_rate)
                        self.cur_mv=0
                        self.vol=0
                        self.tot_inv_amt=0
                        self.irr_helper[0].append(-1 * redeem_amt)
                        self.irr_helper[1].append(cur_date)

            cur_date += datetime.timedelta(days=1)

        # stat
        self.irr_helper[0].append(-1 * (self.cur_mv + amt_to_trade))
        self.irr_helper[1].append(self.end_date)
        self.irr = xirr(self.irr_helper[0], self.irr_helper[1])
        return self.irr

    def get_aip_total_return(self):
        cash_flow = self.irr_helper[0]
        cash_inputs = [i for i in cash_flow if i > 0]
        cash_outputs = [i for i in cash_flow if i < 0]
        return (-sum(cash_outputs) / sum(cash_inputs)) - 1

    def get_fund_ret(self):
        _arr = self.arr[self.start_date:self.end_date]
        return _arr[-1] / _arr[0] - 1

    def get_fund_vol(self):
        _arr = self.arr[self.start_date:self.end_date]
        return _arr.pct_change(1).std(ddof=1)

    def get_cash_flow(self):
        dic = {'datetime':self.irr_helper[1], 'cash_flow':self.irr_helper[0]}
        return pd.DataFrame(dic)

    def plot(self):
        df_net_arr = pd.DataFrame(self.res).set_index('dt')[['p', 'avg_cost']]
        df_net_arr.plot.line(figsize=(12,6))
        plt.legend(fontsize=15)
        plt.title('price vs avg_cost',fontsize=25)
        plt.show()
