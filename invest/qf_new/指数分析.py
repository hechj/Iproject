'''
分析指数估值
中位数，百分位数，市盈率
'''
import datetime
from scipy.stats import rankdata

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro, get_t_name
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
pro = ts_pro()

s_date = "20050408"
e_date = '20210610'


# 返回数组里元素的百分位数
def calc_percentile(a, method='min'):
    return rankdata(a, method=method) / float(len(a))


def get_pe(index_code, x_plot, ax_x, ax_t):
    df = pro.index_dailybasic(ts_code=index_code, start_date=s_date, end_date=e_date,
                              fields='ts_code,trade_date,turnover_rate,pe,pe_ttm,pb')

    df = df.sort_values(by='trade_date')
    df['per'] = calc_percentile(df['pe_ttm'].values)
    print(index_code, "pe_ttm长度:", float(len(df['pe_ttm'].values)))
    print(df['pe_ttm'].values)

    print(df[['ts_code', 'trade_date', 'pe', 'pe_ttm', 'per']])

    df.index = pd.to_datetime(df["trade_date"])

    df_i = pro.index_daily(ts_code=index_code, start_date=s_date, end_date=e_date,
                           fields='ts_code,trade_date,close')
    df_i = df_i.sort_values(by='trade_date')
    df_i['per'] = calc_percentile(df_i['close'].values)
    print(index_code, "close长度:", float(len(df_i['close'].values)))
    df_i.index = pd.to_datetime(df_i["trade_date"])
    print(df_i)
    print("市盈率平均值:", df.pe_ttm.mean())
    print("市盈率中位数:", df.pe_ttm.median())
    print("--------------------")

    if x_plot is False:
        plt.setp(ax_x.get_xticklabels(), visible=False)
    else:
        plt.xticks(rotation=270)  # 旋转270度
        plt.title("".format(datetime.datetime.now().strftime('%Y-%m-%d')), fontproperties='SimHei',
                  fontsize=18)

    ax_x.set_ylabel(get_t_name(index_code), fontproperties='SimHei', fontsize=15)
    ax_x.plot(df.pe_ttm, label='市盈率', c='b')
    ax_t.plot(df.per, label='历史百分位', c='r')
    ax_x.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax_t.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    ax_x.axhline(y=df.pe_ttm.median(), ls='-', c='black')
    ax_x.axhline(y=df.pe_ttm.median() + df.pe_ttm.std(), ls='--', c='gray')
    ax_x.axhline(y=df.pe_ttm.median() - df.pe_ttm.std(), ls='--', c='gray')
    ax_x.spines['bottom'].set_visible(False)
    ax_x.spines['top'].set_visible(False)
    ax_t.spines['bottom'].set_visible(False)
    ax_t.spines['top'].set_visible(False)
    # plt.grid(b='major', color='k', linestyle='--', linewidth=1, alpha=0.3)


if __name__ == '__main__':
    register_matplotlib_converters()

    fig = plt.figure(figsize=(16, 9))
    # plt.style.use('seaborn-whitegrid')  # switch to seaborn style

    ax1 = fig.add_subplot(311)
    ax1_t = ax1.twinx()
    plt.title("指数市盈率TTM与历史百分位", c='green')
    get_pe('399006.SZ', False, ax1, ax1_t)  # 创业板
    ax2 = fig.add_subplot(312, sharex=ax1)
    ax2_t = ax2.twinx()
    get_pe('000300.SH', False, ax2, ax2_t)
    ax3 = fig.add_subplot(313, sharex=ax2)
    ax3_t = ax3.twinx()
    get_pe('000905.SH', True, ax3, ax3_t)

    plt.show()
    plt.close()
