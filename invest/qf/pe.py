# 周期股PE与价格的关系
# 绘制直方图

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from datetime import timedelta
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
fig = plt.figure(figsize=(15, 8))
gird = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

ax1 = fig.add_subplot(gird[0, 0])

ax2 = ax1.twinx()
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
pro = ts_pro()


def draw_stock(code):
    df = pro.daily_basic(ts_code=code, start_date='20150102',
                         fields='ts_code,trade_date,close,pe,pe_ttm')
    df = df.sort_values(by='trade_date')
    df['trade_date'] = pd.to_datetime(df["trade_date"].apply(str)).dt.date
    print(df)

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    ax1.plot(df.trade_date, df.close, label=code, linestyle='-', c='r', linewidth=1)

    ax2.plot(df.trade_date, df.pe_ttm, label='pe_ttm', linestyle='-', linewidth=1)
    ax2.text(x=df.trade_date.iloc[-1] + timedelta(days=-100), y=df.pe_ttm.iloc[-1] + 0.3,
             s='市盈率' + str(df.pe_ttm.iloc[-1]), size=10)
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimlegendHei', 'size': 12})

    hist = np.histogram(df.pe_ttm, bins=50)
    ax_b = fig.add_subplot(gird[0, 1])
    ax_b.barh(y=hist[1][0:50], width=hist[0], height=0.2)
    ax_b.set_title("市盈率直方图")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()
    draw_stock(code='600188.SH')
    plt.close()
