import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect,QSize
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QStatusBar,QMainWindow,QToolBar,QApplication,QFileDialog,QStyleFactory,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette,QKeySequence
from numpy import random
import time
from Classes import *
from votes import *
from MyBar import *  

class ParticipantGenerator(QWidget):
    """Fenêtre de génération de candidat"""
    def __init__(self,menu=None):
        super().__init__(menu)
        self.menu=menu
        #On initialise la fenêtre
        self.setWindowTitle("Générer un Participant")
        self.resize(190, 150)
        #On ajoute les boutons/labels/comboBox
        self._createbuttons()
        self.Buttongenerate.clicked.connect(self.generate)
        self.show()
    def _createbuttons(self):
        #On définit la taille de la police
        font = QFont()
        font.setPointSize(11)

        #On créer les boutons/combobox/champs/labels
        self.label_1 = QLabel(self)
        self.label_1.setGeometry(QRect(20, 30, 91, 20))
        self.label_1.setFont(font)
        self.label_1.setText("Candidate :")


        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(20, 70, 91, 20))
        self.label_2.setFont(font)
        self.label_2.setText("Voter :")

        self.lineEditCandidateNumber = QLineEdit(self)
        self.lineEditCandidateNumber.setGeometry(QRect(120, 30, 50, 23))
        self.lineEditCandidateNumber.setFont(font)
        self.lineEditCandidateNumber.setText("0")



        self.lineEditVoterNumber = QLineEdit(self)
        self.lineEditVoterNumber.setGeometry(QRect(120, 70, 50, 23))
        self.lineEditVoterNumber.setFont(font)
        self.lineEditVoterNumber.setText("0")
        

        self.Buttongenerate = QPushButton("Generate",self)
        self.Buttongenerate.setGeometry(QRect(90, 110, 80, 23))
        self.Buttongenerate.setFont(font)

    def generate(self):
        for i in range(int(self.lineEditVoterNumber.text())):
            newVoter=self.menu.randomParticipant(False)
            self.menu.addVoter(newVoter)
  
        for i in range(int(self.lineEditCandidateNumber.text())):
            newCandidate=self.menu.randomParticipant(True)
            self.menu.addCandidate(newCandidate)

        self.menu.refreshStatusBar()
        self.menu.pt=ParticipantTable(self.menu.centralArea,self.menu.dictcandidates,self.menu.dictvoters)



       

"""if __name__ == '__main__':
    #print(QStyleFactory.keys()) 
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    pg=ParticipantGenerator()
    sys.exit(app.exec_())"""