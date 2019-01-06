import matplotlib.pyplot as plt
import numpy as np

a = np.linspace(0,1,9).reshape(3,3)

plt.imshow(a,interpolation='nearest',cmap='bone',origin='lower')
# 添加颜色条
plt.colorbar()

plt.xticks(())
plt.yticks(())

plt.show()