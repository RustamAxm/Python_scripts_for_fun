import numpy as np
import scipy.stats as sps
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def F(x, a, b, c):
    """Функция синуса"""
    return a * np.sin(b*x) + c

a = -1
b = 5
n = 100
sigma = 0.1
# f = np.sqrt(np.sin(x)) + sigma*du
x = np.linspace(a, b, n)
du = sps.uniform.rvs(loc=a, scale=b, size=n)

y = np.sin(x) + sigma * du
t = np.polyfit(x, y, 3)
f = np.poly1d(t)
index = np.array(f(x)).argmax()

"""часть с фитом по синусу"""
popt, pcov = curve_fit(F, x, y)
A, B, C = popt
print("Параметры синуса A=%g, B=%g, C=%g" % (A, B, C))
y_fitted = F(x, *popt)
index2 = np.array(y_fitted).argmax()
#print(x[index], np.max(f(x)))
errors1 = (y-y_fitted).std()
errors2 = (y-f(x)).std()
print("ошибка синуса = %g, ошибка полинома = %g" %(errors1, errors2))
#Рисуем графики
plt.figure(figsize=(9, 5), dpi=80)
plt.subplot(1, 2, 1)
plt.plot(x, y, 'o', x, f(x), 'b')
plt.ylim(1.25*np.min(y), 1.25*np.max(y))
plt.vlines(x=x[index], ymin=0.0, ymax=np.max(f(x)), linewidth=4, color='r')
plt.title("Аппроксимация полиномами")
plt.ylabel("Значение функций")
plt.xlabel("Аргумент функции")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(x, y, 'o', x, y_fitted, 'b')
plt.ylim(1.25*np.min(y), 1.25*np.max(y))
plt.vlines(x=x[index2], ymin=0.0, ymax=np.max(y_fitted), linewidth=4, color='r')
plt.title("Аппроксимация синусом")
plt.ylabel("Значение функций")
plt.xlabel("Аргумент функции")
plt.grid()
plt.show()