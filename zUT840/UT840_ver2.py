import serial
import numpy as np
import time


class UT840():
    def __init__(self, com):
        self.arduinoData = serial.Serial(com, 2400, bytesize=7,  timeout=0.2, parity=serial.PARITY_ODD)  # Creating our serial object named arduinoData
        time.sleep(0.5)
        print("UT804 is open")
        self.value = 0
        self.unit = ''
        self.ACDC = ''
        self.main_dict = {
            '1': {'1': [1, 'V'], '2': [2, 'V'], '3': [3, 'V'], '4': [4, 'V']},  # DC Voltage
            '2': {'1': [1, 'V'], '2': [2, 'V'], '3': [3, 'V'], '4': [4, 'V']},  # AC Voltage
            '3': {'0': [3, 'mV']},  # DC mV
            '4': {'1': [3, 'Ohm'], '2': [1, 'kOhm'], '3': [2, 'kOhm'], '4': [3, 'kOhm'], '5': [1, 'MOhm'],
                  '6': [2, 'MOhm']},
            '5': {'1': [2, 'nF'], '2': [3, 'nF'], '3': [1, 'uF'], '4': [2, 'uF'], '5': [3, 'uF'], '6': [1, 'mF'],
                  '7': [2, 'mF']},
            '6': {'0': [4, '°C']},
            '7': {'0': [3, 'uA'], '1': [4, 'uA']},
            '8': {'0': [2, 'mA'], '1': [3, 'mA']},
            '9': {'1': [2, 'A']},
            '10': {'0': [3, 'Ohm, Ring']},
            '11': {'0': [1, 'V, Diod']},
            '13': {'0': [4, '°F']},
            '15': {'0': [3, '% between 4mA and 20mA']}
        }

        self.frequency_dict = {'0': [2, 'Hz'], '1': [3, 'Hz'], '2': [1, 'kHz'], '3': [2, 'kHz'], '4': [3, 'kHz'],
                               '5': [1, 'MHz'], '6': [2, 'MHz'], '7': [3, 'MHz']}
        self.ACDC_dict = {'0': 'DC', '1': ' AC TrueRMS', '3': 'AC+DC TrueRMS'}
        self.sign = {
            '0': ' ',
            '1': ' ',
            '2': ' ',
            '4': '-',
            '5': '-',
            '6': '-'
        }


    def read(self):
            output = []
            # while True:  # One full data read (1)
            while (self.arduinoData.inWaiting() == 0):  # Wait here until there is data
                pass  # do nothing
            answer = self.arduinoData.readline()

            # print(answer)

            # print(len(answer), type(answer))
            output = [str(a & 0xf) for a in answer[0: 9]]
            # print(output, type(output))
            values = output[0:5]
            flags = output[5:9]

            if values[3] == '12':
                self.value = 'OL'
                self.unit = ''
            elif values[1] == '15':
                self.value = 'High'
                self.unit = ''
            elif values[1] == '12':
                self.value = 'Low'
                self.unit = ''
            else:
                if flags[1] != '12':
                    dot_pos, self.unit = self.main_dict[flags[1]][flags[0]]
                    self.value = self.sign[flags[3]] + ''.join(values)[:dot_pos] + '.' + \
                                 ''.join(values)[dot_pos:]
                    self.ACDC = self.ACDC_dict[flags[2]]
                else:
                    if flags[3] != '5':
                        dot_pos, self.unit = self.frequency_dict[flags[0]]
                        self.value = ' ' + ''.join(values)[:dot_pos] + '.' + \
                                     ''.join(values)[dot_pos:]
                    else:
                        dot_pos = 2
                        self.unit = '%'
                        self.value = ' ' + ''.join(values)[:dot_pos] + '.' + \
                                     ''.join(values)[dot_pos:]
            return self.value, self.unit, self.ACDC  # Return of one full data read (1)

    def connect(self):
        self.arduinoData.open()

    def disconnect(self):
        self.arduinoData.close()

if __name__ == "__main__":
    x = UT840('com2')
    # y = UT840('com10')
    x.disconnect()
    # y.disconnect()
    while True:
        x.connect()
        # y.connect()
        data = x.read()[0]
        Real_field = float(x.read()[0]) / 8.9
        # datay = y.read()
        print(data, Real_field, type(str(data)))
        # print(datay, type(str(datay)))
        x.disconnect()
        # y.disconnect()
