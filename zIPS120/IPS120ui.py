import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLCDNumber, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QMainWindow, QGroupBox, QAction, QLineEdit, QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout(self) # Main layout of the widget

        # Creating a group box with a title for each of the widget's parts. Adding a layout for each of the group boxes.
        box_labels = ['Display', 'Sweep control', 'Switch']
        self.group_box = {}
        self.group_box_layout = {}
        for label in box_labels:
            self.group_box_layout[label] = QGridLayout()  # Creating a layout for each group box
            self.group_box[label] = QGroupBox(label)  # Creating a group box
            self.group_box[label].setLayout(self.group_box_layout[label])  # Setting layouts to the group boxes
            layout.addWidget(self.group_box[label])  # Setting group boxes to the main layout

        # Creating an lcd number to be a value monitor and adding it to the layout of the 'Display' group box
        self.value_lcd = QLCDNumber(6)
        self.value_lcd.setSmallDecimalPoint(True)
        self.value_lcd.display('0.0000')
        self.value_lcd.setFixedSize(320, 85)
        self.group_box_layout['Display'].addWidget(self.value_lcd, 0, 0, 4, 1, alignment=Qt.AlignCenter)

        # Creating indicators for all the gui
        indicator_labels = ['Clamped', 'Persistent', 'Sweep limit', 'Quench', 'Hold', 'To zero', 'To set', 'Heater']
        indicator_orders = ['i-l', 'i-l', 'i-l', 'i-l', 'l-i', 'l-i', 'l-i', 'l-i']
        indicator_alignments = ['h', 'h', 'h', 'h', 'v', 'v', 'v', 'v']
        self.indicator = {}
        self.sweep_control_btn = {}
        self.heater_btn = Button()
        k = 0
        for label, order, alignment in zip(indicator_labels, indicator_orders, indicator_alignments):
            self.indicator[label] = Indicator(label, alignment, order, 12)
            if k < 4:
                # Adding corresponding indicators to the 'Display' layout
                self.group_box_layout['Display'].addWidget(self.indicator[label], k, 1, alignment=Qt.AlignLeft)
            elif k < 7:
                # Adding corresponding indicators to the 'Sweep control' layout. Also creating buttons and adding
                # them as well
                self.group_box_layout['Sweep control'].addWidget(self.indicator[label], 0, k, alignment=Qt.AlignCenter)
                self.sweep_control_btn[label] = Button()
                self.group_box_layout['Sweep control'].addWidget(self.sweep_control_btn[label], 1, k, alignment=Qt.AlignCenter)
            else:
                # Adding a 'Heater' indicator to the 'Switch' group box layout. Adding a button to switch the heater
                self.group_box_layout['Switch'].addWidget(self.indicator[label], 0, 0, alignment=Qt.AlignCenter)
                self.group_box_layout['Switch'].addWidget(self.heater_btn, 1, 0, alignment=Qt.AlignCenter)
            k += 1


class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.set_point = QDoubleSpinBox()
        self.set_point.setSingleStep(0.0001)
        self.set_point.setDecimals(4)
        self.set_point.setRange(-6, 6)
        self.sweep_rate = QDoubleSpinBox()
        self.sweep_rate.setSingleStep(0.0001)
        self.sweep_rate.setDecimals(4)
        self.sweep_rate.setRange(0, 0.4)
        # TODO: make QLabel notes with the maximum value
        set_point_label = QLabel('Set point, T: ')
        sweep_rate_label = QLabel('Sweep rate, T/min: ')
        self.ok_btn = QPushButton('OK')
        layout.addWidget(set_point_label, 0, 0)
        layout.addWidget(sweep_rate_label, 1, 0)
        layout.addWidget(self.set_point, 0, 1)
        layout.addWidget(self.sweep_rate, 1, 1)
        layout.addWidget(self.ok_btn, 2, 1)
        self.ok_btn.clicked.connect(self.close)
        self.setFixedSize(self.minimumSize())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = MainWidget()
        self.setup_window = SetupWindow()
        self.setCentralWidget(self.widget)
        menu_bar = self.menuBar()
        self.setup_action = QAction('&Setup')
        menu_bar.addAction(self.setup_action)
        self.setup_action.triggered.connect(self.setup_window.show)
        self.show()


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(40, 40)


class Indicator(QWidget):
    def __init__(self, name='hi', alignment='v', order='i-l', size=9, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = QFont()
        font.setPointSize(9)
        self.label = QLabel(name)
        self.label.setFont(font)
        self.indicator = QLabel()
        self.pixmap_on = QPixmap('ON.png').scaled(size, size)
        self.pixmap_off = QPixmap('OFF.png').scaled(size, size)

        if alignment == 'v':
            layout = QVBoxLayout(self)
        elif alignment == 'h':
            layout = QHBoxLayout(self)
        else:
            raise ValueError('Alignment can be only "v" for vertical or "h" for horizontal')
        if order == 'i-l':
            layout.addWidget(self.indicator, alignment=Qt.AlignCenter)
            layout.addWidget(self.label, alignment=Qt.AlignCenter)
        elif order == 'l-i':
            layout.addWidget(self.label, alignment=Qt.AlignCenter)
            layout.addWidget(self.indicator, alignment=Qt.AlignCenter)
        else:
            raise ValueError('Order can be only "l-i" for label-indicator order or "i-l" for indicator-label')
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        self.indicator.setPixmap(self.pixmap_off)
        self.is_on = False

    def set_indicator_on(self):
        self.indicator.setPixmap(self.pixmap_on)
        self.is_on = True

    def set_indicator_off(self):
        self.indicator.setPixmap(self.pixmap_off)
        self.is_on = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
