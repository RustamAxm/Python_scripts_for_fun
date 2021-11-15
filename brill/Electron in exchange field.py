import numpy as np
import matplotlib.pyplot as plt
def Brill(x, T=7.5):
    const = (5.0 * 58.0) / (86.0 * (T)) #
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)

h = 6.58e-16 #eV/c это аш с палкой
k = 8.6e-5 #eV/K
mu = 5.8e-5 #eV/T
g_e = 100  # это же фактор
g_mn = 2
# B_x = np.linspace(0.001, 0.5, 3)
B_x = np.array([0.405, 0.151, 0.1, 0.001])
B_ex = 0.5
M = 1
S = 1
T_pump = 1e-12
t = 1e-12*np.linspace(0, 400, 5000)
S_x = np.zeros((len(t), len(B_x)))
S_z = np.zeros((len(t), len(B_x)))
S_y = np.zeros((len(t), len(B_x)))
phi = np.zeros(len(B_x))
z_0 = np.zeros(len(B_x))
M_z = np.zeros((len(t), len(B_x)))
Theta = np.zeros((len(t), len(B_x)))
Theta_2 = np.zeros((len(t), len(B_x)))
alfa = np.zeros((len(t), len(B_x)))
"""для постоянного внешнего поля"""
for i in range(len(B_x)):
    phi[i] = np.arctan(B_ex/B_x[i])
    print('частота', mu * g_mn * B_x[i] / h/ 1e9/(2*np.pi))
    print(phi[i]*180/np.pi)
    for j in range(len(t)):
        Theta[j][i] = t[j] * mu * g_e * np.sqrt(B_ex ** 2 + B_x[i] ** 2) / h

        Theta_2[j][i] = t[j] * mu * g_mn * B_x[i]/ h
        alfa[j][i] = -(1/2 * np.pi + phi[i]) * (1 - np.exp(-t[j]/(30e-12 - 0e-10*B_x[i])))
        # S_z[j][i] = S * np.sin(phi[i] + alfa[j])**2 - np.cos(phi[i] + alfa[j])**2* np.sin(Theta[j][i])
        S_z[j][i] = S * ((np.sin(phi[i] + alfa[j][i])*np.sin(phi[i]) - np.cos(phi[i] + alfa[j][i])*np.cos(phi[i]) * np.sin(Theta[j][i]))* np.cos(Theta_2[j][i]) + \
                    np.cos(phi[i] + alfa[j][i]) * np.cos(Theta[j][i]) * np.sin(Theta_2[j][i])) #* np.exp(-t[j]/100e-12)
        M_z[j][i] = - M * np.sin(phi[i])* np.cos(Theta_2[j][i])

'''матричный способ поворота'''

# plt.figure(0)
# plt.subplot(1, 2, 1)
# # plt.plot(B_f, z_0)
# plt.plot(B_ex, M_yz, '-', label = "Амплитуда")
# plt.plot(B_ex, z[:][0], '-', label = "Начальная проекция на Z")
# # plt.ylim(0, 1.2)
# plt.legend(loc='upper right', shadow=True)
# plt.ylabel(' амплитуда а.е.')
# plt.xlabel('Фарадеевское поле(Тесла)')
# plt.subplot(1, 2, 2)
# plt.plot(B_ex, phi/np.pi*180,'-', label = "Начальная фаза")
# plt.plot(B_ex, np.arctan(B_f / B_x)/np.pi*180,'-', label = "угол осей х и х'")
# plt.plot(B_ex, Theta/np.pi*180,'-', label = "вращение вокруг x'")
# # plt.ylim(0, 120)
# plt.legend(loc='upper right', shadow=True)
# plt.ylabel('Начальная фаза (градусы)')
# plt.xlabel('Фарадеевское поле(Тесла)')

plt.figure(1)
plt.subplot(3, 1, 1)
for i in range(len(B_x)):
    plt.plot(t, S_z[:,i], '-', label="{} Tesla".format(B_x[i]))
plt.ylabel('проекция Z')
plt.legend(loc='upper right', shadow=True)
plt.subplot(3, 1, 2)
plt.plot(t, alfa*180/np.pi)
plt.ylabel('alfa')
# plt.xlabel('Время(сек)')
plt.subplot(3, 1, 3)
plt.plot(t, M_z)
plt.ylabel('M Z')
plt.xlabel('Время(сек)')
plt.show()