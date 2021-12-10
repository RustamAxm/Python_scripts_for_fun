import serial
import io

class HINDSPEM100control:
    def __init__(self, com):
        # all serial parameters are fixed since they are not chanagble in the controller
        # no handshake, 8N1, no nullmodem cable

        self.serial = serial.Serial(com, baudrate=2400, timeout=0.2)
        self.device = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
        if self.serial.isOpen():
            print('connection to HINDS PEM100 established')

    def query(self, command):
        """
        This method allows to write a command via serial port and read the returned answer.

        :param command: A string contained a command. For example: '*IDN?' - command for SR830 asks for the ID number.
        :return: A string with the response.
        """
        self.device.write(command + '\r')  # A carriage return symbol is necessary for the successful query send.
        self.device.flush()
        return self.device.readline()

    def setWavelength(self, wavelength):
        if wavelength < 0 or wavelength >= 20000:
            print('wavelength out of range')
        else:
            cmd = 'W:{:07.1f}'.format(wavelength)  # needs zero padded 6 digits fixed
            print(cmd)
            return self.query(cmd[:7]+cmd[8:]) # without ythe period

    def  Wavelength(self):
        return self.query("W")

    def setRetardation(self, retardation):
        """
        set retardation in waveunits. 1000 is one lambda, 250 is a quarter lambda
        """
        if retardation < 0 or retardation > 1000:
            print('retardation out of range 0 > ret > 1000')
        else:
            cmd = 'R:{:04.0f}'.format(retardation)  # needs zero padding
            return self.query(cmd)

if __name__ == '__main__':
    '''Сначала на самом блоке управления нужно перейти в режим Remote control'''
    pem = HINDSPEM100control("COM9")
    print(pem.setWavelength(750))
    print(pem.setRetardation(250))