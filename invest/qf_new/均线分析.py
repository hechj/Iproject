import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro, ts_getdate
import tushare as ts
from pylab import mpl
import numpy as np

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
pro = ts_pro()

fig = plt.figure()
plt.style.use("ggplot")

ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

s_date = "20120101"
e_date = "20220314"
index_code = '159920.SZ'
# index_code = '510500.SH'
# index_code = '600276.SH'
global days
days = 20


# 获取交易日历
def get_cal_date(start, end):
    cal_date = pro.trade_cal(exchange='', start_date=start, end_date=end)
    cal_date = cal_date[cal_date.is_open == 1]
    dates = cal_date.cal_date.values
    return dates


# 获取指数数据
def get_index_data(code, start, end):
    # 获取交易日历
    dates = get_cal_date(start, end)
    # tushare限制流量，每次只能获取300条记录
    max_num = 5000
    df = pd.DataFrame()
    # 拆分时间进行拼接，再删除重复项
    dlen = len(dates)
    print(dlen)
    times = dlen // max_num + (0 if (dlen % max_num == 0) else 1)
    for i in range(0, times):
        if i == times - 1 and dlen % max_num != 0:
            d0 = pro.index_daily(ts_code=code, start_date=dates[max_num * i],
                                 end_date=dates[max_num * i + dlen % max_num - 1],
                                 fields='ts_code,trade_date,close,pct_chg')
        else:
            d0 = pro.index_daily(ts_code=code, start_date=dates[300 * i],
                                 end_date=dates[max_num * i + max_num - 1],
                                 fields='ts_code,trade_date,close,pct_chg')

        df = pd.concat([d0, df])
        # 删除重复项
        df = df.drop_duplicates()
        df.index = pd.to_datetime(df.trade_date)
        df = df.sort_index()
    return df


def draw_ma_stock():
    # df = get_index_data(index_code, s_date, e_date)
    df = ts.pro_bar(ts_code=index_code, api=None, adj='qfq', start_date=s_date, asset='E',
                    factors=['tor', 'vr', 'vol'], freq='D')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df.trade_date)

    df['close_log'] = np.log(df['close'])
    days = 60
    df['ma_'] = df['close_log'].rolling(window=days, center=False).mean()
    df['sub_'] = df['close_log'] - df['ma_']
    df['sub_sum'] = df['sub_'].rolling(window=days, center=False).sum()

    print(df)

    # ax1.stackplot(df.index, df.sub_sum, color='blue', labels=[index_code], alpha=0.5)
    #
    # ax1.axhline(y=0, c="black", lw=2)
    # ax1.axhline(y=df.sub_sum.median() + df.sub_sum.std(), c="gray", ls='--')
    # ax1.axhline(y=df.sub_sum.median() - df.sub_sum.std(), c="gray", ls='--')

    ax1.plot(df.close_log, '-', label=index_code, linewidth=1, alpha=1, c='r')
    ax1.plot(df.ma_, '-', label=str(days) + "日均线", linewidth=1, alpha=0.8, c='g')

    ax2.plot(df.sub_, '-', label='偏离度', linewidth=1, alpha=1, c='b')
    ax2.axhline(y=df.sub_.median(), c="black", lw=1)
    ax2.axhline(y=df.sub_.median() + 2 * df.sub_.std(), c="gray", ls='--')
    ax2.axhline(y=df.sub_.median() - 2 * df.sub_.std(), c="gray", ls='--')

    # txt = '现价与移动均线的偏差，滚动计算总和'
    # font = {
    #     'color': 'blue',
    #     'weight': 'bold',
    #     'size': 16,
    # }
    # ax1.set_xlabel('\n' + txt, fontdict=font)


def draw_ma_index():
    df = pro.index_daily(ts_code=index_code, start_date=s_date,
                         fields='ts_code,trade_date,close,pct_chg')

    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])
    df['ma_850'] = df['close'].rolling(window=850, center=False).mean()
    df['ma_420'] = df['close'].rolling(window=420, center=False).mean()
    print(df)

    plt.title("均线分析")
    ax1.plot(df.close, '-', label=index_code, linewidth=1, alpha=1, c='r')
    ax1.plot(df.ma_850, '-', label="ma_850", linewidth=1, alpha=1)
    ax1.plot(df.ma_420, '-', label="ma_420", linewidth=1, alpha=1)


def draw_ma_fund(type):
    days = 126
    df = pro.fund_nav(ts_code=index_code, market='E')
    df = df.sort_values(by='nav_date')
    df.index = pd.to_datetime(df["nav_date"])
    df['ma_'] = df['adj_nav'].rolling(window=days, center=False).mean()
    df['sub_'] = df['adj_nav'] - df['ma_']
    df['sub_sum'] = df['sub_'].rolling(window=days, center=False).sum()
    print(df)
    plt.title('【ETF】   ' + ts_getdate())
    ax1.plot(df.adj_nav, '-', label=index_code, linewidth=1, alpha=0.6, c='r')
    ax1.plot(df.ma_, '-', label=str(days) + "日均线", linewidth=1, alpha=0.8, c='g')
    if type == 0:
        ax2.stackplot(df.index, df.sub_sum, color='blue', labels=['滚动差值求和'], alpha=0.5)
        ax2.axhline(y=0, c="black", lw=1)
        curr_sub_sum = df.iloc[-1]['sub_sum']
        ax2.axhline(y=curr_sub_sum, c="y", lw=0.7)
    else:
        ax2.plot(df.sub_, '-', label='偏离度', linewidth=1, alpha=1, c='b')
        ax2.axhline(y=df.sub_.median(), c="black", lw=1)
        ax2.axhline(y=df.sub_.median() + 2*df.sub_.std(), c="gray", ls='--')
        ax2.axhline(y=df.sub_.median() - 2*df.sub_.std(), c="gray", ls='--')


if __name__ == '__main__':
    register_matplotlib_converters()
    pd.set_option('display.max_columns', None)

    draw_ma_fund(0)
    # 设置时间按“年月”的格式显示
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    # 显示图片
    plt.show()
    plt.close()
