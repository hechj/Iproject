import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib.animation as ani
from matplotlib.pyplot import MultipleLocator

from invest.investbase import ts_pro

pro = ts_pro()
s_date = '20100601'  # 深圳证券交易所于2010年6月1日起正式编制和发布创业板指数
df_300 = pro.index_daily(ts_code='000300.SH', start_date=s_date,
                         fields='ts_code,trade_date,close')
df_300 = df_300.sort_values(by='trade_date')
df_300.index = pd.to_datetime(df_300["trade_date"])
i_value = df_300.loc[df_300.trade_date == s_date, 'close'].values[0]
df_300['rate'] = (df_300.close / i_value - 1) * 100
df_cyb = pro.index_daily(ts_code='399006.SZ', start_date=s_date,
                         fields='ts_code,trade_date,close')
df_cyb = df_cyb.sort_values(by='trade_date')
df_cyb.index = pd.to_datetime(df_cyb["trade_date"])
i_value = df_cyb.loc[df_cyb.trade_date == s_date, 'close'].values[0]
df_cyb['rate'] = (df_cyb.close / i_value - 1) * 100
print(df_cyb)
nums = df_300.shape[0]
if df_cyb.shape[0] != df_300.shape[0]:
    print("数据不相等")
    exit(0)
x = []
y1 = []
y2 = []

register_matplotlib_converters()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
'''
'''
plt.rcParams['animation.ffmpeg_path'] = r'D:\01_software\ffmpeg-4.4-essentials_build\bin\ffmpeg.exe'

fig, ax = plt.subplots()
y_major_locator = MultipleLocator(50)
ax.yaxis.set_major_locator(y_major_locator)

ax.set_ylim(-100, 500)
ax.set_xlim([df_300.index[0], df_300.index[nums - 1]])
plt.gcf().autofmt_xdate()

plt.grid(b='major', color='orange', linestyle='--', linewidth=1, alpha=0.15)
line1, = ax.plot(x, y1, label="沪深300", linestyle='-', linewidth=1, color='red')
line2, = ax.plot(x, y2, label="创业板", linestyle='-', linewidth=1, color='blue')
plt.legend()
plt.title("大小盘对比", fontproperties='SimHei', fontsize=18)
ax.set_ylabel(r"收益率(%)", fontproperties='SimHei', fontsize=15)


def init():
    x.clear()
    y1.clear()
    y2.clear()
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2,


def update(i):
    x.append(df_300.index[i])
    y1.append(df_300.rate[i])
    y2.append(df_cyb.rate[i])
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2,


p_ani = ani.FuncAnimation(fig, update,
                          frames=range(0, nums, 1),  # update函数的参数范围
                          init_func=init,
                          interval=5, blit=True, repeat=False)
p_ani.save('风格切换.mp4', writer='ffmpeg', fps=80)

p_ani.save('风格切换.gif')
'''
'''
# (df_300['close'] / df_cyb['close']).plot(color='darkblue', linestyle='-', linewidth=1, title='沪深300/创业板')

plt.show()
