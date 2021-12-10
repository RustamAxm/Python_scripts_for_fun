import  scipy
import scipy.fftpack
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

data = np.genfromtxt('Faraday_reflection_4_3K_ex840_to_6Tesla.txt')

indexes, _ = find_peaks(data[1:, 3], distance=10)
print(indexes)
mag_field=data[1:,0]
DTheta=np.zeros(len(indexes))
Theta= np.zeros(len(indexes))
for i in range(len(indexes)-1):
    DTheta[i] = 180/(mag_field[indexes[i]]-mag_field[indexes[i+1]])
    Theta[i] = 180*i
    # Theta[i] = 180 * indexes[i]
np.savetxt('Result_4_3K_ex840.txt',np.column_stack((mag_field[indexes[1:len(indexes)-4]],
                                                              Theta[1:len(indexes)-4])),
           header='Magnetic_field(Tesla)  Theta(grad)', comments='')
plt.figure(1)
plt.subplot(3, 1, 1)
plt.plot(mag_field, data[1:, 3])
plt.plot(mag_field[indexes], data[1:, 3][indexes], "x")
plt.xlim(-3, 3)
plt.title('Faraday_reflection_4.3K_ex840')
plt.subplots_adjust(hspace=0.5)
plt.subplot(3, 1, 2)
plt.plot(mag_field[indexes[1:len(indexes)-4]], DTheta[1:len(indexes)-4], '.')
plt.xlim(-3, 3)
plt.title('D_Theta/D_mag_field[grad/Tesla]')
plt.subplot(3, 1, 3)
plt.plot(mag_field[indexes[1:len(indexes)-4]], Theta[1:len(indexes)-4], '.')
plt.xlim(-3, 3)
plt.title('Theta')
# plt.figure(1)
#
# # plt.subplot(2, 1, 1)
# plt.plot(data[1:,0], data[1:,3], Photon_count)
# plt.grid(b=None, which='major', axis='both')
plt.show()
