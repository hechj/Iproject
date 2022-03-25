# in[1]
import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
# in[2]

from matplotlib.ticker import MultipleLocator


# in[3]
# plt.rcParams['font.family'] = ['sans-serif']
# plt.rcParams['font.sans-serif'] = ['simhei']

# in[4]
class FundData:
    code = ''  # 基金代码
    name = ''  # 基金名称
    ema_5 = []  # 5日指数移动平均
    ema_10 = []  # 10日指数移动平均
    ema_20 = []  # 20日指数移动平均
    ma_5 = []  # 5日算术移动平均
    ma_10 = []  # 10日算术移动平均
    ma_20 = []  # 20日算术移动平均
    date = []  # 日期
    dwjz = []  # 单位净值
    jjrzzl = []  # 基金日增长率
    jjweight = 0.0  # 基金权重
    jjrealzzl = []  # 基金在组合中的增长率
    roc_30 = []  # 30日价格变化率


# in[6]
# fund_code_df  = pd.read_csv( 'data/fundcode.csv', encoding='gbk',  header=0)
# buy_fund = [ line.split('/') for line in open('FundBuyRecord.txt') ]
# buy_fund_dict = {}
# for bf in buy_fund:
#     if bf[0] not in buy_fund_dict:
#         buy_fund_dict[bf[0]] = [bf[1:]]
#     else:
#         buy_fund_dict[bf[0]].append([bf[1:]])

# in[9]
def load_fund_data(fund_code, weight=1, start_date=None, end_date=None):
    fdata = FundData()
    if not end_date:
        end_date = datetime.date.today()
    else:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    if not start_date:
        start_date = (datetime.date.today() - relativedelta(month=+1))
    else:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

    data = pd.read_csv('data/%s_lsjz.csv' % str(fund_code), encoding='gbk', header=0)
    data.drop_duplicates(keep='first', inplace=True)
    data['FSRQ'] = data['FSRQ'].map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
    data['roc_30'] = data['DWJZ'] / data['DWJZ'].shift(-30) - 1
    data.sort_values(by='FSRQ', ascending=True, inplace=True)
    data.fillna(0, inplace=True)

    data = data.loc[((data['FSRQ'] >= start_date) & (data['FSRQ'] <= end_date)), :]
    data.loc[data['FSRQ'] == start_date, 'JZZZL'] = 0
    # data.loc[:, 'JZZZL'] = data.loc[:, 'JZZZL'].values.cumsum()

    # apply

    data['FDWJZ'] = data.loc[data['FSRQ'] == start_date, 'DWJZ'].values[0]  # 取开始日期的基金净值
    data.loc[:, 'JZZZL'] = (data['DWJZ'] / data['FDWJZ'] - 1) * 100

    # print(data[['FSRQ','DWJZ','JZZZL']])

    data['ema_5'] = data['DWJZ'].ewm(span=5, min_periods=5, adjust=True, ignore_na=False).mean()
    data['ema_10'] = data['DWJZ'].ewm(span=10, min_periods=10, adjust=True, ignore_na=False).mean()
    data['ema_20'] = data['DWJZ'].ewm(span=20, min_periods=20, adjust=True, ignore_na=False).mean()

    data['ma_5'] = data['DWJZ'].rolling(window=5, center=False).mean();
    data['ma_10'] = data['DWJZ'].rolling(window=10, center=False).mean();
    data['ma_20'] = data['DWJZ'].rolling(window=20, center=False).mean();

    fdata.code = fund_code
    fdata.name = str(fund_code) + fund_code_df.loc[fund_code_df['fundcode'] == int(fund_code), 'name'].values[0]
    fdata.date = [d.strftime('%Y-%m-%d') for d in data['FSRQ'].values]
    fdata.jjrzzl = data['JZZZL'].values
    fdata.dwjz = data['DWJZ'].values

    fdata.jjweight = weight
    tmp = fdata.jjrzzl
    fdata.jjrealzzl = [float(tmp[i]) * float(weight) for i in range(len(tmp))]

    fdata.ema_5 = data['ema_5'].values
    fdata.ema_10 = data['ema_10'].values
    fdata.ema_20 = data['ema_20'].values
    fdata.ma_5 = data['ma_5'].values
    fdata.ma_10 = data['ma_10'].values
    fdata.ma_20 = data['ma_20'].values
    fdata.roc_30 = data['roc_30'].values

    print(weight)
    print(fdata.jjrzzl)
    print(fdata.jjrealzzl)

    return fdata


# in[23]
def draw_fund_trend(fund_data_list, list2):
    start_date = fund_data_list[0].date[0]
    end_date = fund_data_list[0].date[-1]
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    # 把y轴的刻度间隔设置为5，并存在变量里，然后设置
    # y_major_locator = MultipleLocator(5)
    # ax.yaxis.set_major_locator(y_major_locator)

    # ax2.yaxis.set_major_locator(MultipleLocator(0.1))
    plt.xticks(rotation=270)  # 旋转270度
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # ax.xaxis.set_major_locator(MultipleLocator(7))  # 间隔7
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))  # 日期间隔

    print('fund_data_list=', fund_data_list)
    print('list2=', list2)

    t1 = [0 for x in range(len(fund_data_list[0].jjrealzzl))]
    t2 = [0 for x in range(len(list2[0].jjrealzzl))]

    plt_list = []
    fund_code_list = []
    for fund_data in fund_data_list:
        if fund_data not in plt_list and fund_data.code not in fund_code_list:
            plt_list.append(fund_data)
            fund_code_list.append(fund_data.code)
            if fund_data.code == '110026' or fund_data.code == '110020':  # 110020沪深300做为参考
                fund_data.date = pd.to_datetime(fund_data.date)
                # ax.plot(fund_data.date, fund_data.jjrzzl, label=fund_data.name, linestyle='--', linewidth=1)
                # ax2.plot(fund_data.date, fund_data.roc_30, label=fund_data.name, linestyle='--',linewidth=1)

        t1 = [i + j for i, j in zip(t1, fund_data.jjrealzzl)]

    for fund_data in list2:
        if fund_data not in plt_list and fund_data.code not in fund_code_list:
            plt_list.append(fund_data)
            fund_code_list.append(fund_data.code)
        t2 = [i + j for i, j in zip(t2, fund_data.jjrealzzl)]

    # DIY组合中QD基金是T+2更新
    df = pd.DataFrame(columns=('trade_date', 't1', 't2'))
    print(df)
    df['trade_date'] = fund_data.date[0:len(fund_data.date) - 1]
    print('长度', len(fund_data.date), len(t1), len(t2))

    # df['t1'] = t1
    # 同样的表格数据就都要-1
    df['t1'] = t1[0: len(t2) - 1]

    df['t2'] = t2[0:len(t2) - 1]
    df.index = pd.to_datetime(df["trade_date"])

    print(df.head)
    # ax.plot(df.index, df.t1, label='组合基金1走势', linestyle='-', linewidth=2)
    # ax.plot(df.index, df.t2, label='组合基金2走势', linestyle='-', linewidth=2)

    '''
    画5个2组合的买入点
    
    x = ['2020-03-27', '2020-04-24']
    data2 = pd.DataFrame()
    data2['trade_date'] = df['trade_date']
    data2.index = df.index
    for xi in x:
        data2.loc[xi, 't2'] = df.loc[df.index == xi, 't2'].values[0]
    print('data2', data2)
    ax.scatter(data2.index, data2.t2, s=np.pi * 3 ** 2, c='red', alpha=0.8)

    print(plt_list)
'''
    # fig.autofmt_xdate()  # 斜的日期标签
    # 画所有自选基金走势
    for plist in plt_list:
        plist.date = pd.to_datetime(plist.date)
        plt.plot(plist.date, plist.jjrzzl, label=plist.name, linestyle='-', linewidth=2)
    print("类型", type(plist.date))
    print(plist.date)
    ax.set_ylabel('基金累计涨幅(%)', fontproperties='SimHei', fontsize=15)
    ax2.set_ylabel(r"30日价格变化率", fontproperties='SimHei', fontsize=15)

    # # loc=代表图例及位置： 1右上角，2 左上角 3左下角 4右下角  同象限的划分 'best'最优
    ax.legend(loc=3, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc='best', prop={'family': 'SimHei', 'size': 12})

    plt.title("基金业绩走势", fontproperties='SimHei', fontsize=18)
    plt.grid(b='major', color='k', linestyle='--', linewidth=1, alpha=0.3)
    plt.savefig("result.png")
    plt.show(block=True)
    plt.close()


def draw_fund_trend_with_jjzz(fund_data):
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)

    plt.plot(fund_data.date, fund_data.dwjz, label=fund_data.name, linestyle='-', linewidth=2)
    plt.plot(fund_data.date, fund_data.ema_5, label='5日指数均线', linestyle='-', linewidth=1)
    plt.plot(fund_data.date, fund_data.ema_10, label='10日指数均线', linestyle='-', linewidth=1)
    plt.plot(fund_data.date, fund_data.ema_20, label='20日指数均线', linestyle='-', linewidth=1)

    plt.ylabel('基金净值', fontproperties='SimHei', fontsize=15)
    ax.axes.set_xticklabels(fund_data.date, rotation=90)

    plt.legend(prop={'family': 'SimHei', 'size': 12})
    plt.title("基金业绩走势", fontproperties='SimHei', fontsize=18)
    plt.show(block=True)
    plt.close()


# in[35]
# data_list = []
# for fund_code in buy_fund_dict.keys():
#     try:
#         data = load_fund_data(fund_code,start_date='2020-02-03')
#         if data:
#             data_list.append(data)
#     except FileNotFoundError:
#         print('未找到该基金%s' %fund_code)

# in[36]
# draw_fund_trend(data_list)


def buy_some_fund(filename):
    buy_fund = [line.split('/') for line in open(filename, encoding='gbk')]
    global buy_fund_dict
    buy_fund_dict = {}
    for bf in buy_fund:
        if bf[0] not in buy_fund_dict:
            buy_fund_dict[bf[0]] = [bf[1:]]
        else:
            buy_fund_dict[bf[0]].append([bf[1:]])
    data_list = []
    print(buy_fund_dict.keys())
    for fund_code in buy_fund_dict.keys():
        try:
            if fund_code is not None:
                for bfw in buy_fund:
                    if fund_code == bfw[0]:
                        w = bfw[3].strip()
                print('买入该基金%s' % fund_code)
            else:
                break
            data = load_fund_data(fund_code, w, start_date='2011-11-21')  # 需传入有基金净值的交易日
            if data:
                data_list.append(data)
        except FileNotFoundError:
            print('未找到该基金%s' % fund_code)
    return data_list


if __name__ == '__main__':
    register_matplotlib_converters()
    plt.rcParams['font.family'] = ['sans-serif']

    # 正常显示画图中的中文和负号
    plt.rcParams['font.sans-serif'] = ['simhei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('seaborn-whitegrid')  # switch to seaborn style
    # plt.style.use('default')  # switches back to matplotlib style

    buy_fund_dict = {}
    fund_code_df = pd.read_csv('data/fundcode.csv', encoding='gbk', header=0)

    # draw_fund_trend(buy_some_fund('diy.txt'), buy_some_fund('22222.txt'))
    draw_fund_trend(buy_some_fund('110026.txt'), buy_some_fund('110020.txt'))

    # data = load_fund_data('110026', start_date='2019-12-02')
    # draw_fund_trend_with_jjzz(data)
