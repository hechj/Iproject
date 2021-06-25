'''
主要用来研究换手率这个指标
10日移动换手率为领先指标，10日移动平均换手率中位数下方是入场时机
'''
import datetime
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro



pro = ts_pro()


def get_tor(index_code, x_plot, ax_x):
    df = pro.index_dailybasic(ts_code=index_code, start_date='20100926',
                              fields='ts_code,trade_date,turnover_rate,pe')

    df = df.sort_values(by='trade_date')
    df['tor_10'] = df['turnover_rate'].rolling(window=10, center=False).mean();
    print(df)
    # print(df[['ts_code', 'trade_date', 'turnover_rate']])

    plt.style.use('seaborn-whitegrid')  # switch to seaborn style

    df.index = pd.to_datetime(df["trade_date"])

    arr = df['tor_10'].values
    arr = arr[~np.isnan(arr)]  # 去除数组中nan的数据
    mid = np.median(arr)  # 取中位数
    print(mid)
    if x_plot is False:
        plt.setp(ax_x.get_xticklabels(), visible=False)
    else:
        plt.xticks(rotation=270)  # 旋转270度
        plt.title("10日移动平均换手率--{}".format(datetime.datetime.now().strftime('%Y-%m-%d')), fontproperties='SimHei',
                  fontsize=18)
    if index_code == '000300.SH':
        ax_x.set_ylabel('沪深300换手率(%)', fontproperties='SimHei', fontsize=15)
    else:
        if index_code == '399006.SZ':
            ax_x.set_ylabel('创业板换手率(%)', fontproperties='SimHei', fontsize=15)
        else:
            if index_code == '000016.SH':
                ax_x.set_ylabel('上证50换手率(%)', fontproperties='SimHei', fontsize=15)
            else:
                ax_x.set_ylabel('换手率(%)', fontproperties='SimHei', fontsize=15)
    plt.grid(b='major', color='k', linestyle='--', linewidth=1, alpha=0.3)
    plt.plot(df.tor_10)
    plt.axhline(y=mid, color="red")
    # plt.savefig("out/tor.png")


if __name__ == '__main__':
    register_matplotlib_converters()
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(311)
    get_tor('399006.SZ', False, ax)  # 创业板
    ax1 = fig.add_subplot(312, sharex=ax)
    get_tor('000300.SH', False, ax1)
    ax2 = fig.add_subplot(313, sharex=ax1)
    # get_tor('000016.SH', True, ax2)
    get_tor('000905.SH', True, ax2)
    plt.show()
    plt.close()
