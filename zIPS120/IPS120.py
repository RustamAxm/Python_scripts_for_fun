# TODO: 1) SOLVED! By adding a WHILE loop to methods where the values of magnetic field and status were being queried.
# TODO: This WHILE loop is checking the length of the response from the IPS120 and the match of it
# TODO: to the certain pattern.
# TODO: 1) sometimes responds from the IPS120 mixes assignments of the magnetic field ans status values with each
# TODO: others: like output_field = self.ips120.query_status() or status = self.ips120.get_output_field().
# TODO: Especially this happens when the regime is changed from clamped to hold right after the ips120 power supply
# TODO: is switched on and the program is used.

# TODO: 2) Add a traceback and a possibility to record a log file. Because even there was no errors during the run
# TODO: of the application, there was an error after the exact moment when the program was turned off by closing it.
# TODO: This error can be connected with troubles of finishing the thread.

# TODO: 3) Add ZMQ

# TODO: 4) Sometimes if the IPS120 power supply was released from clamped mode and heater was turned on before this
# TODO: program was started, the program will freeze for good.

from SerialClass import SerialClass
from IPS120ui import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
import zmq
import sys
import re
import traceback
from contextlib import contextmanager

COM = 'COM9'
ZMQ_PORT_PUB = '6001'
ZMQ_PORT_SUB = '6000'
TOPIC_FILTER = 'IPS120'
SYSTEM_STATUS_1 = {'0': 'Normal', '1': 'Quench', '2': 'Over Heated', '4': 'Warming up', '8': 'Fault'}
SYSTEM_STATUS_2 = {'0': 'Normal', '1': 'On positive voltage limit', '2': 'On negative voltage limit',
                   '3': 'Outside negative current limit', '4': 'Outside positive current limit'}
ACTIVITY = {'0': 'Hold', '1': 'To set', '2': 'To zero', '4': 'Clamped'}
HEATER = {'0': 'Off zero',   # Heater is off, magnet at zero
          '1': 'On',         # Heater is on
          '2': 'Off field',  # Heater is off, magnet at field
          '3': '3',
          '4': '4',          # This flag once appeared in status when the heater is being switched off
          '5': 'Fault',      # Heater is on, but the current is low
          '8': 'No heater fitted'}
MODE_1 = {'0': 'Amps',   # Fast mode
          '1': 'Tesla',  # Fast mode
          '4': 'Amps',   # Slow mode
          '5': 'Tesla'}  # Slow mode
MODE_2 = {'0': 'At rest',
          '1': 'Sweeping',
          '2': 'Sweep limiting',             # This flag appears if the heater is off (immediate mode)
          '3': 'Sweeping & sweep limiting'}  # This flag appears if the heater is on and you are sweeping the magnet

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

X: Examine status.

Heater Commands:
H0: Heater Off
H1: Heater On if PSU = Magnet
H2: Heater On, No checks (use with care)
"""


class IPS120(SerialClass):
    """
    This class allows to use the IPS120 equipment. Contains the methods which allows to control one and a GUI. Can be
    used as a standalone program or as a imported class.
    Usage:
        magnet = IPS120('COM9')
    """
    previous_activity = None
    heater = None

    def __init__(self):
        super().__init__(port=COM)
        self.query('C3')  # Switches IPS120 to the Remote & Unlock mode.

        # ZMQ settings
        self.zmq_context = zmq.Context()
        self.zmq_socket_pub = self.zmq_context.socket(zmq.PUB)
        self.zmq_socket_pub.bind('tcp://*:{}'.format(ZMQ_PORT_PUB))
        self.zmq_socket_sub = self.zmq_context.socket(zmq.SUB)
        self.zmq_socket_sub.connect('tcp://localhost:{}'.format(ZMQ_PORT_SUB))
        self.zmq_socket_sub.setsockopt_string(zmq.SUBSCRIBE, TOPIC_FILTER)

        # GUI
        self.gui = MainWindow()
        self.init_values()
        self.query_thread = QueryThread(self)
        self.query_thread.start()
        self.query_thread.status_and_magnetic_field.connect(self.decode_status)
        self.gui.widget.sweep_control_btn['Hold'].clicked.connect(self.hold)
        self.gui.widget.sweep_control_btn['To zero'].clicked.connect(self.to_zero)
        self.gui.widget.sweep_control_btn['To set'].clicked.connect(self.to_set_point)
        self.gui.widget.heater_btn.clicked.connect(self.heater_on_off)
        self.gui.setup_window.ok_btn.clicked.connect(self.update_parameters)
        # self.query_thread.status_and_magnetic_field.connect(print)

        # Recieving commands
        self.recv_thread = RecieverThread(self)
        self.recv_thread.start()

    def init_values(self):
        init_set_point = self.get_target_field()
        init_sweep_rate = self.get_sweep_rate()
        init_activity = ACTIVITY[self.query_status()[4]]
        self.gui.setup_window.set_point.setValue(float(init_set_point[1:8]))
        self.gui.setup_window.sweep_rate.setValue(float(init_sweep_rate[1:8]))
        self.previous_activity = init_activity
        self.gui.widget.indicator[init_activity].set_indicator_on()

    # TODO: can one apply a decorator function for the 'get_target_field', 'get_output_field',
    # TODO: 'get_sweep_rate' and 'query_status'?
    def get_target_field(self):
        while True:
            answer = self.query('R8')
            if len(answer) == 9 and re.findall('[+\-][0-9].[0-9]{4}', answer[1:8]):
                return answer[1:8]

    def get_output_field(self):
        while True:
            answer = self.query('R7')
            if len(answer) == 9 and re.findall('[+\-][0-9].[0-9]{4}', answer[1:8]):
                return answer[1:8]

    def get_sweep_rate(self):
        while True:
            answer = self.query('R9')
            if len(answer) == 9 and re.findall('\+[0-9]{2}.[0-9]{3}', answer[1:8]):
                return answer[1:8]

    def hold(self):
        with self.query_thread.pause():
            self.query('A0')

    def to_set_point(self):
        with self.query_thread.pause():
            self.query('A1')

    def to_zero(self):
        with self.query_thread.pause():
            self.query('A2')

    def set_target_field(self, field):
        with self.query_thread.pause():
            self.query('J' + str(field))

    def set_sweep_rate(self, sweep_rate):
        self.query('T' + str(sweep_rate))

    def update_parameters(self):
        with self.query_thread.pause():
            target_field = self.gui.setup_window.set_point.value()
            sweep_rate = self.gui.setup_window.sweep_rate.value()
            self.set_target_field(target_field)
            self.set_sweep_rate(sweep_rate)

    def heater_on_off(self):
        with self.query_thread.pause():
            if 'Off' in self.heater:
                self.query('H1')
            elif 'On' in self.heater:
                self.query('H0')

    def query_status(self):
        while True:
            answer = self.query('X')
            if len(answer) == 16 and re.findall('X[0-9]{2}A[0-9]C[0-9]H[0-9]M[0-9]{2}P[0-9]{2}', answer):
                return answer

    def decode_status(self, status):
        # Displaying the magnetic field
        self.gui.widget.value_lcd.display(status['Magnetic field'])

        # Managing the indicators of the activities: 'Hold', 'To zero', 'To set' and also 'Clamped'
        if not self.gui.widget.indicator[status['Activity']].is_on:
            self.gui.widget.indicator[status['Activity']].set_indicator_on()
            if self.gui.widget.indicator[self.previous_activity].is_on:
                self.gui.widget.indicator[self.previous_activity].set_indicator_off()
        self.previous_activity = status['Activity']

        # Switch heater indicator
        self.heater = status['Heater']
        if not self.gui.widget.indicator['Heater'].is_on and 'On' in status['Heater']:
            self.gui.widget.indicator['Heater'].set_indicator_on()
        elif self.gui.widget.indicator['Heater'].is_on and 'Off' in status['Heater']:
            self.gui.widget.indicator['Heater'].set_indicator_off()

        # Persistent mode indicator
        if (status['Heater'] == 'Off field' and float(status['Magnetic field']) == 0. and
                not self.gui.widget.indicator['Persistent'].is_on):
            self.gui.widget.indicator['Persistent'].set_indicator_on()
        elif (self.gui.widget.indicator['Persistent'].is_on and
              (float(status['Magnetic field']) != 0. or status['Heater'] != 'Off field')):
            self.gui.widget.indicator['Persistent'].set_indicator_off()

        # Quench indicator
        if not self.gui.widget.indicator['Quench'].is_on and status['System status 1'] == 'Quench':
            self.gui.widget.indicator['Quench'].set_indicator_on()
        elif self.gui.widget.indicator['Quench'].is_on:
            self.gui.widget.indicator['Quench'].set_indicator_off()

        try:
            self.zmq_socket_pub.send_pyobj(status)
        except:
            traceback.print_exc()


class QueryThread(QThread):

    status_and_magnetic_field = pyqtSignal(object)

    def __init__(self, device):
        super().__init__()
        self.isQuerying = True
        self.ips120 = device

    def run(self):
        while self.isQuerying:
            # Sometimes IPS120 has some troubles with sending correct response, therefore these WHILE loops are for
            # checking the correct length of input strings
            output_field = self.ips120.get_output_field()
            status = self.ips120.query_status()
            status_dict = {'System status 1': SYSTEM_STATUS_1[status[1]],
                           'System status 2': SYSTEM_STATUS_2[status[2]],
                           'Activity': ACTIVITY[status[4]],
                           'Heater': HEATER[status[8]],
                           'Mode 1': MODE_1[status[10]],
                           'Mode 2': MODE_2[status[11]],
                           'Magnetic field': output_field}
            self.status_and_magnetic_field.emit(status_dict)

    @contextmanager
    def pause(self):
        self.isQuerying = False
        while self.isRunning():
            pass
        yield
        self.isQuerying = True
        self.start()


class RecieverThread(QThread):
    def __init__(self, device, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isRecieving = True
        self.ips120 = device

    def run(self):
        while self.isRecieving:
            recieved_comand = self.ips120.zmq_socket_sub.recv_pyobj()
            print(recieved_comand)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ips120 = IPS120()
    ips120.gui.show()
    app.exec_()
