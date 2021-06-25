'''
某年某月某日起指数收益率展示


'''

import matplotlib
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
from invest.investbase import ts_pro
# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

import matplotlib.font_manager as fm

myfont = fm.FontProperties(fname='C:/Windows/Fonts/simsun.ttc')
pro = ts_pro()

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)

# 传入有净值的日期
startdate = '20201202'

dict = {'399006.SZ': '创业板指', '000300.SH': '沪深300', '000016.SH': '上证50', '000905.SH': '中证500', '000852.SH': '中证1000'}


def drawline(tcode, color):
    df = pro.index_daily(ts_code=tcode, start_date=startdate,
                         fields='ts_code,trade_date,close')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])

    startvalue = df.loc[df.trade_date == startdate, 'close'].values[0]
    df['ret_rate'] = (df.close / startvalue - 1) * 100
    print(df)
    plt.plot(df.index, df.ret_rate, label=dict[df.ts_code[0]], linestyle='-', linewidth=1, color=color, alpha=1)


if __name__ == '__main__':
    register_matplotlib_converters()

    # drawline(tcode='399006.SZ', color='purple')
    # drawline(tcode='000300.SH', color='red')
    drawline(tcode='000852.SH', color='blue')
    drawline(tcode='000905.SH', color='darkgreen')
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.title("收益率展示图", fontproperties='SimHei', fontsize=18)
    ax.set_ylabel(r"收益率(%)", fontproperties='SimHei', fontsize=15)
    plt.grid(b='major', color='orange', linestyle='--', linewidth=1, alpha=0.15)
    # 显示图片
    plt.show()
    plt.close()
