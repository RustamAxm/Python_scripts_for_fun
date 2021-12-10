import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq
FFT_sum = np.zeros(501)
Sum_a = np.zeros(1000)
x = np.linspace(0, 100, 1000)
for i in range(0, 1000):
    a = np.cos(x + i)
    FFT_sum = FFT_sum + np.abs(rfft(a))
    Sum_a = Sum_a + a
print(max(a), max(Sum_a))
SUM_a_fft = np.abs(rfft(Sum_a))
plt.figure(1)
plt.subplot(1, 2, 1)
plt.plot(SUM_a_fft)
plt.plot(FFT_sum)
plt.subplot(1, 2, 2)
plt.plot(x, a)
plt.plot(x, Sum_a)
plt.show()