import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
h = 6.6e-16 #eV/c
k = 8.6e-5 #eV/K
mu = 5.8e-5 #eV/T

def Brill(x, T):
    const = (5 * 58) / (86 * T)
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)
#T = np.linspace(1.5,15,5)
T = [1.5, 2.8, 4.35, 6.8, 9.3, 11.9]
B_line = np.linspace(0.000001,1.5, 10)
B=[0.1025,0.0993,0.0942, 0.0858, 0.0704, 0.0658] # поля из эксперимента ханле
print(T)
print(B)
dE_e = []#np.zeros((6, 1))
dE_em = []#np.zeros((6, 1))
T_s = []#np.zeros((6, 1))
Nu_s = []
Ez_e = []
Sum_Ez = np.zeros((len(B_line),6))
Nu_l = np.zeros((len(B_line),6))
Nu_0 = np.zeros((len(B_line),6))
Ro_1 = np.zeros((len(B_line),6))
e = np.zeros((len(B_line),6))
#for j in range(len(B)):
for i in range(len(T)):
  dE_e.append(0.22 * 0.01 * 5 / 2 * Brill(B[i],T[i])/2)
  dE_em.append(1000*dE_e[i])
  T_s.append(2*np.pi*h/dE_e[i])
  Nu_s.append(dE_e[i]/(2*np.pi*h))

for i in range(len(T)):
    for j in range(len(B_line)):
        Sum_Ez[j][i] = 1000*(0.22 * 0.01 * 5 / 2 * Brill(B_line[j], T[i])/2)
        Nu_l[j][i] = Sum_Ez[j][i]/(2*np.pi*h)/1000
        Nu_0[j][i] = mu*2*B_line[j]/(2*np.pi*h)/1000
        e[j][i] = np.exp(-Sum_Ez[j][i]/(1000*k*T[i]))
        Ro_1[j][i] = 1/(1 + np.square(Sum_Ez[j][i]/(1000*h)*np.exp(-Sum_Ez[j][i]/(1000*k*T[i]))))

plt.plot(B_line,e)
with plt.xkcd():
    # f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    # ax1.plot(T, T_s)
    # ax2.plot(T, Nu_s)


    plt.figure(1)
    plt.subplot(1, 2, 1)
    plt.plot(T, T_s)
    plt.ylabel('Depolarisation_time[c]')
    plt.xlabel('Temperature[K]')
    plt.subplot(1, 2, 2)
    plt.plot(T, Nu_s)
    plt.ylabel('Larmour_precession[Hz]')
    plt.xlabel('Temperature[K]')

    plt.figure(2)
    plt.subplot(1, 2, 1)
    plt.plot(T, dE_em)
    plt.ylabel('Zeeman_energy[meV]')
    plt.xlabel('Temperature[K]')
    plt.subplot(1, 2, 2)
    plt.plot(T, Nu_s)
    plt.ylabel('Larmour_precession[Hz]')
    plt.xlabel('Temperature[K]')

    plt.figure(3)
    plt.subplot(1,2,1)
    plt.title('Elektron_Zeeman_splitting')
    plt.plot(B_line, Sum_Ez)
    plt.ylabel('Zeeman_energy[meV]')
    plt.xlabel('Magnetic_field[T]')
    plt.subplot(1, 2, 2)
    plt.title('Larmour_precession')
    plt.plot(T, np.transpose(Nu_l))
    plt.ylabel('Larmour_freq')
    plt.xlabel('Temperature[K]')

    plt.figure(4)
    plt.title('Ханле')
    plt.plot(B_line, Ro_1)
    plt.ylabel('a.e.')
    plt.xlabel('Magnetic_field[T]')

plt.show()
