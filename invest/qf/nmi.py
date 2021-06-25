'''
有色指数分析
有色指数、铜价与云南铜业的关系
伦敦铜的数据是货币格式,使用正则表达式转换成float


'''

import os
import sys
import time

import matplotlib
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from invest.investbase import ts_pro
from datetime import datetime
from re import sub
# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

import matplotlib.font_manager as fm

myfont = fm.FontProperties(fname='C:/Windows/Fonts/simsun.ttc')
pro = ts_pro()

fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx()
print(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

startdate = '2020-02-05'


def drawline(tcode, sdate):
    datadf = pro.daily(ts_code=tcode, adj='qfq', start_date=sdate)
    datadf = datadf.sort_values(by='trade_date')
    datadf.index = pd.to_datetime(datadf["trade_date"])
    print(datadf)
    stockline = [datetime.strptime(d, '%Y%m%d').date() for d in datadf.trade_date]
    ax2.plot(datadf.index, datadf.close, label=datadf.ts_code[0], linestyle='-', linewidth=1, color='red', alpha=1)


def draw_mcu():
    paths = "E:\\MyStudy\\datas\\"
    data_mcu = pd.read_csv(paths + '铜期货历史数据.csv', encoding='utf-8', header=0)

    # 数据切片，数据倒序排列
    data_mcu = data_mcu.reindex(index=data_mcu.index[::-1])

    # 将*年*月*日数据转化成pandas日期格式
    data_mcu['日期'] = data_mcu['日期'].map(lambda x: time.strptime(x, u"%Y年%m月%d日"))
    data_mcu['日期'] = data_mcu['日期'].map(lambda x: time.strftime('%Y-%m-%d', x))

    data_mcu.index = pd.to_datetime(data_mcu["日期"])
    # 数据切片，从**年开始取
    data_mcu = data_mcu[startdate::]
    data_mcu.dropna(axis=0)
    data_mcu["收盘"] = data_mcu['收盘'].map(lambda x: float(sub(r'[^\d.]', '', x)))

    print(data_mcu)
    ax1.plot(data_mcu.index, data_mcu["收盘"], label='伦敦铜', linestyle='-', linewidth=1)
    # 获取收盘价,并画出图形.
    # cl = data_mcu[['收盘']]
    # closed = cl.copy()
    # closed["收盘"].plot()


def draw_nmi():
    paths = "E:\\MyStudy\\datas\\index\\"
    data = pd.read_csv(paths + '000819.csv', encoding='gbk', header=0)
    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])
    data.index = pd.to_datetime(data["日期"])
    # 数据切片，从**年开始取
    data = data[startdate::]
    print(data)

    ax1.plot(data.index, data["收盘价"], label='000819有色指数', linestyle='-', linewidth=1)


if __name__ == '__main__':
    register_matplotlib_converters()

    draw_nmi()
    draw_mcu()
    drawline(tcode='000878.SZ', sdate=startdate)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    plt.style.use('seaborn-whitegrid')  # switch to seaborn style
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    print(matplotlib.matplotlib_fname())
    plt.title("云南铜业股价相关性", fontsize=20, fontproperties=myfont, bbox=dict(facecolor='blue', alpha=0.1))
    # ax1.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    # ax2.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    # plt.savefig('../png/cb_stock.png')
    # 显示图片
    plt.show()
    plt.close()
