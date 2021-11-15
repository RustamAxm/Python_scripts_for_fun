import numpy as np
import time
import traceback
from zIPS120.IPS120 import IPS120
from zUT804.UT804 import UT804

Magnet = IPS120('COM9')
Mult = UT804()

field = np.linspace(-0.2, 0.2, 51)

for i in range(len(field)):
    try:
        Magnet.set_target_field(field[i])
        Magnet.to_set_point()
        time.sleep(4)
        b = Magnet.get_output_field().rstrip().strip('R+?')

        # print(Mult.read()[0])


        dataArray1 = np.array(float(Mult.read()[0]))

        dataArray = np.hstack((field[i], dataArray1))
        # print(dataArray)
    except:
        traceback.print_exc()
    if i == 0:
        Res = dataArray
    else:
        Res = np.row_stack(((Res, dataArray)))
    print('magnetic_field = %f' %field[i])
    print('voltage = %f mV \n' %dataArray1)



Magnet.set_target_field(0)
Magnet.to_set_point()
np.savetxt('hall_detector2.txt', Res, fmt='%12.10f')
print("experiment_DONE")