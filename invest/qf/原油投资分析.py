import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
from pandas.plotting import register_matplotlib_converters
import datetime, time
from invest.investbase import ts_pro

pro = ts_pro()
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

'''
501018.SH   南方原油
160723.SZ   嘉实原油
004243      广发道琼斯石油指数人民币C
'''
datadf = pro.fund_daily(ts_code="501018.SH", start_date='20160628')
datadf['trade_date'] = datadf['trade_date'].map(lambda x: datetime.datetime.strptime(x, '%Y%m%d').date())
datadf = datadf.rename(columns={'trade_date': 'FSRQ'})

datadf.index = pd.to_datetime(datadf.FSRQ)
datadf = datadf.sort_index()

datadf = datadf[:-1]
startdate = "2017-04-21"

s_code = "004243"

def draw_wti():
    data = pd.read_csv('WTI原油期货历史数据.csv', encoding='utf-8', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])

    # 将*年*月*日数据转化成pandas日期格式
    data['日期'] = data['日期'].map(lambda x: time.strptime(x, u"%Y年%m月%d日"))
    data['日期'] = data['日期'].map(lambda x: time.strftime('%Y-%m-%d', x))
    data.index = pd.to_datetime(data["日期"])
    #     print(data)
    # 数据切片，从**年开始取
    data = data[startdate::]
    startvalue = data.loc[data['日期'] == startdate, '收盘'].values[0]
    data['ret_rate'] = (data['收盘'] / startvalue - 1) * 100
    return data


data = pd.read_csv('%s_lsjz.csv' % str(s_code), encoding='gbk', header=0)
data.drop_duplicates(keep='first', inplace=True)

data.index = pd.to_datetime(data.FSRQ)
data = data.sort_index()
# 数据切片，从**年开始取
data = data[startdate::]
startvalue = data.loc[data.FSRQ == startdate, 'LJJZ'].values[0]
data['ret_rate'] = (data.LJJZ / startvalue - 1) * 100
data.fillna(0, inplace=True)

data2 = pd.read_csv('%s_lsjz.csv' % str("160723"), encoding='gbk', header=0)
data2.drop_duplicates(keep='first', inplace=True)

data2.index = pd.to_datetime(data2.FSRQ)
data2 = data2.sort_index()
# 数据切片，从**年开始取
data2 = data2[startdate::]
data2.fillna(0, inplace=True)

if __name__ == '__main__':
    register_matplotlib_converters()

    fig = plt.figure(figsize=(16, 9))
    ax1 = fig.add_subplot(111)

    ax2 = ax1.twinx()

    ax2.plot(data.LJJZ, label="004243场外净值(右)", linestyle='-', linewidth=1, color='purple', alpha=1)

    ax1.plot(data.ret_rate, label="004243场外收益率(%)", linestyle='-', linewidth=1, color='red', alpha=1)
    df = draw_wti()
    print(df)
    ax1.plot(df["ret_rate"], label='WTI原油涨幅(%)', linestyle='-', color='blue', linewidth=1, alpha=1)
    ax2.plot(data2['LJJZ'], label="嘉实原油场外净值(右)", linestyle='-', linewidth=1, color='gold', alpha=1)
    # ax2.plot(datadf['close'], label="场内收盘价", linestyle='-', linewidth=1, color='gold', alpha=1)
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()

    # loc = 2,左上角；1,右上角
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})

    plt.show()

    df['收盘'].plot()
    plt.show()

    plt.close()
