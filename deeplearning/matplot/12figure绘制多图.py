import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0,9,1)
y = x**1.1

plt.figure()
# figure分成3行3列，得到第一个子图的句柄，第一个子图跨度为1行3列，起点为表格（0，0）
ax1 = plt.subplot2grid((3,3),(0,0),colspan=3,rowspan=1)
ax1.plot(x,y)
ax1.set_title(u'图1',fontproperties='SimHei')

ax2 = plt.subplot2grid((3,3),(1,0),colspan=2,rowspan=1)
ax2.plot(x,x)
ax2.set_title(u'图2',fontproperties='SimHei')

ax3 = plt.subplot2grid((3,3),(1,2),colspan=1,rowspan=2)
ax3.scatter(x,y)

ax4 =plt.subplot2grid((3,3),(2,0),colspan=1,rowspan=1)
ax5 =plt.subplot2grid((3,3),(2,1),colspan=1,rowspan=1)

plt.show()