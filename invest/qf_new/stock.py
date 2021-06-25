# -*- coding: UTF-8 -*-
# 研究个股的价格与10日移动平均换手率、成交量的关联

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro, get_t_code
import numpy as np
# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 指定起止日期
startdate = '20180103'
enddate = None
t_names = ['中国平安']


def drawline(name, sdate, edate, stackcolor='#00BFFF', linecolor='red'):
    fig = plt.figure(figsize=(16, 9), frameon=True)

    # 画布右移，以保证第三个坐标轴显示清晰
    fig.subplots_adjust(right=0.75)

    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    ax4 = ax.twinx()
    ax3.spines["right"].set_position(("axes", 1.1))
    ax4.spines["right"].set_position(("axes", 1.2))
    # 设置右轴和刻度的颜色
    ax3.spines["right"].set_color('blue')
    ax3.tick_params(axis='y', colors='blue')
    t_code = get_t_code(name)
    datadf = ts.pro_bar(ts_code=t_code, api=None, adj='qfq', start_date=sdate, end_date=edate, asset='E',
                        factors=['tor', 'vr', 'vol'], freq='D')
    datadf = datadf.sort_values(by='trade_date')

    datadf['tor_10'] = datadf['turnover_rate'].rolling(window=10, center=False).mean()
    print(datadf[['trade_date', 'amount', 'turnover_rate', 'close', 'tor_10']])
    stockline = [datetime.strptime(d, '%Y%m%d').date() for d in datadf.trade_date]
    ax3.set_ylabel('10日平均换手率(%)', color='blue')
    ax4.set_ylabel('换手率(%)', color='blue')

    # 在绘制时设置label, 逗号是必须的
    l3, = ax3.plot(stockline, datadf.tor_10, linestyle='--', linewidth=1, color='blue', alpha=1)
    l4, = ax4.plot(stockline, datadf.turnover_rate, linestyle='--', linewidth=1, color='green', alpha=1)
    ax.plot(stockline, datadf.close, label='收盘价', linestyle='-', linewidth=1, color=linecolor, alpha=1)
    ax2.stackplot(stockline, datadf.amount, color=stackcolor, alpha=0.4, linewidth=1, labels=['成交额(千)'])
    # 以季度显示横坐标
    plt.xticks(pd.date_range(stockline[0], stockline[-1], freq='Q'))
    plt.title(name)
    ax4.axhline(y=datadf.turnover_rate.median(), ls='--', c='black')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    ax.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1)
    # ax3.legend(loc=4)
    # ax4.legend(loc=4)
    plt.legend(handles=[l3, l4, ], labels=['10日平均换手率(%)', '换手率(%)'], loc=4)

    # 显示图片
    plt.show()


def taskmain():
    for n in t_names:
        drawline(n, startdate, enddate)


if __name__ == '__main__':
    # 主程序
    register_matplotlib_converters()
    plt.style.use("ggplot")
    taskmain()
    plt.close()
