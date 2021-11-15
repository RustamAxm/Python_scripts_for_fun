import pyqtgraph as pg
import numpy as np
import re
import time
from SerialClass import SerialClass
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QDoubleSpinBox, QSpinBox, QLineEdit, QLabel,
                             QPushButton, QGroupBox, QFileDialog)
from PyQt5.QtCore import QThread, pyqtSignal
from zIPS120.IPS120_ver2 import MagneticField
from zIPS120.rs830 import rs830


class SettingsBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__('Settings', *args, *kwargs)
        layout = QGridLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        self.start = QDoubleSpinBox()
        self.start.setMinimum(-6.0)
        self.start.setMaximum(6.0)
        self.start.setValue(-6.0)
        self.start.setDecimals(4)
        self.start.valueChanged.connect(self.value_changed)

        self.stop = QDoubleSpinBox()
        self.stop.setMinimum(-6.0)
        self.stop.setMaximum(6.0)
        self.stop.setValue(6.0)
        self.stop.setDecimals(4)
        self.stop.valueChanged.connect(self.value_changed)

        self.steps = QSpinBox()
        self.steps.setValue(21)
        self.steps.setMinimum(1)
        self.steps.setMaximum(100000)
        self.steps.valueChanged.connect(self.value_changed)

        self.interval = QLineEdit()
        self.interval.setReadOnly(True)
        self.interval.setText(str(12/20))

        self.start_btn = QPushButton('Start')
        self.stop_btn = QPushButton('Stop')
        self.save_btn = QPushButton('Save data to file')

        self.status_fld = QLineEdit('Status')
        self.status_fld.setReadOnly(True)
        self.current_fld = QLineEdit('Current field')
        self.current_fld.setReadOnly(True)



        layout.addWidget(QLabel('Start point, T'), 0, 0, 1, 2)
        layout.addWidget(self.start, 1, 0, 1, 2)
        layout.addWidget(QLabel('Stop point, T'), 3, 0, 1, 2)
        layout.addWidget(self.stop, 4, 0, 1, 2)
        layout.addWidget(QLabel('Number of steps'), 6, 0, 1, 2)
        layout.addWidget(self.steps, 7, 0, 1, 2)
        layout.addWidget(QLabel('Interval of a step, T'), 9, 0, 1, 2)
        layout.addWidget(self.interval, 10, 0, 1, 2)
        layout.addWidget(self.start_btn, 12, 0, 1, 1)
        layout.addWidget(self.stop_btn, 12, 1, 1, 1)
        layout.addWidget(self.save_btn, 13, 0, 1, 2)
        layout.addWidget(self.status_fld, 15, 0, 1, 2)
        layout.addWidget(self.current_fld, 16, 0, 1, 2)
        for i in [2, 5, 8, 11, 14]:
            layout.addWidget(QWidget(), i, 0, 1, 1)

    def value_changed(self):
        self.interval.setText(str((self.stop.value()-self.start.value())/(self.steps.value()-1)))


class MagneticFieldBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__('Magnetic field controls', *args, **kwargs)
        layout = QGridLayout(self)
        self.goto_zero = QPushButton('Goto 0')
        self.goto_start = QPushButton('Goto start')
        self.hold = QPushButton('Hold')
        layout.addWidget(self.goto_start, 0, 0, 1, 1)
        layout.addWidget(self.hold, 0, 1, 1, 1)
        layout.addWidget(self.goto_zero, 0, 2, 1, 1)


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QGridLayout(self)
        self.set_box = SettingsBox()
        self.graph = pg.PlotWidget()
        self.magnetic_field_box = MagneticFieldBox()
        self.plot_data_item = pg.PlotDataItem()
        self.graph.addItem(self.plot_data_item)
        # self.data = None

        layout.addWidget(self.graph, 0, 0, 3, 1)
        layout.addWidget(self.set_box, 0, 1, 1, 1)
        layout.addWidget(self.magnetic_field_box, 1, 1, 1, 1)
        layout.setRowStretch(2, 1)
        layout.setColumnStretch(0, 1)

        self.ips = IPS(self)
        output_field = float(self.ips.get_output_field())
        self.current_fld_str = 'IPS output field = {}T'.format(output_field)
        self.set_box.current_fld.setText(self.current_fld_str)
        self.rs830 = rs830('COM8')

        self.measuring_thread = None
        self.set_box.start_btn.clicked.connect(self.start_thread)
        self.set_box.stop_btn.clicked.connect(self.stop_thread)
        self.set_box.save_btn.clicked.connect(self.save_data)

        self.magnetic_field_controls_thread = MagneticFieldControlsThread(self.ips, self)
        self.magnetic_field_box.goto_start.clicked.connect(self.goto_start)
        self.magnetic_field_box.goto_zero.clicked.connect(self.goto_zero)
        self.magnetic_field_box.hold.clicked.connect(self.hold)

    def start_thread(self):
        self.measuring_thread = MeasuringThread(self.ips, self.rs830, self)
        self.magnetic_field_box.setDisabled(True)
        self.data = None
        self.plot_data_item.clear()
        # self.plot = pg.PlotDataItem()
        # self.graph.addItem(self.plot)
        self.ips.query('A1')  # Goto mode
        self.measuring_thread.start()
        self.measuring_thread.answer.connect(self.update_graph)

    def stop_thread(self):
        if self.measuring_thread is not None and self.measuring_thread.isMeasuring:
            self.magnetic_field_box.setEnabled(True)
            self.ips.query('A0')  # Hold sweeping mode
            self.ips.isSweeping = False
            self.measuring_thread.isMeasuring = False
            self.set_box.status_fld.setText('Measurement stopped by user')

    def goto_zero(self):
        self.magnetic_field_controls_thread.magnetic_field = 0.
        if not self.magnetic_field_controls_thread.isRunning():
            self.magnetic_field_controls_thread.start()
        else:
            self.hold()
            self.magnetic_field_controls_thread.start()

    def goto_start(self):
        self.magnetic_field_controls_thread.magnetic_field = self.set_box.start.value()
        if not self.magnetic_field_controls_thread.isRunning():
            self.magnetic_field_controls_thread.start()
        else:
            self.hold()
            self.magnetic_field_controls_thread.start()

    def hold(self):
        if self.ips.isSweeping:
            self.ips.query('A0')
            self.ips.isSweeping = False
            while not self.magnetic_field_controls_thread.isFinished():
                pass

    def update_graph(self, dict):
        answer = np.array([float(dict['B']), float(dict['X']), float(dict['Y']), float(dict['R']), float(dict['Th'])])
        print(np.shape(answer))
        print(self.data)
        if self.data is None:
            self.data = answer.reshape(1, 5)
            print(1)
        else:
            self.data = np.row_stack((self.data, answer))
            print(2)
        self.plot_data_item.setData(self.data[:, 0], self.data[:, 1])
        print(3)

    def save_data(self):
        name = QFileDialog.getSaveFileName(caption='Save File')
        if name[0] == '':
            return
        np.savetxt(name[0], self.data)


class MeasuringThread(QThread):

    answer = pyqtSignal(object)

    def __init__(self, IPS, SR830, gui):
        super().__init__()
        self.isMeasuring = None
        self.ips = IPS
        self.sr830 = SR830
        self.gui = gui
        X, Y = self.sr830.SNAP(1, 2).rstrip().split(',')
        print(X, Y)

    def run(self):
        self.isMeasuring = True
        self.start_point = self.gui.set_box.start.value()
        self.stop_point = self.gui.set_box.stop.value()
        self.steps = self.gui.set_box.steps.value()
        for step in np.linspace(self.start_point, self.stop_point, self.steps):
            # TODO: Implement magnetic field scan when there will be helium available
            self.ips.goto(step)
            self.waiting(5)
            X, Y, R, Th = self.sr830.SNAP(1, 2, 3, 4).rstrip().split(',')
            dict = {'B': step, 'X': X, 'Y': Y, 'R': R, 'Th': Th}
            print('thread', dict)
            self.answer.emit(dict)
            if not self.isMeasuring:
                return
        self.gui.set_box.status_fld.setText('Measurement finished!')
        self.isMeasuring = False
        self.gui.magnetic_field_box.setEnabled(True)

    def waiting(self, ts):
        t = 0.
        self.gui.set_box.status_fld.setText(self.gui.set_box.status_fld.text() + ', Waiting {} seconds'.format(ts))
        while self.isMeasuring and t < ts:
            t += 0.1
            time.sleep(0.1)
            print(t)


class MagneticFieldControlsThread(QThread):
    def __init__(self, ips, gui):
        super().__init__()
        self.ips = ips
        self.gui = gui
        self.magnetic_field = None

    def run(self):
        self.ips.goto(self.magnetic_field)


class IPS(SerialClass):
    def __init__(self, gui):
        super().__init__('COM4')
        self.query('C3')
        self.isSweeping = None
        self.status_fld_str = None
        self.current_fld_str = None
        self.gui = gui

    def goto(self, b_field):
        self.isSweeping = True
        # self.query('A1')
        while self.isSweeping:
            self.query('J' + str(b_field))
            time.sleep(0.1)
            target_field = float(self.get_target_field())
            self.status_fld_str = 'Next field = {} T, IPS target field = {} T'.format(b_field, target_field)
            self.gui.set_box.status_fld.setText(self.status_fld_str)
            print(self.status_fld_str)
            if np.abs(target_field - b_field) <= 1e-4:
                self.status_fld_str = 'Go to {}T'.format(target_field)
                self.gui.set_box.status_fld.setText(self.status_fld_str)
                print(self.status_fld_str)
                break
        while self.isSweeping:
            output_field = float(self.get_output_field())
            self.current_fld_str = 'IPS output field = {}T'.format(output_field)
            self.gui.set_box.current_fld.setText(self.current_fld_str)
            print(self.current_fld_str)
            if np.abs(output_field - target_field) < 1e-6:
                self.status_fld_str = '{}T reached'.format(target_field)
                self.gui.set_box.status_fld.setText(self.status_fld_str)
                print(self.status_fld_str)
                # self.query('A0')
                self.isSweeping = False
                return True

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

    def set_sweep_rate(self, sweep_rate):
        self.query('T' + str(sweep_rate))
        time.sleep(0.1)
        print('Sweep rate is {}'.format(self.query('R9')))



if __name__ == '__main__':
    app = QApplication([])
    main = MainWidget()
    main.show()
    print(not None)
    app.exec_()
