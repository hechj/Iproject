import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro
from pylab import mpl
import numpy as np

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
pro = ts_pro()

fig = plt.figure()
ax1 = fig.add_subplot(111)
# ax2 = ax1.twinx()

s_date = "20110820"
index_code = '000001.SH'

df = pro.index_daily(ts_code=index_code, start_date=s_date,
                     fields='ts_code,trade_date,close,pct_chg')

df = df.sort_values(by='trade_date')
df.index = pd.to_datetime(df["trade_date"])
df['close_forward'] = df['close'].shift(250)
df.dropna(axis=0, subset=["close_forward"], inplace=True)
df['yoy'] = np.log(df['close']) - np.log(df['close_forward'])
print(df)

plt.title("上证指数同比")
ax1.plot(df.yoy, '-', label="yoy", linewidth=0.5, alpha=1)
ax1.axhline(y=0, c='r')
# 设置时间按“年月”的格式显示
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
# 自动旋转日期标记以避免重叠
plt.gcf().autofmt_xdate()
# 显示图例
ax1.legend()
# 显示图片
plt.show()
plt.close()
