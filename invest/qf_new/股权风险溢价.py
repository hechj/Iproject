# 股权风险溢价
# 绘制直方图
import time
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from datetime import timedelta, datetime
from pandas.plotting import register_matplotlib_converters
from invest.investbase import ts_pro
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
fig = plt.figure(figsize=(15, 8))
gird = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

ax1 = fig.add_subplot(gird[0, 0])

ax2 = ax1.twinx()
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
pro = ts_pro()

s_date = "20120316"
bond_zh_us_rate_df = ak.bond_zh_us_rate()
bond_zh_us_rate_df = bond_zh_us_rate_df[['日期', '中国国债收益率10年']]
bond_zh_us_rate_df.dropna(inplace=True)
bond_zh_us_rate_df.drop_duplicates(inplace=True)
bond_zh_us_rate_df = bond_zh_us_rate_df.reindex(index=bond_zh_us_rate_df.index[::-1])
bond_zh_us_rate_df = bond_zh_us_rate_df.reset_index(drop=True)
bond_zh_us_rate_df['日期'] = pd.to_datetime(bond_zh_us_rate_df["日期"].apply(str)).dt.date
bond_zh_us_rate_df = bond_zh_us_rate_df[bond_zh_us_rate_df['日期'] >= datetime.strptime(s_date, '%Y%m%d').date()]
bond_zh_us_rate_df = bond_zh_us_rate_df.reset_index(drop=True)
'''    
    paths = "E:\\MyStudy\\datas\\"

    data = pd.read_csv(paths + '中国十年期国债收益率历史数据.csv', encoding='utf-8', header=0)

    # 数据切片，数据倒序排列
    data = data.reindex(index=data.index[::-1])

    # 将*年*月*日数据转化成pandas日期格式
    data['日期'] = data['日期'].map(lambda x: time.strptime(x, u"%Y年%m月%d日"))
    data['日期'] = data['日期'].map(lambda x: time.strftime('%Y-%m-%d', x))
    data.index = pd.to_datetime(data["日期"])
    data = data[['日期', '收盘']]
    data = data[s_date::]
    data = data.reset_index(drop=True)
'''


def draw_stock(code):
    df_i = pro.index_dailybasic(ts_code=code, start_date=s_date,
                                fields='ts_code,trade_date,turnover_rate,pe,pe_ttm,pb')
    df_i = df_i.sort_values(by='trade_date')
    df_i['trade_date'] = pd.to_datetime(df_i["trade_date"].apply(str)).dt.date
    df_i = df_i.reset_index(drop=True)
    EP_df = df_i
    EP_df['EP'] = 1 / df_i['pe_ttm']
    EP_df = EP_df.rename(columns={'trade_date': '日期'})
    print(EP_df)
    print(bond_zh_us_rate_df)

    risk_premium = pd.merge(EP_df, bond_zh_us_rate_df, how='left')

    risk_premium['premium'] = risk_premium['EP'] * 100 / risk_premium["中国国债收益率10年"]
    print(risk_premium)
    # 自动旋转日期标记以避免重叠
    plt.title("截止{}".format(datetime.now().strftime('%Y-%m-%d')), fontproperties='SimHei',
              fontsize=18)
    plt.gcf().autofmt_xdate()
    ax2.plot(risk_premium['日期'], risk_premium.premium, label=code + '风险溢价', linestyle='-', c='b', linewidth=1)
    ax2.axhline(y=risk_premium['premium'].mean(), ls='-', c='black')
    ax2.axhline(y=risk_premium['premium'].mean() + risk_premium['premium'].std(), ls='--', c='gray')
    ax2.axhline(y=risk_premium['premium'].mean() - risk_premium['premium'].std(), ls='--', c='gray')
    ax1.plot(risk_premium['日期'], risk_premium.pe_ttm, label='pe_ttm', c='orange', linestyle='-', linewidth=1)

    ax2.legend(loc=1, prop={'family': 'SimHei', 'size': 12})
    ax1.legend(loc=2, prop={'family': 'SimHei', 'size': 12})

    bins = 50
    hist = np.histogram(risk_premium.premium, bins=bins)
    ax_b = fig.add_subplot(gird[0, 1])
    ax_b.barh(y=hist[1][0:bins], width=hist[0] * 2, height=2 / bins)
    ax_b.set_title("风险溢价直方图")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()
    draw_stock(code='000905.SH')
    plt.close()
