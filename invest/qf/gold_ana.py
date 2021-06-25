'''
美国国债与黄金期货分析


'''

import time
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from invest.investbase import ts_pro
# 正常显示画图时出现的中文和负号
from pylab import mpl
from re import sub
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

import matplotlib.font_manager as fm

myfont = fm.FontProperties(fname='C:/Windows/Fonts/simsun.ttc')
pro = ts_pro()

fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx()

startdate = '2008-10-30'
paths = "E:\\MyStudy\\datas\\"


def draw_gold():
    data = pd.read_csv(paths + '黄金期货历史数据.csv', encoding='utf-8', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])
    # 将*年*月*日数据转化成pandas日期格式
    data['日期'] = data['日期'].map(lambda x: time.strptime(x, u"%Y年%m月%d日"))
    data['日期'] = data['日期'].map(lambda x: time.strftime('%Y-%m-%d', x))
    data.index = pd.to_datetime(data["日期"])

    # 数据切片，从**年开始取
    data = data[startdate::]
    data.dropna(axis=0)
    data["收盘"] = data['收盘'].map(lambda x: float(sub(r'[^\d.]', '', x)))
    print(data)
    ax1.plot(data.index, data["收盘"], label='黄金期货', color='gold', linestyle='-', linewidth=1)


def draw_10_bond():
    data = pd.read_csv(paths + '美国十年期国债收益率历史数据.csv', encoding='utf-8', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])
    # 将*年*月*日数据转化成pandas日期格式
    data['日期'] = data['日期'].map(lambda x: time.strptime(x, u"%Y年%m月%d日"))
    data['日期'] = data['日期'].map(lambda x: time.strftime('%Y-%m-%d', x))
    data.index = pd.to_datetime(data["日期"])

    # 数据切片，从**年开始取
    data = data[startdate::]
    print(data)
    ax2.plot(data.index, data["收盘"], label='美国十年期国债收益率', color='red', linestyle='-', linewidth=1)


if __name__ == '__main__':
    register_matplotlib_converters()

    draw_10_bond()
    draw_gold()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()

    plt.title("国债与黄金相关性", fontsize=30, fontproperties=myfont, bbox=dict(facecolor='blue', alpha=0.1))
    ax1.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    ax2.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    plt.savefig('../png/gold_ana.png')
    # 显示图片
    plt.show()
    plt.close()
