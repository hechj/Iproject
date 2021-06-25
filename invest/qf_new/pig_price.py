import pandas as pd
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.114 Safari/537.36'}


# 生成出生当年所有日期
def dateRange(a, b):
    fmt = '%Y-%m-%d'
    bgn = int(time.mktime(time.strptime(a, fmt)))
    end = int(time.mktime(time.strptime(b, fmt)))
    list_date = [time.strftime(fmt, time.localtime(i)) for i in range(bgn, end + 1, 3600 * 24)]
    return list_date


def get_json(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_text = response.json()
            return json_text
    except Exception as e:
        print(e)
        print('此页有问题！')
        return None


def get_comments(url):
    doc = get_json(url)
    print(doc)
    dic = {}

    dic['pigprice'] = doc['pigprice']

    a = '-'.join(doc['time'][3])
    b = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(dateRange(a, b))
    dic['time'] = dateRange(a, b)
    return pd.DataFrame(dic)


data = get_comments('https://zhujia.zhuwang.cc/api/chartData?areaId=-1&aa=1624518801003')

# 作图
from pylab import mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(8, 10), dpi=80)
plt.figure(1)
ax1 = plt.subplot(111)
plt.plot(data['time'], data['pigprice'], color="r", linestyle="-")
plt.xticks([])
plt.annotate(data['pigprice'][365], xy=(data['time'][365], 40), xytext=(data['time'][270], 35),
             arrowprops=dict(facecolor='black', shrink=0.1, width=0.5))
plt.xlabel("生猪(外三元) 元/公斤")
plt.show()
plt.close()
