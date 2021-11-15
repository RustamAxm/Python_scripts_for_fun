import scipy.optimize
import numpy as np
import matplotlib.pyplot as plt




f = lambda x: np.cos(x)
g = np.sin

h = lambda x: f(x) - 0.5

x = np.linspace(0,3,100)
plt.plot(x, f(x), zorder=1)
plt.plot(x, g(x), zorder=1)

x_int = scipy.optimize.fsolve(h, 1.0)
y_int = f(x_int)

plt.scatter(x_int, y_int, marker='x', s=150, zorder=2,
            linewidth=2, color='black')

plt.xlim([0,3])
plt.ylim([-4,2])
plt.show()