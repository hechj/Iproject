'''

10日价格变化率
当短期价格跌到10日股价变化率下沿的贪婪点－0.1，这里大概率是逆向布局的时间点！分批买买买！
同样，当变化率快速上涨，接近或突破风险点0.2时，也只有一个操作，分批卖卖卖！
这样操作明显有个好处，就是大概率提前市场反应而反应……

'''
import datetime
import os
import sys
import pandas as pd
import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from invest.investbase import ts_pro

pro = ts_pro()

fig, ax1 = plt.subplots(frameon=False)  # 使用subplots()创建窗口
ax2 = ax1.twinx()
print(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

s_date = '20210101'


def draw(code):
    df = pro.fund_nav(ts_code=code, market='E')
    df = df.sort_values(by='end_date')

    df['roc'] = df['accum_nav'] / df['accum_nav'].shift(10) - 1

    df.index = pd.to_datetime(df["end_date"])
    df = df[s_date::]
    # 显示所有行
    pd.set_option('display.max_rows', None)
    print(df[['unit_nav', 'accum_nav', 'accum_div', 'adj_nav']])

    ax1.plot(df.index, df['roc'], label='10日价格变化率', linestyle='-', linewidth=1, c='orange')
    ys = [-0.2, -0.1, 0, 0.1, 0.2]
    for y in ys:
        ax1.axhline(y=y, c="darkorange", ls=':')  # 添加水平直线
    ax2.plot(df.index, df.unit_nav, linestyle='-', linewidth=1, label=df.ts_code[0], c='lightskyblue')
    ax2.set_ylabel(r"单位净值", fontproperties='SimHei', fontsize=15)

    # 画出买入点
    # buys = ['2021-06-18', '2021-07-16', '2021-8-18']
    # for xi in buys:
    #     v_buy = df.loc[df.index == xi, 'unit_nav'].values[0]
    #     ax2.scatter(xi, v_buy, s=np.pi * 2 ** 2, c='red', marker='^', alpha=0.8)


if __name__ == '__main__':
    register_matplotlib_converters()

    # draw('159995.SZ') #芯片etf
    # draw('512400.SH') # 有色etf
    # draw('159915.SZ') # 创业板ETF
    # draw('167301.SZ')  # 保险主题基金
    draw('513050.SH')  # 中概互联etf
    # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    # ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    # plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    plt.style.use('ggplot')
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()

    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    # plt.savefig('../png/cb_stock.png')
    # 显示图片
    plt.show()
    plt.close()
