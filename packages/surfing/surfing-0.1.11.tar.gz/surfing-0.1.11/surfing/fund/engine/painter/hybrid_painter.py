import pandas as pd
import numpy as np
import platform
import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.dates as mdates
from ....util.calculator import Calculator
from matplotlib.patches import Rectangle
CURRENT_PLATFORM = platform.system()
if CURRENT_PLATFORM == 'Darwin':
    mpl.rcParams['font.family'] = ['Heiti TC']
else:
    mpl.rcParams['font.family'] = ['STKaiti']
    
pd.plotting.register_matplotlib_converters()
class HybridPainter(object):

    @staticmethod
    def plot_market_value(mv_df:pd.DataFrame, backtest_type:str, index_price:pd.DataFrame, saa_weight:dict, bk_stats:dict):
        index_df_raw = index_price.loc[mv_df.index[0]:mv_df.index[-1],]
        index_df = index_df_raw.copy().fillna(method='bfill')
        index_df = index_df / index_df.iloc[0]
        index_df['cash'] = 1
        w_l = []
        for idx, r in index_df_raw.iterrows():
            nan_asset = [k for k, v in r.to_dict().items() if np.isnan(v)]
            wgts = saa_weight.copy()
            for k in nan_asset:
                wgts[k] = 0
            s = sum([v  for k,v in wgts.items()])
            wgts = {k :v /s for k, v in wgts.items()}
            wgts['datetime'] = idx
            w_l.append(wgts)
        wgts_df = pd.DataFrame(w_l).set_index('datetime')
        mv_df['benchmark'] = (wgts_df * index_df).sum(axis = 1)
        mv_df = mv_df / mv_df.iloc[0]
        mv_df.plot.line(figsize=(20,12),legend=False,fontsize = 17)
        l = pl.legend(loc='lower left',fontsize = 17)
        s = pl.title(f'{backtest_type} market value', fontsize=20)
        ar = round(bk_stats['annual_ret'],4)
        mdd = round(bk_stats['mdd'], 4)
        sharpe = round(bk_stats['sharpe'],4)
        pl.suptitle(f'annual_ret : {ar} mdd : {mdd} sharpe : {sharpe}',y=0.87,fontsize=17)
        plt.grid()

    @staticmethod
    def plot_market_value_with_mdd_analysis(mv_df:pd.DataFrame, backtest_type:str, index_price:pd.DataFrame, saa_weight:dict, bk_stats:dict):
        def get_mdd_result_from_df(df:pd.DataFrame,
                                    date_column: str,
                                    value_column: str):
            dates = df[date_column].values
            values = df[value_column].values
            return mdd_recover_analysis(values,dates)

        def mdd_recover_analysis(values,dates):
            sr = pd.Series(values, index=dates).sort_index()
            if sr.empty:
                mdd = 0
                mdd_date1 = None
                mdd_date2 = None
                mdd_lens = 0
                return mdd, mdd_date1, mdd_date2, mdd_lens
            mdd_part =  sr[:] / sr[:].rolling(window=sr.shape[0], min_periods=1).max()
            mdd = 1 - mdd_part.min()
            if mdd == 0:
                mdd_date1 = None
                mdd_date2 = None
                mdd_lens = 0
            else:
                mdd_date = mdd_part.idxmin()
                mdd_date1 = sr[:mdd_date].idxmax()
                sr_tmp = sr[mdd_date1:]
                recover_sr = sr_tmp[sr_tmp> sr[mdd_date1]]
                if recover_sr.empty:
                    mdd_date2 = sr_tmp.index[-1]
                else: 
                    mdd_date2 = sr_tmp[sr_tmp> sr[mdd_date1]].index[0]
                mdd_lens = sr.loc[mdd_date1:mdd_date2].shape[0]
            return mdd, mdd_date1, mdd_date2, mdd_lens
                
        def plot_mdd_recover(mdd_date1_1, mdd_date1_2, df, c, ax):
            start = mdates.date2num(mdd_date1_1)
            end = mdates.date2num(mdd_date1_2)
            width = end - start
            price_max = df.loc[mdd_date1_1: mdd_date1_2].mv.max()
            bottom = df.loc[mdd_date1_1: mdd_date1_2].mv.min()
            height = price_max - bottom
            rect = Rectangle((start, bottom), width, height, color=c)
            ax.add_patch(rect)   

        def print_st(mdd):
            return str(round(mdd * 100,2)) + '%' 
            
        
        mdd1, mdd_date1_1, mdd_date1_2, mdd_lens1 = get_mdd_result_from_df(mv_df.reset_index(),'date','mv')
        mv_df_1 = mv_df.loc[:mdd_date1_1].reset_index()
        mv_df_2 = mv_df.loc[mdd_date1_2:].reset_index()

        mdd2, mdd_date2_1, mdd_date2_2, mdd_lens2 = get_mdd_result_from_df(mv_df_1,'date','mv')
        mdd3, mdd_date3_1, mdd_date3_2, mdd_lens3 = get_mdd_result_from_df(mv_df_2,'date','mv')
        if mdd3 > mdd2:
            mdd2 = mdd3
            mdd_date2_1 = mdd_date3_1
            mdd_date2_2 = mdd_date3_2
            mdd_lens2 = mdd_lens3
             
        index_df_raw = index_price.loc[mv_df.index[0]:mv_df.index[-1],]
        index_df = index_df_raw.copy().fillna(method='bfill')
        index_df = index_df / index_df.iloc[0]
        index_df['cash'] = 1
        w_l = []
        for idx, r in index_df_raw.iterrows():
            nan_asset = [k for k, v in r.to_dict().items() if np.isnan(v)]
            wgts = saa_weight.copy()
            for k in nan_asset:
                wgts[k] = 0
            s = sum([v  for k,v in wgts.items()])
            wgts = {k :v /s for k, v in wgts.items()}
            wgts['datetime'] = idx
            w_l.append(wgts)
        wgts_df = pd.DataFrame(w_l).set_index('datetime')
        mv_df['benchmark'] = (wgts_df * index_df).sum(axis = 1)
        df = mv_df / mv_df.iloc[0]
        fig, ax = plt.subplots(figsize= [20,12])
        plt.plot(df.index, df['mv'], label = 'mv', linewidth=2.0)
        plt.plot(df.index, df['benchmark'], label = 'benchmark', linewidth=2.0)
        
        ar = print_st(bk_stats['annual_ret'])
        av = print_st(bk_stats['annual_vol'])
        sharpe = round(bk_stats['sharpe'],2)

        st1 = f'annual_ret : {ar} annual_vol : {av} sharpe : {sharpe}'
        st2 = f'first mdd {print_st(mdd1)} {mdd_date1_1} : {mdd_date1_2}, {mdd_lens1} days'
        st3 = f'second mdd {print_st(mdd2)} {mdd_date2_1} : {mdd_date2_2}, {mdd_lens2} days'
        st = st1 + '\n' + st2 + '\n' + st3
        plt.legend(fontsize=20 ,loc = 'upper left')
        plt.title(f'market values ', fontsize=30)
        plt.suptitle(st, y=0.87, fontsize=18)
        plot_mdd_recover(mdd_date1_1, mdd_date1_2, df, 'silver', ax)
        plot_mdd_recover(mdd_date2_1, mdd_date2_2, df, 'gainsboro', ax)
        plt.grid() 
        plt.show()

    @staticmethod
    def plot_asset_fund_mv_diff(asset_mv:pd.DataFrame, fund_mv:pd.DataFrame):
        asset_mv = asset_mv[['mv']]
        fund_mv = fund_mv[['mv']]
        asset_mv.columns = ['asset_mv']
        fund_mv.columns = ['fund_mv']
        check_diff = fund_mv.join(asset_mv)
        check_diff = check_diff / check_diff.iloc[0]
        check_diff['diff'] = 100 * (check_diff['fund_mv']  - check_diff['asset_mv']) / check_diff['asset_mv'] 
        check_diff[['fund_mv','asset_mv']].plot.line(figsize=(20,12),legend=False,fontsize = 17)
        l = pl.legend(loc='lower left',fontsize = 17)
        s = pl.title('asset and fund market value ', fontsize=20)
        plt.grid()
        check_diff[['diff']].plot.line(figsize=(20,12),legend=False,fontsize = 17)
        l = pl.legend(loc='lower left',fontsize = 17)
        s = pl.title('asset and fund market value diff % ', fontsize=20)
        plt.grid() 
        plt.show()

    @staticmethod
    def plot_four_layers_mv(mv_df:pd.DataFrame):
        mv_df = mv_df / mv_df.iloc[0]
        mv_df.plot.line(color=['C3','C1','C2','C0'],figsize=(14,8))
        plt.title('净值对比', fontsize=20)
        plt.legend(loc='upper left', fontsize=15)
        plt.grid() 
        plt.show()

    @staticmethod
    def plot_asset_price_ratio(fund_nav:pd.DataFrame, 
                        fund_info:pd.DataFrame, 
                        index_price:pd.DataFrame,
                        score_dict:dict,
                        backtest_result:dict,
                        dts:pd.Series,
                        saa:dict,
                        ):
        
        proper_number_dict = {'mmf':1} 
        for asset, w in saa.items():
            if asset in ['cash','mmf'] or w == 0:
                continue
            num = min(int(round(w / 0.05, 0)) , 4)
            proper_number_dict[asset] = num
        
        fund_info['trade_fee'] = fund_info['purchase_fee'] + fund_info['redeem_fee']
        fee_df = fund_info[['fund_id','trade_fee']].set_index('fund_id')
        dts = dts[(dts >=fund_nav.index[0]) & (dts <= fund_nav.index[-1])]
        fund_nav = fund_nav.reindex(dts)
        index_price = index_price.reindex(dts)
        rebalance_date = backtest_result['rebalance_date'] + [backtest_result['market_value'].index.tolist()[-1]]
        fund_desc_name = fund_info[['fund_id','desc_name']].set_index('fund_id').to_dict()['desc_name']  
        res = {}
        for idx, begin_date in enumerate(rebalance_date[:-1]):
            end_date = rebalance_date[idx + 1]
            for asset, num in proper_number_dict.items():
                #print(asset, num)
                _score_dict = score_dict[begin_date][asset]
                _score_list = sorted(_score_dict.items(), key=lambda x:x[1], reverse=True)
                _fund_list = [i[0] for i in _score_list]
                dic = {
                    'index_id':asset,
                    'begin_date':begin_date,
                    'end_date':end_date,
                    'fund_list':_fund_list[:proper_number_dict[asset]]
                }
                if asset in res:
                    res[asset].append(dic)
                else:
                    res[asset] = [dic]
        _res = []
        for index_id in res:
            _index_id_res = []
            for date_dic in res[index_id]:
                fund_nav_i = fund_nav.loc[date_dic['begin_date']:date_dic['end_date'],date_dic['fund_list']]
                for fund_id in fund_nav_i:
                    fund_i_fee = fee_df.loc[fund_id,'trade_fee']
                    fee_discount_l = np.linspace(1,1-fund_i_fee,fund_nav_i.shape[0])
                    fund_nav_i[fund_id] = fund_nav_i[fund_id] * fee_discount_l
                fund_ret_combine = pd.DataFrame(fund_nav_i.pct_change(1).mean(axis=1).dropna())
                _index_id_res.append(fund_ret_combine)
            fund_combine_rets = pd.concat(_index_id_res).rename(columns={0:'funds'})
            index_ret = index_price[[index_id]].loc[rebalance_date[0]: rebalance_date[-1]].pct_change(1).dropna()
            price_ratio_index = (fund_combine_rets.join(index_ret)+1).cumprod()
            price_ratio_index = pd.DataFrame(price_ratio_index['funds'] / price_ratio_index[index_id]).rename(columns={0:index_id})
            _res.append(price_ratio_index)
        df_plot = pd.concat(_res, axis=1, sort=False)
        res = []
        for index_id in df_plot:
            _index_stats = Calculator.get_stat_result_from_df(df=df_plot.reset_index(), date_column='datetime', value_column=index_id).__dict__
            _index_stats['index_id'] = index_id 
            res.append(_index_stats)
        
        stats = pd.DataFrame(res).set_index('index_id')[['annualized_ret','annualized_vol','mdd','sharpe','mdd_date1','mdd_date2']]
        df_plot.plot.line(figsize=(14,8))
        plt.title('基金所属各资产价格比',fontsize=20)
        plt.legend(loc='upper left', fontsize=15)
        plt.grid()
        plt.show()
        return stats