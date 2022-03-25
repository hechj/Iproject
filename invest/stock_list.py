import tushare as ts

from invest.investbase import ts_pro


pro = ts_pro()


def get_code_list(date='20201202'):
    # 默认2010年开始回测
    dd = pro.daily_basic(trade_date=date)
    print(dd)
    x1 = dd.close < 100
    # 流通市值低于300亿大于50亿
    x2 = dd.circ_mv > 500000
    x3 = dd.circ_mv < 3000000
    # 市盈率低于80
    x4 = dd.pe_ttm < 80
    # 股息率大于2%
    x5 = dd.dv_ttm > 3
    x = x1 & x2 & x3 & x4 & x5
    stock_list = dd[x].ts_code.values
    return stock_list


# Clist = get_code_list()
# print(Clist)

data = pro.stock_basic(ts_code='600153.SH', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(data)
