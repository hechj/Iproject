'''
深市融资余额/总市值 与 创业板分析

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

startdate = '2016-01-04'


def drawline(tcode, color):
    df = pro.index_daily(ts_code=tcode, start_date=startdate,
                         fields='ts_code,trade_date,close')

    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])
    ax2.plot(df.index, df.close, label=df.ts_code[0], linestyle='-', linewidth=1, color=color, alpha=1)


def draw_financing():
    paths = "E:\\MyStudy\\datas\\"
    data = pd.read_csv(paths + 'financing.csv', encoding='gbk', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])

    data.index = pd.to_datetime(data["date"])
    # 数据切片，从**年开始取
    data = data[startdate::]
    # 只保留数字、dot和minus符号
    data['rate'].replace(regex=True, inplace=True, to_replace=r'[^0-9.\-]', value=r'')
    data['rate'] = pd.to_numeric(data['rate'], errors='coerce')
    data['rate'] = data['rate']/100
    ax1.plot(data.index, data["rate"], label='融资余额/总市值', linestyle='-', linewidth=1)


if __name__ == '__main__':
    register_matplotlib_converters()

    draw_financing()
    # drawline(tcode='399006.SZ', color='r')
    drawline(tcode='000300.SH', color='r')
    plt.style.use('bmh')  # switch to seaborn style
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()

    plt.title("相关性", fontsize=30, fontproperties=myfont, bbox=dict(facecolor='blue', alpha=0.1))
    # ax1.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    # ax2.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    # plt.savefig('../png/financing_ana.png')
    # 显示图片
    plt.show()
    plt.close()
