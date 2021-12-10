from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
import pyqtgraph as pg
import numpy as np


class Main(pg.GraphicsView):
    def __init__(self):
        super().__init__()
        layout = pg.GraphicsLayout()
        layout.setSpacing(0)
        self.field_axis = pg.AxisItem('bottom', text='Magnetic field', units='T')
        self.X_axis = pg.AxisItem('left', text='X channel', units='V')
        self.Y_axis = pg.AxisItem('right', text='Y channel', units='V')
        self.X_axis.showLabel()
        self.Y_axis.showLabel()

        self.field_axis.showLabel()
        self.X_view = pg.ViewBox()
        self.X_view.enableAutoRange()
        self.Y_view = pg.ViewBox()
        self.Y_view.enableAutoRange()


        self.field_axis.linkToView(self.X_view)
        self.X_axis.linkToView(self.X_view)
        self.Y_axis.linkToView(self.Y_view)
        self.Y_view.setXLink(self.X_view)

        layout.addItem(self.X_axis, 0, 0, 1, 1)
        layout.addItem(self.Y_view, 0, 1, 1, 1)
        layout.addItem(self.X_view, 0, 1, 1, 1)
        layout.addItem(self.Y_axis, 0, 2, 1, 1)
        layout.addItem(self.field_axis, 1, 1, 1, 1)

        self.setCentralWidget(layout)


app = QApplication([])
x = np.linspace(0, 1, 100)
y1 = np.sin(x)
y2 = x**2

main = Main()
main.plotdataitem = pg.PlotDataItem()
main.plotdataitem2 = pg.PlotDataItem()

main.X_view.addItem(main.plotdataitem)
main.Y_view.addItem(main.plotdataitem2)

main.plotdataitem.setData(x, y1)
main.plotdataitem2.setData(x, y2)
main.show()

# test1 = Test1()
# test1.show()
app.exec_()

