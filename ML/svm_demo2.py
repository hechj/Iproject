import numpy as np
import pylab as pl
from sklearn import svm

# 生成随机点数据集
np.random.seed(0)
x = np.r_[np.random.randn(5, 2) - [2, 2], np.random.randn(5, 2) + [2, 2]]
y = [0] * 5 + [1] * 5
print(x)
print(y)

clf2 = svm.SVC(kernel='linear')
clf2.fit(x, y)
print(clf2.support_)
print(clf2.support_vectors_)

# 画出散点图
# 画出支持向量的点，参数：x，y，大小
pl.scatter(clf2.support_vectors_[:, 0], clf2.support_vectors_[:, 1], s=100)
# 画出全部的点，参数：x，y，颜色，colormap，形状
pl.scatter(x[:, 0], x[:, 1], c=y, cmap=pl.cm.Paired, marker='o')
pl.axis('tight')
# pl.savefig('LinearSVC.png')
pl.show()
