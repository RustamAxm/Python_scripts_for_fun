from SerialClass import SerialClass
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QGroupBox, QDoubleSpinBox,
                             QPushButton)
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import re

COM_PORTS = ['COM5', 'COM6', 'COM7']


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout(self)
        self.plot_box = PlotBox()
        self.setup_box = SetupBox()
        self.buttons = Buttons()
        self.layout.addWidget(self.setup_box, 0, 0, 1, 2)
        self.layout.addWidget(self.buttons, 0, 2, 1, 1)
        self.layout.addWidget(self.plot_box, 1, 0, 3, 3)


class PlotBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__('Data', *args, **kwargs)
        self.layout = QGridLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)


class SetupBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__('Setup', *args, **kwargs)
        self.layout = QGridLayout(self)
        labels = ['Wavelength', 'Number of frames', 'Accumulation time']
        self.value = {}
        self.label = {}
        k = 0
        for label in labels:
            self.value[label] = QDoubleSpinBox()
            self.label[label] = QLabel(label) if k != 2 else QLabel(label + ', sec')
            self.layout.addWidget(self.value[label], k, 0)
            self.layout.addWidget(self.label[label], k, 1)
            k += 1


class Buttons(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout(self)
        labels = ['Start', 'Stop']
        btn = {}
        for label in labels:
            btn[label] = QPushButton(label)
            btn[label].setFixedSize(80, 80)
            self.layout.addWidget(btn[label])


class Stage(SerialClass):
    def __init__(self, offset=None, com=None, stage_number=None):
        super().__init__(com)
        self.offset = offset
        self.stage_number = stage_number
        self.abs_position = None
        self.rel_position = None

    def init_stage_position(self):
        self.abs_position = re.findall('\-?[0-9]{1,3}.[0-9]{2}', self.query('?nm'))[0]
        if self.stage_number == '2':
            self.rel_position = str(float(self.abs_position) + self.offset)
        else:
            self.rel_position = str(float(self.abs_position) - self.offset)


class Spectrometer:
    program_offset = [0.04, -0.32, 0.054]
    # program_offset = [0, 0, 0]

    def __init__(self):
        self.ui = MainWidget()
        self.stage = {}
        offset_stage = {}
        cfg = {}
        with open('cfg.txt', 'r') as file:
            for cfg_line in file.readlines():
                cfg_key, cfg_value = cfg_line.split('=')
                cfg[cfg_key] = cfg_value
        print(cfg)
        # for i, com in zip(range(1, 4), COM_PORTS):
        #     self.stage[str(i)] = \
        #         Stage(offset=offset_stage[str(i)]+self.program_offset[i-1], com=com, stage_number=str(i))
        #     self.stage[str(i)].init_stage_position()
        #     self.ui.line_edit[str(i)].setText(self.stage[str(i)].rel_position)


if __name__ == '__main__':
    app = QApplication([])
    win = Spectrometer()
    win.ui.show()
    app.exec_()
