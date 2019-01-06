import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1,1,50)
y1 = 2 * x +1
y2 = x**2

plt.figure()
plt.plot(x,y1,'r',)
plt.plot(x,y2,color = 'r', linewidth = 2,linestyle = '--')

plt.xlabel(u'x轴',fontproperties = 'SimHei',fontsize = 14)
plt.ylabel(u'y轴',fontproperties = 'SimHei',fontsize = 12)

plt.xticks(np.linspace(-1,1,4))

# 获取当前坐标轴
ax = plt.gca()

ax.spines['right'].set_color('None')
ax.spines['top'].set_color('None')

# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')

ax.spines['bottom'].set_position(('data',0))
ax.spines['left'].set_position(('data',0))


plt.show()