import numpy as np
import matplotlib.pyplot as plt

def Brill(x, T =5):
    const = (5 * 58) / (86 * T)
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)

E_0 = 12.6
E = np.linspace(0.01, 2, 1000)
B = np.round(np.linspace(0.01, 5, 6), 1)
# B = 5
T = np.linspace(1.5, 10, 6)
E_h = np.zeros(len(B))
F = np.zeros((len(E), len(B)))
x = 0.005
N_0 = 1.47e28
a = 1e-9
gamma = np.pi/6 * x * N_0 * a**3
for j in range(len(E)):
    for i in range(len(B)):
        E_h[i] = 1*880*x*2.5*Brill(B[i], 5)
        F[j][i] = 3*gamma/E[j] * (np.log(E[j]/(E_0 - E_h[i])))**2 * np.exp(gamma*np.log(E[j]/(E_0-E_h[i]))**3)
print([x for x in T])
plt.figure(0)
plt.title(" модель ДА полярона 1.5 K разные поля")
plt.plot(E, F, '-')
plt.legend(((B)), loc='upper right', shadow=True)
plt.ylabel('Амплитуда')
plt.xlabel('Сдвиг энергии (мэВ)')

plt.figure(1)
plt.title(" модель ДА полярона 1.5 K разные поля")
plt.plot(B, (E_0 - E_h), '-')
# plt.legend(((B)), loc='upper right', shadow=True)
plt.ylabel('Сдвиг энергии (мэВ)')
plt.xlabel('Магниное поле')

plt.show()