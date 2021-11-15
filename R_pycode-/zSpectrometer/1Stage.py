import zmq
import struct
import traceback
from sockets import TcpReqSocket
import numpy as np
from zSpectrometer.Spectrometer import Spectrometer
from zIPS120.IPS120_ver2 import MagneticField
from zITC503s.ITC503_ver1 import Temperature_Control
import time
# from zUT840.UT840_ver2 import UT840
# x = UT840('com2')
# x.disconnect()


Wavelenght = np.linspace(600, 800, 51)
# print(Wavelenght)
# Wavelenght = np.array([590])

dev = Spectrometer()
dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(Wavelenght[0], 1000)
time.sleep(2)
mf = MagneticField()
print('Magnetic field initialized')
# Temp = Temperature_Control()
# print('Temperature controller initialized')
# Temperature = np.linspace(25, 45, 5)
# field = np.array([0.1])
# field = np.array([6, 5, 4, 3, 2, 1, 0])
# field = np.hstack((np.linspace(0, 1, 4, endpoint=False), np.linspace(1, 2, 3), \
#                    np.linspace(3, 6, 4)))
# field = np.hstack((np.linspace(-0.2, -0.05, 3, endpoint=False), \
#                    np.linspace(-0.05, 0.05, 20, endpoint=False), np.linspace(0.05, 0.2, 4)))
# field = -np.linspace(-6, 6, 13)
# field = np.array([0, 0.05, 0.1, 0.25, 0.5, 0.75, 1])
# field = np.array([1, 0.75, 0.5, 0.25, 0.1, 0.05, 0])
field = np.array([0])
# field = np.array([1.5, 2, 2.5, 3, 4, 5, 6])
# field = np.array([3, 2.5, 2, 1.5])
# field = np.array([6, 5, 4])
print(len(field), field)
adress = '127.0.0.1'
port = 5020
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b'')
adr = 'tcp://{}:{}'.format(adress, port)
accumulations = 5 #in seconds

Time = time.time()

for b in range(len(field)):
    # Temp.goto_temperature(Temperature[b])
    # mf.goto(-0.05)
    # time.sleep(3)
    # mf.goto(field[b])
    # time.sleep(3)
    # mf.goto(0)
    # time.sleep(3)
    # x.connect()
    # Real_field = np.round(float(x.read()[0])/8.9, 3)
    # x.disconnect()
    for i in range(len(Wavelenght)):
        dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(Wavelenght[i], 1000)
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
        data = np.array([Wavelenght[i], float(c1), float(c2), float(pol)])
        print(data)
        if i == 0:
            Res = data
        else:
            Res = np.row_stack(((Res, data)))



    np.savetxt('1-845 {}Tesla_1.5K_8mW_405nm_withoutPOL_slit 1000__accum_5sec_22V.txt'.format(field[b]), Res, fmt='%10.8f',
                   header='Wavelenght(nm)   C1   C2   POL(%)', comments='')

    '''Some point from data'''
    # sig = np.array([field[b], Res[21][2], Res[41][2]])
    # if b == 0:
    #     Res1 = sig
    # else:
    #     Res1 = np.row_stack(((Res1, sig)))

    # print(Res1)
    '''For mag F(magnrtic field)'''
    # data = np.array([field[b], float(c1), float(c2), float(pol)])
    # print(data)
    # if b == 0:
    #     Res = data
    # else:
    #     Res = np.row_stack(((Res, data)))



# np.savetxt('ZnSe Mn0.11_ DD_ex405_8mWPEM_slit1000_SUB_1.5K_det_sigma-_{}nm_Faraday_test.txt'.format(Wavelenght[0]), Res, fmt='%10.8f',
#                header='Magnetic_field(Tesla)     C1   C2   POL(%)', comments='')
# np.savetxt('det820_840nm.txt'.format(field[b]), Res1, fmt='%10.8f',
#                    header='Mag_field(tesla) Int_820  Int_840', comments='')

print((time.time()-Time)/60, "min")
print("Experiment done")

