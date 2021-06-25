# Python 量化分析ETF指数基金投资
import pandas as pd
import numpy as np
import tushare as ts
from matplotlib import pyplot as plt
import talib

plt.style.use('seaborn')

with open('token.txt') as f:
    token = f.readline()
ts.set_token(token)

print(token)

pro = ts.pro_api()
df = pro.fund_daily(ts_code='510500.SH', start_date='20160101', end_date='20200707')

etf500 = df.sort_values(by='trade_date')
etf500['trade_date'] = pd.to_datetime(etf500['trade_date'], format='%Y%m%d')
etf500.head()

etf500.set_index('trade_date', inplace=True)
etf500.head()

etf500.describe()

# 获取一下最低收盘价的价格和日期.
# print(etf500['close'].min(),etf500['close'].idxmin())

# 获取一下最高收盘价的价格和日期
# print(etf500['close'].max(),etf500['close'].idxmax())

# 获取一下成交量最低的情况
# print(etf500[etf500['amount'].idxmin():etf500['amount'].idxmin()])

# 获取收盘价,并画出图形.
cl = etf500[['close']]
closed = cl.copy()
closed.plot()
plt.show()
# 增加两列,分别是用talib计算2日和20日均线.
closed['MA2'] = talib.SMA(closed.close, timeperiod=2)
closed['MA20'] = talib.SMA(closed.close, timeperiod=20)

# pct_chang()计算出每天变化的百分比.
closed['pct_chg'] = closed.close.pct_change()

# 每日收益变化曲线.
closed['pct_chg'].plot(figsize=(30, 5))
plt.show()
closed.loc[np.abs(closed['pct_chg']) > 0.065]  # 算出收益率变化最大的几天

fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].hist(closed['pct_chg'].dropna(), color='g', bins=50)
axes[1].hist(closed['close'].dropna())

closed['log_ret'] = np.log(closed.close / closed.close.shift(1))  # 计算对数收益率
# closed['log_ret'].plot(figsize=(30,5),color='r') #输出对数收益率

cumulative_rets = closed.log_ret.cumsum().values  # 对数收益率进行累计求和,可以计算出从开始到每个时间点的收益率
plt.figure(figsize=(30, 5))
plt.plot(cumulative_rets)

diff_ma2_ma20 = closed.MA2 - closed.MA20
closed['hold'] = np.where(closed.MA2 > closed.MA20, closed.MA2, None)  # 这里把赋值为None，下面画图好看一点
closed[['MA2', 'MA20', 'hold']].plot(figsize=(30, 5))
plt.title("STOCK:510500", weight='bold');  # 红色的线表示持股的时间

stragy_ret = np.where(closed.hold > 0, closed.log_ret, 0)
stragy_ret = stragy_ret.cumsum()
plt.figure(figsize=(30, 5))
plt.plot(stragy_ret)
plt.plot(cumulative_rets)
plt.show()

print("strage= {},hold ={}".format(np.exp(stragy_ret[-1]), np.exp(cumulative_rets[-1])))

closed.close[-1] / closed.close[0]

year_ret = np.exp(stragy_ret[-1] / 4)
