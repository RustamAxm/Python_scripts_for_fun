from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from UT804 import UT804


class UT804ui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.thread_read = WorkerThread()
        self.thread_read.start()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('UT804 Multimeter')
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setFixedSize(410, 190)
        ut_value = QtWidgets.QLCDNumber(self)
        ut_value.setGeometry(QtCore.QRect(40, 80, 220, 80))
        ut_value.setDigitCount(7)
        ut_value.setObjectName("Value")
        self.thread_read.signal_ut_value.connect(ut_value.display)
        ut_units = QtWidgets.QTextBrowser(self)
        ut_units.setGeometry(QtCore.QRect(270, 80, 100, 80))
        ut_units.setFontPointSize(40)
        ut_units.setObjectName("Units")
        self.thread_read.signal_ut_units.connect(ut_units.setText)
        ut_acdc = QtWidgets.QTextBrowser(self)
        ut_acdc.setGeometry(QtCore.QRect(40, 30, 330, 40))
        ut_acdc.setFontPointSize(14)
        ut_acdc.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        ut_acdc.setObjectName("Units")
        self.thread_read.signal_ut_acdc.connect(ut_acdc.setText)


class WorkerThread(QtCore.QThread):
    signal_ut_value = pyqtSignal(object)
    signal_ut_units = pyqtSignal(object)
    signal_ut_acdc = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.device = UT804()

    def run(self):
        while True:
            answer = self.device.read()
            self.signal_ut_value.emit(answer[0])
            self.signal_ut_units.emit(answer[1])
            self.signal_ut_acdc.emit(answer[2])


def main():
    app = QApplication(sys.argv)
    window = UT804ui()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

