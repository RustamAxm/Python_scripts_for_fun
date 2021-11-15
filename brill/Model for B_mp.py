import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
# import scipy.optimize

h = 6.6e-16 #eV/c
k = 8.6e-5 #eV/K
mu = 5.8e-5 #eV/T
T_eff = 6
S_eff = 0.8
x = 0.15
N=1

def Brill(x, T):
    const = (5.0 * 58.0) / (86.0 * (T)) #
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)
#T = np.linspace(1.5,15,5)



B_line = np.linspace(0.0,6, 500)
# T = [1.5, 2.8, 4.35, 6.8, 9.3, 11.9, 15, 20]
# T = np.linspace(1.5, 16.5, 11)
T = [1.5]
dE = np.zeros(len(T))
Sum_Ez = np.zeros((len(B_line),len(T)))
Sum_Ez_h = np.zeros((len(B_line),len(T)))
dM = np.zeros((len(B_line),len(T)))
Ro = np.zeros((len(B_line),len(T)))
dRo = np.zeros(len(T))
B_p = np.zeros((len(T), N))
E_mp = np.zeros((len(T), N))
E_mp1 = np.zeros((len(T), N))
V_mp = np.zeros((len(T), N))
R_mp = np.zeros((len(T), N))
Exp_Bp = [0.6, 0.27, 0.18, 0.19]
Exp_E = [0.00453, 0.00138, 0.00073, 0.00054]
Exp_Temp = [1.5, 3, 5, 10]

for l in range(N):
    T_eff = 2*l+3.5
    for i in range(len(T)):
        # print(T[i], k*T[i])

        dE[i]=(0.5 * 0.88 * x * S_eff * (Brill(0.001, (T[i] + T_eff)) - Brill(0.01, (T[i] + T_eff))))/(0.001-0.01)
        for j in range(len(B_line)):
            Sum_Ez[j][i] = 1000*(0.22 * x * S_eff * Brill(B_line[j], (T[i]+T_eff))/1)
            Sum_Ez_h[j][i] = 1000 * (0.88 * x * S_eff * Brill(B_line[j], (T[i] + T_eff)) / 1)
            Ro[j][i] = np.tanh((Sum_Ez_h[j][i]+Sum_Ez[j][i])/(2*1000*k*(T[i])))

        for j in range(len(B_line)):
            if j < 499:
                dM[j][i] = (Sum_Ez_h[j][i] - Sum_Ez_h[j+1][i])/(B_line[j]-B_line[j+1])

        dRo[i] = (Ro[1][i] - Ro[100][i]) / (B_line[1] - B_line[100])
        E_mp[i][l] = np.square(dE[i]/dRo[i]) / (2 * np.pi * k * (T[i]))
        B_p[i][l] = dE[i] / (np.square(dRo[i]) * np.pi * k * (T[i]))
        # E_mp1[i][l] = 1/2*0.88 * x * 5 / 2 * (Brill(B_p[i][l], (T[i] + T_eff)))
        V_mp[i][l] = x * S_eff * 7/24 * np.square(0.88)/(k * (T[i] + T_eff) * E_mp[i][l] * 1.47e+28)
        R_mp[i][l] = np.cbrt(V_mp[i][l]*3/(4 * np.pi))


np.savetxt( "Энергия.txt", np.column_stack((T, E_mp)))
np.savetxt( "поле.txt", np.column_stack((T, B_p)))
np.savetxt( "Сдвиг энергии для дырки.txt", np.column_stack((B_line, Sum_Ez_h)))
np.savetxt( "Поларизация в маг поле.txt", np.column_stack((B_line, Ro)))
np.savetxt( "Производная энергии.txt", np.column_stack((B_line, dM)))

plt.figure(0)
plt.subplot(1, 2, 1)
plt.title("magnetic polaron energy ")
plt.plot(T, E_mp)
plt.plot(Exp_Temp, Exp_E, 'o')
plt.ylabel('Energy(eV)')
plt.xlabel('Temperature(K)')
plt.subplot(1, 2, 2)
plt.title('Polaron magnetic field')
plt.plot(T, B_p)
plt.plot(Exp_Temp, Exp_Bp, 'o')
plt.ylabel('Tesla')
plt.xlabel('Temperature(K)')

plt.figure(1)
plt.subplot(1, 2, 1)
plt.title("Polarization")
plt.plot(T, dRo)
plt.ylabel('POL/tesla')
plt.xlabel('Temperature(K)')
plt.subplot(1, 2, 2)
plt.title('dE')
plt.plot(T, dE)
plt.ylabel('dE(eV/Tesla)')
plt.xlabel('Temperature(K)')

plt.figure(2)
plt.subplot(1, 2, 1)
plt.title(" energy shift ")
plt.plot(B_line, dM)
plt.ylabel('dE/dB')
plt.xlabel('magnetic field(Tesla)')
plt.subplot(1, 2, 2)
plt.title('Polarisation')
plt.plot(B_line, Ro)
plt.ylabel('POL')
plt.xlabel('magnetic field(Tesla)')

plt.figure(3)
plt.subplot(1, 2, 1)
plt.title("Volume")
plt.plot(T, V_mp)
plt.ylabel('m^3')
plt.xlabel('Temperature(K)')
plt.subplot(1, 2, 2)
plt.title('Radius')
plt.plot(T, R_mp)
plt.ylabel('m')
plt.xlabel('Temperature(K)')

plt.show()

