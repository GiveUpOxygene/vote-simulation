
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon

class tableView(QWidget):
    def __init__(self,area,candidates,voters,mode=None):
        super(tableView,self).__init__(area)
        self.setWindowTitle("Candidate_Table")
        self.setWindowIcon(QIcon("./pictures/icon.png"))
        self.setGeometry(QRect(930,300, 650, 510))
        self.candidates=candidates
        self.voters=voters
        self.mode=mode
        if self.mode==None:
            self.mode="Participant"
        if self.mode=="Candidat":
            self.setCandidateMode()
        elif self.mode=="Voter":
            self.setVoterMode()
        else:
            self.setParticipantMode()
        self.show()

    def setParticipantMode(self):
        self.mode="Participant"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 650, 510))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.verticalHeader().hide()
        item = QTableWidgetItem("Id")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem("Participant")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem("First Name")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem("Last Name")
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem("Position")
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem("Has\nVoted")
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem("Vote\nReceived")
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.setColumnWidth(0,28)
        self.tableWidget.setColumnWidth(1,75)
        self.tableWidget.setColumnWidth(2,160)
        self.tableWidget.setColumnWidth(3,168)
        self.tableWidget.setColumnWidth(4,72)
        self.tableWidget.setColumnWidth(5,70)
        self.tableWidget.setColumnWidth(6,60)
        self.loaddata(self.candidates,self.voters)
        

    def setVoterMode(self):
        self.mode="Voter"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 650, 540))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.verticalHeader().hide()
        item = QTableWidgetItem("Id")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem("First Name")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem("Last Name")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem("Position")
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem("Has\nVoted")
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,198)
        self.tableWidget.setColumnWidth(2,190)
        self.tableWidget.setColumnWidth(3,110)
        self.tableWidget.setColumnWidth(4,100)
        self.loaddata(self.candidates,self.voters)

    def setCandidateMode(self):
        self.mode="Candidate"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 650, 540))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.verticalHeader().hide()
        item = QTableWidgetItem("Id")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem("First Name")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem("Last Name")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem("Position")
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem("Vote\nReceived")
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,198)
        self.tableWidget.setColumnWidth(2,190)
        self.tableWidget.setColumnWidth(3,110)
        self.tableWidget.setColumnWidth(4,100)
        self.loaddata(self.candidates,self.voters)

    def loaddata(self,candidates,voters):
        if self.mode=="Participant": 
            row=0
            self.tableWidget.setRowCount(len(candidates)+len(voters))
            for (k,v) in candidates.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem(str(v.id)))
                self.tableWidget.setItem(row,1,QTableWidgetItem("Candidate"))
                self.tableWidget.setItem(row,2,QTableWidgetItem(v.firstName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(v.lastName))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(v.pos)))
                self.tableWidget.setItem(row,6,QTableWidgetItem(str(v.vote)))
                row+=1
            for (k,w) in voters.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem(str(w.id)))
                self.tableWidget.setItem(row,1,QTableWidgetItem("Voter"))
                self.tableWidget.setItem(row,2,QTableWidgetItem(w.firstName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(w.lastName))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(w.pos)))
                self.tableWidget.setItem(row,5,QTableWidgetItem(str(w.hasVoted)))
                row+=1
        if self.mode=="Candidate":
            row=0
            self.tableWidget.setRowCount(len(candidates))
            for (k,v) in candidates.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem(str(v.id)))
                self.tableWidget.setItem(row,1,QTableWidgetItem(v.firstName))
                self.tableWidget.setItem(row,2,QTableWidgetItem(v.lastName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(str(v.pos)))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(v.vote)))
                row+=1
        if self.mode=="Voter":
            row=0
            self.tableWidget.setRowCount(len(voters))
            for (k,w) in voters.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem(str(w.id)))
                self.tableWidget.setItem(row,1,QTableWidgetItem(w.firstName))
                self.tableWidget.setItem(row,2,QTableWidgetItem(w.lastName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(str(w.pos)))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(w.hasVoted)))
                row+=1



            
    
    

