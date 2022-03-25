import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
# 设置value的显示值，默认为50
pd.set_option('max_colwidth', 200)
pd.set_option('expand_frame_repr', False)  # 数据超过总宽度后，是否折叠显示


def plan(name, price, rate, money, data):
    df_p = pd.DataFrame(data=data)
    df_p['加仓批次'] = list(range(1, len(df_p) + 1))
    df_p['标的名称'] = name
    df_p['价格'] = df_p['价格系数'] * price
    df_p['买入份额'] = ''
    df_p['买入金额'] = ''

    df_p.loc[df_p['加仓批次'] == 1, '买入金额'] = money
    df_p.loc[df_p['加仓批次'] == 1, '买入份额'] = money / price
    for i in range(len(df_p) - 1):
        n = i + 2
        df_p.loc[df_p['加仓批次'] == n, '买入金额'] = money * df_p.loc[df_p['加仓批次'] == n, '加仓比例'] / rate

        df_p.loc[df_p['加仓批次'] == n, '买入份额'] = df_p.loc[df_p['加仓批次'] == n, '买入金额'] / df_p.loc[df_p['加仓批次'] == n, '价格']

    df_p['累计仓位'] = df_p['加仓比例'].cumsum()
    df_p['累计份额'] = df_p['买入份额'].cumsum()
    df_p['累计金额'] = df_p['买入金额'].cumsum()
    df_p['成本'] = df_p['累计金额'] / df_p['累计份额']
    df_p['收益率'] = df_p['价格'] / df_p['成本'] - 1
    df_p['收益率'] = df_p['收益率'].apply(lambda x: f'{round(x * 100, 2)}%')
    df_p['下跌幅度'] = 1 - df_p['价格系数']
    df_p['下跌幅度'] = df_p['下跌幅度'].apply(lambda x: f'下跌{int(round(x * 100, 0))}%')
    df_p.loc[df_p['加仓批次'] == 1, '下跌幅度'] = '首次'
    df_p = df_p[['标的名称', '加仓批次', '下跌幅度', '价格系数', '价格', '加仓比例', '累计仓位',
                 '买入份额', '累计份额', '买入金额', '累计金额', '成本', '收益率']]
    return df_p


# 标的名称
target_name = '中概互联'

# 首次购入价格
price_init = 1.47

# 首次加仓比例
rate_init = 0.1

# 首次购入金额
money_init = 10000

data_init = {
    '价格系数': [1, 0.95, 0.9, 0.85, 0.8, 0.7],
    '加仓比例': [rate_init, 0.1, 0.1, 0.2, 0.2, 0.3],
}
df = plan(target_name, price_init, rate_init, money_init, data_init)

format_dict = {
                4: '{:.3f}',
                5: '{:.2%}',
                6: '{:.2%}',
                7: '{:.2f}',
                8: '{:.3f}',
                9: '￥{:.3f}',
                10: '￥{:.3f}',
                11: '{:.3f}'
               }
df.style.format(format_dict)
df.style.hide_index()
df.to_html('../out/建仓.html')
