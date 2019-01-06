import matplotlib.pyplot as plt
import numpy as np

n = 1024

x = np.random.normal(0,1,n)
y = np.random.normal(0,1,n)

color = np.arctan2(y,x)

plt.scatter(x,y,s=75,c=color,alpha=0.5)

plt.xlim((-2,2))
plt.ylim((-2,2))

plt.xticks(())
plt.yticks(())
plt.show()