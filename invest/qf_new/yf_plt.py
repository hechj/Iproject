import pandas as pd
import plotly
import plotly.graph_objs as go
import yfinance as yf
import os
from datetime import datetime
from invest.investbase import ts_pro

pro = ts_pro()
s_date = '20050408'  # 2005年4月8日发布沪深300指数
df_300 = pro.index_daily(ts_code='000300.SH', start_date=s_date,
                         fields='ts_code,trade_date,close')
df_300 = df_300.sort_values(by='trade_date')
df_300.index = pd.to_datetime(df_300["trade_date"])
print(df_300)


pyplt = plotly.offline.plot
date_end = datetime.today().strftime('%Y-%m-%d')
# yfinance 雅虎里的标普500是^GSPC，其它地方是SPX
# 数据来源为雅虎财经


data = yf.download('^GSPC', start='1974-01-01', end=date_end)
data = data.sort_values(by='Date')
# data.to_csv("../out/spx.csv")
print(data)

trace0 = go.Scatter(x=data.index, y=data['Close'], mode="text+lines",
                    marker=dict(color='#d66101'))
trace1 = go.Scatter(x=df_300.index, y=df_300['close'], mode="text+lines",
                    marker=dict(color='red'))
fig_spx = go.Figure(data=[trace0, trace1])
fig_spx.update_layout(template='ggplot2')
fig_spx.update_layout(showlegend=True, title=dict(text='SPX', font=dict(size=24, color='#d66101'), x=0.5))

pyplt(fig_spx, filename='../out/spx_hs300.html')

