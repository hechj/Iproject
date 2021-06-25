'''
参考https://blog.csdn.net/weixin_42029733/article/details/107591617

东方财富网爬取股票信息数据
'''

from selenium import webdriver
from time import sleep
import random

'''爬取上证指数的所有股票信息，保存到本地文件/数据库'''


class Break(Exception):
    pass


def extractor(xpath_text):
    '''根据xpath获取内容'''
    try:
        TCases = driver.find_element_by_xpath(xpath_text)
    except Exception as r:
        print('extractor错误 %s' % r)
        return None
    return TCases.text


def export_to_file(stock_dict):
    '''导出股票数据'''
    with open('沪指股票数据.csv', 'a', encoding='gbk') as file:
        file.write(','.join(stock_dict.values()))
        file.write('\n')


url = 'http://quote.eastmoney.com/center/gridlist.html#sh_a_board'
driver = webdriver.Chrome("chromedriver")
driver.get(url)
sleep(5)

ele_list = ['代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '最高价', '最低价', '今开',
            '昨收', '量比', '换手率', '市盈率', '市净率']
f = open('沪指股票数据.csv', "w+", encoding='gbk')
f.write(','.join(ele_list))
f.write("\n")
f.close()

try:
    for page_num in range(1, 100):
        for i in range(1, 10 + 1):
            for ele_type in ['odd', 'even']:
                stock_dict = {}
                number_list = ['2', '3', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']

                for j, name in zip(number_list, ele_list):

                    temp_xpath = "//*[@id='table_wrapper-table']/tbody/tr[@class='{}'][{}]/td[{}]".format(ele_type, i, j)

                    stock_dict[name] = extractor(temp_xpath)
                    # print(stock_dict[name])
                    if stock_dict[name] is None:
                        print("取得空值,退出!")
                        raise Break('break')
                print(list(stock_dict.values()))
                export_to_file(stock_dict)
        # 到下一页继续爬
        try:
            driver.find_element_by_xpath('//*[@class="next paginate_button"]').click()
        except Exception as r:
            print('错误 %s' % r)
            break

        sleep(random.choice([1, 2]))  # 两次访问之间休息1-2秒

        # driver.find_element_by_xpath( "/html/body/div[@class='page-wrapper']/div[@id='page-body']/div[
        # @id='body-main']/div[@id='table_wrapper']/div[@class='listview full']/div[@class='dataTables_wrapper']/div[
        # @id='main-table_paginate']/a[@class='next paginate_button']").click()
except Break as e:
    driver.close()
    print(e)

driver.close()
