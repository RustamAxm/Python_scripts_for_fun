from CCDui import MainWindow
from PyQt5.QtWidgets import QApplication


app = QApplication([])
gui = MainWindow()
gui.widget.data_plot.plot([1, 2, 3, 4])
app.exec_()