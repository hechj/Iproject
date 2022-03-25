'''
分析指数估值
中位数，百分位数，市盈率
'''

from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
pro = ts_pro()

s_date = "20110820"
index_code = '000016.SH'

df = pro.index_daily(ts_code=index_code, start_date=s_date,
                     fields='ts_code,trade_date,close,pct_chg')

df = df.sort_values(by='trade_date')
x = np.arange(0, len(df), 1)
xt = pd.to_datetime(df['trade_date'])
y = df['close'].tolist()

x = np.reshape(x, newshape=(len(x), 1))
y = np.reshape(y, newshape=(len(y), 1))

# 调用模型
lr = LinearRegression()
# 训练模型
lr.fit(x, y)

print(lr.score(x, y))
# 计算y_hat
y_hat = lr.predict(x)
# 打印出图
plt.title(index_code + "线性回归图", fontproperties='SimHei', fontsize=18)
plt.ylabel('净值', fontproperties='SimHei', fontsize=15)
plt.plot(xt, y, color="blue")
plt.plot(xt, y_hat, color="red")
plt.show()
