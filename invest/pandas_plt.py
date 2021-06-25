from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt

df = DataFrame([{'A': '1', 'B': '11'}, {'A': '2', 'B': '22'}, {'A': '3', 'B': '33'}])
ser = Series([4, 5, 7])
ser.plot()
# plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter([1, 2, 3, 4], [2, 4, 6, 8], s=np.pi * 3 ** 2,
           c=['r', 'b', 'y', 'k'],alpha=1)  # x，y，大小，颜色，颜色也可以用随意的数字代替，比如[1,2,3,4]表示不同颜色即可，具体怎么设置想要的颜色后续再研究
plt.show()
