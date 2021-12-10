import numpy as np
from SerialClass import SerialClass
import time
import traceback
from R_pycode.zIPS120.IPS120 import IPS120
from zIPS120.rs830 import rs830

Magnet = IPS120('COM9')
rs1 = rs830('COM1')
# ard = SerialClass('COM10')
# rs2 = rs830('COM3')


field = np.linspace(0, 0.5, 51),

for i in range(len(field)):
    try:
        Magnet.set_target_field(field[i])
        Magnet.to_set_point()
        time.sleep(1.75)
        b = Magnet.get_output_field().rstrip().strip('R+?')
        Rs_data1 = rs1.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
        # Rs_data2 = rs2.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
        # Real_mag_field = float(ard.query('s')) / 34.5625  # from Hall detector

        dataArray1 = np.array([float(Rs_data1[0]), float(Rs_data1[1]),
                          float(Rs_data1[2]), float(Rs_data1[3]), float(Rs_data1[4])])
        # dataArray2 = np.array([float(Rs_data2[0]), float(Rs_data2[1]),
        #                        float(Rs_data2[2]), float(Rs_data2[3]), float(Rs_data2[4])])

        # dataArray = np.hstack((field[i], dataArray1, dataArray2))
        dataArray = np.hstack((field[i], dataArray1))
        # print(dataArray)
    except:
        traceback.print_exc()
    if i == 0:
        Res = dataArray
    else:
        Res = np.row_stack(((Res, dataArray)))
    print('magnetic_field = %f' %field[i])
    # print('Real_mag field = ', Real_mag_field)
    print('Result1: \n  Tesla, X: {} , Y: {} , R: {}, Theta: {}, freq {}'.format(*dataArray1))
    # print('Result2: \n  Tesla, X: {} , Y: {} , R: {}, Theta: {}, freq {}'.format(*dataArray2))

# Magnet.set_target_field(0)
# Magnet.to_set_point()
np.savetxt('Si_Co.txt', Res, fmt='%10.8f',
           header='Magnetic_field(Tesla)   Ux(V)   Uy(V)   R(V)    Theta   Freq(Hz)', comments='')
print("experiment_DONE")