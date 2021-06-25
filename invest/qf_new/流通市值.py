# -*- coding: UTF-8 -*-
# 研究个股的流通市值,在年线下方可能是入场时机

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

from invest.investbase import ts_pro, get_t_code
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

pro = ts_pro()

# 指定起止日期
startdate = '20070301'
enddate = None

t_names = ['中国平安', '新大陆']


def drawline_day(name, sdate, stackcolor='#00BFFF', linecolor='red'):
    fig = plt.figure(figsize=(16, 9), frameon=False)
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    tcode = get_t_code(name)
    datadf = pro.daily_basic(ts_code=tcode, start_date=sdate,
                             fields='close,ts_code,trade_date,total_share,float_share,free_share,total_mv,circ_mv')
    data = ts.pro_bar(ts_code=tcode, api=None, adj='qfq', start_date=sdate, asset='E', freq='D')
    data = data.sort_values(by='trade_date')

    datadf = datadf.sort_values(by='trade_date')
    datadf['day_365'] = datadf['circ_mv'].rolling(window=250, center=False).mean()
    datadf['day_180'] = datadf['circ_mv'].rolling(window=125, center=False).mean()
    print(data)
    print(datadf)
    stockline = [datetime.strptime(d, '%Y%m%d').date() for d in datadf.trade_date]

    ax.plot(stockline, datadf.day_365, label='年线', linestyle='-', linewidth=1, color=linecolor,
            alpha=1)
    ax.plot(stockline, datadf.day_180, label='半年线', linestyle='-', linewidth=1, color='y',
            alpha=1)
    ax.stackplot(stockline, datadf.circ_mv, color=stackcolor, alpha=0.4, labels=['流通市值(万)'])
    ax2.plot(stockline, data.close, label='close', linestyle='-', linewidth=1, color='black', alpha=1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    ax.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1)
    # 显示图片
    plt.title(name)
    plt.show()


def taskmain():
    for name in t_names:
        drawline_day(name, startdate)


if __name__ == '__main__':
    # 主程序
    register_matplotlib_converters()
    plt.style.use("ggplot")
    taskmain()
    plt.close()
