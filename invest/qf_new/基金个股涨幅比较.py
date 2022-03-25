# -*- coding: UTF-8 -*-
# 研究个股的涨跌幅比较,可应用在对同一行业内的个股进行分析
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro
# 正常显示画图时出现的中文和负号
from pylab import mpl
import akshare as ak

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
pro = ts_pro()
# 指定起止日期
s_date = '20190222'

t_codes = pd.DataFrame(
    {'code': ['513050.SH', '513050.SH', '006327', '007657', '006567', '004958', '166005', '202023', '519697',
              '159920.SZ'],
     'market': ['E', 'D', 'L', 'A', 'A', 'A', 'A', 'A', 'A', 'E'],
     'name': ['中概互联', '场内行情', 'ETF联接', '竞争力指数', '中泰星元灵活', '圆信永丰优享', '中欧价值发现', '南方优选成长', '交银优势混合', '恒生ETF']})


def drawline():
    for i in range(2):  # len(t_codes)
        code = t_codes.iloc[i].values[0]
        name = t_codes.iloc[i].values[2]
        if t_codes.iloc[i].values[1] == 'E':  # 场内基金
            df = pro.fund_nav(ts_code=code, market='E')
            df = df.sort_values(by='nav_date')
            df.index = pd.to_datetime(df["nav_date"])
            df = df[s_date::]
            print(df)

            v_close = df.loc[df.nav_date == s_date, 'adj_nav'].values[0]
            df['rate'] = (df['adj_nav'] / v_close - 1) * 100
            # plt.plot(df.rate, label=name, linestyle='--', linewidth=1, alpha=1)
            plt.plot(df.adj_nav, label=name, linestyle='--', linewidth=1, alpha=1)
        elif t_codes.iloc[i].values[1] == 'D':  # 场内基金行情
            df = pro.fund_daily(ts_code=code)
            df = df.sort_values(by='trade_date')
            df.index = pd.to_datetime(df["trade_date"])
            df = df[s_date::]
            print(df)

            v_close = df.loc[df.trade_date == s_date, 'close'].values[0]
            df['rate'] = (df['close'] / v_close - 1) * 100
            plt.plot(df.close, label=name, linestyle='--', linewidth=1, alpha=1)
            # plt.plot(df.rate, label=name, linestyle='--', linewidth=1, alpha=1)
        elif t_codes.iloc[i].values[1] == 'A':  # AKshare获取基金数据
            data = ak.fund_em_open_fund_info(fund=code, indicator="累计净值走势")
            data['累计净值'] = data['累计净值'].astype('float')
            data.index = pd.to_datetime(data["净值日期"])
            data = data[s_date::]
            print(data)
            v_ljjz = data.iloc[0].values[1]  # 取开始日期的基金净值
            data['rate'] = (data['累计净值'] / v_ljjz - 1) * 100
            plt.plot(data.rate, label=name, linestyle='--', linewidth=1, alpha=1)
        elif t_codes.iloc[i].values[1] == 'S':  # 股票
            data = ts.pro_bar(ts_code=code, api=None, adj='qfq', start_date=s_date, asset='E',
                              factors=['tor', 'vr', 'vol'], freq='D')
            data = data.sort_values(by='trade_date')
            v_close = data.loc[data.trade_date == s_date, 'close'].values[0]

            data['rate'] = (data['close'] / v_close - 1) * 100
            stockline = [datetime.strptime(d, '%Y%m%d').date() for d in data.trade_date]
            plt.plot(stockline, data.rate, label=name, linestyle='--', linewidth=1, alpha=1)
        elif t_codes.iloc[i].values[1] == 'L':  # 本地文件
            data = pd.read_csv('E:/MyStudy/cpitest/invest/funds_related/data/%s_lsjz.csv' % str(code),
                               encoding='gbk')
            data.drop_duplicates(keep='first', inplace=True)
            data = data[['DWJZ', 'FSRQ', 'LJJZ']]
            data = data.sort_values(by='FSRQ')
            data.index = pd.to_datetime(data["FSRQ"])
            data = data[s_date::]
            v_ljjz = data.iloc[0].values[2]  # 取开始日期的基金净值
            print(v_ljjz)
            data['rate'] = (data['LJJZ'] / v_ljjz - 1) * 100
            print(data)
            plt.plot(data.rate, label=name, linestyle='--', linewidth=1, alpha=1)
        else:
            print("Error!")
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    plt.legend(loc='best', prop={'family': 'SimHei', 'size': 12})
    plt.title(s_date + '至今')


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
    drawline()
    # 显示图片
    plt.show()

    plt.close()
