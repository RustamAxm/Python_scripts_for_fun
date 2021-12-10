import zmq
import struct
import numpy as np
import traceback
from sockets import TcpReqSocket
from SerialClass import SerialClass
from zSpectrometer.Spectrometer import Spectrometer
from PEM_100.PEM_100 import HINDSPEM100control
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

    def get_target_field(self):
        while True:
            answer = self.query('R8')
            if len(answer) == 9 and re.findall('[+\-][0-9].[0-9]{4}', answer[1:8]):
                return answer[1:8]


mf = MagneticField()
wavelengths = np.array([496, 586, 644])
dev = Spectrometer()
pem = HINDSPEM100control('COM9')
print('Magnetic field initialized')
# field = -1*np.array([-1.0, -0.75, -0.5, -0.3, -0.2, -0.15, -0.1, -0.05, -0.02, 0.0,
#                     0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0])
field = np.array([-1.0, -0.8, -0.6, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.6,
                  0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0])
# field = np.arange(2.0, 6.5, 0.5)
# field = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0])
# field = np.array([6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.8, 2.6, 2.4, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0.0])
# field = np.array([0, 0.01])
adress = '127.0.0.1'
port = 5020
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b'')
adr = 'tcp://{}:{}'.format(adress, port)
accumulations = 30 #in seconds

Res = {}
data = {}
Time = time.time()
for i in range(len(field)):
    try:
        if abs(field[i]) < 1e-5:
            fld = 0
        else:
            fld = field[i]

        mf.goto(fld)
        for wl in range(len(wavelengths)):
            dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(wavelengths[wl], 1000)
            pem.setWavelength(wavelengths[wl])
            time.sleep(2)
            socket.connect(adr)
            c1 = 0
            c2 = 0
            for k in range(accumulations):
                print('Accumulation: {}/{}'.format(k + 1, accumulations))
                Pak = socket.recv()
                s = [c & 127 for c in struct.unpack("xxxxBBBBBBBB", Pak[:12])]
                c1 += s[0] * 2097152 + s[1] * 16384 + s[2] * 128 + s[3]
                c2 += s[4] * 2097152 + s[5] * 16384 + s[6] * 128 + s[7]
                print("C1= {}, C2= {}".format(c1, c2))
            socket.disconnect(adr)
            pol = (c2 - c1) / (c2 + c1) * 100
            data[wl] = np.array([fld, float(c1), float(c2), float(pol)])
            print(data)
            if i == 0:
                Res[wl] = data[wl]
            else:
                Res[wl] = np.row_stack(((Res[wl], data[wl])))
            np.savetxt('PL(B)_temp_1.5K_1432_reg{}nm.txt'.format(wavelengths[wl]), Res[wl], fmt='%10.8f',
                       header='Magnetic_field(Tesla)   C1   C2   POL(%)', comments='')
    except:
        traceback.print_exc()

print((time.time()-Time)/60, "min")


print("Experiment done")
