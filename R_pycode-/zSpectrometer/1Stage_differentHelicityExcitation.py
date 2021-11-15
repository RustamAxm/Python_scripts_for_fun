import zmq
import struct
import traceback
from sockets import TcpReqSocket
import numpy as np
from zSpectrometer.Spectrometer import Spectrometer
from zIPS120.IPS120_ver2 import MagneticField
from zITC503s.ITC503_ver1 import Temperature_Control
import time
from PEM_100.PEM_100 import HINDSPEM100control
from ctypes import *
import sys
import os

cur_dir = os.path.abspath(os.path.dirname(__file__))
ximc_dir = os.path.join(cur_dir, "ximc")
ximc_package_dir = os.path.join(ximc_dir, "crossplatform", "wrappers", "python")
sys.path.append(ximc_package_dir)  # add ximc.py wrapper to python path

if sys.platform in ("win32", "win64"):
    libdir = os.path.join(ximc_dir, sys.platform)
    os.environ["Path"] = libdir + ";" + os.environ["Path"]  # add dll

from pyximc import *

class RotationalStage:
    def __init__(self):
        self.lib = WinDLL(r'C:\D\PyTest\ximc\win32\libximc.dll')
        self.lib.set_bindy_key(os.path.join(ximc_dir, "win32", "keyfile.sqlite").encode("utf-8"))
        probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
        enum_hints = b"addr=192.168.0.1,172.16.2.3"
        devenum = self.lib.enumerate_devices(probe_flags, enum_hints)
        open_name = self.lib.get_device_name(devenum, 0)
        self.device_id = self.lib.open_device(open_name)

    def move(self, distance):
        print("\nGoing to {0} steps".format(distance))
        self.lib.command_move(self.device_id, distance, 0)
        errcnt = 0
        while True:
            position = self.get_position()
            if position == distance:
                return True
            errcnt += 1
            if np.abs(position - distance) < 2:
                errcnt += 100
            if errcnt > 10000:
                print('Step motor did not reach the {} position, returned at {} instead.'.format(distance, position))
                return True

    def get_position(self):
        x_pos = get_position_t()
        self.lib.get_position(self.device_id, byref(x_pos))
        return x_pos.Position


# Wavelenght = np.append(np.arange(458.5, 475, 0.5), np.arange(476, 602, 2)) #574 778
# Wavelenght = np.arange(458.35, 459, 0.01)
Wavelenght = np.array([632])

dev = Spectrometer()
dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(Wavelenght[0], 1000)
pem = HINDSPEM100control('COM9')
pem.setRetardation(250)
rs = RotationalStage()
time.sleep(2)
# mf = MagneticField()
print('Magnetic field initialized')
# Temp = Temperature_Control()
# print('Temperature controller initialized')
# Temperature = np.linspace(25, 45, 5)
field = np.array([0])
# field = np.array([6, 5, 4, 3, 2, 1, 0])
# field = np.hstack((np.linspace(-1, -0.5, 3, endpoint=False), np.linspace(-0.5, -0.05, 6, endpoint=False), \
#                    np.linspace(-0.05, 0.05, 10, endpoint=False), np.linspace(0.05, 0.5, 6, endpoint=False), np.linspace(0.5, 1, 4)))
# field = np.hstack((np.linspace(-0.2, -0.05, 3, endpoint=False), \
#                    np.linspace(-0.05, 0.05, 20, endpoint=False), np.linspace(0.05, 0.2, 4)))
# field = np.linspace(0.0, 0.1, 2)
# field = np.array([3, 4])
# field = np.zeros(100)
# field = [2]
print(field)
adress = '127.0.0.1'
port = 5020
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b'')
adr = 'tcp://{}:{}'.format(adress, port)
accumulations = 5 #in seconds

Time = time.time()
data = {}
Res = {}
for b in range(len(field)):
    # Temp.goto_temperature(Temperature[b])
    # mf.goto(-0.05)
    # time.sleep(3)
    # mf.goto(field[b])
    # time.sleep(3)
    # mf.goto(0)
    # time.sleep(3)
    for i in range(len(Wavelenght)):
        for exc in ['lin', 'circ']:
            if exc is 'lin':
                rs.move(57000)
            if exc is 'circ':
                rs.move(60600)
            dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(Wavelenght[i], 1000)
            pem.setWavelength(Wavelenght[i])
            # time.sleep(0.75)
            c1 = 0
            c2 = 0
            socket.connect(adr)
            for k in range(accumulations):
                print('Accumulation: {}/{}'.format(k + 1, accumulations))
                Pak = socket.recv()
                s = [c & 127 for c in struct.unpack("xxxxBBBBBBBB", Pak[:12])]
                c1 += s[0] * 2097152 + s[1] * 16384 + s[2] * 128 + s[3]
                c2 += s[4] * 2097152 + s[5] * 16384 + s[6] * 128 + s[7]
                # print("C1= {}, C2= {}".format(c1, c2))
            socket.disconnect(adr)
            pol = (c2 - c1) / (c2 + c1) * 100
            '''for F(Wavelenght)'''
            data[exc] = np.array([Wavelenght[i], float(c1), float(c2), float(pol)])
            print(data)
            if i == 0:
                Res[exc] = data[exc]
            else:
                Res[exc] = np.row_stack(((Res[exc], data[exc])))


            np.savetxt('superfine1-666, 1.5K,{}T_457.8nm exc_{}.txt'.format(field[b], exc), Res[exc], fmt='%10.8f',
                       header='Wavelenght(nm)   C1   C2   POL(%)', comments='')

    '''Some point from data'''
    # sig = np.array([field[b], Res[21][2], Res[41][2]])
    # if b == 0:
    #     Res1 = sig
    # else:
    #     Res1 = np.row_stack(((Res1, sig)))

    # print(Res1)
    '''For mag F(magnrtic field)'''
#     data = np.array([field[b], float(c1), float(c2), float(pol)])
#     print(data)
#     if b == 0:
#         Res = data
#     else:
#         Res = np.row_stack(((Res, data)))
#
#
#
# np.savetxt('Transverse field_ex790_10mWPEM_slit1000_1000_SUB_1.5K_det_sigma+_{}nm_2.txt'.format(Wavelenght[0]), Res, fmt='%10.8f',
#                header='Magnetic_field(Tesla)     C1   C2   POL(%)', comments='')
# np.savetxt('det820_840nm.txt'.format(field[b]), Res1, fmt='%10.8f',
#                    header='Mag_field(tesla) Int_820  Int_840', comments='')

print((time.time()-Time)/60, "min")
print("Experiment done")

