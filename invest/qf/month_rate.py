# 研究每月收益率情况

import pandas as pd
from pandas.plotting import register_matplotlib_converters
from math import e
from pyecharts import Bar
from invest.investbase import ts_pro

pro = ts_pro()


def draw():
    index_code = '399606.SZ'
    df = pro.index_monthly(ts_code=index_code, start_date='20100102',
                           fields='ts_code,trade_date,open,close,pct_chg,amount')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df["trade_date"])

    # 取前6个字符
    df['trade_date'] = df['trade_date'].str[:6]
    df['pct_chg'] = df['pct_chg'] * 100
    bar = Bar('月收益率', '(%)', width=1200, height=800)

    print(type(df.index))
    bar.add('创业板', x_axis=df.trade_date, y_axis=df.pct_chg, is_label_show=False, label_color=['lightskyblue'], xaxis_rotate=90,
            label_pos='top')
    bar.render('bar3.html')


if __name__ == '__main__':
    register_matplotlib_converters()

    draw()
