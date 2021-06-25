import pandas as pd
import plotly
import plotly.express as px
import tushare as ts

ts.set_token('f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8')

s_date = '20150105'
df = ts.pro_bar(ts_code='601318.SH',  adj='qfq', start_date=s_date,
                asset='E', freq='D')
print(df)
df['trade_date'] = pd.to_datetime(df['trade_date'])
df = df.set_index('trade_date')
area_chart = px.area(df['close'], title='中国平安')

area_chart.update_xaxes(title_text='日期')
area_chart.update_yaxes(
    title_text='中国平安收盘价'
)
area_chart.update_layout(showlegend=False)

plotly.offline.plot(area_chart, filename='../out/area_update.html')

