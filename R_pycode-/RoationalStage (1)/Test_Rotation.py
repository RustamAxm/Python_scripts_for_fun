from zIPS120.IPS120_ver2 import MagneticField
from zSpectrometer import CCD
import RoationalStage.RotationStage
import numpy as np
import time

"""CCD settings"""
accum_time = 5000  # msec
number_of_frames = 10
Lambda_start = 802.041
Lambda_end = 813.825
ccd = CCD.CCD(accum_time, number_of_frames, Lambda_start, Lambda_end)
data_s1 = np.zeros((1340,))
data_s2 = np.zeros((1340,))
print('CCD initialized')

"""Magnet"""
mf = MagneticField()
# magnetic_fields = -1*np.array([6, 5, 4, 3, 2, 1.5, 1, 0.75, 0.5, 0.4, 0.3, 0.2, 0.1, 0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.75,  -1, -1.5, -2, -3, -4, -5, -6])
magnetic_fields = np.flipud(np.array([0, 1, 2, 3, 4, 5, 6]))
# magnetic_fields = np.array([0, 1, 2, 3, 4, 5, 6])
# magnetic_fields = np.array([0])
print(magnetic_fields)
# magnetic_fields = np.arange(-0.5, 0.5, 0.05)
# magnetic_fields = np.array([0])
print('Magnetic field initialized')

"""RotationStage"""
rs = RoationalStage.RotationStage.RotationStage() # это решает проблему с модулем импорта
number_of_steps = 1 #количество итераций вращения
print('Rotational stage initialized')

Time = time.time()
for i in range(len(magnetic_fields)):
    mf.goto(magnetic_fields[i])
    for step in range(number_of_steps):
        # rs.move_Rotation_Togever(0, 7200)  # сигма+ условно
        rs.Sigma_1()
        print('Measuring s1 polarization')
        ccd.start()
        data_s1 += ccd.data_y
        ccd.data_y = None
        print('s1 polarization has been measured')

        # rs.move_Rotation_Togever(7200, 0)  # сигма минус условно
        rs.Sigma_2()
        print('Measuring s2 polarization')
        ccd.start()
        data_s2 += ccd.data_y
        ccd.data_y = None
        print('s1 polarization has been measured')
    data_s1 -= 90*number_of_frames
    data_s2 -= 90*number_of_frames
    np.savetxt(r'MN_0.001_POlaron_s1_1.5K_ex795.6_1.5mW_{}T_{}msec-{}frames-{}turns_slit200.txt'.format(magnetic_fields[i], accum_time, number_of_frames,
                                                               number_of_steps), np.column_stack((ccd.data_x, data_s1)))
    np.savetxt(r'MN_0.001_POlaron_s2_1.5K_ex795.6_1.5mW_{}T_{}msec-{}frames-{}turns_slit200.txt'.format(magnetic_fields[i], accum_time, number_of_frames,
                                                                number_of_steps),np.column_stack((ccd.data_x, data_s2)))
    pol = (data_s1 - data_s2) / (data_s1 + data_s2)
    np.savetxt(r'MN_0.001_POlaron_pol_1.5K_795.6_1.5mW_{}T_{}msec-{}frames-{}turns_slit200.txt'.format(magnetic_fields[i], accum_time, number_of_frames,
                                                                 number_of_steps), np.column_stack((ccd.data_x, pol)))


    print('data saved!')
    data_s1 = np.zeros((1340,))
    data_s2 = np.zeros((1340,))


print((time.time() - Time)/60, "min")
print("experiment DONE")

