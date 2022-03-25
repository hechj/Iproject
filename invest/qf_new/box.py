import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px

paths = "E:\\MyStudy\\cpitest\\invest\\funds_related"
data_df = pd.read_csv(paths + '/data/110003_lsjz.csv', encoding='gbk', header=0, parse_dates=['FSRQ'])
fig = px.box(data_df, x='LJJZ', orientation='h', title='上证50')
# fig.write_image('./images/px-box.png')
fig.show()
