from SerialClass import SerialClass
import time
"""
Communication Commands:
C0: Local & Locked
C1: Remote & Locked
C2: Local & Unlocked
C3: Remote & Unlocked

Read Parameter:
R7: Output Field 
R8: Target Field
R9: Sweep Rate

Control Commands:
A0: Hold
A1: To Set Point
A2: To Zero

J%number%: Set Target Field
T%number%: Set Field Sweep Rate
"""


class IPS120(SerialClass):
    """
    This class allows to use the IPS120 equipment. Contains the methods which allows to control one.
    Usage:
        magnet = IPS120('COM9')
    """
    def __init__(self, com):
        super().__init__(com)
        self.query('C3')    # Switches IPS120 to the Remote & Unlock mode.

    def get_target_field(self):
        return self.query('R8')

    def get_output_field(self):
        return self.query('R7')

    def get_sweep_rate(self):
        return self.query('R9')

    def hold(self):
        self.query('A0')

    def to_set_point(self):
        self.query('A1')

    def to_zero(self):
        self.query('A2')

    def set_target_field(self, field):
        self.query('J' + str(field))

    def set_sweep_rate(self, sweep_rate):
        self.query('T' + str(sweep_rate))

# From Romas Experiments
if __name__ == "__main__":
    magnet = IPS120('COM9')
    print(magnet.get_target_field())
    print(magnet.get_sweep_rate())
    print(magnet.get_output_field())
    print(magnet.set_target_field(0))
    magnet.to_set_point()

    while float(magnet.get_output_field().rstrip().strip('R+?')) != float(magnet.get_target_field().rstrip().strip('R+?')):
        time.sleep(2)
        print("realtime Magneticfield = ", magnet.get_output_field().rstrip().strip('R?'))

    time.sleep(2)
    print(magnet.get_output_field())
