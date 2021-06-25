import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 登陆系统
lg = bs.login()

# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond error_msg:' + lg.error_msg)

# 获取货币供应量
rs = bs.query_money_supply_data_month(start_date="2019-06", end_date="2020-12")
print('query_money_supply_data_month respond error_code:' + rs.error_code)
print('query_money_supply_data_month respond  error_msg:' + rs.error_msg)

# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())

result = pd.DataFrame(data_list, columns=rs.fields)
result['date'] = pd.to_datetime(result['statYear'].astype(str) + result['statMonth'].astype(str), format='%Y%m')
# print(type(result.loc[0, 'date']))
result_copy = result.copy()

result_copy['m1YOY'] = pd.to_numeric(result_copy['m1YOY'], errors='coerce')
result_copy['m2YOY'] = pd.to_numeric(result_copy['m2YOY'], errors='coerce')

result_copy['m1subm2'] = result_copy.apply(lambda x: x['m1YOY'] - x['m2YOY'], axis=1)
print(result_copy)

# 结果集输出到csv文件
''' 
try:
    result_copy.to_csv("money_supply_data_month.csv", encoding="gbk", index=False)
except:
    pass
'''
# 登出系统
bs.logout()

plt.rcParams['font.family'] = ['sans-serif']

# 正常显示画图中的中文和负号
plt.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False


def draw_m1m2(data):
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)

    date = data['date']
    print(date)
    print('类型',type(date))

    plt.plot(date, data['m1YOY'], label='M1增长率(%)', linestyle='-', linewidth=2)
    plt.plot(date, data['m2YOY'], label='M2增长率(%)', linestyle='-', linewidth=2)
    plt.plot(date, data['m1subm2'], label='M1-M2变化率(%)', linestyle='-', linewidth=1)

    plt.ylabel('增长率(%)', fontproperties='SimHei', fontsize=15)
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    # ax.xaxis.set_major_locator(mdates.MonthLocator())
    #数据完全填满X轴
    ax.margins(x=0)
    # ax.set_xticks
    # fig.autofmt_xdate()
    # ax.axes.set_xticklabels(date, rotation=270)

    plt.xticks(rotation=90)  # 旋转90度
    # 设置图片边缘距离
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)
    plt.grid(b='major', color='k', linestyle='--', linewidth=1, alpha=0.3)
    plt.legend(prop={'family': 'SimHei', 'size': 12})
    plt.title("M1-M2走势", fontproperties='SimHei', fontsize=18)
    plt.savefig('png\m1m2.png')
    plt.show(block=True)
    plt.close()


draw_m1m2(result_copy)
