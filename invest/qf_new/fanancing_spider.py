'''
爬取关于融资余额占流通市值比的数据爬取

'''
import random
import time

import pandas as pd
# 请求库
import requests
# 解析库
from bs4 import BeautifulSoup
# 用于解决爬取的数据格式化
import io
import sys


def stock_star(page=10):
    url = 'http://quote.stockstar.com/Financing/FinancingTotal_1_1_{}_0_1.html'.format(page)
    print(url)

    # 爬取的网页链接
    r = requests.get(url)

    print(r.status_code)
    if r.status_code != 200:
        print('访问%s异常', url)
        return
    # 中文显示
    # r.encoding='utf-8'
    r.encoding = None
    print(r.encoding)
    result = r.text
    # 再次封装，获取具体标签内的内容
    # bs = BeautifulSoup(result, 'html.parser')
    bs = BeautifulSoup(result, 'lxml')

    # 具体标签
    all = bs.find_all('tbody', class_='tbody_right', id='datalist')
    if all is not None:
        print("解析后的数据:")
        print(all)
        tr_parse(all)


def tr_parse(trs):
    global count
    tr_s = trs[0].find_all('tr')
    for tr in tr_s:
        cells = tr.find_all('td')
        c_len = len(cells)
        if c_len < 3:
            break
        p_list = []
        for cell in cells:
            p_list.append(cell.get_text())
        df.loc[count] = p_list[:3]
        count += 1


if __name__ == '__main__':
    count = 0
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    df = pd.DataFrame(columns=('date', 'value', 'rate'))
    for i in range(1, 25 + 1):
        stock_star(page=i)
        time.sleep(random.randint(2, 3))
    df.to_csv("financing.csv", encoding='gbk')
    print(df)
