# 获取沪深港股通持股比例与股价走势。
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import tushare as ts
from invest.investbase import ts_pro, get_t_code

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
my_font = matplotlib.font_manager.FontProperties(fname=r"C:\Windows\Fonts\simkai.ttf")
fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx()
pro = ts_pro()
s_date = '20170102'


def draw_stock(code):
    df = pro.hk_hold(ts_code=code, start_date=s_date)
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])
    print(df)
    name = df.iloc[0].at["name"]

    df_day = ts.pro_bar(ts_code=code, api=None, adj='qfq', start_date=s_date, asset='E', freq='D')
    df_day = df_day.sort_values(by='trade_date')
    df_day.index = pd.to_datetime(df_day["trade_date"])
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    ax1.set_ylabel('陆股通持股占比(%)', fontproperties=my_font, fontsize=18, c='b')
    ax1.plot(df.ratio, label=name, linestyle='--', linewidth=1, c='b')
    ax2.plot(df_day.close, label='close', linestyle='-', linewidth=1, c='r')
    ax1.legend(loc='best', prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc='best', prop={'family': 'SimHei', 'size': 12})
    plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()
    draw_stock(get_t_code('中国平安'))
    plt.close()
