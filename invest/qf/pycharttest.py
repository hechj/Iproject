import pandas as pd

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from math import e
from pyecharts import Bar, Line
from invest.investbase import ts_pro


pro = ts_pro()
fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx()


def func(df_param, date, d):
    if d == 1:
        value = df_param.loc[df_param.index == date, '收盘价'].values[0]
    else:
        value = df_param.loc[df_param.index == date, 'close'].values[0]
    return value


def draw_cb():
    ydata1 = []
    ydata2 = []
    index_code = '000300.SH'
    df = pro.index_daily(ts_code=index_code, start_date='20080102',
                         fields='ts_code,trade_date,open,close,pct_chg,amount')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])
    df.to_csv('300.csv', encoding='UTF-8')

    df_rate = [func(df, '2008-12-31', 2) / func(df, '2008-01-02', 2) - 1,
               func(df, '2009-12-31', 2) / func(df, '2009-01-05', 2) - 1,
               func(df, '2010-12-31', 2) / func(df, '2010-01-04', 2) - 1,
               func(df, '2011-12-30', 2) / func(df, '2011-01-04', 2) - 1,
               func(df, '2012-12-31', 2) / func(df, '2012-01-04', 2) - 1,
               func(df, '2013-12-31', 2) / func(df, '2013-01-04', 2) - 1,
               func(df, '2014-12-31', 2) / func(df, '2014-01-02', 2) - 1,
               func(df, '2015-12-31', 2) / func(df, '2015-01-05', 2) - 1,
               func(df, '2016-12-30', 2) / func(df, '2016-01-04', 2) - 1,
               func(df, '2017-12-29', 2) / func(df, '2017-01-03', 2) - 1,
               func(df, '2018-12-28', 2) / func(df, '2018-01-02', 2) - 1,
               func(df, '2019-12-31', 2) / func(df, '2019-01-02', 2) - 1,
               func(df, '2020-10-13', 2) / func(df, '2020-01-02', 2) - 1]

    paths = "E:\\MyStudy\\Jupter_prj\\"
    data = pd.read_csv(paths + '000832.csv', encoding='gbk', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])
    data.index = pd.to_datetime(data["日期"])
    # 数据切片，从2008年开始取
    data = data['2008-01-02'::]
    str_date = ['2008', '2009', '2010', '2011', '2012',
                '2013', '2014', '2015', '2016', '2017',
                '2018', '2019', '2020-10-13']
    year_rate = [func(data, '2008-12-31', 1) / func(data, '2008-01-02', 1) - 1,
                 func(data, '2009-12-31', 1) / func(data, '2009-01-05', 1) - 1,
                 func(data, '2010-12-31', 1) / func(data, '2010-01-04', 1) - 1,
                 func(data, '2011-12-30', 1) / func(data, '2011-01-04', 1) - 1,
                 func(data, '2012-12-31', 1) / func(data, '2012-01-04', 1) - 1,
                 func(data, '2013-12-31', 1) / func(data, '2013-01-04', 1) - 1,
                 func(data, '2014-12-31', 1) / func(data, '2014-01-02', 1) - 1,
                 func(data, '2015-12-31', 1) / func(data, '2015-01-05', 1) - 1,
                 func(data, '2016-12-30', 1) / func(data, '2016-01-04', 1) - 1,
                 func(data, '2017-12-29', 1) / func(data, '2017-01-03', 1) - 1,
                 func(data, '2018-12-28', 1) / func(data, '2018-01-02', 1) - 1,
                 func(data, '2019-12-31', 1) / func(data, '2019-01-02', 1) - 1,
                 func(data, '2020-10-13', 1) / func(data, '2020-01-02', 1) - 1]

    for i in year_rate:
        ydata1.append(float("%.2f" % (i * 100)))
    for i in df_rate:
        ydata2.append(float("%.2f" % (i * 100)))
    print(ydata1)
    print(ydata2)

    line = Line('年收益率', '(%)', width=1200, height=800)
    # line.add('沪深300', str_date, ydata2, is_label_show=True, xaxis_rotate=45, label_pos='top', area_opacity=0.4
    #          , area_color='red', line_opacity=0.2)
    # line.add('中债指数', str_date, ydata1, is_label_show=True, xaxis_rotate=45, label_pos='bottom', area_opacity=0.4)

    line.add('沪深300', str_date, ydata2, is_label_show=True, xaxis_rotate=45, label_pos='top')
    line.add('中债指数', str_date, ydata1, is_label_show=True, xaxis_rotate=45, label_pos='bottom')

    line.render('bar2.html')


if __name__ == '__main__':
    register_matplotlib_converters()

    draw_cb()
