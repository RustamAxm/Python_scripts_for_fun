from zIPS120.IPS120 import IPS120
from zIPS120.rs830 import rs830
from SerialClass import SerialClass
import numpy as np
import time
import struct
from sockets import TcpReqSocket
import zmq
'''for graph'''
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
class WorkerThread(QThread):
    data_signal = pyqtSignal(object)

    def __init__(self, rs, magnet):
        super().__init__()
        self.rs = rs
        self.magnet = magnet

    def run(self):
        start_field = -6
        end_field = 6
        N_field = 1501
        accum = 1

        field = np.linspace(start_field, end_field, N_field)
        for fld in field:
            self.magnet.set_target_field(fld)
            self.magnet.to_set_point()
            time.sleep(0.7)
            b = self.magnet.get_output_field().strip('R+')
            for i in range(accum):
                Rs_data = self.rs.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
                dataArray = np.array([float(Rs_data[0]), float(Rs_data[1]),
                                      float(Rs_data[2]), float(Rs_data[3]), float(Rs_data[4])])
                if i > 0:
                    dataArray = (dataArray + np.array([float(Rs_data[0]), float(Rs_data[1]),
                             float(Rs_data[2]), float(Rs_data[3]), float(Rs_data[4])]))/2
                #print(dataArray)
                time.sleep(0.1)
            dataArray = np.append(float(b), dataArray)
            print('Result: \n mag_field: {} Tesla, X: {} , Y: {} , R: {}, Theta: {}, freq {}'.format(*dataArray))

            self.data_signal.emit(dataArray)
            # print(type(dataArray))
        print('Accumulation_DONE')



def main():
    A0 = []
    A1 = []
    A2 = []
    A3 = []
    A4 = []
    def update(dataArray):
        A0.append(dataArray[0]) #mag_field
        A1.append(dataArray[1]) # X
        A2.append(dataArray[2]) # Y
        A3.append(dataArray[3]) # R
        A4.append(dataArray[4]) # Theta
        p1.setData(x=A0, y=A1)
        p2.setData(x=A0, y=A2)

    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('pyqtgraph example: PlotWidget')
    mw.resize(800, 600)
    cw = QtGui.QWidget()
    mw.setCentralWidget(cw)
    l = QtGui.QVBoxLayout()
    cw.setLayout(l)

    pw = pg.PlotWidget(name='X')  ## giving the plots names allows us to link their axes together
    l.addWidget(pw)
    pw2 = pg.PlotWidget(name='Y')  ## giving the plots names allows us to link their axes together
    l.addWidget(pw2)

    mw.show()
    p1 = pw.plot()
    p1.setPen((200, 200, 100))
    rect = QtGui.QGraphicsRectItem(QtCore.QRectF())
    rect.setPen(QtGui.QPen(QtGui.QColor(100, 200, 100)))
    pw.addItem(rect)
    pw.setYRange(0, 0.01)

    p2 = pw2.plot()
    p2.setPen((200, 200, 100))
    rect = QtGui.QGraphicsRectItem(QtCore.QRectF())
    rect.setPen(QtGui.QPen(QtGui.QColor(100, 200, 100)))
    pw2.addItem(rect)
    pw2.setYRange(0, 0.01)
    '''magnet'''
    magnet = IPS120('COM9')
    # magnet = TcpReqSocket(("127.0.0.1", 6006), timeout=2)


    ''''RS830'''
    '''i,j,k,l,m,n     parameter
            1               X
            2               Y
            3               R
            4               ?
            5               Aux In 1
            6               Aux In 2
            7               Aux In 3
            8               Aux In 4
            9               Reference Frequency
            10              CH1 display
            11              CH2 display'''
    rs = rs830('COM3')
    # Rs_data = []


    worker_thread = WorkerThread(rs, magnet)
    worker_thread.start()
    worker_thread.data_signal.connect(update)
    app.exec_()
    np.savetxt('042318A_1mkA_Ac_R_xy_4_6.txt', np.column_stack((A0, A1, A2, A3, A4)), fmt='%10.4f')
    print("data saved")


if __name__ == "__main__":
    main()


