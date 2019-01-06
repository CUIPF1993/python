import matplotlib.pyplot as plt
import numpy as np

n = 10
x = np.arange(n)

print(np.random.uniform(0,0.5,10))
y1 = 1 - x/float(n)*np.random.uniform(0.5,1,n)
y2 = 1 - x/float(n)*np.random.uniform(0.5,1,n)

plt.bar(x,y1,facecolor = 'b',edgecolor = 'w',)
plt.bar(x,-y2,facecolor = 'r',edgecolor = 'w',)

plt.ylim(-2,2)

for x,y in zip(x,y1):
    plt.text(x+0.05,y+0.1,'%.2f'%y,ha='center',va='bottom')
x = np.arange(10)
for x,y in zip(x,y2):
    plt.text(x+0.05,-y-0.2,'%.2f'%(-y),ha = 'center',va = 'bottom')

plt.xticks(())
plt.yticks(())

plt.show()