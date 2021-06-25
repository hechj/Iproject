'''

AR指标是通过比较某个周期内开盘价与最高、最低价，来反映市场买卖人气。
计算公式为：N日AR=(N日内（H－O）之和）/(N日内（O－L）之和)*100。

BR指标是通过比较一段周期内收盘价在该周期价格波动中的地位，来反映市场买卖意愿程度。
计算公式为：N日BR=（N日内（H－YC）之和）/N日内（YC－L）之和）*100。

其中，O 为当日开盘价，H 为当日最高价，L 为当日最低价，YC 为前一交易日的收盘价，N 为设定的时间参数，
一般原始参数日设定为 26 日，计算周期可以根据自己的经验或回测结果进行修正。

BRAR指标的讯号不如其他指标明确，许多关键点必须靠个人的领悟及自由心证，并且不同交易市场，BRAR高低档数据皆不尽相同。
双方的分界线是 100，100 以上是多方优势，100 以下是空方优势。

买入信号：
BR通常运行在AR上方，一旦BR跌破AR并在AR之下运行时，表明市场开始筑底，视为买进信号；BR<40,AR<60: 空方力量较强，但随时可能反转上涨，考虑买进。
开盘价低于昨日收盘价？？
卖出信号：
BR>400,AR>180，多方力量极强，但随时可能反转下跌，考虑卖出；BR快速上升，AR并未上升而是小幅下降或横盘，视为卖出信号。

背离信号：
AR、BR指标的曲线走势与股价K线图上的走势正好相反。

顶背离：
当股价K线图上的股票走势一峰比一峰高，股价一直向上涨，而AR、BR指标图上的走势却一峰比一峰低，说明出现顶背离，股价短期内将高位反转，是比较强烈的卖出信号。

底背离：
当股价K线图上的股票走势一底比一底低，股价一直向下跌，而AR、BR指标图上的走势却一底比一底高，说明出现底背离，股价短期内将低位反转，是比较强烈的买入信号。

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

# 引入TA-Lib库
import talib as ta
from invest.investbase import ts_pro, get_t_code
# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

index = {'上证综指': '000001.SH', '深证成指': '399001.SZ',
         '沪深300': '000300.SH', '创业板指': '399006.SZ',
         '上证50': '000016.SH', '中证500': '000905.SH',
         '中小板指': '399005.SZ', '上证180': '000010.SH'}


# 默认设定时间周期为当前时间往前推120个交易日
# 日期可以根据需要自己改动
def get_data(code, n=120):
    from datetime import datetime, timedelta
    t = datetime.now()
    t0 = t - timedelta(n)
    start = t0.strftime('%Y%m%d')
    end = t.strftime('%Y%m%d')
    # 如果代码在字典index里，则取的是指数数据
    if code in index.values():
        df = ts_pro().index_daily(ts_code=code, start_date=start, end_date=end)
    # 否则取的是个股数据
    else:
        df = ts_pro().daily(ts_code=code, start_date=start, end_date=end)
    # 将交易日期设置为索引值
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()
    # 计算收益率
    return df


# 计算AR、BR指标
def arbr(stock, n=120):
    code = get_t_code(stock)
    df = get_data(code, n)[['open', 'high', 'low', 'close']]
    df['HO'] = df.high - df.open
    df['OL'] = df.open - df.low
    df['HCY'] = df.high - df.close.shift(1)
    df['CYL'] = df.close.shift(1) - df.low
    # 计算AR、BR指标
    df['AR'] = ta.SUM(df.HO, timeperiod=26) / ta.SUM(df.OL, timeperiod=26) * 100
    df['BR'] = ta.SUM(df.HCY, timeperiod=26) / ta.SUM(df.CYL, timeperiod=26) * 100
    return df[['close', 'AR', 'BR', 'open', 'high', 'low']].dropna()


# 对价格和ARBR进行可视化
def plot_arbr(stock, n=120):
    df = arbr(stock, n)
    print('行数=', df.shape[0], 'n=', n)
    print(df)
    fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
    ax2 = ax1.twinx()
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    ax1.plot(df.close, label=stock, linestyle='-', c='b', linewidth=1)

    ax2.plot(df.AR, label='AR', linestyle='-', linewidth=1)
    ax2.plot(df.BR, label='BR', linestyle='-', linewidth=1)
    ax2.axhline(y=40, color="red")
    ax2.axhline(y=60, color="red")
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()

    # plot_arbr('创业板指', n=250)
    # plot_arbr('沪深300', n=250)
    plot_arbr('中国平安', n=1000)
    plt.close()

'''
股票市场上，随着多空双方的较量，股价会向上或向下偏离这一平衡价位区，股价偏离得越大，说明力量越大，偏离得越小，说明力量越小。
因此,利用股票各种价格之间的关系，找到这个平衡价位区，对研判多空力量的变化起着重要的作用。
而ARBR指标就是根据股票的开盘价、收盘价、最高价和最低价之间的关系来分析多空力量的对比，预测股价的未来走势。
ARBR指标计算简单，容易理解，但是使用起来并非容易，需要深厚的实盘交易经验才能作出准确判断。
另外，ARBR指标也存在一定的局限性，如只利用了历史价格信息，而忽略了成交量的重要性。
'''
