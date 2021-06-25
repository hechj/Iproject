'''
伦敦铜历史数据
https://cn.investing.com/commodities/copper-historical-data
中国十年期国债收益率数据
https://cn.investing.com/rates-bonds/china-10-year-bond-yield-historical-data
美国
https://cn.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data
需将chromedriver.exe拷贝到chrome安装目录及python.exe目录，否则selenium会找不到浏览器

'''

#!E:/MyStudy/cpitest/venv/Scripts/python.exe
#!venv/Scripts/python.exe
from selenium import webdriver
from time import sleep
import re
import pandas as pd
from bs4 import BeautifulSoup as bs

option = webdriver.ChromeOptions()
# 默认登录状态
option.add_argument(r'user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')
browser = webdriver.Chrome("chromedriver", 0, option)

urls = ['https://cn.investing.com/commodities/copper-historical-data',
        'https://cn.investing.com/rates-bonds/china-10-year-bond-yield-historical-data']
for url in urls:
    browser.get(url)
    browser.maximize_window()
    sleep(3)
    browser.find_element_by_xpath('//*[@id="widget"]').click()
    sleep(3)
    browser.find_element_by_xpath('//*[@id="startDate"]').clear()
    browser.find_element_by_xpath('//*[@id="startDate"]').send_keys('2002/06/06')
    # browser.find_element_by_id("datepicker").send_keys('2020/01/01')
    sleep(2)
    # browser.find_element_by_xpath('//*[@id="endDate"]').clear()
    # browser.find_element_by_xpath('//*[@id="endDate"]').send_keys('2020/11/19')
    sleep(2)
    browser.find_element_by_xpath('//*[@id="applyBtn"]').click()
    sleep(7)
    # js跳转
    js = 'document.getElementsByClassName("newBtn LightGray downloadBlueIcon js-download-data")[0].click();'
    browser.execute_script(js)

    print('当前地址:', browser.current_url)
    sleep(6)

# print(browser.page_source)
'''
a = browser.page_source
soup = bs(a, "lxml")
content = soup.find('div', id="results_box").find_all('tbody')[0].find_all('tr')


resultdf = pd.DataFrame(columns=('date', 'close', 'open', 'high', 'low'))
for tr in content:
    td = tr.find_all('td')
    date = re.findall(r'<td[^>]*>(.*?)</td>', str(td[0]), re.I | re.M)[0]
    resultdf = resultdf.append(pd.DataFrame({'date': [date],
                                             'close': [float(td[1].get("data-real-value"))],
                                             'open': [float(td[2].get("data-real-value"))],
                                             'high': [float(td[3].get("data-real-value"))],
                                             'low': [float(td[4].get("data-real-value"))]}), ignore_index=True)

print(resultdf)
'''

browser.quit()
