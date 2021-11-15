import numpy as np
from SerialClass import SerialClass
import sys
import os
import re
import time


class MagneticField(SerialClass):
    def __init__(self):
        super().__init__('COM4')
        self.query('C3')
        # self.query('J0')
        self.query('A1')

    def goto(self, b_field):
        while True:
            self.query('J'+str(b_field))
            time.sleep(0.1)
            target_field = float(self.get_target_field())
            print('Next field = {} T, IPS target field = {} T'.format(b_field, target_field))
            if np.abs(target_field-b_field) <= 1e-4:
                print('Go to {}T'.format(target_field))
                break
        while True:
            output_field = float(self.get_output_field())
            print('IPS output field = {} T'.format(output_field))
            if np.abs(output_field-target_field) < 1e-6:
                print('Field {} reached'.format(target_field))
                return True

    def get_target_field(self):
        while True:
            answer = self.query('R8')
            if len(answer) == 9 and re.findall('[+\-][0-9].[0-9]{4}', answer[1:8]):
                return answer[1:8]

    def get_output_field(self):
        while True:
            answer = self.query('R7')
            if len(answer) == 9 and re.findall('[+\-][0-9].[0-9]{4}', answer[1:8]):
                return answer[1:8]

    def set_sweep_rate(self, sweep_rate):
        self.query('T' + str(sweep_rate))
        time.sleep(0.1)
        print('Sweep rate is {}'.format(self.query('R9')))

if __name__ == "__main__":
    mf = MagneticField()
    print('Magnetic field initialized')
    # print(mf.get_output_field())
    #  # field = -1 * np.array([-1.0, -0.75, -0.5, -0.3, -0.2, -0.15, -0.1, -0.05, -0.02, 0.0,
     #                       0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0])
    # mf.set_sweep_rate(400)
    field = 0
    mf.goto(field)
    # print(mf.query('R7'))
    # import re
    #
    # def output_temperature2():
    #     while True:
    #         answer = "jsbdkjbvsdk24.56899034bskjbgkjsdbg"
    #         print(answer)
    #         nums = re.findall(r'\d*\.\d+|\d+', answer)
    #         nums = [float(i) for i in nums]
    #         print(nums)
    #         return nums
    #
    # print(output_temperature2())

