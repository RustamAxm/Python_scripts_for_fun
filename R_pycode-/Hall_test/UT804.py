import usb.core
import usb.util


class UT804:
    idVendor = 0x1A86
    idProduct = 0xE008

    def __init__(self):
        self.device = usb.core.find(idVendor=UT804.idVendor, idProduct=UT804.idProduct)
        if self.device is None:
            print('Device not found!')
            exit()
        self.ep = self.device[0][0, 0][0]
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
        try:
            output = []
            while True:  # One full data read (1)
                answer = self.ep.read(self.ep.wMaxPacketSize, timeout=100)
                if answer[0] == 241:
                    output.append(str(answer[1] & 0xf))
                    if answer[1] == 138 and len(output) != 11:
                        output = []
                    if answer[1] == 138 and len(output) == 11:
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
        except usb.core.USBError:
            return None, None, 'Run the UNIT generic program first!'


if __name__ == '__main__':
    dev = UT804()
    print(dev.read())
    print(usb.util.release_interface(dev.device, dev.device[0][0, 0]))
    print(float(dev.read()[0]))


