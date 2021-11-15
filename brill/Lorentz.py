import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
import scipy.optimize

h = 6.6e-16 #eV/c
k = 8.6e-5 #eV/K
mu = 5.8e-5 #eV/T
T_eff = 12
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
T_podgon = [3.5e-11,
4.25e-11,
4.8e-11,
5.8e-11,
7.9e-11,
9.2e-11]
Sum_Ez = np.zeros((len(B_line),6))
Sum_Ez_neg = np.zeros((len(B_line),6))
Sum_Ez_h = np.zeros((len(B_line),6))
Nu_l = np.zeros((len(B_line),6))
Nu_l_neg = np.zeros((len(B_line),6))
Nu_0 = np.zeros((len(B_line),6))
Ro_1 = np.zeros((len(B_line),6))
Ro_neg = np.zeros((len(B_line),6))
Ro_neg_norm = np.zeros((len(B_line),6))
e = np.zeros((len(B_line),6))
Ts = np.zeros((len(B_line),6))
Omega_T = np.zeros((len(B_line),6))
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
for i in range(len(T)):
    print(T[i], k*T[i])
    for j in range(len(B_line)):
        Sum_Ez[j][i] = 1000*(0.22 * x * 5 / 2 * Brill(B_line[j], (T[i]+T_eff))/1)
        Sum_Ez_h[j][i] = 1000 * (0.88 * x * 5 / 2 * Brill(B_line[j], (T[i] + T_eff)) / 1)
        Nu_l[j][i] = Sum_Ez[j][i]/(2*np.pi*h)/1000
        Ts[j][i] = 4e-10*4e-10/(0.9*(T[i]+T_eff))/(4e-10+4e-10/(0.9*(T[i]+T_eff)))#np.exp(-1*Sum_Ez[j][i]/(1000*k*(T[i]+T_eff)))*1e-11
        # Ts[j][i] = 4e-10*30e-12/(4e-10+30e-12)
        Omega_T[j][i] = Sum_Ez[j][i]/(1000*h*2*np.pi)*Ts[j][i]
        Ro_1[j][i] = 1/(1 + np.square(Omega_T[j][i]))

        if abs(Ro_1[j][i] - 0.5) <= 0.01:
            HWHM_poz[i] = B_line[j]




    #Ro_neg[:][i] = Ro_neg[:][i] / max(Ro_neg[:][i])

    Nu_poz_teor[i] = (0.22 * x * 5 / 2 * Brill(HWHM_poz[i], (T[i] + T_eff)) / 1) / (2 * np.pi * h)
print("Полуширина в позитивном",HWHM_poz )

'''Для перевода в частоты полуширины экспериментально ханле '''
dE_e_poz=[]
Nu_poz_ex=[]
for i in range(len(T_poz)):
    dE_e_poz.append(0.22 * x * 5 / 2 * Brill(B_poz[i],(T_poz[i] + T_eff))/1)
    Nu_poz_ex.append(dE_e_poz[i] / (2 * np.pi * h))
    Tau_s_poz_exp[i] = 1/Nu_poz_ex[i]
dE_e_neg=[]
Nu_neg_ex=[]
for i in range(len(T)):
    dE_e_neg.append(0.22 * x * 5 / 2 * Brill(B_neg[i],(T[i] + T_eff))/1)
    Nu_neg_ex.append(dE_e_neg[i] / (2 * np.pi * h))
    Tau_s_neg_exp[i] = 1/Nu_neg_ex[i]
print('Позитивный эксперимент Tau_s',Tau_s_poz_exp)
print("ОТрицательный Эксперимент Tau_s",Tau_s_neg_exp)

'''Заполняем поляризация для отрицательной области'''
for i in range(len(T)):
    Tau_s_poz[i] = 1 / Nu_poz_teor[i]
    T_form[i] = (T[i]+T_eff)*1e-13
    for j in range(len(B_line)):
        Sum_Ez_neg[j][i] = 1000 * (0.22 * x * 5 / 2 * Brill(B_line[j], (T[i] + T_eff)) / 1)
        Nu_l_neg[j][i] = (Sum_Ez[j][i]) / (2 * np.pi * h) / 1000
        Omega_T_neg[j][i] = (Sum_Ez[j][i]) / (1000 * h * 2*np.pi)
        # Ro_neg[j][i] = (1 - np.square(Omega_T[j][i]))/ np.square(1 + np.square(Omega_T[j][i]))
        Ro_neg[j][i] = np.exp(- T_form[i]/Tau_s_poz[i]) * np.cos(Omega_T_neg[j][i] * T_form[i] )*np.exp(- np.square(Omega_T_neg[j][i])*np.square((25.36+5.52*T[i])*1e-12)/2)
        if abs(Ro_neg[j][i] - 0.5) <= 0.01:
            HWHM_neg[i] = B_line[j]
    Nu_neg_teor[i] = (0.22 * x * 5 / 2 * Brill(HWHM_neg[i], (T[i] + T_eff)) / 1) / (2 * np.pi * h)

print("Полуширина в негативном", HWHM_neg)
print("Позитивный режим", Tau_s_poz)

np.savetxt("Computing_Poz_Hanle", np.column_stack((B_line,Ro_1)), fmt='%10f4')
np.savetxt("Computing_NEg_Hanle", np.column_stack((B_line,Ro_neg)), fmt='%10f4')
# for i in range(len(T)):
#     for j in range(len(B_line)):
#         Ro_neg_norm[j][i] = Ro_neg[j][i]/max(Ro_neg[:][i])
#         if abs(Ro_neg_norm[j][i] - 0.5) <= 0.01:
#             HWHM_neg_norm[i] = B_line[j]

with plt.xkcd():
    '''Ханле Для положительной области'''
    plt.figure(4)
    plt.subplot(1, 2, 1)
    plt.title('Ханле в положительной области')
    plt.plot(B_line, Ro_1)
    plt.ylabel('a.e.')
    plt.xlabel('Magnetic_field[T]')
    plt.subplot(1, 2, 2)
    plt.title('Лармор')
    plt.plot(B_line, Nu_l)
    plt.ylabel('Larmour_precession[Hz]')
    plt.xlabel('Magnetic_field[T]')
    '''Ханле Для отрицателной области '''
    plt.figure(1)
    plt.subplot(1, 2, 1)
    plt.title('Ханле в отрицательной области')
    plt.plot(B_line, Ro_neg)
    plt.ylabel('a.e.')
    plt.xlabel('Magnetic_field[T]')
    plt.subplot(1, 2, 2)
    plt.title('Energy')
    plt.plot(B_line, Sum_Ez )
    plt.ylabel('Energy_shift[meV]')
    plt.xlabel('Magnetic_field[T]')
    '''Для всех полуширина'''
    plt.figure(2)
    # plt.subplot(1, 2, 1)
    # plt.title('Лармор')
    # plt.plot(T, Nu_neg_teor)
    # plt.plot(T, Nu_neg_ex, 'o')
    # plt.plot(T, Nu_poz_teor)
    # plt.plot(T_poz, Nu_poz_ex, 'o')
    # plt.ylim(1.1e10, 1.8e10)
    # plt.ylabel('Larmour_precession[Hz]')
    # plt.xlabel('Temperature[K]')
    # plt.subplot(1, 2, 2)
    plt.title('Полуширина Ханле Exp_vs_Theory')
    plt.plot(T, HWHM_neg,label='Negative_Theory')
    plt.plot(T, B_neg, 'o', label= 'Negative_Experiment')
    plt.plot(T, HWHM_poz,label='Pozitive_Theory')
    plt.plot(T_poz, B_poz, 'o',label='Pozitive_Experiment')
    plt.legend(loc='upper left', shadow=True, fontsize='x-small')
    plt.ylabel('HWHM[T]')
    plt.xlabel('Temperature[K]')

    '''Tau_s от температуры'''
#     plt.figure(3)
#     plt.subplot(1,2,1)
#     plt.title('Tau_s от температуры')
#     # plt.plot(T, HWHM_neg, label='Negative_Theory')
#     plt.plot(T_poz, Tau_s_poz_exp, 'o', label='Pozitive_Experiment')
#     # plt.plot(T, Tau_s_poz, '-', label='Pozitive_Theory')
#     plt.legend(loc='upper left', shadow=True, fontsize='x-small')
#     plt.ylabel('Tau_s[s]')
#     plt.xlabel('Temperature[K]')
#     plt.subplot(1, 2, 2)
#     plt.title('Частоты от температуры')
#     # plt.plot(T, Nu_neg_teor, label='Negative_Theory')
#     plt.plot(T_poz, Nu_poz_ex, 'o', label='Pozitive_Experiment')
#     plt.plot(T, Nu_poz_teor ,'-', label='Negative_Theory')
#     plt.legend(loc='upper left', shadow=True, fontsize='x-small')
#     plt.ylim(1.4e10, 2e10)
#     plt.ylabel('Frequansy[Hz]')
#     plt.xlabel('Temperature[K]')
#
plt.show()

