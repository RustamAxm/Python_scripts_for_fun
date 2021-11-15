import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QVBoxLayout, QLineEdit
from PyQt5 import QtCore
from SerialClass import SerialClass
from time import sleep

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.sr830 = SerialClass('COM9')
        self.query_thread = QueryThread(self.sr830)
        self.query_thread.start()
        main_layout = QVBoxLayout(self)
        self.display = QLCDNumber(11)
        self.line_edit = QLineEdit()
        self.line_edit.returnPressed.connect(self.query)
        self.query_thread.output.connect(self.display.display)
        main_layout.addWidget(self.display)
        main_layout.addWidget(self.line_edit)
        self.show()

    def query(self):
        if self.query_thread.is_querying:
            self.query_thread.output.disconnect(self.display.display)
            self.query_thread.is_querying = False
            while self.query_thread.isRunning():
                pass
        self.display.display('s')
        self.query_thread.is_querying = True
        self.query_thread.start()
        self.query_thread.output.connect(self.display.display)


class QueryThread(QtCore.QThread):
    output = QtCore.pyqtSignal(object)

    def __init__(self, device):
        super().__init__()
        self.device = device
        self.is_querying = True

    def run(self):
        while self.is_querying:
            answer = self.device.query('OUTP?1')
            self.output.emit(answer)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
