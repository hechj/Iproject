from sklearn import svm

x = [[1, 1], [2, 5], [5, 5], [2, 4]]
y = [5, 6, 5, 6]  # 对应x的分类标记
clf = svm.SVC(kernel='linear')  # 线性核函数
clf.fit(x, y)

print(clf)
print(clf.support_vectors_) # 支持向量
print(clf.support_)  # 支持向量是哪几个(下标)
print(clf.n_support_) # 每一类中有几个支持向量
print(clf.predict([[4, 4]])) # 测试数据