import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
year = ['30周', '31周', '32周', '33周']
y1 = [0.3, 0.2, 0.82, 0.38]
y2 = [0.9, 0.1, 0.42, 0.98]
x1 = range(len(y1))
x2 = [i + 0.35 for i in x1]

plt.bar(x1, y1, width=0.3, color='blue', label='及时率')
plt.bar(x2, y2, width=0.3, color='green', label='饱和度')
plt.xticks([i + 0.2 for i in x1], year)
plt.legend()
plt.show()
