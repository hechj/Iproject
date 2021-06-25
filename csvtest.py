import tushare as ts
import os
import pandas as pd

filename = 'D:/workspace/PycharmProjects/cpitest/csvfile/file.csv'
if os.path.exists(filename):
    os.remove(filename)

for code in ['000997']:
    df = ts.get_hist_data(code)
    if os.path.exists(filename):
        df.to_csv(filename, mode='a')
    else:
        df.to_csv(filename)

fund_code = pd.read_csv(filepath_or_buffer=filename, encoding='gbk')
Code = fund_code.date
print(fund_code.loc[0])
record = tuple(fund_code.loc[0])
print(type(record))
sqlSentence4 = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % record
print(type(sqlSentence4))
print(sqlSentence4)
print(len(fund_code))


def getFundCodesFromCsv():
    '''
    从csv文件中获取基金代码清单（可从wind或者其他财经网站导出）
    '''

    file_path = os.path.join(os.getcwd(), 'fundtest.csv')
    print(file_path)
    fund_code = pd.read_csv(filepath_or_buffer=file_path, encoding='gbk')
    print(fund_code.trade_code[0])
    print(type(fund_code.trade_code[0]))


getFundCodesFromCsv()
