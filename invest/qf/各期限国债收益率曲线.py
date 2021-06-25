'''
画国债收益率曲线
数据来源：http://yield.chinabond.com.cn/cbweb-czb-web/czb/showHistory?locale=cn_ZH
暂只能一次获取一年间数据
'''
import time
from datetime import timedelta
import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
paths = "E:\\MyStudy\\datas\\中国国债收益率曲线历史数据.xlsx"
df = pd.read_excel(paths, '中国国债收益率曲线')
# 数据切片，数据倒序排列
df = df.reindex(index=df.index[::-1])
df.index = pd.to_datetime(df["日期"])


def date_to_num(d):
    d_num = (d - pd.to_datetime("1970-01-01")).days
    return d_num


if __name__ == '__main__':
    register_matplotlib_converters()

    df['长短差'] = df['10年'] - df['3月']
    # list的日期不用在y轴画了
    # for li in list(df)[1::]:
    for li in ['3月', '1年', '10年', '长短差']:
        plt.plot(df.index, df[li], label=li, linestyle='-', linewidth=1, alpha=1)

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.title("国债收益率曲线", fontproperties='SimHei', fontsize=18)
    ax.set_ylabel(r"收益率(%)", fontproperties='SimHei', fontsize=15)
    plt.grid(b='major', color='orange', linestyle='--', linewidth=1, alpha=0.15)
    # 显示图片
    print(df.index[0])
    print(df.index[100])
    print(plt.gca().get_xlim())
    print(plt.gca().get_ylim())
    zero_day = pd.to_datetime(0, unit='D').date()
    print(zero_day)
    print(df)
    # 这样转的时间戳是unix，与EXCEL表格里的时间不一致。EXCEL表格的时间转为数值是整数部分是日为单位，小数部分是时间。
    print(time.mktime(pd.to_datetime("2018-12-05 00:00:00").timetuple()))

    # 这样画矩形框
    plt.gca().add_patch(
        plt.Rectangle((date_to_num(pd.to_datetime("2020-01-01")), 0.3), 365,
                      2, fill=False, edgecolor='black', linewidth=2, linestyle='--', clip_on=False))
    plt.show()
    plt.close()
