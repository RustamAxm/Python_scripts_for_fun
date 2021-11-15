from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, QSpinBox, QGroupBox, QLabel, QMainWindow,
                             QPushButton)
import pyqtgraph as pg
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = CentralWidget()
        self.setCentralWidget(self.widget)
        self.show()


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        labels = ['Data', 'Setup']
        self.group_box = {}
        self.group_box_layout = {}

        for label in labels:
            self.group_box[label] = QGroupBox(label)
            self.group_box_layout[label] = QGridLayout(self.group_box[label])
            layout.addWidget(self.group_box[label])

        # Data plot
        self.data_plot = pg.PlotWidget()
        self.group_box_layout['Data'].addWidget(self.data_plot)

        # Parameters group box
        number_of_frames_label = QLabel('Number of frames: ')
        exposition_time_label = QLabel('Exposition time, ms: ')
        self.number_of_frames = QSpinBox()
        self.exposition_time = QSpinBox()
        self.group_box_layout['Setup'].addWidget(number_of_frames_label, 0, 0)
        self.group_box_layout['Setup'].addWidget(exposition_time_label, 1, 0)
        self.group_box_layout['Setup'].addWidget(self.number_of_frames, 0, 1)
        self.group_box_layout['Setup'].addWidget(self.exposition_time, 1, 1)

        # Start button
        self.start_btn = QPushButton('Start')
        self.start_btn.setFixedSize(50, 50)
        self.group_box_layout['Setup'].addWidget(self.start_btn, 0, 2, 2, 1)


class ExperimentalSetup(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()


