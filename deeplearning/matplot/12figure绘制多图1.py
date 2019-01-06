import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec

x = np.arange(0,9,1)
y = x**1.1

plt.figure()
# figure分成3行3列，得到第一个子图的句柄，第一个子图跨度为1行3列，起点为表格（0，0）
gs = gridspec.GridSpec(3,3)
ax1 = plt.subplot(gs[0,:])
ax2 = plt.subplot(gs[1,0:2])
ax3 = plt.subplot(gs[1:,2])
ax4 = plt.subplot(gs[2,0])
ax5 = plt.subplot(gs[2,1])


ax1.plot(x,y)
ax1.set_title(u'图1',fontproperties='SimHei')
ax2.plot(x,x)
ax2.set_title(u'图2',fontproperties='SimHei')
ax3.plot(x,y)

plt.show()