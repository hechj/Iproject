import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from invest.investbase import ts_pro
import empyrical

import matplotlib as mpl
# pandas赋值老提示警告
import warnings

warnings.filterwarnings('ignore')

mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']
mpl.rcParams['axes.unicode_minus'] = False

pro = ts_pro()


# 获取交易日历
def get_cal_date(start, end):
    cal_date = pro.trade_cal(exchange='', start_date=start, end_date=end)
    cal_date = cal_date[cal_date.is_open == 1]
    dates = cal_date.cal_date.values
    return dates


# 获取北向资金数据
def get_north_money(start, end):
    # 获取交易日历
    dates = get_cal_date(start, end)
    # tushare限制流量，每次只能获取300条记录
    df = pd.DataFrame()
    # 拆分时间进行拼接，再删除重复项
    dlen = len(dates)
    print(dlen)
    times = dlen // 300 + (0 if (dlen % 300 == 0) else 1)
    for i in range(0, times):
        if i == times - 1 and dlen % 300 != 0:
            d0 = pro.moneyflow_hsgt(start_date=dates[300 * i], end_date=dates[300 * i + dlen % 300 - 1])
        else:
            d0 = pro.moneyflow_hsgt(start_date=dates[300 * i], end_date=dates[300 * i + 300 - 1])

        df = pd.concat([d0, df])
        # 删除重复项
        df = df.drop_duplicates()
        df.index = pd.to_datetime(df.trade_date)
        df = df.sort_index()
    return df


# 获取指数数据
def get_index_data(code, start, end):
    index_df = pro.index_daily(ts_code=code, start_date=start, end_date=end)
    index_df.index = pd.to_datetime(index_df.trade_date)
    index_df = index_df.sort_index()
    return index_df


def North_Strategy(data, window, stdev_n, cost):
    '''输入参数：
    data:包含北向资金和指数价格数据
    window:移动窗口
    stdev_n:几倍标准差
    cost:手续费
    '''
    # 中轨
    df = data.copy().dropna()
    df['mid'] = df['北向资金'].rolling(window).mean()
    stdev = df['北向资金'].rolling(window).std()
    # 上下轨
    df['upper'] = df['mid'] + stdev_n * stdev
    df['lower'] = df['mid'] - stdev_n * stdev
    df['ret'] = df.close / df.close.shift(1) - 1
    df.dropna(inplace=True)

    # 北向资金按月求和

    # df['month'] = df.index.to_period('M')
    # df_sum = df.groupby(df.month)['北向资金'].sum().reset_index()
    # df_sum['month'] = df_sum['month'].map(lambda x: x.asfreq('D', 'end').to_timestamp())

    df['week'] = df.index.to_period('W')
    df_sum = df.groupby(df.week)['北向资金'].sum().reset_index()
    df_sum['week'] = df_sum['week'].map(lambda x: x.asfreq('D', 'end').to_timestamp())

    print(df_sum)
    # 设计买卖信号
    # 当日北向资金突破上轨线发出买入信号设置为1 且持仓为空
    # 当日北向资金跌破下轨线发出卖出信号设置为0
    df['position'] = np.nan
    df['signal'] = np.nan
    df = df.copy()
    flag = 0
    for i in range(1, df.shape[0] - 1):
        if df['北向资金'][i] > df.upper[i] and df['position'][i - 1] != 1:
            df['signal'][i] = 1
            flag = 1

        if df['北向资金'][i] < df.lower[i] and df['position'][i - 1] == 1:
            df['signal'][i] = 0
            flag = 0

        df = df.copy()
        if flag == 1:
            df['position'][i] = 1
        else:
            df['position'][i] = 0
    # df.loc[df['北向资金']>df.upper , 'signal'] = 1
    # df.loc[df['北向资金']<df.lower, 'signal'] = 0

    df['position'] = df['signal'].shift(1)
    df['position'].fillna(method='ffill', inplace=True)
    df['position'].fillna(0, inplace=True)

    # 根据交易信号和仓位计算策略的每日收益率
    df.loc[df.index[0], 'capital_ret'] = 0
    # 今天开盘新买入的position在今天的涨幅(扣除手续费)
    df.loc[df['position'] > df['position'].shift(1), 'capital_ret'] = \
        (df.close / df.open - 1) * (1 - cost)
    # 卖出同理
    df.loc[df['position'] < df['position'].shift(1), 'capital_ret'] = \
        (df.open / df.close.shift(1) - 1) * (1 - cost)
    # 当仓位不变时,当天的capital是当天的change * position
    df.loc[df['position'] == df['position'].shift(1), 'capital_ret'] = \
        df['ret'] * df['position']
    # 计算标的、策略、指数的累计收益率
    df['策略净值'] = (df.capital_ret + 1.0).cumprod()
    df['指数净值'] = (df.ret + 1.0).cumprod()
    return df, df_sum


'''   
    DataFrame.cummax(axis=None, skipna=True, *args, **kwargs)
    返回一个DataFrame或Series轴上的累积最大值。
    返回包含累积最大值的相同大小的DataFrame或Series。
'''


def performance(df, name):
    df1 = df.loc[:, ['ret', 'capital_ret']]
    # 计算每一年(月,周)股票,资金曲线的收益
    year_ret = df1.resample('A').apply(lambda x: (x + 1.0).prod() - 1.0)
    month_ret = df1.resample('M').apply(lambda x: (x + 1.0).prod() - 1.0)
    week_ret = df1.resample('W').apply(lambda x: (x + 1.0).prod() - 1.0)
    # 去掉缺失值
    year_ret.dropna(inplace=True)
    month_ret.dropna(inplace=True)
    week_ret.dropna(inplace=True)
    # 计算策略的年（月，周）胜率
    year_win_rate = len(year_ret[year_ret['capital_ret'] > 0]) / len(year_ret[year_ret['capital_ret'] != 0])
    month_win_rate = len(month_ret[month_ret['capital_ret'] > 0]) / len(month_ret[month_ret['capital_ret'] != 0])
    week_win_rate = len(week_ret[week_ret['capital_ret'] > 0]) / len(week_ret[week_ret['capital_ret'] != 0])
    # 计算总收益率、年化收益率和风险指标
    total_ret = df[['策略净值', '指数净值']].iloc[-1] - 1
    annual_ret = pow(1 + total_ret, 250 / len(df1)) - 1

    dd = (df[['策略净值', '指数净值']].cummax() - df[['策略净值', '指数净值']]) / \
         df[['策略净值', '指数净值']].cummax()
    print("---")
    print(dd)
    d = dd.max()
    beta = df[['capital_ret', 'ret']].cov().iat[0, 1] / df['ret'].var()
    alpha = annual_ret['策略净值'] - annual_ret['指数净值'] * beta
    exReturn = df['capital_ret'] - 0.03 / 250
    print('----------')
    print(total_ret)
    print(annual_ret)
    print(len(exReturn), '标准差:', df['capital_ret'].std(), exReturn.std())
    print('日平均无风险回报:', exReturn.mean())

    alpha2, beta2 = empyrical.alpha_beta(returns=df['capital_ret'], factor_returns=df['ret'],
                                         annualization=250)

    # 无风险收益，默认3
    rf = 0.03 / 250.0
    arr = df['capital_ret']
    sharpe_r = empyrical.sharpe_ratio(arr, rf, annualization=len(df['capital_ret']))

    vol_annual1 = np.sqrt(250) * arr.std()
    vol_annual2 = np.sqrt(250) * df['ret'].std()
    print(f'策略年化波动率为： {round(vol_annual1 * 100, 2)}%')
    print(f'{name}年化波动率为： {round(vol_annual2 * 100, 2)}%')
    sharper_atio = np.sqrt(len(exReturn)) * exReturn.mean() / df['capital_ret'].std()
    TA1 = round(total_ret['策略净值'] * 100, 2)
    TA2 = round(total_ret['指数净值'] * 100, 2)
    AR1 = round(annual_ret['策略净值'] * 100, 2)
    AR2 = round(annual_ret['指数净值'] * 100, 2)
    MD1 = round(d['策略净值'] * 100, 2)
    MD2 = round(d['指数净值'] * 100, 2)
    S = round(sharper_atio, 2)
    # 输出结果
    print(f'策略年胜率为：{round(year_win_rate * 100, 2)}%')
    print(f'策略月胜率为：{round(month_win_rate * 100, 2)}%')
    print(f'策略周胜率为：{round(week_win_rate * 100, 2)}%')

    print(f'总收益率：  策略：{TA1}%，{name}：{TA2}%')
    print(f'年化收益率：策略：{AR1}%, {name}：{AR2}%')
    print(f'最大回撤：  策略：{MD1}%, {name}：{MD2}%')
    print(f'策略Alpha： {alpha},{alpha2}, Beta：{beta},{beta2}，夏普比率：{sharper_atio},{sharpe_r}')


# 对策略累计收益率进行可视化
def plot_performance(df, df2, name):
    fig = plt.figure()
    plt.style.use("ggplot")

    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    d1 = df[['策略净值', '指数净值', 'signal']]
    ax1.plot(df['策略净值'], label='策略净值', linestyle='--', linewidth=1, alpha=1)
    ax1.plot(df['指数净值'], label='指数净值', linestyle='--', linewidth=1, alpha=1)

    ax2.plot(df2.week, df2['北向资金'], label='北向资金', marker='o', linewidth=0.8, alpha=0.5, c='blue')
    # d1[['策略净值', '指数净值']].plot(figsize=(15, 7))

    buy = []
    sell = []
    for i in d1.index:
        v = d1['策略净值'][i]
        if d1.signal[i] == 1:
            ax1.scatter(i, v, c='r')
            buy.append(i.strftime('%Y%m%d'))
        if d1.signal[i] == 0:
            ax1.scatter(i, v, c='g')
            sell.append(i.strftime('%Y%m%d'))
    print('买入点:', buy)
    print('卖出点:', sell)

    plt.title(name + '—' + '北向资金择时交易策略回测', size=15)
    plt.xlabel('')

    ax1.spines['top'].set_color('none')
    ax2.spines['top'].set_color('none')
    # 显示图例
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    plt.show()


# 将上述函数整合成一个执行函数
def main(code='000300.SH', start='20190102', end='20210111', window=250, stdev_n=1.5, cost=0.01):
    code_index = get_index_data(code, start, end)
    north_data = get_north_money(start, end)
    result_df = code_index.join(north_data['north_money'], how='inner')
    result_df.rename(columns={'north_money': '北向资金'}, inplace=True)
    result_df = result_df[['close', 'open', '北向资金']].dropna()
    df, df_m = North_Strategy(result_df, window, stdev_n, cost)
    df.to_csv('north_data.csv', encoding='gbk')
    print(df[['北向资金', 'position', 'signal']].tail(20))
    name = list(indexs.keys())[list(indexs.values()).index(code)]
    print(f'回测标的：{name}指数')
    startDate = df.index[0].strftime('%Y%m%d')
    print(f'回测期间：{startDate}—{end}')
    performance(df, name)
    plot_performance(df, df_m, name)


if __name__ == "__main__":
    # 获取指数数据
    # 常用大盘指数
    indexs = {'上证综指': '000001.SH', '深证成指': '399001.SZ', '沪深300': '000300.SH',
              '创业板指': '399006.SZ', '上证50': '000016.SH', '中证500': '000905.SH',
              '中小板指': '399005.SZ', '上证180': '000010.SH'}
    start = '20180104'
    end = '20220125'

    index_data = pd.DataFrame()
    for name, code in indexs.items():
        index_data[name] = get_index_data(code, start, end)['close']

    # 将价格数据转为收益率
    all_ret = 100 * (index_data / index_data.shift(1) - 1)

    north_data = get_north_money(start, end)
    # north_data.to_csv('north_data.csv')
    # north_data=pd.read_csv('north_data',index_col=0,header=0)
    all_data = all_ret.join(north_data['north_money'], how='inner')
    all_data.rename(columns={'north_money': '北向资金'}, inplace=True)
    all_data.dropna(inplace=True)
    final_data = all_data[['沪深300', '北向资金']].dropna()
    print(final_data)
    main(code='000300.SH', start=start, end=end)
