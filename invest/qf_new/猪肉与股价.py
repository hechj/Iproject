'''
分析猪肉价与股价的关系
'''

import time
import pandas as pd
import tushare as ts
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
from invest.investbase import ts_pro
# 正常显示画图时出现的中文和负号
from pylab import mpl
from datetime import datetime

pro = ts_pro()

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
myfont = fm.FontProperties(fname='C:/Windows/Fonts/simsun.ttc')
fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx()

startdate = '2016-07-08'

dict_code = {'300498.SZ': '温氏股份', '000895.SZ': '双汇发展', '002714.SZ': '牧原股份'}


def draw():
    paths = "E:\\MyStudy\\datas\\"
    data = pd.read_csv(paths + 'porkprice.csv', encoding='utf-8', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])

    # 将*年*月*日数据转化成pandas日期格式
    data.index = pd.to_datetime(data["date"])
    print(data)
    # 数据切片，从**年开始取
    data = data[startdate::]
    ax2.plot(data.index, data["porkprice"], label='外三元生猪', c='red', linestyle='--', linewidth=1)


def drawline(tcode):
    # datadf = pro.daily(ts_code=tcode, start_date=startdate)

    # 前复权处理
    date_p = datetime.strptime(startdate, '%Y-%m-%d').date()
    datadf = ts.pro_bar(ts_code=tcode, adj='qfq', start_date=str(date_p))
    datadf = datadf.sort_values(by='trade_date')
    stockline = [datetime.strptime(d, '%Y%m%d').date() for d in datadf.trade_date]

    ax1.plot(stockline, datadf.close, label=dict_code[datadf.ts_code[0]], linestyle='-', linewidth=1, alpha=1)


if __name__ == '__main__':
    register_matplotlib_converters()

    draw()

    for key in dict_code.keys():
        drawline(key)

    # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.style.use('seaborn-whitegrid')  # switch to seaborn style

    plt.title("外三元生猪与股价的关系", fontsize=20, fontproperties=myfont, bbox=dict(facecolor='blue', alpha=0.1))
    # ax1.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    # ax2.grid(b='major', color='lightskyblue', linestyle='--', linewidth=1, alpha=0.5)
    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    # plt.savefig('../png/cb_stock.png')
    # 显示图片
    plt.show()
    plt.close()
