import numpy as np
from SerialClass import SerialClass
import sys
import os
import re
import time

class Temperature_Control(SerialClass):
    def __init__(self):
        super().__init__('COM3')
        self.query('C3')
        # # self.query('J0')
        # self.query('A1')


    def version(self):
        return self.query('V')

    def output_temperature(self):
        while True:
            answer = self.query('R1')
            if len(answer) == 8:
                return float(" ".join(re.findall(r'\d*\.\d+|\d+', answer)))

    def get_set_temperature(self):
        while True:
            answer = self.query('R0')
            if len(answer) == 8:
                return float(" ".join(re.findall(r'\d*\.\d+|\d+', answer)))

    def output_temperature2(self):
        while True:
            answer = self.query('R1')
            if len(answer) == 8:
                return float(" ".join(re.findall(r'\d*\.\d+|\d+', answer)))


    def goto_temperature(self, b_field, accuracy=1e-2):
        while True:
            self.query('T'+str(b_field))
            time.sleep(0.5)
            target_Temp = self.get_set_temperature()
            print('Next Temp = {} K, ITC output Temp = {} K'.format(b_field, target_Temp))
            if np.abs(target_Temp-b_field) <= 1e-3:
                print('Go to {}K'.format(target_Temp))
                break
        while True:
            time.sleep(1)
            output_field = self.output_temperature()
            print('ITC output Temp = {} K'.format(output_field))
            if np.abs(output_field-target_Temp) <= accuracy:
                print('Temperature {} reached'.format(target_Temp))
                return True



if __name__ == "__main__":
    x = Temperature_Control()
    print('Temperature controller initialized')
     # field = -1 * np.array([-1.0, -0.75, -0.5, -0.3, -0.2, -0.15, -0.1, -0.05, -0.02, 0.0,
     #                       0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0])
    # mf.set_sweep_rate(200)
    print(x.version())
    for i in range(1):
        print(x.output_temperature2())
        time.sleep(0.1)

    print(x.get_set_temperature())
    # print(x.output_temperature2())
    print(x.get_set_temperature())
    x.goto_temperature(164.3, 4e-2)
    # import numpy as np
    # a = np.array(([1, 2, 3, 4], [2, 4, 5, 6]))
    # print(a)
    # print(np.flip(a[0][:], 0))
