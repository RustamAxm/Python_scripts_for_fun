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


class Stage(SerialClass):
    def __init__(self, offset=None, com=None, stage_number=None):
        super().__init__(com)
        self.offset = offset
        self.stage_number = stage_number

    def goto(self, pos):
        if self.stage_number == '2':
            k = -1
        else:
            k = 1
        goto_pos = k*(pos + self.offset)
        self.query('{} >NM'.format(goto_pos))
        sleep(0.05)
        print(self.query('?NM'))
        # current_pos = re.findall('\-?[0-9]{1,3}.[0-9]{2}', self.query('?NM'))[0]
        # print('Stage # {} is at {} nm'.format(self.stage_number, current_pos))
        #
        # print(goto_pos)
        # while float(re.findall('[0-9]', self.query('MONO-?DONE'))[0]) == 0:
        #     # current_pos = re.findall('\-?[0-9]{1,3}.[0-9]{2}', self.query('?NM'))[0]
        #     print(self.query('?NM'))
        #     # print('Stage # {} is at {} nm'.format(self.stage_number, self.query('?NM')))


class Spectrometer:
    program_offset = [0.04, -0.32, 0.054]
    # program_offset = [0, 0, 0]

    def __init__(self):
        self.stage = {}
        offset_stage = {}
        cfg = {}
        with open('cfg.txt', 'r') as file:
            for cfg_line in file.readlines():
                cfg_key, cfg_value = cfg_line.split('=')
                cfg[cfg_key] = cfg_value
        print(cfg)
        for i, com in zip(range(1, 4), COM_PORTS):
            self.stage[str(i)] = \
                Stage(offset=float(cfg['stage{}_offset '.format(i)])+self.program_offset[i-1], com=com, stage_number=str(i))

    def goto(self, pos):
        for i in ['1', '2']:
            self.stage[i].goto(pos)
        print('Current position is {} nm'.format(pos))


if __name__ == '__main__':
    spec = Spectrometer()
    i = 0
    for wavelength in wavelengths:
        spec.goto(wavelength)
        c1 = 0
        c2 = 0
        socket.connect(adr)
        for k in range(1):
            print('Accumulation: {}/{}'.format(k + 1, 30))
            Pak = socket.recv()
            s = [c & 127 for c in struct.unpack("xxxxBBBBBBBB", Pak[:12])]
            c1 += s[0] * 2097152 + s[1] * 16384 + s[2] * 128 + s[3]
            c2 += s[4] * 2097152 + s[5] * 16384 + s[6] * 128 + s[7]
        socket.disconnect(adr)
        pol = (c2 - c1) / (c2 + c1) * 100
        data = np.array([wavelength, c1, c2, pol])
        print(data)
        print('Result: \nWavelegth: {} nm, channel 1: {} cps, channel 2: {} cps, polarization: {}'.format(*data))
        if i == 0:
            result = data
        else:
            result = np.column_stack((result, data))
        print(result)
        i += 1
    np.savetxt('D:\PyTest\R_pycode\s.txt', result.transpose(), header='Wavelegth(nm)   C1(Hz)   C2(Hz)   pol(%)', comments='')