'''
3年期AAA票据与10年期国债的到期收益率这二者的利差主要受信用利差、期限风险、宏观基本面、资金成本、股市波动等因素影响，
其中信用利差起主要解释作用。

'''

import akshare as ak
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import tushare as ts
import pandas as pd
import datetime
from invest.investbase import ts_pro

pro = ts_pro()


# 将日期字符串20200101变成2020-01-01
def date_insert(src):
    src_list = list(src)

    src_list.insert(4, '-')
    src_list.insert(7, '-')
    dec = "".join(src_list)
    return dec


# 获取交易日历
def get_cal_date(start, end):
    cal_date = pro.trade_cal(exchange='', start_date=start, end_date=end)
    cal_date = cal_date[cal_date.is_open == 1]
    dates = cal_date.cal_date.values
    return dates


# 获取债券数据
def get_bond_data(s_start, s_end):
    start = s_start
    end = s_end
    g_start = start.replace('-', '')
    g_end = end.replace('-', '')

    #   一年按240个交易计算
    year = 240
    # 获取交易日历
    dates = get_cal_date(g_start, g_end)

    # 每次只能获取一年数据
    df = pd.DataFrame()
    # 拆分时间进行拼接，再删除重复项
    dlen = len(dates)
    print(dlen)
    times = dlen // year + (0 if (dlen % year == 0) else 1)
    for i in range(0, times):
        if i == times - 1 and dlen % year != 0:
            print(date_insert(dates[year * i]), date_insert(dates[year * i + dlen % year - 1]))
            d0 = ak.bond_china_yield(start_date=date_insert(dates[year * i]),
                                     end_date=date_insert(dates[year * i + dlen % year - 1]))
        else:
            print(date_insert(dates[year * i]), date_insert(dates[year * i + year - 1]))
            d0 = ak.bond_china_yield(start_date=date_insert(dates[year * i]),
                                     end_date=date_insert(dates[year * i + year - 1]))

        df = pd.concat([d0, df])
        # 删除重复项
        df = df.drop_duplicates()
        df.index = pd.to_datetime(df['日期'])
        df = df.sort_index()
    return df


# df_hsi = ak.index_investing_global(country="香港", index_name="恒生指数", period="每日",
#                                    start_date="2015-01-02", end_date="2021-04-01")
# print(df_hsi)
# df_hsi['收盘'].plot()

if __name__ == '__main__':
    register_matplotlib_converters()

    fig = plt.figure(figsize=(16, 9))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    # 当前日期的前一天
    end = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

    bond_china_yield_df = get_bond_data("2010-04-01", end)
    AAA_df = bond_china_yield_df[["曲线名称", "3年"]]
    AAA_df = AAA_df[AAA_df['曲线名称'] == '中债中短期票据收益率曲线(AAA)']

    china_df = bond_china_yield_df[["曲线名称", "日期", "10年"]]
    china_df = china_df[china_df['曲线名称'] == '中债国债收益率曲线']

    china_df['信用利差'] = AAA_df['3年'] - china_df['10年']

    print(bond_china_yield_df)

    ax2.plot(china_df['10年'], label="中债国债收益率曲线(右)", linestyle='-', linewidth=1, color='purple', alpha=1)
    ax2.plot(AAA_df['3年'], label="3年期AAA中债中短期票据(%)", linestyle='-', linewidth=1, color='red', alpha=1)
    ax1.plot(china_df['信用利差'], label='3年期AAA中债中短期-10年期国债走势图(%)', linestyle='-', color='blue', linewidth=1, alpha=1)
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()

    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    plt.show()
    plt.close()
