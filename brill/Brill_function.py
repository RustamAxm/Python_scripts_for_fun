import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
B = np.linspace(0.0001,6,150)
E_b = -0.003
#print(B)


def Brill(x, T):
    const = (5 * 58) / (86 * T)
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)
'''for i in range(len(B)):
    print(Brill(B[i]))'''
dE_e = []
dE_h = []
dE_e_1 = []
dE_h_1 = []
X_f = []
X_f_1 = []
X_v = []
T_e = []
T_h = []
T_e_f = []
T_h_f = []
T_e_v = []
T_h_v = []
for i in range(len(B)):

    dE_e.append(-0.22 * 0.01 * 5 / 2 * Brill(B[i],1.6)/2)
    dE_h.append(-0.88 * 0.01 * 5 / 2 * Brill(B[i],1.6)/2)
    #расчет энергии для экситона и триона Faraday
    X_f.append(dE_e[i] + dE_h[i])
    T_e_f.append(E_b + dE_h[i])
    T_h_f.append(E_b + dE_e[i])
    # расчет энергии для экситона и триона Voight
    X_v.append(dE_e[i] + 0.01 * dE_h[i])
    T_e_v.append(E_b + 0.01 * dE_h[i])
    T_h_v.append(E_b + dE_e[i])
    #kjbsnkbnsk
    dE_e_1.append(-0.22 * 0.01 * 5 / 2 * Brill(B[i], 10.6) / 2)
    dE_h_1.append(-0.88 * 0.01 * 5 / 2 * Brill(B[i], 10.6) / 2)
    X_f_1.append(dE_e_1[i] + dE_h_1[i])
with plt.xkcd():
 plt.subplot(2, 1, 1)
 plt.title('Faraday')
 a, = plt.plot(B, X_f)
 b, = plt.plot(B, T_e_f)
 c, = plt.plot(B, T_h_f)
 plt.grid(b=None, which='major', axis='both')
 plt.ylabel('Energy shift[eV]')
 plt.ylim((-0.02, 0.001))
 plt.legend([a, b, c], ["X", "X-", "X+"])

 plt.subplot(2, 1, 2)
 plt.title('Voigt')
 a, = plt.plot(B, X_v)
 b, = plt.plot(B, T_e_v)
 c, = plt.plot(B, T_h_v)
 plt.grid(b=None, which='major', axis='both')
 plt.xlabel('Magnetic field [T]')
 plt.ylabel('Energy shift[eV]')
 plt.ylim((-0.02, 0.001))
 plt.legend([a, b, c], ["X", "X-", "X+"])
plt.show()

