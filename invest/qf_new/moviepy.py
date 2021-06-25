import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

fig = plt.figure()

ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
x = []
y1 = []
y2 = []
line1, = ax.plot(x, y1)
line2, = ax.plot(x, y2)


def init():
    x.clear()
    y1.clear()
    y2.clear()
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2,


def update(i):
    x.append(i)
    y1.append(3)
    y2.append(4)
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2,


p_ani = ani.FuncAnimation(fig, update,
                          frames=range(0, 100, 1),  # update函数的参数范围
                          init_func=init,
                          interval=100, blit=True, repeat=False)
# p_ani.save('moviepy.gif', writer='Pillow')
plt.show()
