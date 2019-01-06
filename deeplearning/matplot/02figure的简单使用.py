import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1,1,50)

# figure1
y1 = 2*x +1
plt.figure()
plt.plot(x,y1)

# figure2
y2 = x**2 +1
plt.figure()
plt.plot(x,y2)

plt.show()


# figure3
plt.figure()
plt.plot(x,y1)
plt.plot(x,y2)
plt.show()