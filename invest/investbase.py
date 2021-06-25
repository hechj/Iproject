import tushare as ts

# python 量化
ts.set_token('f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8')

index_code = {
    '上证综指': '000001.SH', '深证成指': '399001.SZ',
    '沪深300': '000300.SH', '创业板指': '399006.SZ',
    '上证50': '000016.SH', '中证500': '000905.SH',
    '中小板指': '399005.SZ', '上证180': '000010.SH'
}


def ts_pro():
    pro = ts.pro_api()
    return pro


df = ts_pro().stock_basic(exchange='', list_status='L')
codes = df.ts_code.values
names = df.name.values
stock = dict(zip(names, codes))
# 双星号 ** 将其转化成字典
stocks = dict(stock, **index_code)
inverse_stock = dict(zip(codes, names))
inverse_index_code = dict(zip(index_code.values(), index_code.keys()))
# 双星号 ** 将其转化成字典
inverse_stocks = dict(inverse_stock, **inverse_index_code)


# 获取个股名称对应的代码
def get_t_code(name):
    return stocks[name]


# 获取个股代码对应的名称
def get_t_name(code):
    return inverse_stocks[code]

