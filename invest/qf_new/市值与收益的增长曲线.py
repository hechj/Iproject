# -*- coding: UTF-8 -*-
'''
彼得林奇投资方法：
研究个股的市值与收益的增长情况
仅适用于每年盈利且持续增长的企业
'''

import pandas as pd
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

from invest.investbase import ts_pro, get_t_code
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

pro = ts_pro()

# 指定起止日期
# 银行 20140228
# 保险 20140429
s_date = '20140228'

t_names = ['工商银行']
pd.set_option('display.max_columns', None)


def drawline(name, stackcolor='#00BFFF', linecolor='red'):
    fig = plt.figure(figsize=(16, 9), frameon=False)
    # 画布右移，以保证第三个坐标轴显示清晰
    fig.subplots_adjust(right=0.9)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.06))
    # 设置右轴和刻度的颜色
    ax2.spines["right"].set_color('green')
    ax3.spines["right"].set_color('blue')
    ax3.tick_params(axis='y', colors='blue')
    t_code = get_t_code(name)
    fina_df = pro.fina_indicator(ts_code=t_code, start_date=s_date,
                                 fields='ts_code,ann_date,end_date,roe_waa,ocf_to_or')

    fina_df.rename(columns={'ocf_to_or': '经现流比营业收入'}, inplace=True)

    for i in range(fina_df.shape[0]):
        if not fina_df.end_date[i].endswith("1231"):
            fina_df.drop(i, inplace=True)
    # income_df = income_df[s_date::]
    fina_df.dropna(axis=0, inplace=True)
    fina_df = fina_df.drop_duplicates(subset=['end_date'])
    fina_df.index = pd.to_datetime(fina_df["end_date"], format='%Y%m%d')
    fina_df = fina_df.reindex(index=fina_df.index[::-1])
    fina_df['rate'] = np.nan
    fina_df['roe_waa'] = fina_df['roe_waa'] / 100
    for i in range(fina_df.shape[0]):
        if i == 0:
            fina_df.loc[fina_df.index[i], 'rate'] = 1 + fina_df.loc[fina_df.index[i], 'roe_waa']
        else:
            fina_df.loc[fina_df.index[i], 'rate'] = fina_df.loc[fina_df.index[i - 1], 'rate'] * (
                    1 + fina_df.loc[fina_df.index[i], 'roe_waa'])
    print(fina_df)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    ax1.plot(fina_df.index, fina_df.rate, "m", marker='.', ms=3, label="收益增长曲线")

    data1 = pro.daily_basic(ts_code=t_code, start_date=s_date,
                            fields='trade_date,pe_ttm,pb,total_mv,circ_mv')
    data2 = ts.pro_bar(ts_code=t_code, api=None, adj='qfq', start_date=s_date,
                       asset='E', freq='D')
    data = pd.merge(data2, data1, on='trade_date')
    data = data.sort_values(by='trade_date')
    data.index = pd.to_datetime(data["trade_date"])
    i_value = data.loc[data.trade_date == s_date, 'total_mv'].values[0]
    data['total_rate'] = data.total_mv / i_value
    i_close_value = data.loc[data.trade_date == s_date, 'close'].values[0]
    data['close_rate'] = data.close / i_close_value
    x0 = '2020-12-31'
    y0 = fina_df.loc[fina_df.index[-1], 'rate']
    # ax1.text(x, y, "价值：%s元" % str(round(i_close_value * y, 2)))
    print(round(i_close_value * y0, 2))
    ax1.annotate(r"价值：%s元" % str(round(i_close_value * y0, 2)), xy=(x0, y0), xycoords='data', xytext=(+15, -15),
                 textcoords='offset points', fontsize=12,
                 arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-0.2"))
    # ax2 = fig.add_subplot(212)
    ax1.plot(data.index, data.total_rate, label='总市值', linestyle='-', linewidth=1, color=linecolor, alpha=1)
    ax1.plot(data.index, data.close_rate, label='每股价格', linestyle='-', linewidth=1, color='orange', alpha=0.8)
    ax2.plot(data.index, data.pe_ttm, label='市盈率TTM', linestyle='-', linewidth=1, color='green', alpha=0.8)
    ax3.set_ylabel('市净率', color='blue')
    l3, = ax3.plot(data.index, data.pb, linestyle='--', linewidth=1, color='blue', alpha=1)
    print(data)
    plt.title(name + s_date + '-' + datetime.today().strftime('%Y%m%d'))
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    plt.legend(handles=[l3, ], labels=['市净率'], loc=4)
    # 显示图片
    plt.show()


def task_main():
    for name in t_names:
        drawline(name)


if __name__ == '__main__':
    # 主程序
    register_matplotlib_converters()
    plt.style.use("ggplot")
    task_main()
    plt.close()
