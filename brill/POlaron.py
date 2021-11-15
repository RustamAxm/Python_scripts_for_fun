import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
# import scipy.optimize

h = 6.6e-16 #eV/c
k = 8.6e-5 #eV/K
mu = 5.8e-5 #eV/T
T_eff = 1
x = 0.02


def Brill(x, T):
    const = (5.0 * 58.0) / (86.0 * (T))
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)
#T = np.linspace(1.5,15,5)



B_line = np.linspace(0.0,0.5, 500)
B_neg = [0.1025,0.0993,0.0942, 0.0858, 0.0704, 0.0658] # поля из эксперимента ханле отриц поляризация
T = [1.5, 2.8, 4.35, 6.8, 9.3, 11.9]
B_poz = [0.117, 0.1307, 0.1427, 0.1725 ]
T_poz = [1.5, 2.8, 4.5, 6.8]
Ro_temp_poz_exp = [2.45, 1.78, 1.25, 1.1]
data = np.loadtxt("0.5M_POL(Temp)_det719_ex718_5mW.txt", float)
Sum_Ez = np.zeros((len(B_line),6))
Sum_Ez_h = np.zeros((len(B_line),6))
Nu_l = np.zeros((len(B_line),6))
Ro_1 = np.zeros((len(B_line),6))
Ro_neg = np.zeros((len(B_line),6))
Ro_neg_norm = np.zeros((len(B_line),6))
Ro = np.zeros((len(B_line),6))
e = np.zeros((len(B_line),6))
Ts = np.zeros((len(B_line),6))
Omega_T = np.zeros((len(B_line),6))
E_mp_1 = np.zeros((len(B_line),6))
Omega_T_neg = np.zeros((len(B_line),6))
g = np.zeros(len(B_line))
HWHM_poz = np.zeros(6)
HWHM_neg = np.zeros(6)
HWHM_neg_norm = np.zeros(6)
Nu_poz_teor = np.zeros(6)
Nu_neg_teor = np.zeros(6)
T_form = np.zeros(6)
Tau_s_poz = np.zeros(len(B_neg))
Tau_s_poz_exp = np.zeros(len(B_poz))
Tau_s_neg_exp = np.zeros(len(B_neg))
dE = [0.0051285916786865766, 0.0046781563243407818, 0.0042347011087024086, 0.0036828766562939821, 0.0032506372606940148, 0.0028970263972356008]
dRo = np.zeros(len(T))
E_mp = np.zeros(len(T))
E_mp1 = np.zeros(len(T))
B_ex = np.zeros(len(T))
B_p = np.zeros(len(T))
Ro_temp = np.zeros(len(T))
Ro_temp_poz = np.zeros(len(T))
Ro_temp1 = np.zeros(len(T))

for i in range(len(T)):
    print(T[i], k*T[i])
    Tau_s_poz[i] = 1e-10/(0.11*(T[i]+T_eff))
    Ro_temp_poz[i] = 7/(1+1*(T[i]))
    B_ex[i] = 0.5 -0.02*(T[i])
    # B_ex[i] = 0.200 - 0.01*(T[i])
    # B_ex[i]= 0.05
    dE[i]=(1.1 * x * 5 / 2 * (Brill(0.001, (T[i] + T_eff)) - Brill(0.01, (T[i] + T_eff))))/(0.001-0.01)
    # E_mp1[i] = 0.5 * dE[i] * 0.4
    for j in range(len(B_line)):
        Sum_Ez[j][i] = 1000*(0.22 * x * 5 / 2 * Brill(B_line[j], (T[i]+T_eff))/1)
        Sum_Ez_h[j][i] = 1000 * (0.88 * x * 5 / 2 * Brill(B_line[j], (T[i] + T_eff)) / 1)
        Nu_l[j][i] = Sum_Ez[j][i]/(2*np.pi*h)/1000
        Ts[j][i] = 1e-10*Tau_s_poz[i]/(1e-10+Tau_s_poz[i])#np.exp(-1*Sum_Ez[j][i]/(1000*k*(T[i]+T_eff)))*1e-11
        Omega_T[j][i] = Sum_Ez[j][i]/(1000*h*2*np.pi)*Ts[j][i]
        Ro_1[j][i] = 1/(1 + np.square(Omega_T[j][i]))
        Ro[j][i] = np.tanh((Sum_Ez_h[j][i]+Sum_Ez[j][i])/(2*1000*k*(T[i]+T_eff)))
        # E_mp_1[j][i] = (1.1 * x * 5 / 2 * Brill((np.square(B_ex[i])/np.sqrt(np.square(B_ex[i])+np.square(B_line[j]))), (T[i] + T_eff)) / 2)
        # E_mp_1[j][i] = 10*(0.88 * x * 5 / 2 * Brill(B_ex[i]*np.cos(np.arctan((B_line[j]/B_ex[i]))),(T[i] + T_eff)) / 2)
        E_mp_1[j][i] = 0.5*dE[i]*B_ex[i]*(np.sqrt(1+np.square(B_line[j]/B_ex[i]))*(np.sqrt(1+np.square(B_line[j]/B_ex[i]))-B_line[j]/B_ex[i])-0.)
        # E_mp_1[j][i] = 0.5 * dE[i] * B_ex[i]
        # Ro_neg[j][i] = np.tanh((E_mp_1[j][i])/(4*k*(T[i]+T_eff)))
        # Ro_neg_norm[j][i] = Ro_neg[j][i] / Ro_neg[0][i]

        Ro_neg[j][i] = 1*(1/(1+100/np.exp((E_mp_1[j][i])/(4*k*(T[i]+T_eff)))))

    for j in range(len(B_line)):
        Ro_neg_norm[j][i] = (Ro_neg[j][i]-Ro_neg[499][i])/ (Ro_neg[0][i]-Ro_neg[400][i])
        if abs(Ro_1[j][i] - 0.5) <= 0.01:
            HWHM_poz[i] = B_line[j]
        if abs(Ro_neg_norm[j][i] - 0.5) <= 0.01:
            HWHM_neg[i] = B_line[j]
    Ro_temp[i] = Ro_neg[0][i]
    E_mp[i] = E_mp_1[0][i]

for i in range(len(T)):
    # dE[i] = ((Sum_Ez_h[1][i] - Sum_Ez_h[100][i])  ) /(B_line[1]-B_line[100])/1000
    dRo[i] = (Ro[1][i] - Ro[100][i]) /(B_line[1]-B_line[100])
    # E_mp1[i] = 0.5*dE[i]*1.5 #np.square(dE[i]/dRo[i]) / (2 * np.pi * k * (T[i]+T_eff))
    B_p[i] = dE[i]/(np.square(dRo[i])*np.pi*k*(T[i]+T_eff))
    Ro_temp1[i] = np.tanh(E_mp1[i]/(16*np.pi*k*(T[i]+T_eff)))



print('Тау_  =',Tau_s_poz)
print(dE, dRo)
print(B_ex)
print(B_p)
print(E_mp1,E_mp)
print(Ro_temp)
print(Ro_temp1)
plt.figure(0)
plt.subplot(1, 2, 1)
plt.title('Магнитное поле полярона')
# plt.plot(T, dE,'-', label = "Флуктационная модель")
plt.plot(T, B_p,'-', label = "Эффективное поле")
# plt.legend(loc='upper left', shadow=True, fontsize='x-small')
# plt.ylabel('Энергия')
# plt.subplot(1, 2, 2)
# plt.title('Полризация от температуры')
# plt.plot(T,Ro_temp1,'-', label = "Флуктационная модель")
# plt.plot(T,Ro_temp,'-', label = "Эффективное поле")
# plt.legend(loc='upper left', shadow=True, fontsize='x-small')
plt.figure(1)
plt.subplot(1, 2, 1)
plt.title('Ханле в отрицательной области')
plt.plot(B_line, Ro_neg)
plt.ylabel('POl')
plt.xlabel('Magnetic_field[T]')
plt.subplot(1, 2, 2)
plt.title('Normalized_Hanle')
plt.plot(B_line, Ro_neg_norm)
plt.ylabel('a.e')
plt.xlabel('Magnetic_field[T]')

plt.figure(2)
plt.subplot(1, 2, 1)
plt.title('Температурная зависимость поляризации')
plt.plot(T, Ro_temp, '-', label = "POlarization_Theory Negative")
plt.plot(T, Ro_temp_poz, '-', label = "POlarization_Theory POzitive")
plt.plot(T_poz, Ro_temp_poz_exp, 'o', label = "POlarization_Experiment POzitive")
plt.plot(data[:15,0], abs(data[:15,1])/100,'o', label = "Polarization_Exp_Negative")
plt.plot(T,Ro_temp1,'-', label = "Флуктационная модель отрицаетльная")
plt.legend(loc='upper right', shadow=True, fontsize='small')
plt.ylabel('POl')
plt.xlabel('Temperature[K]')
plt.subplot(1, 2, 2)
plt.title('Энергия полярона')
plt.plot(T, E_mp1,'-', label = "Флуктационная модель")
plt.plot(T, E_mp,'-', label = "Эффективное поле")
plt.legend(loc='upper left', shadow=True, fontsize='x-small')
plt.ylabel('eV')
plt.xlabel('Temperature[K]')

plt.figure(3)
plt.title('Полуширина Ханле Exp_vs_Theory')
plt.plot(T, HWHM_neg,label='Negative_Theory')
plt.plot(T, B_neg, 'o', label= 'Negative_Experiment')
plt.plot(T, HWHM_poz, label='Pozitive_Theory')
plt.plot(T_poz, B_poz, 'o', label='Pozitive_Experiment')
plt.legend(loc='upper left', shadow=True, fontsize='x-small')
plt.ylabel('HWHM[T]')
plt.xlabel('Temperature[K]')
plt.show()