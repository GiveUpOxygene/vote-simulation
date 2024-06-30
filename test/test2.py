import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from MyBar import *



class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title="LE ONE PIECE EXISTE"
        self.layout  = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800,400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())