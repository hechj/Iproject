'''
成交量的角度分析
'''
import baostock as bs
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker
import numpy as np
from pandas.plotting import register_matplotlib_converters

# 设置token，只需要在第一次调用或者token失效时设置
# 设置完成后，之后就不再需要这一个命令了

s_date = "20190102"
# python 量化
ts.set_token('673c8a107006b7c4a4d1a8528420874bb99e848c0241ffb95ef24f3b')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_from_ts_day():
    index_code1 = '399001.SZ'
    index_code2 = '000001.SH'
    pro = ts.pro_api()
    df1 = pro.index_daily(ts_code=index_code1, start_date=s_date,
                          fields='ts_code,trade_date,open,high,low,close,vol,amount')
    df2 = pro.index_daily(ts_code=index_code2, start_date=s_date,
                          fields='ts_code,trade_date,open,high,low,close,vol,amount')

    df1 = df1.sort_values(by='trade_date')
    df2 = df2.sort_values(by='trade_date')
    # df1.index = pd.to_datetime(df1["trade_date"])
    # df2.index = pd.to_datetime(df2["trade_date"])
    plt.style.use('seaborn-whitegrid')  # switch to seaborn style
    fig = plt.figure(figsize=(16, 9))

    plt.xticks(rotation=270)  # 旋转270度

    # plt.plot(df_basic.pe_ttm)
    df = pd.DataFrame(columns=('trade_date', 'amount'))
    df['trade_date'] = df1['trade_date']
    df['amount'] = df1['amount'] + df2['amount']
    df.index = pd.to_datetime(df["trade_date"])
    print(df.tail(10))
    # 沪深两市日成交量
    plt.plot(df.amount)

    # 0706天量？
    # axamout = df.loc[df.index == '20200706', 'amount'].values[0]
    axamout = df.loc[:, 'amount'].max()
    plt.axhline(y=axamout, color="red")
    # plt.scatter(df.index , df['amount'], alpha=0.8)
    plt.savefig('png\day.png')
    plt.show()
    plt.close()


def get_from_ts_code_day(index_code):
    pro = ts.pro_api()
    df = pro.index_daily(ts_code=index_code, start_date=s_date,
                         fields='ts_code,trade_date,open,high,low,close,vol,amount')

    df = df.sort_values(by='trade_date')
    plt.style.use('seaborn-whitegrid')  # switch to seaborn style
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)

    plt.xticks(rotation=270)  # 旋转270度
    df.index = pd.to_datetime(df["trade_date"])
    print(df[-50:-10])

    plt.plot(df.index, df.amount)

    data2 = pd.DataFrame()
    data2['trade_date'] = df['trade_date']
    x = ['2020-03-27', '2020-04-24']
    for xi in x:
        data2.loc[xi, 'amt'] = df.loc[df.index == xi, 'amount'].values[0]
    # print('data2', data2)
    plt.scatter(data2.index, data2.amt, s=np.pi * 3 ** 2, c='red', alpha=0.8)
    # 0706天量？
    # axamout = df.loc[df.index == '2020-07-07', 'amount'].values[0]
    axamout = df.loc[:, 'amount'].max()
    plt.axhline(y=axamout, color="red")
    # plt.savefig('png\day.png')
    plt.show()
    plt.close()


def get_from_ts_week():
    pro = ts.pro_api()

    '''
    使用postman或curl接口也可以实现
    {
    "api_name":"index_dailybasic",
    "token":"673c8a107006b7c4a4d1a8528420874bb99e848c0241ffb95ef24f3b",
    "params":{"ts_code":"000300.SH"},
    "fields":"ts_code,trade_date,turnover_rate,pe,pe_ttm,pb"
    }
    '''

    df_weekly = pro.index_weekly(ts_code='000300.SH', start_date=s_date,
                                 fields='ts_code,trade_date,open,high,low,close,vol,amount')

    df_weekly = df_weekly.sort_values(by='trade_date')
    print(df_weekly.head(5))
    plt.style.use('seaborn-whitegrid')  # switch to seaborn style
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    stockline = [datetime.strptime(d, '%Y%m%d').date() for d in df_weekly.trade_date]

    # plt.xticks(rotation=270)  # 旋转270度
    fig.autofmt_xdate()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=df_weekly.index.size/10))

    ax.plot(df_weekly.trade_date, df_weekly.amount)
    # plt.tight_layout()
    # plt.axhline(y=df_basic.pe_ttm[0], color="red")

    # 0228周天量
    # axamout = df_weekly.loc[df_weekly.trade_date == '20200228', 'amount'].values[0]
    axamout = df_weekly.loc[:, 'amount'].max()

    ax.axhline(y=axamout, color="red")
    ax.scatter(df_weekly.trade_date, df_weekly['amount'], alpha=0.8)
    plt.savefig('png\week.png')
    plt.show()
    plt.close()


def get_from_baostock():
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取指数(综合指数、规模指数、一级行业指数、二级行业指数、策略指数、成长指数、价值指数、主题指数)K线数据
    # 综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
    # 规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
    # 一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
    # 二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
    # 策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
    # 成长指数，例如：sz.399376 小盘成长 等；
    # 价值指数，例如：sh.000029 180价值 等；
    # 主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；

    # 详细指标参数，参见“历史行情指标参数”章节 w代表周线
    rs = bs.query_history_k_data_plus(code="sh.000300",
                                      fields="date,code,open,high,low,close,volume,amount,pctChg",
                                      start_date='2020-01-02', end_date='2020-08-31', frequency='d')
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result = result.sort_values('date', ascending=False)  # 倒序排列
    # 结果集输出到csv文件
    # result.to_csv("out/history_Index_k_data.csv", index=False)
    print(result[['date', 'close', 'amount']].head(40))

    # 登出系统
    bs.logout()


if __name__ == '__main__':
    register_matplotlib_converters()
    # get_from_ts_week()
    get_from_ts_code_day('000300.SH')
    # get_from_ts_day()
