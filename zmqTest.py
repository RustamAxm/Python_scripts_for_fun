import zmq
import struct
from zSpectrometer.Spectrometer import Spectrometer
import numpy as np
from time import sleep
from sockets import TcpReqSocket

file = r'test_for_D.txt'
adress = '127.0.0.1'
port = 5020
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b'')
adr = 'tcp://{}:{}'.format(adress, port)
spec = Spectrometer()
magnet = TcpReqSocket(("127.0.0.1", 6006), timeout=2)
# wavelength = np.linspace(515, 550, 36)
wavelength = np.linspace(520, 550, 11)
accumulations = 120
"""
wavelength
"""
# for i in wavelength:
#     spec.goto(i)
#     print('Spectrometer position {:0.3f}'.format(i))
#     c1 = 0
#     c2 = 0
#     socket.connect(adr)
#     for k in range(accumulations):
#         print('Accumulation: {}/{}'.format(k+1, accumulations))
#         Pak = socket.recv()
#         if len(Pak) >= 12:
#             s = [c & 127 for c in struct.unpack("xxxxBBBBBBBB", Pak[:12])]
#             c1 += s[0] * 2097152 + s[1] * 16384 + s[2] * 128 + s[3]
#             c2 += s[4] * 2097152 + s[5] * 16384 + s[6] * 128 + s[7]
#     socket.disconnect(adr)
#     pol = (c2 - c1) / (c2 + c1) * 100
#     data = ['{:0.3f}'.format(i), '{}'.format(c1), '{}'.format(c2), '{:0.2f}'.format(pol)]
#     print('Result: \nWavelength: {} nm, channel 1: {} cps, channel 2: {} cps, polarization: {}'.format(*data))
#     with open(file, 'a+') as f:
#         f.write('\t'.join(data) + '\n')
"""
magnetic field
"""
field = [0., 0.0010, 0.0020]#np.linspace(0, 0.01, 6)
for fld in field:
    print('Field set= {:0.4f}'.format(fld))
    print(type(fld))
    magnet.ask('setField %f' % float(fld))

    c1 = 0
    c2 = 0
    sleep(3)
    b = magnet.ask("getField")
    print('Field read = {}'.format(b))
    socket.connect(adr)
    for k in range(1):
        print('Accumulation: {}/{}'.format(k+1, 30))
        Pak = socket.recv()
        s = [c & 127 for c in struct.unpack("xxxxBBBBBBBB", Pak[:12])]
        c1 += s[0] * 2097152 + s[1] * 16384 + s[2] * 128 + s[3]
        c2 += s[4] * 2097152 + s[5] * 16384 + s[6] * 128 + s[7]
    socket.disconnect(adr)
    pol = (c2 - c1) / (c2 + c1) * 100
    data = ['{}'.format(b), '{}'.format(c1), '{}'.format(c2), '{:0.2f}'.format(pol)]
    print('Result: \nMagnetic field: {} Tesla, channel 1: {} cps, channel 2: {} cps, polarization: {}'.format(*data))
    with open(file, 'a+') as f:
        f.write('\t'.join(data) + '\n')
print('Done!')
