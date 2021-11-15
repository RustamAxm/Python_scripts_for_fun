import serial
import io
import time


class SerialClass:
    """
    A class, which allows to connect an equipment to a computer via COM-port.
    usage:
        device = SerialClass('COM3')
    """
    def __init__(self, port):
        """
        Class constructor.

        self.serial = serial.Serial(com, timeout=0.1)
        This creates a Serial object with the parameter com which is a COM-port name and a timeout.
        com - string.
        timeout - float. It is obligatory because without it the program can stuck.

        self.device = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
        This makes the write and read commands more suitable to use.

        """
        self.ser = serial.Serial(port=port,
                                 baudrate=9600,
                                 timeout=0.1)
        self.ser_io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser),
                                       newline='\r',
                                       line_buffering=True)

    def query(self, command):
        """
        This method allows to write a command via serial port and read the returned answer.

        :param command: A string contained a command. For example: '*IDN?' - command for SR830 asks for the ID number.
        :return: A string with the response.
        """
        self.ser_io.write(command+'\r')
        return self.ser_io.readline()


if __name__ == '__main__':
    for i in range(1, 17):
        st1 = SerialClass('COM{}'.format(i))
        print('COM', i, st1.query('*IDN?'))
    # print(st2.query('MONO-STOP'))
    # print(st3.query('MONO-STOP'))
    # print(st2.query('?NM'))
    # print(st3.query('?NM'))