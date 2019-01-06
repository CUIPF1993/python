import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,9,10)
y = x**2
print(x,y)
plt.figure()
plt.subplot(2,2,1)
plt.plot(x,x)

plt.subplot(2,2,2)
plt.plot(x,y)

plt.subplot(2,2,3)
plt.bar(x,y)

plt.subplot(2,2,4)
plt.scatter(x,y)

plt.show()