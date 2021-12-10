import numpy as np
import time
import traceback
from zIPS120.IPS120_ver2 import MagneticField
from zIPS120.rs830 import rs830



mf = MagneticField()
rs1 = rs830('COM8')
rs2 = rs830('COM15')


field = -np.linspace(-2, 2, 81)
Time = time.time()

for i in range(len(field)):
    try:
        mf.goto(field[i])
        time.sleep(2)

        rs_data1 = rs1.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
        rs_data2 = rs2.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
        data = np.array((field[i],
                         float(rs_data1[0]), float(rs_data1[1]), float(rs_data1[2]), float(rs_data1[3]),
                         float(rs_data2[0]), float(rs_data2[1]), float(rs_data2[2]), float(rs_data2[3]),
                                                                            float(rs_data2[0]) - float(rs_data1[0])))

        print(data)
        # print(dataArray)
    except:
        traceback.print_exc()
    if i == 0:
        Res = data
    else:
        Res = np.row_stack(((Res, data)))
    print('magnetic_field = %f' %field[i])



np.savetxt('HALL CdMnTe 6% объёмный, T=42K, I=180uA, 1.6kHz, time constant 3_0810, через усил и 20к.txt',
           Res, fmt='%12.10f',
           header='Magnetic_field(Tesla)   Ux1(V)   Uy1(V)   R1(V)    Theta1   Ux2(V)   Uy2(V)   R2(V)    Theta2    Hall', comments='')

# data2 = np.array((Res[0][:], Res[10][:], (Res[10][(len(field)-1):0] - Res[10][0:(len(field)-1)])/2,
#                   (Res[10][(len(field)-1):0] + Res[10][0:(len(field)-1)])/2))
# np.savetxt('HALL CdMnTe 6% объёмный, T=140K, I=180uA, 1.6kHz, time constant 3_Process.txt', data2, fmt='%12.10f',
#            header='Magnetic_field(Tesla)    Hall  Anti    Simm   ', comments='')
print("Accumulation time = ", (time.time() - Time) / 60, 'min')
print("experiment_DONE")