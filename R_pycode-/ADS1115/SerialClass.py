import serial
import io



class SerialClass:
    """
    A class, which allows to connect an equipment to a computer via COM-port.
    usage:
        device = SerialClass('COM3')
    """
    def __init__(self, com):
        """
        Class constructor.

        self.serial = serial.Serial(com, timeout=0.1)
        This creates a Serial object with the parameter com which is a COM-port name and a timeout.
        com - string.
        timeout - float. It is obligatory because without it the program can stuck.

        self.device = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
        This makes the write and read commands more suitable to use.

        """
        self.serial = serial.Serial(com, timeout=0.1)
        self.device = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))

    def query(self, command):
        """
        This method allows to write a command via serial port and read the returned answer.

        :param command: A string contained a command. For example: '*IDN?' - command for SR830 asks for the ID number.
        :return: A string with the response.
        """
        self.device.write(command + '\r')  # A carriage return symbol is necessary for the successful query send.
        self.device.flush()
        return self.device.readline()


if __name__ == '__main__':
    dev = SerialClass('COM18')
    import time
    time.sleep(2)
    for i in range(5):
        print(dev.query('s'))

