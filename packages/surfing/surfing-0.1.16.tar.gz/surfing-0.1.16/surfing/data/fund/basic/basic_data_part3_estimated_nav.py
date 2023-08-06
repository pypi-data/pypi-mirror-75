
import datetime
import traceback
import pandas as pd

from ...api.raw import RawDataApi
from ...api.basic import BasicDataApi
from ...view.basic_models import *
from .basic_data_helper import BasicDataHelper


class BasicDataPart3:

    def __init__(self, data_helper: BasicDataHelper):
        self._data_helper = data_helper

    def _get_yesterday(self):
        yesterday = datetime.datetime.today() - datetime.timedelta(days = 1)
        yesterday_str = datetime.datetime.strftime(yesterday, '%Y%m%d')
        print(f'yesterday: {yesterday_str}')
        return yesterday_str

    def rq_stock_code_to_em(self, rq_stock_code):
        if not rq_stock_code:
            return None
        em_stock_code = rq_stock_code.replace("XSHG", "SH")
        em_stock_code = rq_stock_code.replace("XSHE", "SZ")
        return em_stock_code

    def load_fund_stock(self):
        fund_stock_df = BasicDataApi().get_fund_hold_stock()
        # print(f'fund_stock_df\n {fund_stock_df}')
        fund_stock_info_list = [(fund_stock_df.columns.get_loc(f'rank{i}_stock_code'), 
            fund_stock_df.columns.get_loc(f'rank{i}_stockweight')) for i in range(1,11,1)]
        fund_stock = {}
        for row in fund_stock_df.itertuples(index=False):
            stock_info = []
            for fund_stock_info in fund_stock_info_list:
                if not row[fund_stock_info[0]]:
                    break
                stock_info.append([row[fund_stock_info[0]], row[fund_stock_info[1]]])
            if not stock_info:
                continue
            fund_stock[row.fund_id] = stock_info
        return fund_stock

    def load_fund_nav(self, dt):
        fund_nav_df = BasicDataApi().get_fund_nav(dt=dt)
        # print(f'fund_nav_df\n {fund_nav_df}')
        fund_nav = {}
        for row in fund_nav_df.itertuples(index=False):
            fund_nav[row.fund_id] = [row.unit_net_value, row.acc_net_value, row.adjusted_net_value]
        return fund_nav

    def load_stock_minute(self, stock_minute_df=None):
        if not stock_minute_df:
            stock_minute_df = RawDataApi().get_rq_stock_minute()
        # print(f'stock_minute_df\n {stock_minute_df}')
        if stock_minute_df is None or stock_minute_df.empty:
            return None

        curr_datetime = stock_minute_df.iloc[0].datetime
        
        stock_minute = {}
        for row in stock_minute_df.itertuples(index=False):
            em_stock_code = self.rq_stock_code_to_em(row.order_book_id)
            if not em_stock_code:
                continue
            stock_minute[em_stock_code] = row.close
        return curr_datetime, stock_minute

    def load_stock_price(self, dt):
        em_stock_price_df = RawDataApi().get_em_stock_price(dt, dt, columns=['close'])
        # print(f'em_stock_price_df\n {em_stock_price_df}')
        stock_price = {}
        for row in em_stock_price_df.itertuples(index=False):
            stock_price[row.stock_id] = row.close
        return stock_price

    def delta_estimated(self, stock_weight, stock_price_yesterday, stock_price_now):
        return stock_weight / 100.0 * (stock_price_now / stock_price_yesterday - 1)

    def calc_fund_estimated_nav(self, stock_minute_df=None):
        try:
            stock_minute_parse_result = self.load_stock_minute(stock_minute_df)
            if not stock_minute_parse_result:
                return False
            curr_datetime, stock_minute = stock_minute_parse_result
            fund_stock = self.load_fund_stock()

            yesterday = self._get_yesterday()
            fund_nav_yesterday = self.load_fund_nav(yesterday)
            stock_price_yesterday = self.load_stock_price(yesterday)

            res = []
            for fund_id, stock_list in fund_stock.items():
                if fund_id not in fund_nav_yesterday:
                    continue

                ratio = 1.0
                for stock in stock_list:
                    if stock[0] not in stock_price_yesterday or stock[0] not in stock_minute:
                        continue
                    curr_stock_price_yesterday = stock_price_yesterday[stock[0]]
                    curr_stock_price_now = stock_minute[stock[0]]

                    # WARNING: this stock component weight is not evaluated at YESTERDAY!!!
                    # TODO: re-calc stock component weight for yesterday to get a more accurate estimation!
                    ratio += self.delta_estimated(
                        stock[1], curr_stock_price_yesterday, curr_stock_price_now)

                unit_net_value_estimated = fund_nav_yesterday[fund_id][0] * ratio
                acc_net_value_estimated = fund_nav_yesterday[fund_id][1] * ratio
                adjusted_net_value_estimated = fund_nav_yesterday[fund_id][2] * ratio
                # print(f'unit_net_value_estimated: {unit_net_value_estimated}')
                # print(f'acc_net_value_estimated: {acc_net_value_estimated}')
                # print(f'adjusted_net_value_estimated: {adjusted_net_value_estimated}')
                res.append([fund_id, unit_net_value_estimated, acc_net_value_estimated, adjusted_net_value_estimated, curr_datetime])
                # print(res)
                # # For debug only
                # if input() == '':
                #     break
            result_df = pd.DataFrame(res, columns = ['fund_id', 'unit_net_value', 'acc_net_value', 'adjusted_net_value', 'datetime']) 
            print(result_df)
            self._data_helper._upload_basic(result_df, FundEstimatedNav.__table__.name)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False


if __name__ == '__main__':
    bdp = BasicDataPart3(BasicDataHelper())

