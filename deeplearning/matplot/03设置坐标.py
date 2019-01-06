import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1,1,50)
y1 = 2 * x + 1
y2= x**2 + 1

plt.figure()

plt.plot(x,y1)
plt.plot(x,y2,color='red',linewidth=1.1,linestyle = '--')

plt.xlim((-1,1))
plt.ylim((-1,3))

# 标签中必须添加字体变量：fontproperties='SimHei',不然会乱码
plt.xlabel(u"x轴",fontproperties='SimHei',fontsize= 14)
plt.ylabel(u"y轴",fontproperties='SimHei',fontsize= 14)

#设置x轴坐标刻度
plt.xticks(np.linspace(-1,1,5))
plt.show()