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
import random

class ParticipantTable(QWidget):
    """Tableau des participants"""
    def __init__(self,menu,mode=None):
        super(ParticipantTable,self).__init__(menu.tab1)
        self.menu=menu
        self.setWindowTitle("Candidate_Table")
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + "/pictures/icon.png"))
        self.setGeometry(QRect(930,260, 504, 500))
        self.candidates=menu.dictcandidates
        self.voters=menu.dictvoters
        self.mode=mode
        if self.mode==None:
            self.mode="Participant"
        if self.mode=="Candidate":
            self.setCandidateMode()
        elif self.mode=="Voter":
            self.setVoterMode()
        else:
            self.setParticipantMode()
        self.show()

    def setParticipantMode(self):
        self.mode="Participant"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 504, 500))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.verticalHeader().hide()
        item = QTableWidgetItem("Participant")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem("Id")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem("First Name")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem("Last Name")
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem("Position")
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem("Score")
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem("M.U.")
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.setColumnWidth(0,80)
        self.tableWidget.setColumnWidth(1,50)
        self.tableWidget.setColumnWidth(2,110)
        self.tableWidget.setColumnWidth(3,98)
        self.tableWidget.setColumnWidth(4,80)
        self.tableWidget.setColumnWidth(5,70)
        self.tableWidget.setColumnWidth(6,50)
        self.loaddata(self.candidates,self.voters)
        

    def setVoterMode(self):
        self.mode="Voter"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 504, 500))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.verticalHeader().hide()
        item = QTableWidgetItem("Id")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem("First Name")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem("Last Name")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem("Position")
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,142)
        self.tableWidget.setColumnWidth(3,110)
        self.loaddata(self.candidates,self.voters)

    def setCandidateMode(self):
        self.mode="Candidate"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 504, 500))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.verticalHeader().hide()
        item = QTableWidgetItem("Id")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem("First Name")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem("Last Name")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem("Position")
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem("Score")
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem("M.U.")
        self.tableWidget.setHorizontalHeaderItem(5, item)

        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,145)
        self.tableWidget.setColumnWidth(2,125)
        self.tableWidget.setColumnWidth(3,98)
        self.tableWidget.setColumnWidth(4,70)
        self.tableWidget.setColumnWidth(5,70)
        self.loaddata(self.candidates,self.voters)

    def loaddata(self,candidates,voters):
        if self.mode=="Participant": 
            row=0
            self.tableWidget.setRowCount(len(candidates)+len(voters))
            for (_,v) in candidates.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem("Candidate"))
                self.tableWidget.setItem(row,1,QTableWidgetItem(str(v.id)))
                self.tableWidget.setItem(row,2,QTableWidgetItem(v.firstName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(v.lastName))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(v.pos)))
                self.tableWidget.setItem(row,5,QTableWidgetItem(str(v.score)))
                self.tableWidget.setItem(row,6,QTableWidgetItem(( "%.1f" % v.mu)))
                row+=1
            for (_,w) in voters.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem("Voter"))
                self.tableWidget.setItem(row,1,QTableWidgetItem(str(w.id)))
                self.tableWidget.setItem(row,2,QTableWidgetItem(w.firstName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(w.lastName))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(w.pos)))
                row+=1
        if self.mode=="Candidate":
            row=0
            self.tableWidget.setRowCount(len(candidates))
            for (_,v) in candidates.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem(str(v.id)))
                self.tableWidget.setItem(row,1,QTableWidgetItem(v.firstName))
                self.tableWidget.setItem(row,2,QTableWidgetItem(v.lastName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(str(v.pos)))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(v.score)))
                self.tableWidget.setItem(row,5,QTableWidgetItem( "%.1f" % v.mu))
                row+=1
        if self.mode=="Voter":
            row=0
            self.tableWidget.setRowCount(len(voters))
            for (_,w) in voters.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem(str(w.id)))
                self.tableWidget.setItem(row,1,QTableWidgetItem(w.firstName))
                self.tableWidget.setItem(row,2,QTableWidgetItem(w.lastName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(str(w.pos)))
                row+=1