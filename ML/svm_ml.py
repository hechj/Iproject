#-*- coding=utf-8 -*-
import random

from numpy import *

# 将文本中的样本数据添加到列表中
def loadDataSet(fileName):
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines() : # 对文本按行遍历
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])   # 每行前两个是属性数据，最后一个是类标号
        labelMat.append(float(lineArr[2]))
    return dataMat , labelMat

# 随机选取对偶因子alpha ,参数i 是alpha 的下标，m 是alpha 的总数
def selectJrand(i,m):
    j = i
    while (j==i):
        j = int(random.uniform(0,m))
    return j

# 对所求的对偶因子按约束条件的修剪
def clipAlpha(aj, H, L): # H 为上界，L为下界
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj


class optStruct:
    def __init__(self,dataMatIn, classLabels, C, toler, kTup):
        self.X = dataMatIn # 样本数据
        self.labelMat = classLabels # 样本的类标号
        self.C = C # 对偶因子的上界值
        self.tol = toler
        self.m = shape(dataMatIn)[0] # 样本的行数，即样本对象的个数
        self.alphas = mat(zeros((self.m, 1))) # 对偶因子
        self.b = 0 # 分割函数的截距
        self.eCache = mat(zeros((self.m, 2))) # 差值矩阵 m * 2，第一列是对象的标志位 1 表示存在不为零的差值 0 表示差值为零，第二列是实际的差值 E
        self.K = mat(zeros((self.m, self.m))) # 对象经过核函数映射之后的值
        for i in range(self.m): # 遍历全部样本集
            self.K[:,i] = kernelTrans(self.X, self.X[i,:], kTup ) # 调用径向基核函数



# 预测的类标号值与真实值的差值，参数 oS 是类对象，k 是样本的对象的标号
def calcEk(oS, k):
    fXk = float(multiply(oS.alphas, oS.labelMat).T * oS.K[:, k] + oS.b)  # 公式（1）
    Ek = fXk - float(oS.labelMat[k]) # 差值
    return Ek


# 由启发式选取第二个 alpha，以最大步长为标准
def selectJ(i, oS, Ei): # 函数的参数是选取的第一个 alpha 的对象号、类对象和对象差值
    maxK = -1; maxDeltaE = 0; Ej = 0 # 第二个 alpha 的初始化
    oS.eCache[i] = [1,Ei] # 更新差值矩阵的第 i 行
    validEcacheList = nonzero(oS.eCache[:,0].A)[0] # 取差值矩阵中第一列不为 0 的所有行数（标志位为 1 ），以元组类型返回
    if (len(validEcacheList)) > 1 : #
        for k in validEcacheList : # 遍历所有标志位为 1 的对象的差值
            if k == i: continue
            Ek = calcEk(oS, k) # 计算对象 k 的差值
            deltaE = abs(Ei - Ek) # 取两个差值之差的绝对值
            if (deltaE > maxDeltaE): # 选取最大的绝对值deltaE
                maxK = k; maxDeltaE = deltaE; Ej = Ek
        return maxK, Ej # 返回选取的第二个 alpha
    else: # 随机选取第二个 alpha
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS,j)
    return j, Ej # 返回选取的第二个 alpha

# 更新差值矩阵的数据
def updateEk(oS, k):
    Ek = calcEk(oS, k) # 调用计算差值的函数
    oS.eCache [k] = [1,Ek]


# 优化选取两个 alpha ，并计算截距 b
def innerL(i, oS):
    Ei = calcEk(oS, i) # 计算 对象 i 的差值
    # 第一个 alpha 符合选择条件进入优化
    if ((oS.labelMat [i]*Ei <- oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat [i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
        j,Ej =selectJ(i, oS, Ei) # 选择第二个 alpha
        alphaIold = oS.alphas[i].copy() # 浅拷贝
        alphaJold = oS.alphas[j].copy() # 浅拷贝

        # 根据对象 i 、j 的类标号（相等或不等）确定KKT条件的上界和下界
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas [j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else :
            L = max(0, oS.alphas[j] + oS.alphas [i] - oS.C)
            H = min(oS.C, oS.alphas [j] + oS.alphas [i])

        if L==H:print("L==H");return 0 # 不符合优化条件（第二个 alpha）
        eta = 2.0 * oS.K[i,j] - oS.K[i,i] - oS.K[j,j]  # 计算公式的eta ,是公式的相反数
        if eta >= 0:print("eta>=0");return 0 # 不考虑eta 大于等于 0 的情况（这种情况对 alpha 的解是另外一种方式，即临界情况的求解）
        # 优化之后的第二个 alpha 值
        oS.alphas[j] -= oS.labelMat[j]*(Ei - Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
        updateEk(oS, j) # 更新差值矩阵
        if (abs(oS.alphas[j] - alphaJold) < 0.00001): # 优化之后的 alpha 值与之前的值改变量太小，步长不足
            print("j not moving enough")
            return 0
        oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*(alphaJold - oS.alphas[j]) # 优化第二个 alpha
        updateEk(oS, i) # 更新差值矩阵
        # 计算截距 b
        b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, i] - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.K[i, j]
        b2 = oS.b - Ej - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, j] - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.K[j, j]
        if (0 < oS.alphas [i]) and (oS.C > oS.alphas[i]):
            oS.b = b1
        elif (0 < oS.alphas [j]) and (oS.C > oS.alphas [j]):
            oS.b = b2
        else :
            oS.b = (b1 + b2)/2.0
        return 1 # 进行一次优化
    else :
        return 0


# 遍历所有能优化的 alpha
def smoP(dataMatIn, classLabels, C, toler, maxIter, kTup=('lin', 0)):
    oS = optStruct(mat(dataMatIn), mat(classLabels).transpose(), C, toler, kTup) # 创建一个类对象 oS ,类对象 oS 存放所有数据
    iter = 0 # 迭代次数的初始化
    entireSet = True # 违反 KKT 条件的标志符
    alphaPairsChanged = 0 # 迭代中优化的次数

    # 从选择第一个 alpha 开始，优化所有alpha
    while(iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet )): # 优化的终止条件：在规定迭代次数下，是否遍历了整个样本或 alpha 是否优化
        alphaPairsChanged  = 0
        if entireSet: #
            for i in range(oS.m): # 遍历所有对象
                alphaPairsChanged += innerL(i ,oS) # 调用优化函数（不一定优化）
            print("fullSet , iter: %d i %d, pairs changed %d" % (iter, i , alphaPairsChanged ))
            iter += 1 # 迭代次数加 1
        else:
            nonBoundIs = nonzero((oS.alphas .A > 0) * (oS.alphas.A < C))[0]
            for i in nonBoundIs : # 遍历所有非边界样本集
                alphaPairsChanged += innerL(i, oS) # 调用优化函数（不一定优化）
                print("non-bound, iter: %d i :%d, pairs changed %d" % (iter, i, alphaPairsChanged ))
            iter += 1 # 迭代次数加 1
        if entireSet : # 没有违反KKT 条件的alpha ，终止迭代
            entireSet = False
        elif (alphaPairsChanged == 0): # 存在违反 KKT 的alpha
            entireSet = True
        print("iteration number: %d" % iter)
    return oS.b, oS.alphas # 返回截距值和 alphas

# 径向基核函数（高斯函数）
def kernelTrans(X, A, kTup): # X 是样本集矩阵，A 是样本对象（矩阵的行向量） ， kTup 元组
    m,n = shape(X)
    K = mat(zeros((m,1)))
    # 数据不用核函数计算
    if kTup [0] == 'lin': K = X * A.T

    # 用径向基核函数计算
    elif kTup[0] == 'rbf':
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow * deltaRow.T
        K = exp(K/(-1*kTup[1]**2))
    # kTup 元组值异常，抛出异常信息
    else:raise NameError('Houston We Have a Problem --That Kernel is not recognized')
    return K

# 训练样本集的错误率和测试样本集的错误率
def testRbf(k1=1.3):
    dataArr,labelArr = loadDataSet('../dataset/trainSetRBF.txt') # 训练样本的提取
    b,alphas = smoP(dataArr, labelArr, 200, 0.0001, 10000, ('rbf', k1)) # 计算得到截距和对偶因子
    datMat=mat(dataArr); labelMat = mat(labelArr).transpose()
    svInd=nonzero(alphas.A>0)[0] # 对偶因子大于零的值，支持向量的点对应对偶因子
    sVs=datMat[svInd]
    labelSV = labelMat[svInd]
    print("there are %d Support Vectors" % shape(sVs)[0])
    m,n = shape(datMat)
    errorCount = 0
    # 对训练样本集的测试
    for i in range(m):
        kernelEval = kernelTrans(sVs,datMat[i,:],('rbf', k1)) # 对象 i 的映射值
        predict=kernelEval.T * multiply(labelSV,alphas[svInd]) + b # 预测值
        if sign(predict)!=sign(labelArr[i]): errorCount += 1
    print("the training error rate is: %f" % (float(errorCount)/m))
    dataArr,labelArr = loadDataSet('../dataset/testSetRBF2.txt') # 测试样本集的提取
    errorCount = 0
    datMat=mat(dataArr); labelMat = mat(labelArr).transpose()
    m,n = shape(datMat)
    # 对测试样本集的测试
    for i in range(m):
        kernelEval = kernelTrans(sVs,datMat[i,:],('rbf', k1)) # 测试样本对象 i 的映射值
        predict=kernelEval.T * multiply(labelSV,alphas[svInd]) + b # 预测值
        if sign(predict)!=sign(labelArr[i]): errorCount += 1
    print("the test error rate is: %f" % (float(errorCount)/m))


if __name__ == '__main__':
    '''
    # 显示计算的截距值b 和对偶因子 alphas
    dataMat ,labelMat = loadDataSet('testSet.txt')
    b, alphas = smoP(dataMat, labelMat , 0.6, 0.11, 40,('rbf',2))
    print '------'
    print b, '----',alphas
    '''
    # 支持向量机的测试
    testRbf()


