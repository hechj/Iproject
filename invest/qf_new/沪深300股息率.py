"""
手动计算沪深300股息率
1.得到成分股及权重
2.每支成分股加权计算股息率

"""
import time
from datetime import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
from invest.investbase import ts_pro
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
pro = ts_pro()


def get_cal_date(start, end):
    df_cal = pro.trade_cal(exchange='', start_date=start, end_date=end)
    df_cal = df_cal[df_cal.is_open == 1]
    df_cal['month'] = df_cal['cal_date'].str[:6]

    df_cal['match1'] = df_cal.month != df_cal.month.shift(1)
    df_cal['match2'] = df_cal.month != df_cal.month.shift(-1)
    df_cal['match'] = df_cal.match1 | df_cal.match2
    #     df_cal = df_cal[df_cal.match1 == True] # 取每个月第一个交易日
    #     df_cal = df_cal[df_cal.match2 == True] # 取每个月最后一个交易日
    df_cal = df_cal[df_cal.match == True]  # 获取的是交易日历的每月第一天和最后一天
    print(df_cal)
    date = df_cal.cal_date.values
    return date


# 获取成分股数据
def get_dv(date_nums):
    df_d = pd.DataFrame()
    # 拆分时间进行拼接，再删除重复项
    dlen = len(date_nums)
    print(date_nums)
    print('dlen=', dlen)
    for j in range(0, dlen):
        time.sleep(0.2)  # 休眠
        d0 = pro.index_weight(index_code='399300.SZ', trade_date=date_nums[j])
        df_d = pd.concat([d0, df_d])
        df_d = df_d.drop_duplicates()
    df_d = df_d.reset_index(drop=True)
    return df_d


s_date = '20210615'
e_date = '20210630'

# 获取交易日历
dates = get_cal_date(s_date, e_date)
df_get_dv = get_dv(dates)
df_get_dv = df_get_dv.iloc[::-1]

print(df_get_dv)

paths = "E:\\MyStudy\\datas\\"
data = pd.read_csv(paths + '中国十年期国债收益率历史数据.csv', encoding='utf-8', header=0)

# 数据切片，数据倒序排列
data = data.reindex(index=data.index[::-1])

# 将*年*月*日数据转化成pandas日期格式
data['日期'] = data['日期'].map(lambda x: time.strptime(x, u"%Y年%m月%d日"))
data['日期'] = data['日期'].map(lambda x: time.strftime('%Y%m%d', x))
data = data.set_index("日期")
print(data)

i = 0
df_plt = pd.DataFrame(columns=('date_dv', 'dv', 'rate'), index=np.arange(len(dates)))
for date in dates:
    print("正在获取", "i=", i, date, "成分股:")
    time.sleep(1)  # 休眠1秒
    df1 = df_get_dv[df_get_dv['trade_date'] == date]
    df1 = df1.reset_index(drop=True)
    if df1.empty:
        print("df1为空")
        continue
    print(df1)
    df_ttm = pd.DataFrame()

    for j in range(len(df1.con_code)):
        time.sleep(0.1)
        df11 = pro.daily_basic(ts_code=df1.con_code[j], trade_date=date, fields='trade_date,ts_code, dv_ratio, dv_ttm')
        df11['weight'] = df1.weight[j]
        df_ttm = pd.concat([df_ttm, df11])
        df_ttm['dv_ttm'].fillna(0, inplace=True)  # df_ttm['dv_ratio']表示dv_ttm为空值用dv_ratio填充

    print(df_ttm)
    df_ttm['ttm_total'] = df_ttm['dv_ttm'] * df_ttm['weight']

    dv_value = df_ttm['ttm_total'].sum() / 100
    rate_value = dv_value / data.loc[date, '收盘']
    df_plt.loc[i] = [date, dv_value, rate_value]
    i = i + 1
df_plt.dropna(axis=0, inplace=True)
df_plt.index = pd.to_datetime(df_plt["date_dv"])
# df_plt.to_csv('dv_new.csv', mode="a+", header=False, index=False)
print(df_plt)
plt.figure(figsize=(12, 6))
plt.title("沪深300股息率/十年期国债收益率")
# plt.plot(df_plt.index, df_plt.dv, "b", marker='*', ms=3, label="dv")
plt.plot(df_plt.index, df_plt.rate, "r", marker='.', ms=3, label="rate")
plt.axhline(y=0.8, color="black")
plt.legend()
plt.show()
