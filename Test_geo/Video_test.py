from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QLabel,QSlider, QStyle, QFileDialog, QTextBrowser
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl, QRect


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt_VMP")
        self.setGeometry(450, 200, 800, 600)
        self.setWindowIcon(QIcon('player.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        self.init_ui()
        self.show()

    def init_ui(self):
        #player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videowidget = QVideoWidget()

        # open
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
        #play
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(10,10,10,10)
        # set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        #hboxLayout.addWidget(self.setWindowTitle())
        # hboxLayout.addWidget(self.slider)
        # create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(videowidget)



        self.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileNames(self, caption="Open Video")
        #сама открывашка
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(str(filename[0]))))
            self.playBtn.setEnabled(True)
            self.setWindowTitle(str(filename[0]))

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())

