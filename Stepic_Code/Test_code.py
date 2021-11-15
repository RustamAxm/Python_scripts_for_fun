from scipy.stats import chi2
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(10, 6))

df_s = 100

x = np.linspace(0, 100, 1000)

for i in range(0, df_s, 10):
    df = i + 1
    plt.plot(x, chi2.pdf(x, df), label=f'k={df}')
plt.legend(bbox_to_anchor=(1, 1), fontsize=14)
plt.title('Сhi-square distribution depends on degrees of freedom', fontsize=16)
plt.grid()
plt.show()