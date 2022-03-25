# 股权风险溢价对股债相对收益的预测
# 绘制散点图
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from datetime import timedelta, datetime
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro
from pylab import mpl
from sklearn.linear_model import LinearRegression

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
fig = plt.figure(figsize=(15, 8))
gird = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

ax1 = fig.add_subplot(gird[0, 0])

ax2 = ax1.twinx()
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
pd.set_option('display.max_columns', None)
pro = ts_pro()
index_code = '000300.SH'
s_date = "20150504"
e_date = "20220314"
bond_zh_us_rate_df = ak.bond_zh_us_rate()
bond_zh_us_rate_df = bond_zh_us_rate_df[['日期', '中国国债收益率10年']]
bond_zh_us_rate_df.dropna(inplace=True)
bond_zh_us_rate_df.drop_duplicates(inplace=True)
bond_zh_us_rate_df = bond_zh_us_rate_df.reindex(index=bond_zh_us_rate_df.index[::-1])
bond_zh_us_rate_df = bond_zh_us_rate_df.reset_index(drop=True)
bond_zh_us_rate_df['日期'] = pd.to_datetime(bond_zh_us_rate_df["日期"].apply(str)).dt.date
bond_zh_us_rate_df = bond_zh_us_rate_df[bond_zh_us_rate_df['日期'] >= datetime.strptime(s_date, '%Y%m%d').date()]
bond_zh_us_rate_df = bond_zh_us_rate_df.reset_index(drop=True)


def draw_stock(code):
    df_i = pro.index_dailybasic(ts_code=code, start_date=s_date, end_date=e_date,
                                fields='ts_code,trade_date,turnover_rate,pe,pe_ttm,pb')
    df_i = df_i.sort_values(by='trade_date')
    df_i['trade_date'] = pd.to_datetime(df_i["trade_date"].apply(str)).dt.date
    df_i = df_i.reset_index(drop=True)
    EP_df = df_i
    EP_df['EP'] = 1 / df_i['pe_ttm']
    EP_df = EP_df.rename(columns={'trade_date': '日期'})

    risk_premium = pd.merge(EP_df, bond_zh_us_rate_df, how='left')

    risk_premium['premium'] = risk_premium['EP'] * 100 - risk_premium["中国国债收益率10年"]
    print(risk_premium)

    df = pro.index_daily(ts_code=code, start_date=s_date, end_date=e_date,
                         fields='ts_code,trade_date,close,pct_chg')

    df = df.sort_values(by='trade_date')
    df.trade_date = pd.to_datetime(df["trade_date"].apply(str)).dt.date
    df = df.rename(columns={'trade_date': '日期'})
    df['close_back'] = df['close'].shift(-252)

    df['yoy'] = 100 * (df['close_back'] / df['close'] - 1)
    df = pd.merge(df, risk_premium, how='left')
    print(df)
    # 自动旋转日期标记以避免重叠
    plt.title("截止{}".format(datetime.now().strftime('%Y-%m-%d')), fontproperties='SimHei',
              fontsize=18)
    plt.gcf().autofmt_xdate()

    ax1.plot(df['日期'], df.premium, label='风险溢价', c='brown', linestyle='-', linewidth=1)
    ax2.plot(df['日期'], df.yoy, '-', label='未来一年沪深300收益率(RHS-%)', linewidth=1, alpha=0.8, c='Orange')
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})
    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    plt.show()

    fig_line = plt.figure()
    ax = fig_line.add_subplot(111)
    ax.scatter(df.premium, df.yoy)
    df.dropna(axis=0, subset=["yoy"], inplace=True)
    x = df['premium'].tolist()
    y = df['yoy'].tolist()
    x = np.reshape(x, newshape=(len(x), 1))
    y = np.reshape(y, newshape=(len(y), 1))
    # 调用模型
    lr = LinearRegression()
    # 训练模型
    lr.fit(x, y)
    # 计算R平方
    print("准确度", lr.score(x, y))
    # 计算y_hat
    y_hat = lr.predict(x)
    plt.plot(x, y_hat, color="red")
    plt.ylabel("年化收益")
    plt.xlabel("风险溢价")
    plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()
    draw_stock(code=index_code)
    plt.close()
