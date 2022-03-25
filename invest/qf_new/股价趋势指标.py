# -*- coding: UTF-8 -*-
import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()


def drawline(tcode, sdate):
    # 前复权处理
    datadf = ts.pro_bar(ts_code=tcode, api=None, adj='qfq', start_date=sdate, asset='E', freq='D')
    datadf = datadf.sort_values(by='trade_date').reset_index(drop=True)
    datadf['ma_60'] = datadf['close'].rolling(window=60, center=False).mean()
    datadf['ma_250'] = datadf['close'].rolling(window=250, center=False).mean()
    datadf['sub_'] = datadf['ma_60'] - datadf['ma_250']
    datadf['div_'] = datadf['ma_60'] / datadf['ma_250']
    datadf['vol_5'] = datadf['vol'].rolling(window=5, center=False).mean()
    datadf = datadf[5::].reset_index()
    datadf['vol_active'] = datadf['vol_5'] / datadf.loc[0, 'vol_5']
    print(datadf)
    stockline = [datetime.strptime(d, '%Y%m%d').date() for d in datadf.trade_date]
    #    plt.figure(figsize=(12, 6), facecolor='none')  # 设置画布大小,长、宽,facecolor显示的是画布的背景，非图形的背景
    ax1.plot(stockline, datadf.close, '-', label=datadf.ts_code[0])
    ax1.plot(stockline, datadf.ma_60, '-', label="MA_60")
    ax1.plot(stockline, datadf.ma_250, '-', label="MA_250")
    # ax1.plot(stockline, datadf.sub_, '-', label="sub")
    ax2.plot(stockline, datadf.div_, '--', color='r', label="3/12")
    div_std = datadf['div_'].std()
    print('标准差', div_std)
    ax2.axhline(y=datadf['div_'].mean(), ls='--', c='black')
    ax2.axhline(y=datadf['div_'].mean() + div_std, ls='--', c='gray')
    ax2.axhline(y=datadf['div_'].mean() - div_std, ls='--', c='gray')
    # ax1.axhline(y=0)

    # for index, row in datadf.iterrows():
    #     if index >= len(datadf) - 1:
    #         break
    #     elif datadf.loc[index, 'sub_'] * datadf.loc[index + 1, 'sub_'] < 0:
    #         print(row['trade_date'])
    #         ax1.axvline(x=pd.to_datetime(row['trade_date']), linestyle='--', color='gray')


def drawmain():
    # 设置时间按“年月”的格式显示
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
    # X轴按年进行标记，还可以用MonthLocator()和DayLocator()
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    # 显示图例
    ax1.legend()
    ax2.legend()
    # 显示图片
    plt.show()


def taskmain():
    # 在tushare官网注册后，进入个人中心得到你的唯一指定token，替换***
    ts.set_token('673c8a107006b7c4a4d1a8528420874bb99e848c0241ffb95ef24f3b')
    # 初始化api
    api = ts.pro_api()

    for cd in tscode:
        drawline(cd, startdate)


# 指定起止日期
startdate = '2010-02-27'
# 指定股票代码
tscode = {'601318.SH'}
# 主程序
taskmain()
drawmain()
