import time
import numpy as np
from zUT840.UT840_ver2 import UT840


x = UT840('com2')
y = UT840('com10')
x.disconnect()
y.disconnect()
with open("Resistance_CdTe 0% P.txt", "w") as file:
    file.write("T_real(K) R(OHm) " + '\n')
    file.close()
    while True:
        with open("Resistance_CdTe 0% P.txt", "a") as file:
            time.sleep(5)
            x.connect()
            y.connect()
            data = x.read()
            answer = y.read()
            T_real = np.round(27528.72 * np.exp(-float(answer[0]) / 0.2103) + 0.5687, 2)
            print("Temperature", T_real, "resistance = ", data[0])
            file.write(str(T_real) + ' ' + data[0] + '\n')
            x.disconnect()
            y.disconnect()
        file.close()
