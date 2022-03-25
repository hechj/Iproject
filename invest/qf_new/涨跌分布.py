# 导入常用模块
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import *
from invest.investbase import ts_pro

# 设置绘图参数(中文显示以及坐标轴负数显示)
plt.rcParams['font.sans-serif'] = ['Simhei']  # 解决中文显示问题,黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负数坐标显示问题

# 设置DataFrame的显示
pd.set_option('display.unicode.ambiguous_as_wide', True)  # 设置pd中亚洲文字处理
pd.set_option('display.unicode.east_asian_width', True)  # 设置pd中亚洲文字渲染显示
pd.set_option('display.max_colwidth', None)  # 设置最大列宽
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 20)
pd.set_option('display.colheader_justify', 'left')

pro = ts_pro()


# 获取主板涨跌数据
def get_chg(trade_dt, market_type):
    if market_type != 'A':
        data = pro.query(
            'stock_basic',
            exchange='',
            list_status='L',
            fields=
            'ts_code,symbol,name,area,industry,market,exchange,curr_type,list_status,list_date,'
            'delist_date,is_hs',
            trade_date=trade_dt)
        print(data['market'].unique())

        codes = list(data[data['market'] == market_type].ts_code)
        data = pro.query('daily', trade_date=trade_dt)
        data = data[data.ts_code.apply(lambda x: True if x in codes else False)]
    else:
        data = pro.query('daily', trade_date=trade_dt)
    return data["pct_chg"]


# 绘图主板涨跌分布的函数
def st_plot(trade_dt, market_type):
    ret = get_chg(trade_dt, market_type)
    total = ret.count()
    up = ret[ret > 0].count()
    equal = ret[ret == 0].count()
    down = ret[ret < 0].count()
    status = market_type + f"交易股票数量：{total}  上涨：{up}  下跌：{down}  平：{equal}"
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.set_xticks(range(-21, 22))

    bins1 = list(range(-21, 1))
    bins2 = list(range(0, 22))

    n1, bins1, patches1 = ax.hist(x=ret[ret <= 0], bins=bins1, rwidth=0.9, color='g')
    n2, bins2, patches2 = ax.hist(x=ret[ret > 0], bins=bins2, rwidth=0.9, color='r')
    n = list(n1) + list(n2)
    bins = list(bins1) + list(bins2)[1:]

    ax.set_xlabel(market_type + '涨跌分布', fontsize=14)
    ax.text(x=11, y=max(n) + 30, s=status, va='bottom', ha='right', fontsize=12, color='blue')
    ax.set_title(trade_dt + market_type + '情绪', fontsize=20, fontweight='bold', loc='center', pad=10)
    for num in range(0, len(n)):
        ax.text(x=bins[num] + 0.5, y=n[num], s=int(n[num]), va='bottom', ha='center', fontsize=12)
    plt.savefig(f"../png/{trade_dt}{market_type}情绪.jpg")
    # plt.show()
    # plt.close()


# st_plot("20211103", 'A')

# 获取最近5个交易日
yesterday = datetime.today() + timedelta(-1)
start_date = (yesterday + timedelta(-10)).strftime(format="%Y%m%d")
end_date = yesterday.strftime(format="%Y%m%d")
df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
df = df[df.is_open == 1].iloc[-2:]
for i in df.cal_date:
    print(i)
    st_plot(i, 'A')
