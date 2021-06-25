# 周期股PE与价格的关系

import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro


fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx()
pro = ts_pro()


def draw_stock(code):
    df = pro.daily_basic(ts_code=code, start_date='20150102',
                         fields='ts_code,trade_date,close,pe,pe_ttm')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])
    print(df)

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    ax1.plot(df.close, label=code, linestyle='-', c='r', linewidth=1)

    ax2.plot(df.pe, label='pe', linestyle='-', linewidth=1)
    ax2.plot(df.pe_ttm, label='pe_ttm', linestyle='-', linewidth=1)
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()
    draw_stock(code='601318.SH')
    plt.close()
