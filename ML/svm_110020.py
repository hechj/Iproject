import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import tushare as ts


def pltdayline():
    paths = "E:\\MyStudy\\cpitest\\invest\\funds_related"
    data_df = pd.read_csv(paths + '/data/110020_lsjz.csv', encoding='gbk', header=0)
    data_df.sort_values(by='FSRQ', ascending=True, inplace=True)
    data_df.fillna(0, inplace=True)
    data_df = data_df[['FSRQ', 'DWJZ']]
    x = np.arange(0, len(data_df), 1)
    xt = pd.to_datetime(data_df['FSRQ'])
    y = data_df['DWJZ'].tolist()

    x = np.reshape(x, newshape=(len(x), 1))
    y = np.reshape(y, newshape=(len(y), 1))
    # 调用模型
    lr = LinearRegression()
    # 训练模型
    lr.fit(x, y)
    # 计算R平方
    print(lr.score(x, y))
    # 计算y_hat
    y_hat = lr.predict(x)
    # 打印出图
    plt.xticks(rotation=270)  # 旋转270度
    plt.plot(xt, y, color="blue")
    plt.plot(xt, y_hat, color="red")
    plt.show()


def pltline():
    pro = ts.pro_api()

    df = pro.index_weekly(ts_code='399006.SZ', start_date='20080101',
                           fields='ts_code,trade_date,open,high,low,close,vol,amount')
    df.sort_values(by='trade_date', ascending=True, inplace=True)
    df = df[['trade_date', 'close']]
    x = np.arange(0, len(df), 1)
    xt = pd.to_datetime(df['trade_date'])
    y = df['close'].tolist()
    print(df)
    x = np.reshape(x, newshape=(len(x), 1))
    y = np.reshape(y, newshape=(len(y), 1))
    # 调用模型
    lr = LinearRegression()

    # 训练模型
    lr.fit(x, y)

    # 截距
    a = lr.intercept_
    # 回归系数
    b = lr.coef_
    print('最佳拟合线：截距a=', a, '，回归系数b=', b)
    # 计算R平方
    print(lr.score(x, y))
    # 计算y_hat
    y_hat = lr.predict(x)
    # 打印出图
    value = df.loc[df.trade_date == '20200529', 'close'].values[0]
    plt.plot(xt, y, color="blue")
    plt.axhline(y=value, color="y")
    plt.plot(xt, y_hat, color="red")
    plt.show()


if __name__ == '__main__':
    pltdayline()
