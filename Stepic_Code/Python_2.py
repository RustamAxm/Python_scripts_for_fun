import matplotlib.pyplot as plt
import numpy as np

n = np.linspace(1, 100, 100)
f = np.log(n) * np.log(n)
g = np.sqrt(n)

plt.figure()
plt.plot(n, f, 'r', label = 'n /np.log(n)')
plt.plot(n, g,  'b', label = 'np.log(n) * np.log(n)')
plt.legend(loc='lower right')
plt.show()
