import numpy as np
import matplotlib.pyplot as plt
def Brill(x, T=7.5):
    const = (5.0 * 58.0) / (86.0 * (T)) #
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)

h = 6.6e-16 #eV/c это аш с палкой
k = 8.6e-5 #eV/K
mu = 5.8e-5 #eV/T
g = 2 # это же фактор
B_x = np.linspace(0.01, 100, 100)
B_f = 0.5

T_pump = 1e-12
t = 1e-9*np.linspace(0, 0.1, 100)
z = np.zeros((len(t), len(B_x)))
phi = np.zeros(len(B_x))
z_0 = np.zeros(len(B_x))
Theta = np.zeros(len(B_x))
M_yz = np.zeros(len(B_x))
M = np.zeros(len(B_x))
"""для постоянного внешнего поля"""
for i in range(len(B_x)):
    M[i] = Brill(B_x[i])
    Theta[i] = T_pump * mu * g * np.sqrt(B_f ** 2 + B_x[i] ** 2) / h
    phi[i] = np.arctan((np.cos(np.arctan(B_f / B_x[i])) / np.sin(Theta[i]) *
                        (1 - np.cos(Theta[i])))**(-1))
    # z_0[i] = 0.5 / np.sin(phi[i]) * M * np.sin(2 * np.arctan(B_f / B_x[i])) * \
    #          (1 - np.cos(Theta[i]))
    M_yz[i] = np.sqrt((0.5 * M[i] * np.sin(2 * np.arctan(B_f / B_x[i])) * (1 - np.cos(Theta[i]))) ** 2 + \
                      (M[i] * np.sin(np.arctan(B_f / B_x[i])) * np.sin(Theta[i])) ** 2)
    for j in range(len(t)):
        z[j][i] = M_yz[i] * np.cos(mu * g * B_x[i] / h * t[j] + phi[i])

plt.figure(0)
plt.subplot(1, 2, 1)
# plt.plot(B_f, z_0)
plt.plot(B_x, M_yz, '-', label = "Амплитуда")
plt.plot(B_x, z[:][0], '-', label = "Начальная проекция на Z")
plt.plot(B_x, M, '-', label = "полный магнитный момент М")
plt.ylim(0, 1.2)
plt.legend(loc='upper right', shadow=True)
plt.ylabel(' амплитуда а.е.')
plt.xlabel('внешнее поле(Тесла)')
plt.subplot(1, 2, 2)
plt.plot(B_x, phi/np.pi*180,'-', label = "Начальная фаза")
plt.plot(B_x, np.arctan(B_f / B_x)/np.pi*180,'-', label = "угол осей х и х'")
plt.plot(B_x, Theta/np.pi*180,'-', label = "вращение вокруг x'")
# plt.ylim(0,120)
plt.legend(loc='upper left', shadow=True)
plt.ylabel('Начальная фаза (градусы)')
plt.xlabel('внешнее поле(Тесла)')

plt.figure(1)
plt.plot(t, z)
plt.ylabel('проекция на ось Z')
plt.xlabel('Время(сек)')

plt.show()