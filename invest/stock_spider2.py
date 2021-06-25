import re
import requests
from lxml import etree
import random
from bs4 import BeautifulSoup as bs
import time
import redis


class StockCode(object):
    def __init__(self):
        # self.start_url = "http://quote.eastmoney.com/stocklist.html#sh"  # 此网址应该不能直接爬到股票代码列表了
        self.start_url = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?&type=CT&token' \
          r'=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&cmd=C._A&st=(ChangePercent)&sr=-1&p=1&ps=3932 '
        self.headers = {
            "User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

    def run(self):
        html = requests.get(self.start_url)
        html = html.text

        stock = re.findall(re.compile('\((.*)\)'), html)
        stock = stock[0]
        stock = stock.split('","')

        stock[0] = stock[0][2:]
        stock[-1] = stock[-1][:-2]
        stock_data = []
        for i, item in enumerate(stock):
            t = item.split(',')
            stock_data.append(t[1])
        stock_data.sort()
        print(stock_data)
        return stock_data


class Download_HistoryStock(object):
    def __init__(self, code):
        self.code = code
        self.start_url = "http://quotes.money.163.com/trade/lsjysj_" + self.code + ".html"
        print(self.start_url)
        self.headers = {
            "User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

    def parse_url(self):

        response = requests.get(self.start_url)
        print(response.status_code)
        if response.status_code == 200:
            return etree.HTML(response.content)
        return False

    def get_date(self, response):
        # 得到开始和结束的日期
        start_date = ''.join(response.xpath('//input[@name="date_start_type"]/@value')[0].split('-'))
        end_date = ''.join(response.xpath('//input[@name="date_end_type"]/@value')[0].split('-'))
        return start_date, end_date

    def download(self, start_date, end_date):

        # 由于东方财富网上获取的代码一部分为基金，无法获取数据，故将基金剔除掉。
        # 沪市股票以6,9开头，深市以0,2,3开头，但是部分基金也是2开头，201/202/203/204这些也是基金
        # 另外获取data的网址股票代码 沪市前加0， 深市前加1
        # stock_code_new 为 0000832时可下载中证转债指数数据，电脑里已下载保存为000832.csv

        stock_code = self.code
        stock_code_new = ''
        if int(stock_code[0]) in [0, 2, 3, 6, 9]:
            if int(stock_code[0]) in [6, 9]:
                stock_code_new = '0' + stock_code
            elif int(stock_code[0]) in [0, 2, 3]:
                if not int(stock_code[:3]) in [201, 202, 203, 204]:
                    stock_code_new = '1' + stock_code

        if stock_code_new == '':
            print('不合法的股票代码',self.code)
            return
        download_url = "http://quotes.money.163.com/service/chddata.html?code=" + stock_code_new \
                       + "&start=" + "20200103" + "&end=" + end_date + \
                       "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        data = requests.get(download_url)
        f = open('stock_data2/{}.csv'.format(self.code), 'wb')
        for chunk in data.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print('股票---', self.code, '历史数据正在下载')

    def run(self):
        try:
            html = self.parse_url()
            start_date, end_date = self.get_date(html)
            print("日期")
            print(start_date)
            print(end_date)
            self.download(start_date, end_date)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    code = StockCode()
    code_list = code.run()

    for temp_code in code_list:
        time.sleep(1)
        download = Download_HistoryStock(temp_code)
        download.run()
        time.sleep(random.choice([1, 2]))  # 两次访问之间休息1-2秒
