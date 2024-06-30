from PyQt5.QtCore import  QRect
from PyQt5.QtWidgets import QWidget,  QComboBox, QLabel, QLineEdit
from PyQt5.QtGui import  QFont

class CreateParticipant(QWidget):
    def __init__(self,centralArea):
        super().__init__(centralArea)
        #On initialise les attributs du Participant
        self.firstName=None
        self.lastName=None
        self.x=None
        self.y=None
        #On initialise la fenêtre
        self.setWindowTitle("Créer un Participant")
        self.resize(314, 154)
        #On ajoute les boutons/labels/comboBox
        self._createbuttons()
   
        #On initialise les différents attributs
        self.firstName=None
        self.lastName=None
        self.x=None
        self.y=None
        self.show()
    def _createbuttons(self):
        #On définit la taille de la police
        font = QFont()
        font.setPointSize(11)

        #On créer les boutons/combobox/champs/labels

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QRect(140, 30, 111, 23))
        self.comboBox.setFont(font)
        self.comboBox.addItems(["Candidate","Voter"])


        self.label_1 = QLabel(self)
        self.label_1.setGeometry(QRect(20, 30, 91, 20))
        self.label_1.setFont(font)
        self.label_1.setText("Participant :")

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(20, 60, 91, 20))
        self.label_2.setFont(font)
        self.label_2.setText("First Name :")

        self.lineEditFirstname = QLineEdit(self)
        self.lineEditFirstname.setGeometry(QRect(120, 60, 161, 23))
        self.lineEditFirstname.setFont(font)

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(20, 90, 91, 20))
        self.label_3.setFont(font)
        self.label_3.setText("Last Name :")

        self.lineEditLastname = QLineEdit(self)
        self.lineEditLastname.setGeometry(QRect(120, 90, 161, 23))
        self.lineEditLastname.setFont(font)

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(20, 130, 241, 16))
        self.label_4.setText("Position :        (            ,            )")
        self.label_4.setFont(font)

        self.posx = QLineEdit(self)
        self.posx.setGeometry(QRect(140, 130, 41, 23))
        self.posx.setFont(font)
   
        self.posy = QLineEdit(self)
        self.posy.setGeometry(QRect(200, 130, 41, 23))
        self.posy.setFont(font)
        


        
    

                     
            

       
      

        
     

    


