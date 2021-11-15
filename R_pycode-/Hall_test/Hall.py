from R_pycode.Hall_test.UT804 import UT804
from SerialClass import SerialClass
from R_pycode.zIPS120.IPS120 import IPS120
import time
import numpy as np
import traceback

dev = UT804()
ard = SerialClass('COM10')
time.sleep(2)
Magnet = IPS120('COM9')

print('Real mag field = ', ard.query('s'))
print('UT_data = ', float(dev.read()[0]))

Set_field = np.linspace(6, -6, 1001)

for i in range(len(Set_field)):
    try:
        Magnet.set_target_field(Set_field[i])
        Magnet.to_set_point()
        time.sleep(2)
        b = Magnet.get_output_field().rstrip().strip('R+?')
        Real_mag_field = float(ard.query('s'))/34.5625 #from Hall detector
        UT_volt = float(dev.read()[0])         #data from UT804
        dataArray = np.array([Set_field[i], Real_mag_field, UT_volt])
        print(dataArray)
    except:
        traceback.print_exc()

    if i == 0:
        Res = dataArray
    else:
        Res = np.row_stack(((Res, dataArray)))

    print('Result: \n  Tesla, Set_field: {} Tesla, Real_mag_field: {} Tesla, UT_volt: {} V'.format(*dataArray))

np.savetxt('Hall_samplA_0mkA_10V_Uxy_.txt', Res, fmt='%10.8f')
print("experiment_DONE")

