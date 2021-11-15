import numpy as np
import time
import traceback
from R_pycode.zIPS120.IPS120 import IPS120
from R_pycode.zIPS120.rs830 import rs830

Magnet = IPS120('COM9')
rs1 = rs830('COM3')
#rs2 = rs830('COM6')
Start = time.time()
field = np.linspace(6, -6, 6001)

for i in range(len(field)):
    try:
        Magnet.set_target_field(field[i])
        Magnet.to_set_point()
        # time.sleep(0.15)
        print("realtime Magneticfield = ", Magnet.get_output_field().rstrip().strip('R+?'))
        Rs_data1 = rs1.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
        #Rs_data2 = rs2.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
        # print(Rs_data1)
        # print(Rs_data2)
        dataArray1 = np.array([float(Rs_data1[0]), float(Rs_data1[1]),
                               float(Rs_data1[2]), float(Rs_data1[3]), float(Rs_data1[4])])
        #dataArray2 = np.array([float(Rs_data2[0]), float(Rs_data2[1]),
                               #float(Rs_data2[2]), float(Rs_data2[3]), float(Rs_data2[4])])
        #dataArray = np.hstack((field[i], dataArray1, dataArray2))
        dataArray = np.hstack((field[i], dataArray1))
        # print(dataArray)
    except:
        traceback.print_exc()
    if i == 0:
        Res = dataArray
    else:
        Res = np.row_stack(((Res, dataArray)))
    print('magnetic_field = %f' %field[i])
    print('Result1: \n  Tesla, X: {} , Y: {} , R: {}, Theta: {}, freq {}'.format(*dataArray1))
    #print('Result2: \n  Tesla, X: {} , Y: {} , R: {}, Theta: {}, freq {}'.format(*dataArray2))


# Magnet.set_target_field(-4)
# Magnet.to_set_point()
np.savetxt('Faraday_reflection_1_5K_ex790_to_6Tesla_1.txt', Res, fmt='%12.10f',
           header='Magnetic_field(Tesla)   Ux(V)   Uy(V)   R(V)    Theta   Freq(Hz)', comments='')
print("experiment_DONE")
print(abs(Start-time.time())/60, "min")