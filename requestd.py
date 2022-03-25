# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 09:19:33 2019
@author: Lenovo
"""

import requests
import time
import json
import matplotlib.pyplot as plt


# 用来获得 时间戳
def gettime():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    #    "一，请求数据"
    # 用来定义头部
    headers = {}
    # 用来传递参数
    keyvalue = {}
    # 目标网址
    url = 'http://data.stats.gov.cn/easyquery.htm'

    # 头部填充
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                            'Chrome/70.0.3538.102 Safari/537.36'

    # 参数填充
    keyvalue['m'] = 'QueryData'
    keyvalue['dbcode'] = 'hgnd'
    keyvalue['rowcode'] = 'zb'
    keyvalue['colcode'] = 'sj'
    keyvalue['wds'] = '[]'
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
    keyvalue['k1'] = str(gettime())

    print("--------")
    print("k1=", keyvalue['k1'])
    print("--------")
    # 发出请求，使用get方法，这里使用我们自定义的头部和参数
    r = requests.get(url, headers=headers, params=keyvalue)
    print(r.text)
    #    "二，解析数据"
    year = []
    population = []
    data = json.loads(r.text)
    data_one = data['returndata']['datanodes']
    print(data_one)

    for value in data_one:
        if 'A030101_sj' in value['code']:
            year.append(value['code'][-4:])
            population.append(int(value['data']['strdata']))

    print(year)
    print(population)

    #    "三，绘制数据"
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.bar(year, population)
    plt.xlabel(u'年份')
    plt.ylabel(u'万人')
    plt.title(u'年末总人口')
    plt.show()
