import time
import numpy as np
from PyQt5 import QtWidgets
from Secondomer import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys


class Secondomer (QtWidgets.QMainWindow):
    def __init__(self):
        super(Secondomer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.T = 0
        self.A = []
        self.ui.Stop_button.clicked.connect(self.StopBT)
        self.ui.Start_button.clicked.connect(self.StartBT)
        self.ui.AddBT.clicked.connect(self.AddBT)

    def StartBT(self):
        self.T = int(self.T + 1)
        print(self.T)
        self.A.append(self.T)
        self.ui.lcdNumber.display(self.T)
        self.ui.label.setText(str(self.T))
        self.ui.graph.plot(self.A)


    def StopBT(self):
        self.T = int(self.T - 1)
        print(self.T)
        self.A.append(self.T)
        self.ui.lcdNumber.display(self.T)
        self.ui.label.setText(str(self.T))
        self.ui.graph.plot(self.A)

    def AddBT(self):
        Input = self.ui.lineEdit.text()
        self.T = int(Input)
        self.A.append(self.T)
        self.ui.graph.plot(self.A)
        self.ui.lineEdit.clear()





if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Secondomer()
    application.show()
    sys.exit(app.exec())