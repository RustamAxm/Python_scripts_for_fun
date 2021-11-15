import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


def Brill(x, T = 5):
    const = (5 * 58) / (86 * T)
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)

h = 6.6e-16 #eV/c это аш с палкой
k = 8.6e-5 #eV/K
mu = 5.8e-5 #eV/T
g = 2 # это же фактор
B_ex = [3.5]# np.linspace(2, 4, 3)

B_ex_2 = [0.5] #np.linspace(0.25, 0.75, 3)
x = 0.02
B_x = np.linspace(0.01, 10, 100)
M_i = np.zeros((len(B_ex), len(B_x)))
M_i_2 = np.zeros((len(B_ex), len(B_x)))
M_f = np.zeros((len(B_ex), len(B_x)))
E_e = np.zeros((len(B_ex), len(B_x)))
delta_M = np.zeros((len(B_ex), len(B_x)))
delta_W = np.zeros((len(B_ex), len(B_x)))
sigma = np.zeros((len(B_ex), len(B_x)))
print(np.shape(M_i))


for i in range(len(B_x)):
    for j in range(len(B_ex)):

        M_i[j][i] = 2.5 * Brill(np.sqrt(B_x[i]**2 + B_ex[j]**2)) * (B_ex[j]/np.sqrt(B_x[i]**2 + B_ex[j]**2))
        M_f[j][i] = 2.5 * Brill(np.sqrt(B_x[i]**2 + 4 * B_ex[j]**2)) * (2*B_ex[j]/np.sqrt(B_x[i]**2 + 4 * B_ex[j]**2))
        delta_M[j][i] = (M_f[j][i] - M_i[j][i]) * (1 - np.exp(-180/150))
        delta_W[j][i] = 0.5 * 0.22 * x * delta_M[j][i] + \
                    0.5 * 0.88 * x * delta_M[j][i]  # -\
                      # 0.44 * x * delta_M[i] * (B_ex/np.sqrt(B_x[i]**2 + B_ex**2))
        M_i_2[j][i] = 2.5 * Brill(np.sqrt(B_x[i] ** 2 + B_ex_2[j] ** 2)) * (B_ex_2[j] / np.sqrt(B_x[i] ** 2 + B_ex_2[j] ** 2))
        E_e[j][i] = 0.22 * x * M_i_2[j][i]
        sigma[j][i] = E_e[j][i] - 0.5 * 0.22 * x * M_i_2[j][i] * np.exp(-180/150)  + 0.5 * 0.88 * x * M_i_2[j][i] * np.exp(-180/150)


# B_x = np.linspace(0.0, 10, 100)
# B_ex = [0]
# for i in range(len(B_x)):
#     for j in range(len(B_ex)):
#         M_i[j][i] = 2.5 * Brill(B_x[i])
#         M_f[j][i] = 2.5 * Brill(2*B_x[i])
#         delta_M[j][i] = (M_f[j][i] - M_i[j][i]) * (1 - np.exp(-180/150))
#         delta_W[j][i] = 0.5 * 0.22 * x * delta_M[j][i] + \
#                     0.5 * 0.88 * x * delta_M[j][i]  # -\
#
#         E_e[j][i] = 0.22 * x * M_i[j][i]
#         sigma[j][i] = E_e[j][i] - 0.5 * 0.22 * x * M_i[j][i] * np.exp(-180/30)  + 0.5 * 0.88 * x * M_i[j][i] * np.exp(-180/30)



# plt.figure(0)
# plt.subplot(1, 2, 1)
# # plt.plot(B_f, z_0)
# plt.plot(B_x, delta_W, '-', label = "Энергия сдвига в фл")
# plt.plot(B_x, sigma , '-', label = "сдвиг для сигма минус")
# # plt.ylim(0.00, 0.006)
# plt.legend(loc='upper right', shadow=True)
# plt.ylabel(' Энергия эВ')
# plt.xlabel('поперечное  поле(Тесла)')
# plt.subplot(1, 2, 2)
# plt.plot(B_x, M_f, '-', label = "Намагничессность в конце")
# plt.plot(B_x, M_i, '-', label = "Намагничессность в начале")
# plt.plot(B_x, (M_f - M_i), '-', label = "Разность намагниченности")
# # plt.ylim(0, 3)
# plt.legend(loc='upper right', shadow=True)
# plt.ylabel('намагниченность')
# plt.xlabel('поперечное поле(Тесла)')

plt.figure(1)
plt.subplot(1, 2, 1)
# plt.plot(B_f, z_0)
plt.plot(B_x, np.transpose(delta_W))
plt.plot(B_x, np.transpose(sigma))
# plt.ylim(0.00, 0.006)
plt.legend(loc='upper right', shadow=True)
plt.ylabel('Энергия эВ')
plt.xlabel('поперечное поле(Тесла)')
plt.subplot(1, 2, 2)
plt.plot(B_x, np.transpose(M_f))
plt.plot(B_x, np.transpose(M_i))
plt.plot(B_x, np.transpose(M_f - M_i))
# plt.ylim(0, 3)
plt.legend(loc='upper right', shadow=True)
plt.ylabel('намагниченность')
plt.xlabel('поперечное поле(Тесла)')
plt.show()
