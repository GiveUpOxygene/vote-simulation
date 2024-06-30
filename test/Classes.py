from PyQt5.QtCore import pyqtSignal,QRect
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QComboBox,QLabel
from PyQt5.QtGui import QIcon,QFont    

"""Regroupe l'Ensemble des classes contenues dans le répertoire classes"""

class Participant :
    """
    Classe définissant un Participant caractérisée par :
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
        - une liste pos de coordonnées [x,y] correspondant à la positions du Participant
    """
    def __init__ (self,firstName, lastName, x, y) :
        """ str x str x int x int x bool-> Participant
        constructeur de participant
        """
        self.firstName = firstName
        self.lastName = lastName
        self.pos=[int(x),int(y)]

    def __repr__(self) :
        """ -> str
        renvoie une description du Participant sous la forme d'une chaîne
        de caractères contenant son Prénom et son Nom
        elle permet d'utiliser print pour les participants
        """

        return self.firstName+" "+self.lastName


    def __eq__(self, other) :
        """ Val -> bool
        rend le booléen vrai si le participant est égal à other, faux sinon
        elle permet que == fonctionne pour les participants
        Attention : ne teste que type et identifiant !
        """
        return type(self) == type(other) and self.id == other.id
    
    def move(self,x,y):
        """int x int ->None
        déplace le participant aux coordonnées [x,y]"""
        self.pos[0]=x
        self.pos[1]=y

    @staticmethod

    def nextId():
        """->str
        renvoie l'id du prochain participant créé"""
        return str(Participant.idCounter+1)

class Candidate(Participant) :
    """
    Classe définissant un Candidat caractérisée par :
        - un identifiant
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
        - un flottant vote correspondant au vote reçu / points reçu
    """
    idCounter=0
    def __init__ (self, firstName, lastName, x, y, score=0) :
        """ str x str x int x int-> Candidate
        constructeur de candidat
        """
        super().__init__(firstName, lastName, x, y)
        Candidate.idCounter+=1
        self.id=Candidate.idCounter
        self.label = "Candidate_n° "+str(self.id)
        self.score=score
    
    def __repr__(self) :
        """ -> str
        renvoie une description du candidat sous la forme d'une chaîne
        de caractères contenant son id, son Prénom et son Nom
        elle permet d'utiliser print pour les candidats
        """

        return self.label+" "+super().__repr__()+" [ "+str(self.pos[0])+" , "+str(self.pos[1])+" ]"

    def __eq__(self, other) :
        """ Val -> bool
        rend le booléen vrai si le candidat est égal à other, faux sinon
        elle permet que == fonctionne pour les candidats
        Attention : ne teste que type et identifiant !
        """
        return type(self) == type(other) and self.id == other.id
    
    def voted(self,n=1):
        """->None
        On ajoute n à l'attribut score"""
        self.score+=n
    
    def resetVote(self):
        """->None
        l'attribue score est réinitialisé à 0"""
        self.score=0
    
    @staticmethod

    def nextId():
        """->str
        renvoie l'id du prochain participant créé"""
        return str(Candidate.idCounter+1)

class Voter(Participant) :
    """
    Classe définissant Votant caractérisée par :
        - un identifiant
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
        - un booléen hasVoted égale à True si le votant a voté, False sinon
    """
    idCounter=0
    def __init__ (self, firstName, lastName, x, y, hasVoted=False) :
        """ str x str x int x int-> Votant
        constructeur de votant
        """
        super().__init__(firstName, lastName, x, y)
        Voter.idCounter+=1
        self.id=Voter.idCounter
        self.label="Votant_n° "+str(self.id)
        self.hasVoted=hasVoted
   
    def __repr__(self) :
        """ -> str
        renvoie une description du votant sous la forme d'une chaîne
        de caractères contenant son id, son Prénom,son Nom et sa position
        elle permet d'utiliser print pour les votants
        """

        return self.label+" "+super().__repr__()+" [ "+str(self.pos[0])+" , "+str(self.pos[1])+" ]"
    
    def __eq__(self, other) :
        """ Val -> bool
        rend le booléen vrai si le votant est égal à other, faux sinon
        elle permet que == fonctionne pour les votants
        Attention : ne teste que type et identifiant !
        """
        return type(self) == type(other) and self.id == other.id
    
    def voteFor(self,candidate,n=1):
        """Candidate->None
        le candidat reçoit n vote et l'attribut hasVoted prend la valeur True"""
        candidate.voted(n)
        self.toVote()

    def toVote(self):
        """->None
        Le booléen hasVoted prend la valeur True"""
        self.hasVoted=True

    def resethasVoted(self):
        """->None
        Le booléen hasVoted prend la valeur False """
        self.hasVoted=False

    @staticmethod

    def nextId():
        """->str
        renvoie l'id du prochain participant créé"""
        return str(Voter.idCounter+1)

class ParticipantCreator(QWidget):
    """Fenêtre de création de participant"""
    def __init__(self,menu):
        super().__init__(menu)
        self.menu=menu
        #On initialise la fenêtre
        self.setWindowTitle("Créer un Participant")
        self.resize(314, 194)
        #On ajoute les boutons/labels/comboBox
        self._createbuttons()
        self.Buttoncreate.clicked.connect(self.create)
        self.show()
    def _createbuttons(self):
        #On définit la taille de la police
        font = QFont()
        font.setPointSize(11)

        #On créer les boutons/combobox/champs/labels

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QRect(130, 30, 110, 23))
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
        self.lineEditFirstname.setGeometry(QRect(120, 60, 120, 23))
        self.lineEditFirstname.setFont(font)
        self.lineEditFirstname.setObjectName("lineEditFirstname")

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(20, 90, 91, 20))
        self.label_3.setFont(font)
        self.label_3.setText("Last Name :")

        self.lineEditLastname = QLineEdit(self)
        self.lineEditLastname.setGeometry(QRect(120, 90, 120, 23))
        self.lineEditLastname.setFont(font)

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(15, 130, 241, 16))
        self.label_4.setText("Position :        (           ,          )")
        self.label_4.setFont(font)

        self.posx = QLineEdit(self)
        self.posx.setGeometry(QRect(135, 125, 38, 23))
        self.posx.setFont(font)
   
        self.posy = QLineEdit(self)
        self.posy.setGeometry(QRect(190, 125, 38, 23))
        self.posy.setFont(font)

        self.Buttoncreate = QPushButton("Create",self)
        self.Buttoncreate.setGeometry(QRect(160, 167, 80, 23))
        self.Buttoncreate.setFont(font)

    def create(self):
        firstname=self.lineEditFirstname.text()
        lastname=self.lineEditLastname.text()
        newx=self.posx.text()
        newy=self.posy.text()
        if ((firstname!="") and (lastname!="")) and ((newx!="") and (newy !="")) :
            if self.comboBox.currentText()=="Candidate":
                self.newCandidate=Candidate(firstname,lastname,newx,newy)
                self.menu.addCandidate(self.newCandidate)
            else:
                self.newVoter=Voter(firstname,lastname,newx,newy)
                self.menu.addVoter(self.newVoter)
            self.menu.refreshStatusBar()
            self.menu.pt=ParticipantTable(self.menu.centralArea,self.menu.dictcandidates,self.menu.dictvoters)

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

class Dialog(QDialog):
    donnees = pyqtSignal(list)
    def __init__(self,act):
        QWidget.__init__(self)

        # création du champ de texte
        self.champ = QLineEdit()
        # création des boutons
        self.bouton_action= QPushButton(act)
        self.bouton_cancel = QPushButton("Cancel")
        # on connecte le signal "clicked" à la méthode "appui_bouton_action"
        self.bouton_action.clicked.connect(self.action)
        self.bouton_cancel.clicked.connect(self.cancel)
 
        # mise en place du gestionnaire de mise en forme
        layout = QHBoxLayout()
        layout.addWidget(self.champ)
        layout.addWidget(self.bouton_action)
        layout.addWidget(self.bouton_cancel)
        self.setLayout(layout)
        self.setWindowTitle(act)
    
    def action(self):
        self.donnees.emit([self.champ.text()])
        self.close()
    def cancel(self):
        self.donnees.emit([None])
        self.close()

class ParticipantTable(QWidget):
    def __init__(self,area,candidates,voters,mode=None):
        super(ParticipantTable,self).__init__(area)
        self.setWindowTitle("Candidate_Table")
        self.setWindowIcon(QIcon("./pictures/icon.png"))
        self.setGeometry(QRect(930,300, 504, 500))
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
        self.tableWidget.setGeometry(QRect(0, 0, 504, 500))
        self.tableWidget.setColumnCount(6)
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
        self.tableWidget.setColumnWidth(0,80)
        self.tableWidget.setColumnWidth(1,50)
        self.tableWidget.setColumnWidth(2,110)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,78)
        self.tableWidget.setColumnWidth(5,70)
        self.loaddata(self.candidates,self.voters)
        

    def setVoterMode(self):
        self.mode="Voter"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 504, 500))
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
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,142)
        self.tableWidget.setColumnWidth(3,110)
        self.tableWidget.setColumnWidth(4,100)
        self.loaddata(self.candidates,self.voters)

    def setCandidateMode(self):
        self.mode="Candidate"
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(0, 0, 504, 500))
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
        item = QTableWidgetItem("Score")
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,145)
        self.tableWidget.setColumnWidth(2,125)
        self.tableWidget.setColumnWidth(3,98)
        self.tableWidget.setColumnWidth(4,70)
        self.loaddata(self.candidates,self.voters)

    def loaddata(self,candidates,voters):
        if self.mode=="Participant": 
            row=0
            self.tableWidget.setRowCount(len(candidates)+len(voters))
            for (k,v) in candidates.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem("Candidate"))
                self.tableWidget.setItem(row,1,QTableWidgetItem(str(v.id)))
                self.tableWidget.setItem(row,2,QTableWidgetItem(v.firstName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(v.lastName))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(v.pos)))
                self.tableWidget.setItem(row,5,QTableWidgetItem(str(v.score)))
                row+=1
            for (k,w) in voters.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem("Voter"))
                self.tableWidget.setItem(row,1,QTableWidgetItem(str(w.id)))
                self.tableWidget.setItem(row,2,QTableWidgetItem(w.firstName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(w.lastName))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(w.pos)))
                row+=1
        if self.mode=="Candidate":
            row=0
            self.tableWidget.setRowCount(len(candidates))
            for (k,v) in candidates.items():
                self.tableWidget.setItem(row,0,QTableWidgetItem(str(v.id)))
                self.tableWidget.setItem(row,1,QTableWidgetItem(v.firstName))
                self.tableWidget.setItem(row,2,QTableWidgetItem(v.lastName))
                self.tableWidget.setItem(row,3,QTableWidgetItem(str(v.pos)))
                self.tableWidget.setItem(row,4,QTableWidgetItem(str(v.score)))
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

        