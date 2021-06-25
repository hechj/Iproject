
import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  #绘图库导入
import matplotlib.dates as mdates

#在tushare官网注册后，进入个人中心得到你的唯一指定token，替换***
ts.set_token('e0eeb08befd1f07516df2cbf9cbd58663f77fd72f92a04f290291c9d')
#初始化api
api = ts.pro_api()


startdate = '20180101'
#获取CPI并生成相应图表
CPI = ts.get_cpi()  #获取cpi数据
CPI['cpi'] = CPI['cpi']-100.0   #转化为百分比
CPI['month'] = pd.to_datetime(CPI['month'])  # 将Str和Unicode转化为时间格式，2019.7转化为2019-07-01
CPI = CPI[CPI['month'] >= pd.to_datetime(startdate)]    #选取的该时间点后的所有CPI数据
#先筛选数据再排序
CPI = CPI.sort_values('month')   #根据时间顺序排，默认按照升序排列
#print(CPI)

#获取PPI并生成相应图表
PPI = ts.get_ppi() #获取PPI数据
print(PPI)

PPI['ppiip'] = PPI['ppiip']-100
PPI['month'] = pd.to_datetime(PPI['month'])
PPI = PPI[PPI['month'] >= pd.to_datetime(startdate)]
PPI = PPI.sort_values('month')
print(PPI)
#货币供应量

MNS= ts.get_money_supply()


MNS['month'] = pd.to_datetime(MNS['month'])
MNS = MNS[MNS['month'] >= pd.to_datetime(startdate)]
MNS = MNS.sort_values('month')

MNS['col2'] = MNS['m2_yoy']
dcol = pd.DataFrame(MNS, columns=['col2','m2_yoy'])
dcol[["col2", "m2_yoy"]] = dcol[["col2", "m2_yoy"]].apply(pd.to_numeric,errors='ignore')


#plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] #设置默认字体，解决标签显示乱码的问题
plt.rcParams['font.sans-serif'] = ['SimHei']

plt.rcParams['axes.unicode_minus'] = False    #用来正常显示负号
#创建一个图形实例
plt.figure(figsize=(12,6),facecolor='none') #设置画布大小,长、宽,facecolor显示的是画布的背景，非图形的背景
#开始画图

new_ticks = CPI['month']
print('类型',type(new_ticks))
#plt.xticks(new_ticks)
plt.plot(new_ticks,CPI['cpi'],color = 'red',  label='居民消费价格指数 - CPI')  #注意color的位置
new_ticks = PPI['month']
#plt.xticks(new_ticks)
plt.plot(new_ticks,PPI['ppiip'],color = 'blue',  label = '工业品出厂价格指数 - PPI')
new_ticks = MNS['month']
#plt.xticks(new_ticks)
plt.plot(new_ticks,dcol['col2'],color = 'green',  label = '(广义货币M2)同比增长(%)')
plt.axis('tight')            #设置坐标轴：紧凑型，使得坐标轴适应数据量
plt.xlabel('年度',color='red', size = 12)     # x轴的名称，注意color的位置
plt.ylabel('同比',color='red',size = 12)    # y轴的名称
plt.title('PPI\CPI\M2走势同比对比分析', size = 12) # 图形标题
plt.legend(loc = 0)  #用来标示不同图形的文本标签图例，不添加的话label标签CPI显示不出来，0表示图例位置自动
# 将右边 上边的两条边颜色设置为空 其实就相当于抹掉这两条边
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

#设置时间按“年月”的格式显示
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))
#X轴按年进行标记，还可以用MonthLocator()和DayLocator()
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
#自动旋转日期标记以避免重叠
plt.gcf().autofmt_xdate()


#设置网格线颜色为黑色,线型为虚线,alpha表示网格的清晰度;用'major'|'minor'|'both' to set the grid
plt.grid(b='major',color = 'k',linestyle='--',linewidth=3,alpha=0.3)

plt.savefig('cpi.png')
plt.show()    #显示图形，show要放在savefig的后面，不然savefig的图形为空