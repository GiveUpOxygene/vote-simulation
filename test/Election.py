import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect
from PyQt5.QtWidgets import QMainWindow,QApplication,QStyleFactory,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette    
from numpy import random
import time
from Classes import *
from votes import *
class Election(QWidget):
    def __init__(self,candidates,voters):
        super().__init__()
        self.setGeometry(0,0,900,900)
        self.show()

if __name__ == '__main__':
    #print(QStyleFactory.keys()) 
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    E = Election()
    sys.exit(app.exec_())
