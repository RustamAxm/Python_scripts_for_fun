import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
#константы
k = 86e-3#
Alfa = 220 # умноженная на N_0 - те обменная константа размерности энергии
Beta = 880 # умноженная на N_0 - те обменная константа размерности энергии
N_0 = 1/0.056 # обратная концентрация катионов в нм^3
print(N_0)
S = 5/2 # спин марганца
g = 2
h = 6.6e-34
x = 0.015 #  концентрация марганца
T = 4
Qw = np.array([4]) #nm
A_1h = np.linspace(2, 20, 10)
A_2h = np.linspace(2, 20, 5)
a_e = np.array([6])
mu = 58e-3
delta_hh = 0# np.linspace(0.00, 2, 10) # расщепление между дырками
data_Int1 = np.zeros((len(A_1h), 4))
data_Int2 = np.zeros(len(A_1h))
data_Bex = np.zeros(len(A_1h))
data_delta_B = np.zeros(len(A_1h))
data_B_ex_A1 = np.zeros(len(A_1h))
data_B_ex_A2 = np.zeros(len(A_1h))
# функции и интегралы
#cos2 = lambda z: (np.cos(np.pi/Qw*z))**2
def Integrate_fun(A_1h, A_2h):
        cos4 = lambda z: (np.cos(np.pi / Qw * z)) ** 4
        # exp1 = lambda r: (1/A_1h**2 * np.exp(-2*r/A_1h) + 1/A_2h**2  * np.exp(-2*r/A_2h))*r
        exp2 = lambda r: 1 / a_e ** 2 * np.exp(-2 * r / a_e) * (
                        1 / A_1h ** 2 * np.exp(-2 * r / A_1h) - 1 / A_2h ** 2 * np.exp(-2 * r / A_2h)) * r
        Phi = lambda r: 1 / A_1h ** 2 * np.exp(-2 * r / A_1h) * r
        exp3 = lambda r: (np.exp(-4 * r / A_1h)) * r
        exp4 = lambda r: (np.exp(-2 * r / A_1h) * np.exp(-2 * r / A_2h)) * r
        exp5 = lambda r: (np.exp(-4 * r / A_2h)) * r
        # Integral_cos2 = integrate.quad(cos2, -Qw/2, Qw/2)
        # Integral_exp1 = integrate.quad(exp1, 0, np.inf)
        Integral_cos4 = integrate.quad(cos4, -Qw / 2, Qw / 2)
        Integral_exp2 = integrate.quad(exp2, 0, np.inf)
        Integral_exp3 = integrate.quad(exp3, 0, np.inf)
        Integral_exp4 = integrate.quad(exp4, 0, np.inf)
        Integral_exp5 = integrate.quad(exp5, 0, np.inf)
        VOL1 = 1 / (Integral_exp3[0] * (4 / (np.pi * Qw * A_1h ** 2)) ** 2 * Integral_cos4[0])
        VOL2 = 1 / (Integral_exp5[0] * (4 / (np.pi * Qw * A_2h ** 2)) ** 2 * Integral_cos4[0])
        # radius = np.sqrt(VOL / (np.pi * Qw))
        # print(VOL, radius)
        print(Integral_cos4, Integral_exp2, Integral_exp3, Integral_exp4, Integral_exp5)
        '''до сюда ок'''
        Int_1 = (32 / (np.pi * Qw ** 2 * A_1h ** 4)) * Integral_cos4[0] * Integral_exp3[0] \
                - 2 * np.pi * (4 / (np.pi * Qw * A_1h ** 2)) * (4 / (np.pi * Qw * A_2h ** 2)) * Integral_cos4[0] * \
                Integral_exp4[0] \
                + (32 / (np.pi * Qw ** 2 * A_2h ** 4)) * Integral_cos4[0] * Integral_exp5[0]

        Int_2 = 32 / (np.pi * Qw ** 2) * Integral_cos4[0] * Integral_exp2[0]

        return Int_1, Int_2, VOL1, VOL2

def Brill(x, T):
    const = (5.0 * 58.0) / (86.0 * (T))
    return 1.2/np.tanh(1.2*const*x)-0.2/np.tanh(0.2*const*x)

for j in range(len(A_2h)):
        for i in range(len(A_1h)):
                data_Int1[i] = Integrate_fun(A_1h[i], A_2h[j])

        print("data_Int ", np.shape(data_Int1))
        # расчет обменного поля
        Const_1 = Alfa/N_0*Beta*x*S*(S+1)/(6*k*T)
        Const_2 = Beta**2 /N_0 * x * S*(S+1)/(6*k*T)
        print(Const_1, Const_2)
        #B_ex = Const_1 * np.sqrt((Const_2 * Int_1)**2 - 4*delta_hh**2) / (Const_2 * Int_1) * Int_2
        B_ex2 = Alfa/Beta * np.sqrt((Const_2 * data_Int1[:, 0])**2 - 4*delta_hh**2) / (data_Int1[:, 0]) * data_Int1[:, 1]
        # B_ex2 = Const_1 * data_Int1[:, 1]
        B_ex_A1 = Beta / N_0 * 3 / 2 / (3 * mu * 2 * data_Int1[:, 2])
        B_ex_A2 = Beta / N_0 * 3 / 2 / (3 * mu * 2 * data_Int1[:, 3])
        delta_B = abs(B_ex_A2 - B_ex_A1)

        if j == 0:
                data_Bex = B_ex2
                data_delta_B = delta_B
                data_B_ex_A1 = B_ex_A1
                data_B_ex_A2 = B_ex_A2
        else:
                data_Bex = np.column_stack((data_Bex, B_ex2))
                data_delta_B = np.column_stack((data_delta_B, delta_B))
                data_B_ex_A1 = np.column_stack((data_B_ex_A1, B_ex_A1))
                data_B_ex_A2 = np.column_stack((data_B_ex_A2, B_ex_A2))

print(data_Bex)
np.savetxt("data_from_Kavokin_function.txt", np.column_stack((A_1h, data_Bex)),fmt='%10.8f',
                header='Radius_hole(nm)     E_for{}_(meV)]'.format(A_2h), comments='' )
B_field = np.linspace(0.001, 1, 20)
E_e = Alfa*x*5/2 *Brill(B_field, T)
plt.figure(1)
plt.subplot(1, 2, 1)
plt.title("Exchange field_Kavokin")
for i in range(len(A_2h)):
        plt.plot(A_1h, data_Bex[:, i], label= np.transpose(A_2h[i]) )
plt.legend(loc='upper right', shadow=True)
plt.ylabel('meV')
plt.xlabel('Hole_radius(nm)')
plt.subplot(1, 2, 2)
plt.title("electron energy")
plt.plot(B_field, E_e)
plt.ylabel('meV')
plt.xlabel('Magnetic_field[T]')
plt.figure(2)
plt.title("delta_B_simple")
plt.plot(A_1h, data_delta_B)
plt.ylabel('Exchange_field(Tesla)')
plt.xlabel('Hole_radius(nm)')
plt.figure(3)
plt.title("Exchane field for one hole")
plt.plot(A_1h, data_B_ex_A1)
plt.figure(4)
plt.plot(A_2h, np.transpose(data_B_ex_A2))


plt.show()
