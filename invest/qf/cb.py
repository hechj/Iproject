# 研究可转债指数与A股的关系
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro

fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx()


pro = ts_pro()


def draw_cb():
    paths = "E:\\MyStudy\\Jupter_prj\\"
    data = pd.read_csv(paths + '000832.csv', encoding='gbk', header=0)
    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])
    data.index = pd.to_datetime(data["日期"])
    # 数据切片，从2008年开始取
    data = data['2008-01-02'::]
    print(data)

    ax1.plot(data.index, data["收盘价"], label='000832中证转债', linestyle='-', linewidth=2)


def draw_stock():
    index_code = '000300.SH'
    df = pro.index_daily(ts_code=index_code, start_date='20080102',
                         fields='ts_code,trade_date,open,close,pct_chg,amount')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])
    ax2.plot(df.index, df.close, linestyle='-', linewidth=2, label=df.ts_code[0], c='red')

    # print(df)


if __name__ == '__main__':
    register_matplotlib_converters()

    draw_cb()
    draw_stock()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    plt.style.use('seaborn-whitegrid')  # switch to seaborn style
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    ax1.grid(b='major', color='k', linestyle='--', linewidth=3, alpha=0.3)
    ax2.grid(b='major', color='k', linestyle='--', linewidth=3, alpha=0.3)
    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    # plt.savefig('../png/cb_stock.png')
    # 显示图片
    plt.show()
    plt.close()
