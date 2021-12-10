from R_pycode.zIPS120.IPS120_ver2 import MagneticField
import time
import numpy as np
from zIPS120.rs830 import rs830
import traceback

B_start = -1
B_stop = 1

field = np.append(np.linspace(B_start, B_stop, 201), np.linspace(B_stop, B_start, 201))
# field = np.array([0])
print(np.shape(field))

mf = MagneticField()
print('Magnetic field initialized')

rs1 = rs830('COM1')
print('RS initialized')

for b in range(len(field)):
    mf.goto(field[b])
    try:
        time.sleep(0.75)
        Rs_data1 = rs1.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
            # Rs_data2 = rs2.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
            # Real_mag_field = float(ard.query('s')) / 34.5625  # from Hall detector

        dataArray1 = np.array([float(Rs_data1[0]), float(Rs_data1[1]),
                                   float(Rs_data1[2]), float(Rs_data1[3]), float(Rs_data1[4])])
            # dataArray2 = np.array([float(Rs_data2[0]), float(Rs_data2[1]),
            #                        float(Rs_data2[2]), float(Rs_data2[3]), float(Rs_data2[4])])

            # dataArray = np.hstack((field[i], dataArray1, dataArray2))
        dataArray = np.hstack((field[b], dataArray1))
            # print(dataArray)
    except:
        traceback.print_exc()
    if b == 0:
        Res = dataArray
    else:
        Res = np.row_stack(((Res, dataArray)))
    print('magnetic_field = %f' % field[b])
        # print('Real_mag field = ', Real_mag_field)
    print('Result1: \n  Tesla, X: {} , Y: {} , R: {}, Theta: {}, freq {}'.format(*dataArray1))
        # print('Result2: \n  Tesla, X: {} , Y: {} , R: {}, Theta: {}, freq {}'.format(*dataArray2))

np.savetxt('Si_Co_188K_1V_R=0Ohm+-1Tesla.txt', Res, fmt='%10.8f',
           header='Magnetic_field(Tesla)   Ux(V)   Uy(V)   R(V)    Theta   Freq(Hz)', comments='')

print("experiment_DONE")