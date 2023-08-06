
from typing import List, Dict
import pandas as pd
import numpy as np
import traceback
import math
import json
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from .derived_data_helper import DerivedDataHelper
from ...api.basic import BasicDataApi
from ...view.derived_models import FundScoreExtended


class FundScoreExtendedProcess:

    # 无风险收益率
    _RF = 0.011

    def __init__(self, data_helper: DerivedDataHelper):
        self._data_helper = data_helper
        self._basic_api = BasicDataApi()

    def init(self, start_date: str, end_date: str):
        start_date: str = (pd.to_datetime(start_date) - datetime.timedelta(days=365*3+1)).strftime('%Y%m%d')
        print(f'start date for calc: {start_date}')
        self._end_date: str = end_date

        # 获取区间内交易日列表
        all_trading_days: pd.Series = self._basic_api.get_trading_day_list().drop(columns='_update_time').set_index('datetime')
        self._trading_days: pd.Series = all_trading_days.loc[pd.to_datetime(start_date).date():pd.to_datetime(end_date).date()]

        # 基金净值数据、指数价格数据的index对齐到交易日列表
        fund_nav: pd.DataFrame = self._basic_api.get_fund_nav_with_date(start_date, end_date)
        self._fund_nav: pd.DataFrame = fund_nav.pivot_table(index='datetime', columns='fund_id', values='adjusted_net_value').reindex(self._trading_days.index).fillna(method='ffill')
        index_price: pd.DataFrame = self._basic_api.get_index_price().drop(columns='_update_time')
        # 有的index最近没有数据，如活期存款利率/各种定期存款利率等，需要先reindex到全部的交易日列表上ffill
        index_price = index_price.pivot_table(index='datetime', columns='index_id', values='close').reindex(all_trading_days.index).fillna(method='ffill')
        # 再reindex到参与计算的交易日列表上
        self._index_price: pd.DataFrame = index_price.reindex(self._trading_days.index)
        pd.testing.assert_index_equal(self._fund_nav.index, self._index_price.index)

        try:
            # 这个指数有一天的点数是0，特殊处理一下
            self._index_price['spi_spa'] = self._index_price['spi_spa'].where(self._index_price.spi_spa != 0).fillna(method='ffill')
        except KeyError:
            pass

        # 对数净值取差分并且去掉第一个空值，得到基金对数收益率数列
        self._fund_ret: pd.DataFrame = np.log(self._fund_nav).diff().iloc[1:, :]

        # 计算benchmark return，且index对齐到fund_ret
        benchmark_ret: pd.DataFrame = self._get_benchmark_return()
        self._benchmark_ret: pd.DataFrame = benchmark_ret.reindex(self._fund_ret.index)
        pd.testing.assert_index_equal(self._fund_ret.index, self._benchmark_ret.index)

        # 获取待计算的基金列表
        fund_list: pd.DataFrame = self._basic_api.get_fund_info().drop(columns='_update_time')
        self._fund_list: pd.DataFrame = fund_list[fund_list.structure_type <= 1]
        # 获取wind一级分类
        self._wind_class_1: np.ndarray = fund_list.wind_class_1.unique()

    def _get_benchmark_return(self) -> pd.DataFrame:
        benchmark_list: Dict[str, float] = {}
        fund_benchmark_df: pd.DataFrame = self._basic_api.get_fund_benchmark().drop(columns='_update_time')
        # 遍历每一只基金的benchmark进行处理
        for row in fund_benchmark_df.itertuples(index=False):
            values: List[pd.Series] = []
            cons: float = 0
            # 空的benchmark表明我们没有对应的指数或无法解析公式
            if row.benchmark_s:
                benchmark: Dict[str, float] = json.loads(row.benchmark_s)
                benchmark_raw: Dict[str, float] = eval(row.benchmark)
                for (index, weight), index_raw in zip(benchmark.items(), benchmark_raw.keys()):
                    if index_raw == 1:
                        # 表示benchmark中该项为常数
                        cons += weight
                    elif index_raw.startswith('RA000'):
                        if weight == -1:
                            # 表示我们无法解析公式
                            print(f'[benchmark_return] Error: Need fix {row.fund_id} {index} {index_raw}')
                        else:
                            try:
                                ra: pd.Series = self._index_price.loc[:, index]
                            except KeyError:
                                # 表示我们没有该指数的价格数据
                                print(f'[benchmark_return] Error: Data Missing: {row.fund_id} {index} {index_raw}')
                            else:
                                values.append(ra.iloc[1:] * 0.01 * weight)
                    else:
                        if weight == -1:
                            # 表示我们无法解析公式
                            print(f'[benchmark_return] Error: Need fix {row.fund_id} {index} {index_raw}')
                        else:
                            try:
                                ra: pd.Series = self._index_price.loc[:, index]
                            except KeyError:
                                # 表示我们没有该指数的价格数据
                                print(f'Error: Data Missing: {row.fund_id} {index} {index_raw}')
                            else:
                                ra = np.log(ra).diff().iloc[1:]
                                values.append(ra * weight)
            if values or cons:
                benchmark_list[row.fund_id] = sum(values) + cons
            else:
                benchmark_list[row.fund_id] = np.nan
        return pd.DataFrame.from_dict(benchmark_list)

    '''
    _get_resample_ret
    输入：日频率数据
    输出：月频率数据
    备注：输入需要DatetimeIndex
    '''
    @staticmethod
    def _get_resample_ret(df: pd.DataFrame) -> pd.DataFrame:
        df = df.set_axis(pd.to_datetime(df.index), inplace=False)
        return df.resample('1M').sum(min_count=1)

    @staticmethod
    def _lambda_2(x: pd.Series, fund_ret_sampled: pd.DataFrame):
        temp: float = x.var()
        if pd.isnull(temp):
            return np.nan
        elif temp == 0:
            return 0

        fund_ret: pd.Series = fund_ret_sampled[x.name]
        if fund_ret.count() <= 1:
            return np.nan
        return x.cov(fund_ret) / temp

    @staticmethod
    def _lambda_1(x: pd.Series, fund_ret_sampled: pd.DataFrame):
        total = pd.concat({'Y': fund_ret_sampled[x.name], 'x': x}, axis=1)
        total = total[total.notna().all(axis=1)]
        if total.empty:
            return np.nan
        Y: pd.Series = total['Y']
        x = total['x']
        if x.count() != Y.count():
            return np.nan
        X: pd.DataFrame = pd.concat([x, x], axis=1)
        X.columns = [0, 1]
        X[0][X[0] < 0] = 0
        X[1][X[1] > 0] = 0
        regr = LinearRegression()
        regr.fit(X, Y)
        return regr.coef_[0] - regr.coef_[1]

    def calc(self):
        # 计算月度数据
        fund_ret_sampled: pd.DataFrame = FundScoreExtendedProcess._get_resample_ret(self._fund_ret)
        benchmark_ret_sampled: pd.DataFrame = FundScoreExtendedProcess._get_resample_ret(self._benchmark_ret)
        # 对齐基金收益和benchmark收益的月度数据的columns
        avail_fund_list: pd.Index = fund_ret_sampled.columns.intersection(benchmark_ret_sampled.columns)
        fund_ret_sampled = fund_ret_sampled.loc[:, avail_fund_list]
        benchmark_ret_sampled = benchmark_ret_sampled.loc[:, avail_fund_list]
        pd.testing.assert_index_equal(fund_ret_sampled.columns, benchmark_ret_sampled.columns)
        pd.testing.assert_index_equal(fund_ret_sampled.index, benchmark_ret_sampled.index)

        # beta
        beta = benchmark_ret_sampled.apply(self._lambda_2, fund_ret_sampled=fund_ret_sampled)

        # sharpe_ratio_M
        annualized_ret = fund_ret_sampled.sum(min_count=1) * 12 / fund_ret_sampled.shape[0]
        annualized_vol_0 = fund_ret_sampled.std(ddof=0) * math.sqrt(12)
        sharpe_ratio_M = (annualized_ret - self._RF) / annualized_vol_0

        # information_ratio
        ex_ret = fund_ret_sampled - benchmark_ret_sampled
        annualized_ex_ret = ex_ret.sum(min_count=1) * 12 / fund_ret_sampled.shape[0]
        annualized_vol_1 = fund_ret_sampled.std() * math.sqrt(12)
        information_ratio = annualized_ex_ret / annualized_vol_1

        # jensen_alpha
        rm = benchmark_ret_sampled.sum(min_count=1) * 12 / benchmark_ret_sampled.shape[0]
        jensen_alpha = annualized_ret - self._RF - beta * (rm - self._RF)

        # max_drawdown
        max_drawdown = 1 - (self._fund_nav / self._fund_nav.cummax()).min()

        # chang_lewellen
        chang_lewellen = benchmark_ret_sampled.apply(FundScoreExtendedProcess._lambda_1, fund_ret_sampled=fund_ret_sampled)

        ret = np.exp(self._fund_ret.sum(min_count=1)) - 1
        vol = self._fund_ret.std(ddof=0) * math.sqrt(12)

        total_df = pd.DataFrame.from_dict({'ret': ret, 'vol': vol, 'sr': sharpe_ratio_M, 'ir': information_ratio, 'beta': beta, 'alpha': jensen_alpha, 'mdd': max_drawdown, 'timing': chang_lewellen})
        total_df = total_df.replace([np.Inf, -np.Inf], np.nan)

        scaler = StandardScaler()
        minmax_scaler = MinMaxScaler()
        # blocklist = ['001274!0','001428!0','002232!0','002834!0','002839!0','004049!0','004051!0', '005950!0','006050!0','006567!0','007234!0','007350!0','007501!0','007514!0','519618!0', '960009!0','960010!0','960013!0','960014!0','960015!0','960017!0','960019!0','960023!0', '960025!0', '960026!0', '960030!0', '960031!0', '960032!0', '960041!0', 'F050004!0', 'F050026!0', 'F080012!0', 'F161616!0', 'F202003!0', 'F450004!0', 'F450005!0', ]
        for cl in self._wind_class_1:
            # 与该类型下的基金列表取交集作为新的索引
            df = total_df.reindex(total_df.index.intersection(self._fund_list[self._fund_list.wind_class_1 == cl].fund_id))
            # 每列标准化后即为各列的score
            df_standardized = scaler.fit_transform(df)
            df = df.join(pd.DataFrame(df_standardized, index=df.index, columns=[one + '_score' for one in df.columns]))
            # 计算return score
            df['return_score'] = df['ret_score'].add(df['sr_score'], fill_value=0).add(df['ir_score'], fill_value=0).add(df['beta_score'], fill_value=0).add(df['alpha_score'], fill_value=0)
            # 计算robust score
            df['robust_score'] = df['mdd_score'].sub(df['vol_score'], fill_value=0)
            for column in ('return_score', 'robust_score', 'timing_score'):
                df[column] = scaler.fit_transform(df[[column]])
                # 百分制分数
                df[column] = minmax_scaler.fit_transform(df[[column]]) * 100
                df[column.split('_')[0] + '_rank'] = df[column].rank(method='min', ascending=False)
            total_score = scaler.fit_transform(pd.DataFrame(df['return_score'].add(df['robust_score'], fill_value=0).add(df['timing_score'], fill_value=0)))
            df['total_score'] = minmax_scaler.fit_transform(total_score) * 100
            df['total_rank'] = df['total_score'].rank(method='min', ascending=False)

            df['wind_class_1'] = cl
            df['datetime'] = self._end_date
            df = df.reset_index().rename(columns={'index': 'fund_id'})
            # df.to_csv('./res/' + cl + '_indicator.csv', encoding="utf_8_sig")
            print(f'calc score for funds in {cl} done')
            self._data_helper._upload_derived(df, FundScoreExtended.__table__.name)

    def process(self, start_date: str, end_date: str) -> List[str]:
        failed_tasks = []
        try:
            self.init(start_date, end_date)
            print('init done, begin to calc score')
            self.calc()
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('fund_score_extended')
        return failed_tasks


if __name__ == '__main__':
    start_date = '20200730'
    end_date = '20200730'
    fse = FundScoreExtendedProcess(DerivedDataHelper())
    fse.process(start_date, end_date)
