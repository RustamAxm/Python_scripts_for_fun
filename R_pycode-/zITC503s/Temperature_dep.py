from zITC503s.ITC503_ver1 import Temperature_Control
from zIPS120.rs830 import rs830
from Hall_test.UT804 import UT804
import numpy as np
import time

ITC = Temperature_Control()
SR1 = rs830("COM8")
SR2 = rs830("COM15")
dev = UT804()
print(ITC.version())
print(ITC.output_temperature())
print(ITC.get_set_temperature())
print(SR1.SNAP(1,  2, 3, 4, 9).rstrip().split(','))
print(SR2.SNAP(1,  2, 3, 4, 9).rstrip().split(','))
T_set = np.linspace(115, 270, 156)
print(T_set)
answer = dev.read()
T_real = np.round(27528.72 * np.exp(-float(answer[0]) / 0.2103) + 0.5687, 2)
print(T_real)
Time = time.time()
#откроем файл
with open("Temp_dep_CdMnTe_6%_180uA_5Tesla_to 180K2.txt", "w") as file:
    file.write("T_set(K) T_real(K) X1(V) Y1(V) R1(V) Theta1(deg) X2(V) Y2(V) R2(V) Theta2(deg)" + '\n')
    file.close()
    T_ITC = float(ITC.output_temperature())
    # ITC.query('T' + str(270))
    # time.sleep(0.5)
    # target_Temp = ITC.get_set_temperature()
    # print(target_Temp)

    for i in range(len(T_set)):
        ITC.goto_temperature(np.round(T_set[i], 2), 4e-2)
        T_ITC = ITC.output_temperature()
        time.sleep(2)
        answer = dev.read()
        T_real = np.round(27528.72 * np.exp(-float(answer[0]) / 0.2103) + 0.5687, 3)  # настоящая темпартура около образца

        rs_data1 = SR1.SNAP(1,  2, 3, 4, 9).rstrip().split(',')
        rs_data2 = SR2.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
        data = np.array((np.round(T_ITC, 2), np.round(T_real, 2),
                         float(rs_data1[0]), float(rs_data1[1]), float(rs_data1[2]), float(rs_data1[3]),
                         float(rs_data2[0]), float(rs_data2[1]), float(rs_data2[2]), float(rs_data2[3])))

        print(data)
        with open("Temp_dep_CdMnTe_6%_180uA_5Tesla_to 180K2.txt", "a") as file:
            for j in range(len(data)):
                file.write(str(data[j]) + ' ')
            file.write("\n")
        file.close()

print("Accumulation time = ", (time.time() - Time) / 60, 'min')
print("Experiment_done")




