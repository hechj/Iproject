'''
根据积极型资产配置指南3：
商品价格到顶之后，通常都是投资债券的好时机。而债券收益率到底，之后通常是投资商品的好时机。

本内容以南华工业品指数，十年期国债收益率制图验证以上逻辑。
'''

import datetime
import time

import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro


pro = ts_pro()
s_date = '20050408'

df = pro.index_daily(ts_code='NHII.NH', start_date=s_date)
df = df.sort_values(by='trade_date')
df.index = pd.to_datetime(df["trade_date"])
print(df)

df_300 = pro.index_daily(ts_code='000300.SH', start_date=s_date,
                         fields='ts_code,trade_date,close')
df_300 = df_300.sort_values(by='trade_date')
df_300.index = pd.to_datetime(df_300["trade_date"])


def draw_rate():
    paths = "E:\\MyStudy\\datas\\"

    data = pd.read_csv(paths + '中国十年期国债收益率历史数据.csv', encoding='utf-8', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])

    # 将*年*月*日数据转化成pandas日期格式
    data['日期'] = data['日期'].map(lambda x: time.strptime(x, u"%Y年%m月%d日"))
    data['日期'] = data['日期'].map(lambda x: time.strftime('%Y%m%d', x))
    data.index = pd.to_datetime(data["日期"])
    print(data)
    # 数据切片，从**年开始取
    data = data[s_date::]

    ax2.plot(data["收盘"], label='十年期国债收益率(%)', linestyle='-', linewidth=1, color='skyblue', alpha=0.7)


if __name__ == '__main__':
    register_matplotlib_converters()
    fig = plt.figure(figsize=(16, 9))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    draw_rate()
    ax1.plot(df['close'], label='南华工业品', linestyle='-', color='b', linewidth=1, alpha=1)
    ax1.plot(df_300['close'], label='沪深300指数走势', linestyle='-', color='r', linewidth=1, alpha=0.6)
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()

    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    plt.show()
    plt.close()
