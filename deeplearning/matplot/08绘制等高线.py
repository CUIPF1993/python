import matplotlib.pyplot as plt
import numpy as np


n = 256
x = np.linspace(-3,3,n)
y = np.linspace(-3,3,n)

print(x*y)

def f(x, y):
    return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(- x ** 2 - y ** 2)

X,Y = np.meshgrid(x,y)
# 填充等高线颜色
plt.contourf(X,Y,f(X,Y),8,alpha=0.75,cmap=plt.cm.hot)
# 绘制等高线
C = plt.contour(X,Y,f(X,Y),8,colors='black',linewidth=0.5)
# 绘制等高线数据
plt.clabel(C,inline=True,fontsize =10)

plt.xticks(())
plt.yticks(())

plt.show()