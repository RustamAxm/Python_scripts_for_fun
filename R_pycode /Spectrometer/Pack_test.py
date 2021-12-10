from SerialClass import SerialClass
import pyqtgraph as pg
import numpy as np
import re
from time import sleep
import zmq
import struct

COM_PORTS = ['COM5', 'COM6', 'COM7']
adress = '127.0.0.1'
port = 5020
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b'')
adr = 'tcp://{}:{}'.format(adress, port)
wavelengths = np.linspace(702, 704, 30)
accumulations = 120





if __name__ == '__main__':
    i = 0
    for j in range(110):
        c1 = 0
        c2 = 0
        socket.connect(adr)
        print(j)
        for k in range(1):
            print('Accumulation: {}/{}'.format(k + 1, 30))
            Pak = socket.recv()
            s = [c & 127 for c in struct.unpack("xxxxBBBBBBBB", Pak[:12])]
            c1 += s[0] * 2097152 + s[1] * 16384 + s[2] * 128 + s[3]
            c2 += s[4] * 2097152 + s[5] * 16384 + s[6] * 128 + s[7]
        socket.disconnect(adr)
        pol = (c2 - c1) / (c2 + c1) * 100
        data = np.array([c1, c2, pol])
        print(data)
        print('Result: \n channel 1: {} cps, channel 2: {} cps, polarization: {}'.format(*data))
        if i == 0:
            result = data
        else:
            result = np.column_stack((result, data))
        # print(result)
        i += 1
        sleep(1)
    np.savetxt('D:\PyTest\R_pycode\s.txt', result.transpose(), header='C1(Hz)   C2(Hz)   pol(%)', comments='')