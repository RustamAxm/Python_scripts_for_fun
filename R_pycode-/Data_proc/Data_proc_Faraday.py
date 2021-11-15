import scipy
import peakutils
import matplotlib.pyplot as plt
import numpy as np
from peakutils.plot import plot as pplot

data = np.genfromtxt('Faraday_reflection_1_5K_ex820_to_6Tesla.txt')
print(max(data[1:,3]))
indexes = peakutils.indexes(data[1:,3],thres=0.7,min_dist=4)
print(indexes)
mag_field=data[1:,0]
DTheta=np.zeros(len(indexes))
Theta= np.zeros(len(indexes))
for i in range(len(indexes)-1):
    DTheta[i] = 180/(mag_field[indexes[i]]-mag_field[indexes[i+1]])
    Theta[i] = 180*i
    # Theta[i] = 180 * indexes[i]
np.savetxt('Result_1_5K_ex820.txt',np.column_stack((mag_field[indexes[1:len(indexes)-4]],
                                                              Theta[1:len(indexes)-4],DTheta[1:len(indexes)-4])))
plt.figure(1)
plt.subplot(3, 1, 1)
pplot(data[1:,0], data[1:,3], indexes)
plt.xlim(-3, 3)
plt.title('Faraday_reflection_1_5K_ex820_to_6Tesla')
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