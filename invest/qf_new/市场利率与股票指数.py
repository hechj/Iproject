'''
根据积极型资产配置指南6：如何控制股票和债券的投资风险
当市场利率大幅提升，这对股市也不是个好消息，作者用了一个指标来给我们做提示：
他说当股票指数在12月移动平均线上方，这就是一个多头行情，
此时如果市场利率在12月移动平均线下方，那么这就是一个特别好的机会!

本内容以沪深300为股票指数，3个月SHIBOR为短期市场利率绘制年线验证以上逻辑。
'''

from datetime import timedelta
import time
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from invest.investbase import ts_pro

pro = ts_pro()
s_date = '20060706'

df = pro.shibor(start_date=s_date)
df = df.sort_values(by='date')
df.index = pd.to_datetime(df["date"])
df['y_line'] = df['3m'].rolling(window=250, center=False).mean()
print(df)

df_300 = pro.index_daily(ts_code='000001.SH', start_date=s_date,
                         fields='ts_code,trade_date,close')
df_300 = df_300.sort_values(by='trade_date')
df_300.trade_date = pd.to_datetime(df_300["trade_date"]).dt.date
# 设置成索引，即可在坐标轴上画数据
df_300.set_index(df_300.trade_date, drop=True, inplace=True)
df_300['y_line'] = df_300['close'].rolling(window=250, center=False).mean()
print(df_300)


def draw_rate(long_rate):
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

    if long_rate:
        data['y_line'] = data['收盘'].rolling(window=250, center=False).mean()
        ax2.plot(data["收盘"], label='十年期国债收益率(%)', linestyle='-', linewidth=2, color='skyblue', alpha=0.6)
        ax2.plot(data['y_line'], label="利率年线", linestyle='-', linewidth=1, color='deepskyblue', alpha=1)
    else:

        ax2.plot(df['3m'], label="利率走势", linestyle='-', linewidth=0.8, color='skyblue', alpha=1)
        ax2.plot(df['y_line'], label="利率年线", linestyle='-', linewidth=1, color='deepskyblue', alpha=1)


if __name__ == '__main__':
    register_matplotlib_converters()
    fig = plt.figure(figsize=(16, 9))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    draw_rate(False)
    ax1.plot(df_300['close'], label='指数走势', linestyle='-', color='salmon', linewidth=2, alpha=0.6)
    ax1.plot(df_300['y_line'], label="指数年线", linestyle='-', linewidth=1, color='red', alpha=1)
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate(bottom=0.2, rotation=45, ha='right')

    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax1.set_ylim(0, 6000)
    ax1.set_xlim([df_300.index[0], df_300.index[-1]])
    print(df_300.trade_date.iloc[0])
    print(df_300.close.iloc[0])
    # 这样画矩形框

    ax1.add_patch(
        plt.Rectangle(((pd.to_datetime("2012-01-01") - pd.to_datetime("1970-01-01")).days, 1000), 360,
                      4000, fill=False, edgecolor='black', linewidth=1, linestyle='--', clip_on=False)
    )
    ax1.add_patch(
        plt.Rectangle(((pd.to_datetime("2018-06-01") - pd.to_datetime("1970-01-01")).days, 1000), 360,
                      4000, fill=False, edgecolor='black', linewidth=1, linestyle='--', clip_on=False)
    )
    # ax1.text(x="2012-01-01", y=1000, s='hs300', size=12)
    # 以季度显示横坐标
    plt.xticks(pd.date_range(df_300.index[0], df_300.index[-1], freq='6m'))
    # plt.setp(ax1.get_xticklabels(), rotation=90)

    plt.savefig("../png/利率年线与指数年线.jpg")
    plt.show()
    plt.close()
