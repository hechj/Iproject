import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px

import yfinance as yf
import os
from datetime import datetime
from invest.investbase import ts_pro

s_date = '20050408'  # 2005年4月8日发布沪深300指数

pyplt = plotly.offline.plot
date_end = datetime.today().strftime('%Y-%m-%d')
# yfinance 雅虎里的标普500是^GSPC，其它地方是SPX
# 数据来源为雅虎财经

'''
道琼斯指数 ^DJI
标普500指数 ^GSPC
'''
y_code = '^GSPC'

# data = yf.download(y_code, start='2014-09-15', end=date_end)
# data = data.sort_values(by='Date')
# data.to_csv("../out/spx.csv")

pro = ts_pro()
df_300 = pro.index_daily(ts_code='000300.SH', start_date=s_date,
                         fields='ts_code,trade_date,close')
df_300 = df_300.sort_values(by='trade_date')
df_300.index = pd.to_datetime(df_300["trade_date"])

df_cyb = pro.index_daily(ts_code='399006.SZ', start_date=s_date,
                         fields='ts_code,trade_date,close')
df_cyb = df_cyb.sort_values(by='trade_date')
df_cyb.index = pd.to_datetime(df_cyb["trade_date"])

print(df_300)

# trace0 = go.Scatter(x=data.index, y=data['Close'], mode="text+lines",
#                     marker=dict(color='#d66101'))
hs300 = go.Scatter(x=df_300.index, y=df_300['close'], mode="text+lines",
                   name='沪深300', marker=dict(color='red'))
cyb = go.Scatter(x=df_cyb.index, y=df_cyb['close'], mode="text+lines",
                 name='创业板', marker=dict(color='blue'),
                 xaxis='x',
                 yaxis='y2'  # 标明设置一个不同于trace1的一个坐标轴
                 )
fig_spx = go.Figure(data=[hs300, cyb])
fig_spx.update_layout(template='ggplot2')
fig_spx.update_layout(showlegend=True, title=dict(text="沪深300及创业板走势", font=dict(size=24, color='#d66101'), x=0.5))
fig_spx.update_layout({"xaxis": {"title": {"text": '时间'}, "tickformat": ''},
                       "yaxis": {"title": {"text": "沪深300点位"}},
                       "yaxis2": {"title": {"text": "创业板点位"}, 'anchor': 'x', "overlaying": 'y', "side": 'right'},
                       # 设置坐标轴的格式，一般次坐标轴在右侧
                       "legend": {"title": {"text": ""}, "x": 0.9, "y": 1.1},
                       "width": 1000,
                       "height": 1000 * 0.5625
                       })

pyplt(fig_spx, filename='../out/' + "主要指数" + '.html')
