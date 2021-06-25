import numpy as np
import matplotlib.pyplot as plt

global K
global N
global spot
global unite
global mean
global count


def cluster():  # 划分每个点一个到簇
    global unite
    unite = []  # 这里千万注意，需要每次都定义，否则会重复添加长度。当下一次运行cluster函数时才会重置unite列表
    for i in range(K):
        print("i={}".format(i))
        unite.append([])
    for i in range(len(spot)):
        max_max = np.iinfo(np.int32).max  # 预定义一个极大值,用于比较
        flag = -1
        for j in range(K):
            n = (spot[i][0] - mean[j][0]) ** 2 + (spot[i][1] - mean[j][1]) ** 2
            if n < max_max:
                max_max = n
                flag = j
        unite[flag].append(spot[i])
    for i in range(K):
        print("第{}簇：{}".format(i, unite[i]))


def square_d():
    global count
    sum_E = 0
    for i in range(len(unite)):
        for j in range(len(unite[i])):
            sum_E += ((unite[i][j][0] - mean[i][0]) ** 2 + (unite[i][j][1] - mean[i][1]) ** 2)
    count += 1
    return sum_E


def remean():
    for i in range(len(unite)):
        sum_x = 0
        sum_y = 0
        for j in range(len(unite[i])):
            sum_x += unite[i][j][0]
            sum_y += unite[i][j][1]
        # if(len(unite[i]) == 0):     #分母不为0，如果前面判断了中心值不一样可以省略
        #     mean[i] = (0,0)
        # else:
        #     mean[i] = (sum_x/len(unite[i]),sum_y/len(unite[i]))
        mean[i] = (sum_x / len(unite[i]), sum_y / len(unite[i]))  # 根据均值，重新定义的中心值


def show():
    # 样本数据横坐标列表
    xx = []
    for i in range(K):
        xx.append([])
    # 样本数据纵坐标列表
    yy = []
    for i in range(K):
        yy.append([])
    # 使用样本坐标，绘制散点图
    for i in range(K):
        for j in range(len(unite[i])):
            xx[i].append(unite[i][j][0])
        for j in range(len(unite[i])):
            yy[i].append(unite[i][j][1])

        print("unite[i][j]={}\nunite[i][j]={}".format(unite[i][j], unite[i][j]))
        print("unite[i][j][0]={}\nunite[i][j][1]={}".format(unite[i][j][0], unite[i][j][1]))
        plt.scatter(xx[i], yy[i], label=i)
#        plt.scatter(mean[i][0], mean[i][1], label=i)
        plt.legend()
    # 显示散点图
    plt.show()


if __name__ == "__main__":
    K = 4  # 聚类数    手动设置
    N = 30  # 样本数    手动设置
    spot = []  # 样本列表
    for i in range(N):
        spot.append((np.random.randint(50), np.random.randint(50)))  # 50是我给它定义的范围

    unite = []  # 每个点归属簇
    mean = []  # 每个簇的中心值

    set_t = set()
    while 1:  # 虽然两行代码就可以搞定这个选值，但是我建议使用集合，防止重复值
        d = np.random.randint(N)  # 当然如果你有更简单的方法除外，就我觉得使用集合比较简单
        set_t.add(d)
        if len(set_t) == K:
            for i in set_t:
                mean.append(spot[i])
            break

    print("set_t={}\nspot={}\nspot[0]={}\nspot[0][0]={}\nmean={}".format(set_t, spot,spot[0],spot[0][0],mean))

    count = 0
    m = []
    for i in range(2):  # 首先两次循环，得出两个比较的平方误差
        cluster()  # 聚类
        temp = square_d()  # 计算平方误差
        m.append(temp)
        print("i第{}次聚类平方的差值为：{}".format(count, temp))
        remean()  # 重定义中心值

    while m[0] != m[1]:  # 就两次循环后，重复选中心值，直至相等
        m[0] = m[1]
        cluster()
        m[1] = square_d()
        print("m第{}次聚类平方的差值为：{}".format(count, m[1]))
        remean()

    show()  # 构散点图    构图与k-means无关，但是利用图表将数据展示出来更直观、更有说服力
