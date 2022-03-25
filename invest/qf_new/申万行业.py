'''
分析指数估值
中位数，百分位数，市盈率
'''
import datetime
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro
from pylab import mpl
from matplotlib import gridspec

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
pro = ts_pro()

s_date = "20050408"
e_date = '20210831'

codes = ['801150.SI', '801780.SI']


# 获取交易日历
def get_cal_date(start, end):
    cal_date = pro.trade_cal(exchange='', start_date=start, end_date=end)
    cal_date = cal_date[cal_date.is_open == 1]
    dates = cal_date.cal_date.values
    return dates


# 获取申万行业数据
def get_sw_data(code, start, end):
    # 获取交易日历
    dates = get_cal_date(start, end)
    # tushare限制流量，每次只能获取n条记录
    n = 1000
    df = pd.DataFrame()
    # 拆分时间进行拼接，再删除重复项
    dlen = len(dates)
    times = dlen // n + (0 if (dlen % n == 0) else 1)
    print(dlen, times)
    for i in range(0, times):
        if i == times - 1 and dlen % n != 0:
            d0 = pro.sw_daily(ts_code=code, start_date=dates[n * i], end_date=dates[n * i + dlen % n - 1])
        else:
            d0 = pro.sw_daily(ts_code=code, start_date=dates[n * i], end_date=dates[n * i + n - 1])

        df = pd.concat([d0, df])
        # 删除重复项
        df.drop_duplicates(inplace=True)
        df.index = pd.to_datetime(df.trade_date)
        df = df.sort_index()
    return df


def drawline(t_code):
    fig = plt.figure(figsize=(15, 8))
    gird = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

    ax = fig.add_subplot(gird[0, 0])

    ax2 = ax.twinx()
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    data = get_sw_data(t_code, s_date, e_date)

    print(data)
    print(data.info())
    stock_line = [datetime.datetime.strptime(d, '%Y%m%d').date() for d in data.trade_date]

    ax.stackplot(stock_line, data.close, color='#00BFFF', alpha=0.4, labels=['收盘价'])
    ax2.plot(stock_line, data.pe, label='pe', linestyle='-', linewidth=1, color='black', alpha=1)
    ax2.axhline(y=data.pe.mean(), ls='-', c='black')
    ax2.axhline(y=data.pe.mean() + data.pe.std(), ls='--', c='gray')
    ax2.axhline(y=data.pe.mean() - data.pe.std(), ls='--', c='gray')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    ax.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1)
    # 显示图片
    plt.title(t_code)

    data.dropna(subset=['pb', 'pe'], inplace=True)
    bins = 80
    hist = np.histogram(data.pe, bins=bins)  # 如果数据中存在空值，则无法输出
    ax_b = fig.add_subplot(gird[0, 1])
    ax_b.barh(y=hist[1][0:bins], width=hist[0] * 2, height=2 / bins)
    ax_b.set_title("风险溢价直方图")
    plt.tight_layout()

    plt.show()


def task_main():
    for code in codes:
        drawline(code)


if __name__ == '__main__':
    # 主程序
    register_matplotlib_converters()
    task_main()
    plt.close()
