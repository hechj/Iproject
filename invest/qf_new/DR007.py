from invest.investbase import ts_pro
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak

s_date = '20190504'

gksccz_df = ak.macro_china_gksccz()
gksccz_df = gksccz_df.drop_duplicates()
gksccz_df['正/逆回购'] = gksccz_df['正/逆回购'].astype(str)
print(gksccz_df.info())
gksccz_df = gksccz_df[(gksccz_df['期限'] == 7) & (gksccz_df['正/逆回购'] == '逆回购')]
gksccz_df = gksccz_df.sort_values(by='操作日期')
gksccz_df.index = pd.to_datetime(gksccz_df["操作日期"])
gksccz_df = gksccz_df[s_date::]

print(gksccz_df)

pro = ts_pro()

df = pro.shibor(start_date=s_date)
df = df.sort_values(by='date')
df.index = pd.to_datetime(df["date"])
print(df)
plt.plot(df.index, df['1w'], '-', label='DR007', linewidth=1)
plt.plot(gksccz_df.index, gksccz_df["中标利率"], '-', label='Reverse repo rate', linewidth=1)
plt.legend()
plt.show()
plt.close()
