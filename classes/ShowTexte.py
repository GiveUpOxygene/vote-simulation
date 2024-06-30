from PyQt5.QtCore import pyqtSignal,QRect,Qt,QSize,QPoint
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QWidget,QStyle,QToolButton,QPushButton,QHBoxLayout,QLineEdit,QDialog,QComboBox,QLabel,QDesktopWidget
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPainter,QPen,QColor
import numpy as np  
import os
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.cm as cm
from votes import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from Classes import *
import random

class ShowTexte(QDialog):
    def __init__(self,title,texte,icon=None):
        QWidget.__init__(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.titleBar = MyBar(self)
        self.titleBar.resizable=False
        self.titleBar.minButton.hide()
        self.titleBar.maxButton.hide()
        self.titleBar.image.hide()
        self.setContentsMargins(1, self.titleBar.height(), 1, 1)
        self.setStyleSheet("""
        QDialog{background-color: #ffffff;font: 14px;spacing: 8px;border: 1px solid;border-color: #b8bcc0;}""")       
       
        
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + "/pictures/icons/icon.png")) 
        #Titre
        self.titre = QLabel (self)
        self.titre.setGeometry(QRect(90, 20+self.titleBar.height(), 628, 20))
        self.titre.setText(title)
        self.titre.setStyleSheet("font-weight: bold; color: black; font-size:14pt;")
        
        if (icon!=None):
            self.pix=(QPixmap(os.path.dirname(__file__) + "/pictures/{}".format(icon))).scaledToHeight(60)
            self.image=QLabel(self)
            self.image.setStyleSheet("background-color: #ffffff;border: 1px solid;border-color: #dadfe5;")
            self.image.setGeometry(QRect(10,10+self.titleBar.height(),self.pix.width(),self.pix.height()))
            self.image.setPixmap(self.pix)
            self.image.setStyleSheet("border : none ")
        #Texte
        file=open(os.path.dirname(__file__) + "/doc/{}.txt".format(texte),"r", encoding="utf8")
        s=""
        for line in file.readlines():
            s+=line
        nb=s.count("\n")
        self.setGeometry(QRect(300,200,725,nb*20+self.titleBar.height()+70))
        self.texte = QLabel(self)
        self.texte.setGeometry(QRect(90, 45+self.titleBar.height(), 628, 19*nb))
        self.texte.setText(s)
        self.texte.setStyleSheet("color: black; font-size:10.5pt")
        

        #Bouton ok
        self.button = QPushButton("Ok",self)
        self.button.setGeometry(QRect(550, self.height()-55, 160, 40))
        self.button.setStyleSheet("QPushButton{border: none; background-color: #70afea}QPushButton::hover{border: none; background-color:  #b2d2f0}")
        self.button.clicked.connect(self.close)

        self.show()
    
    def showEvent(self, event):
        self.CenterOnScreen()

    def CenterOnScreen(self):
        screen=QDesktopWidget()
  
        screenGeom = QRect(screen.screenGeometry(self))
  
        screenCenterX = screenGeom.center().x()
        screenCenterY = screenGeom.center().y()
  
        self.move(int(screenCenterX - self.width () / 2),int (screenCenterY - self.height() / 2))
    
    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())