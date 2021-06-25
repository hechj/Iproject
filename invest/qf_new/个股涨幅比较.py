# -*- coding: UTF-8 -*-
# 研究个股的涨跌幅比较,可应用在对同一行业内的个股进行分析

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
startdate = '20160104'

t_names = ['中国平安', '中国太保', '新华保险', '中国人寿']


def drawline(names, sdate):
    for name in names:
        t_code = get_t_code(name)
        datadf = ts.pro_bar(ts_code=t_code, api=None, adj='qfq', start_date=sdate, asset='E',
                            factors=['tor', 'vr', 'vol'], freq='D')
        datadf = datadf.sort_values(by='trade_date')
        v_close = datadf.loc[datadf.trade_date == startdate, 'close'].values[0]

        datadf['rate'] = datadf['close'] / v_close - 1
        stockline = [datetime.strptime(d, '%Y%m%d').date() for d in datadf.trade_date]
        plt.plot(stockline, datadf.rate, label=name, linestyle='--', linewidth=1, alpha=1)

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    plt.legend(loc='best', prop={'family': 'SimHei', 'size': 12})
    plt.title(startdate + '至今涨幅')


def taskmain():
    drawline(t_names, startdate)


if __name__ == '__main__':
    # 主程序
    register_matplotlib_converters()
    # 创建画板
    fig = plt.figure(figsize=(16, 9), frameon=True)
    # 创建画纸
    # ax = fig.add_subplot(111)
    # 创建画纸，生成1行1列的子图矩阵，选择画纸1
    # ax = plt.subplot(111)
    plt.style.use("ggplot")
    taskmain()
    # 显示图片
    plt.show()

    plt.close()
