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
"""Regroupe l'Ensemble des Classes utilisées dans l'application (Participants, Candidats, Votants et toutes les Classes fenêtres)"""

#---------------Classe Candidats/Votants---------------#

class Participant :
    """
    Classe définissant un Participant caractérisée par :
        - firstName : une chaîne de caractère correspondant au Prénom
        - lastName : une chaîne de caractère correspondant au Nom
        - pos : une liste de coordonnées [x,y] correspondant à la positions du Participant
    """
    def __init__ (self,firstName, lastName, x, y) :
        """ str * str * int * int * bool-> Participant
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
        """int * int ->None
        déplace le participant aux coordonnées [x,y]"""
        self.pos[0]=max(min(x,400),-400) #Pour que le point reste toujours dans le repère
        self.pos[1]=max(min(y,400),-400)

class Candidate(Participant) :
    """
    Classe définissant un Candidat caractérisée par :
<<<<<<< HEAD
        - id : un identifiant
        - fistName : une chaîne de caractère correspondant au Prénom
        - lastName : une chaîne de caractère correspondant au Nom
        - score : un flottant correspondant au vote reçu / points reçu
        - mu : une "métrique utilitariste"
        - budget : un budget donné par : 1/3 * max(|c_i - c_j|)
        - att_budget : un budget d'attaque
        - def_budget : un budget de défense
=======
        - un identifiant
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
        - un flottant score correspondant au vote reçu / points reçu
        - une "métrique utilitariste"
        - un budget donné par : 1/3 * max(|c_i - c_j|)
>>>>>>> 6c9b2f981ef78f1817b63fc6d54d7a0fbf9301ae
    """
    idCounter=0
    def __init__ (self, firstName, lastName, x, y, score=0) :
        """ str * str * int * int-> Candidate
        constructeur de candidat
        """
        super().__init__(firstName, lastName, x, y)
        Candidate.idCounter+=1
        self.id=Candidate.idCounter
        self.label = "Candidate_n° "+str(self.id)
        self.score=score
        self.mu = -1
        self.budget = -1
        self.att_budget = -1
        self.def_budget = -1
    
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
    
    def calculate_mu(self, voters:dict):
        """->None
        Calcule la mesure utilitariste du candidat en fonction des votants
        mu = 1/n² * sum(|c_i - v_j|²)
        coorespond au carré de la distance moyenne des votants par rapport au candidat
        avec :
        - n le nombre de votants
        - c_i la position du candidat
        - v_j la position du votant
        ----------
        Args:
            voters (dict): _description_
        """
        n=len(voters)
        if n==0:
            self.mu=0
            return None
        somme = 0
        for (_,voter) in voters.items():
            somme += np.linalg.norm(np.array(self.pos) - np.array(voter.pos))*np.linalg.norm(np.array(self.pos) - np.array(voter.pos))
        self.mu = somme/(n*n)
        
        
    def calculate_budget(self, candidates:dict):
        """->None
        Calcule le budget du candidat en fonction des autres candidats
        budget = 1/3 * max(|c_i - c_j|)
        avec :
        - c_i la position du candidat
        - c_j la position d'un autre candidat
        -----------
        Args:
            candidates (dict): _description_
        """
        max = -1
        for (_,cand) in candidates.items():
            if cand != self:
                dist = np.linalg.norm(np.array(self.pos) - np.array(cand.pos))
                if dist > max:
                    max = dist
        self.budget = max/3
        
    def attack(self, candidates:dict):
        """Dict[Candidate]->Bool
        Bouge aléatoirement un candidat dans un certain rayon défini par son budget d'attaque
        renvoie False si aucun candidat à sa portée, True sinon
        
        Args:
            candidates (dict): dictionnaire des candidats, généralement self.dictcandidates dans le main
        """
        #On créer la liste de tous les candidats dans le rayon défini par le budget d'attaque du candidat
        close_cands = [] 
        for (_,cand) in candidates.items():
            if cand != self and np.linalg.norm(np.array(self.pos) - np.array(cand.pos)) <= self.att_budget:
                close_cands.append(cand)

        #On vérifie qu'il y a bien des candidats à portée
        if len(close_cands)==0:
            return False
        
        #On prend un candidat aléatoirement dans close_cands
        cand = close_cands[np.random.randint(0,len(close_cands))]

        # On déplace ce candidat
        cand.move(np.random.randint(self.pos[0]-self.att_budget,self.pos[0]+self.att_budget),np.random.randint(self.pos[1]-self.att_budget,self.pos[1]+self.att_budget))
        return True
    def defend(self, candidates:dict, voters:dict):
        """->None
        
        Bouge le candidat pour gagner le plus de voix possibles dans un cercle de rayon défini par son budget de défense.

        Args:
            candidates (dict): dictionnaire des candidats, généralement self.dictcandidates dans le main
        """
        positions=list(pos_r_set(self.pos[0],self.pos[1],int(self.def_budget)))
        n=len(positions)//50
        positions=positions[:50*n:n]

        ##Pour obtenir un nombre de positions à tester raisonnable, (10) on va convertir cet ensemble en liste puis la mélanger et tester que les 20 premières positions
        bestpos=self.pos
        self.calculate_mu(voters)
        bestMU=self.mu
        #bestscore=testposition(candidates, voters, self.id) #Position avec le meilleur résultat pour un vote plural
        for x,y in positions:
            self.move(x,y)
            self.calculate_mu(voters)
            testMU=self.mu
            #testscore=testposition(candidates, voters, self.id) #Position avec le meilleur résultat pour un vote plural
            if self.mu<bestMU: #> pour le score
                bestpos=[x,y]
                bestMU=self.mu
                #bestscore=testscore
        self.pos=bestpos

    def voted(self,n=1):
        """->None
        On ajoute n à l'attribut score"""
        self.score+=n
    
    def resetVote(self):
        """->None
        l'attribue score est réinitialisé à 0"""
        self.score=0
    
    def name(self):
        """->str 
        retourne le nom abrégé du participant sous la forme premiere lettre du prenom + point + nom du candidat"""
        return self.firstName[0]+". "+self.lastName

    @staticmethod

    def nextId():
        """->str
        renvoie l'id du prochain Candidat créé"""
        return str(Candidate.idCounter+1)

class Voter(Participant) :
    """
    Classe définissant Votant caractérisée par :
<<<<<<< HEAD
        - id : un identifiant
        - firstName : une chaîne de caractère correspondant au Prénom
        - lastName : une chaîne de caractère correspondant au Nom
        - weight :une chaîne de caractère correspond au poid de vote, correspond aux votes cumulés que le votant a pu recevoir
=======
        - un identifiant
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
>>>>>>> 6c9b2f981ef78f1817b63fc6d54d7a0fbf9301ae
    """
    idCounter=0
    def __init__ (self, firstName, lastName, x, y) :
        """ str * str * int * int-> Votant
        constructeur de votant
        """
        super().__init__(firstName, lastName, x, y)
        Voter.idCounter+=1
        self.id=Voter.idCounter
        self.label="Votant_n° "+str(self.id)
        self.weight=1 #Poid de vote du candidat initialisé à 1
   
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

    def delegate(self,voter):
        """Voter -> None
        Le votant délégue son/ses vote(s) au votant voter placé en parametre"""
        voter.weight+=self.weight
        self.weight=0

    @staticmethod

    def nextId():
        """->str
        renvoie l'id du prochain votant créé"""
        return str(Voter.idCounter+1)


#---------------Widgets---------------#

class MyBar(QWidget):
    """Barre de Titre personnalisée"""
    clickPos = None
    def __init__(self, parent):
        super(MyBar, self).__init__(parent)
        self.resizable=True
        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        self.pix=(QPixmap(os.path.dirname(__file__) + "/pictures/icons/icon3.png")).scaledToHeight(34)
        self.image=QLabel(self)
        self.image.setGeometry(QRect(0,0,self.pix.width(),self.pix.height()))
        self.image.setPixmap(self.pix)
        layout.addWidget(self.image)
        layout.addStretch()

        self.title = QLabel("My Own Bar", self, alignment=Qt.AlignCenter)

        style = self.style()
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PM_ButtonMargin) * 2
        self.setMaximumHeight(ref_size + 2)

        btn_size = QSize(ref_size, ref_size)
        icons=dict()
        icons["min"]=QIcon(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/classic/iconMinimize.png")
        icons["normal"]=QIcon(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/classic/iconRestore.png")
        icons["max"]=QIcon(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/classic/iconRestore2.png")
        icons["close"]=QIcon(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/classic/iconClose2.png")

        for target in ('min', 'normal', 'max', 'close'):
            btn = QToolButton(self, focusPolicy=Qt.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)

            iconType = getattr(style, 
                'SP_TitleBar{}Button'.format(target.capitalize()))
            btn.setIcon(icons[target])

            if target == 'close':
                colorNormal = "white"
                colorHover = "#ff8a8a"
            else:
                colorNormal = "white"
                colorHover = "#dadfe5"
            btn.setStyleSheet('''
                QToolButton {{
                    background-color: {};
                    border: none
                }}
                QToolButton:hover {{
                    background-color: {};
                }}
            '''.format(colorNormal, colorHover))

            signal = getattr(self, target + 'Clicked')
            btn.clicked.connect(signal)

            setattr(self, target + 'Button', btn)

        self.normalButton.hide()

        self.updateTitle(parent.windowTitle())
        parent.windowTitleChanged.connect(self.updateTitle)
        self.isNormal=True

    def updateTitle(self, title=None):
        if title is None:
            title = self.window().windowTitle()
        width = self.title.width()
        width -= self.style().pixelMetric(QStyle.PM_LayoutHorizontalSpacing) * 2
        self.title.setText(self.fontMetrics().elidedText(
            title, Qt.ElideRight, width))

    def windowStateChanged(self, state):
        self.normalButton.setVisible(state == Qt.WindowMaximized)
        self.maxButton.setVisible(state != Qt.WindowMaximized)
        

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPos = event.windowPos().toPoint()
    
    def mouseDoubleClickEvent(self, event):
        if self.resizable:
            if event.button() == Qt.LeftButton:
                if  self.isNormal:
                    self.window().showMaximized()
                    self.isNormal=False
                else :
                    self.window().showNormal()
                    self.isNormal=True
            
        
            
    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            self.window().move(QPoint(event.globalPos().x() - self.clickPos.x(),event.globalPos().y() -58))

    def mouseReleaseEvent(self, QMouseEvent):
        self.clickPos = None

    def closeClicked(self):
        self.window().close()

    def maxClicked(self):
        self.isNormal=False
        self.window().showMaximized()

    def normalClicked(self):
        self.isNormal=True
        self.window().showNormal()

    def minClicked(self):
        self.window().showMinimized()

    def resizeEvent(self, event):
        self.title.resize(self.minButton.x(), self.height())
        self.updateTitle()

class ViewResults(FigureCanvasQTAgg):
    """Graphique des résultats des élections"""
    def __init__(self, menu=None,candidates=None,voters=None,width=5, height=4, dpi=100):
        if candidates==None:
            candidates=menu.dictcandidates
        if voters==None:
            voters=menu.dictvoters
        scores=[c.score for (k,c) in candidates.items()]
        names=[c.name() for (k,c) in candidates.items()]
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes= fig.add_subplot(111)
        super(ViewResults, self).__init__(fig)
        self.axes.set_title("Election Results")
        self.axes.set_xlabel("Candidates")
        self.axes.set_ylabel("Scores")
        if(len(candidates)>10):
            self.axes.tick_params(axis="x", labelrotation=45)
        p=self.axes.bar(names, scores,label=scores, color = cm.rainbow(np.linspace(0, 1, len(candidates))))
        self.axes.bar_label(p, padding=3)

class ParticipantCreator(QWidget):
    """Fenêtre de création de participant"""
    def __init__(self,menu):
        super().__init__(menu.home)
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
        self.label_4.setGeometry(QRect(20, 130, 241, 16))
        self.label_4.setText("Position :        (          ,          )")
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
        newx=int(self.posx.text())
        newy=int(self.posy.text())
        
        if (((firstname!="") and (lastname!="")) and ((newx!="") and (newy !=""))) and goodPosition(newx,newy):
            if self.comboBox.currentText()=="Candidate":
                self.newCandidate=Candidate(firstname,lastname,newx,newy)
                self.newCandidate.calculate_mu(self.menu.dictvoters)
                self.menu.addCandidate(self.newCandidate)
                
            else:
                self.newVoter=Voter(firstname,lastname,newx,newy)
                self.menu.addVoter(self.newVoter)
                self.menu.refreshMU()
            self.menu.refreshStatusBar()
            self.menu.pt=ParticipantTable(self.menu.home,self.menu.dictcandidates,self.menu.dictvoters)

class ParticipantGenerator(QWidget):
    """Fenêtre de génération de participants"""
    def __init__(self,menu=None):
        super().__init__(menu.home)
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
        for _ in range(int(self.lineEditVoterNumber.text())):
            newVoter=self.menu.randomParticipant(False,mode=self.menu.distribution)
            self.menu.addVoter(newVoter)
  
        for _ in range(int(self.lineEditCandidateNumber.text())):
            newCandidate=self.menu.randomParticipant(True,mode=self.menu.distribution)
            self.menu.addCandidate(newCandidate)

        self.menu.refreshMU()
        self.menu.refreshStatusBar()
        self.menu.pt=ParticipantTable(self.menu)

class ParticipantTable(QWidget):
    """Tableau des participants"""
    def __init__(self,menu,mode=None):
        super(ParticipantTable,self).__init__(menu.home)
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
   
class Drawing(QWidget):
    def __init__(self,menu):
        super().__init__(menu.home)
        self.menu=menu
        self.pix=(QPixmap(os.path.dirname(__file__) + "/pictures/axes.png")).scaledToHeight(800)
        self.image=QLabel(self)
        self.image.setStyleSheet("background-color: {};border: 1px solid;border-color: #dadfe5;".format(self.menu.backgroundColor))
        self.image.setGeometry(QRect(0,0,self.pix.width(),self.pix.height()))
        self.image.setPixmap(self.pix)

    def mousePressEvent(self,event):
        """Méthode appelée lors du click de la souris"""
        if event.buttons() == Qt.LeftButton :
            if not(self.menu.place_voters):
                c=self.menu.randomParticipant(True,self.coord_to_pos(x=event.x()),self.coord_to_pos(y=event.y()))
                c.calculate_mu(self.menu.dictvoters)
                self.menu.addCandidate(c)
                
            else:
                self.menu.addVoter(self.menu.randomParticipant(False,self.coord_to_pos(x=event.x()),self.coord_to_pos(y=event.y())))
                self.menu.refreshMU()
            self.menu.refreshTab()
            self.menu.refreshStatusBar()
            
            
    def coord_to_pos(self,x=None,y=None):
        if x==None:
            return 400-y
        if y==None:
            return x-400
        else:
            return (x-400,400-y) 
    
    def pos_to_coord(self,x=None,y=None):
        if x==None:
            return 400-y
        if y==None:
            return x+400
        else:
            return (x+400,400-y) 
        
    def paintEvent(self, event):
        painter = QPainter(self)
        self.image.setPixmap(self.pix)
         
    
    def drawEllipse(self,x,y,color,size):
        painter = QPainter(self.pix)
        painter.setPen(QPen(QColor(color), 0, Qt.SolidLine))
        painter.setBrush(QColor(color))
        x2=self.pos_to_coord(x=x)
        y2=self.pos_to_coord(y=y)
        painter.drawEllipse(QPoint(x2,y2),size,size)
        painter.end()

    
    def setBackgroundColor(self):
        self.image.setStyleSheet("background-color: {};".format(self.menu.backgroundColor))

    def reset(self):
        self.pix=(QPixmap(os.path.dirname(__file__) + "/pictures/axes.png")).scaledToHeight(800)
        self.image.setPixmap(self.pix)
        self.setBackgroundColor()

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
        self.setGeometry(QRect(300,200,725,self.titleBar.height()+nb*19+100))
        self.texte = QLabel(self)
        self.texte.setGeometry(QRect(90, 50+self.titleBar.height(), 628, 17*nb+15))
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

class ElectionGenerator(QWidget):
    def __init__(self,menu):
        super().__init__(menu.home)
        self.setGeometry(QRect(0,0,275,138))
        self.menu=menu
        font = QFont()
        font.setPointSize(11)
        self.comboBoxVotingRules = QComboBox(self)
        self.comboBoxVotingRules.setGeometry(QRect(5, 0, 100, 23))
        self.comboBoxVotingRules.setFont(font)
        self.comboBoxVotingRules.addItems(["Plurality","Borda","Veto","Approval","Copeland","Simpson","Two-Round Majority","Alternative Vote","Nanson","Coombs","Liquid Democracy"])
        self.ButtonGenerateVotes = QPushButton("Generate Votes",self)
        self.ButtonGenerateVotes.setGeometry(QRect(0, 40, 140, 23))
        self.ButtonGenerateVotes.setFont(font)
        self.ButtonResetScores = QPushButton("Reset Scores",self)
        self.ButtonResetScores.setGeometry(QRect(160, 40, 115, 23))
        self.ButtonResetScores.setFont(font)
        self._connect()
    def _connect(self):
        self.ButtonGenerateVotes.clicked.connect(self.generateVotes)
        self.ButtonResetScores.clicked.connect(self.menu.resetScores)

    def generateVotes(self):
        if len(self.menu.dictcandidates)<=0:
            return None
        self.menu.winners=set()
        n=1
        if (self.comboBoxVotingRules.currentText()=="Plurality"):
            self.menu.pluralityContent()
        elif(self.comboBoxVotingRules.currentText()=="Borda"):
            self.menu.bordaContent()
        elif(self.comboBoxVotingRules.currentText()=="Veto"):
            self.menu.vetoContent()
            n=-1
        elif(self.comboBoxVotingRules.currentText()=="Approval"):
            self.menu.approvalContent()
        elif(self.comboBoxVotingRules.currentText()=="Copeland"):
            self.menu.copelandContent()
        elif(self.comboBoxVotingRules.currentText()=="Simpson"):
            self.menu.simpsonContent()
        elif(self.comboBoxVotingRules.currentText()=="Two-Round Majority"):
            self.menu.maj2TurnsContent()
        elif(self.comboBoxVotingRules.currentText()=="Alternative Vote"):
            self.menu.avContent()
        elif(self.comboBoxVotingRules.currentText()=="Nanson"):
            self.menu.nansonContent()
        elif(self.comboBoxVotingRules.currentText()=="Coombs"):
            self.menu.coombsContent()
            #Le gagnant est celui avec le nombre de vote le moins élevé
            n=0
        elif(self.comboBoxVotingRules.currentText()=="Liquid Democracy"):
            self.menu.liquidDemocracyContent()

        self.menu.refreshTab()
        #On affiche le(s) gagnant(s) des élections
        self.menu.refreshImage()
        winnerpointsize=max(self.menu.candidatePointsize*2,self.menu.candidatePointsize+30)
        if n!=0:
            self.menu.winners=winners(self.menu.dictcandidates,n)
        for id in self.menu.winners:
            self.menu.image.drawEllipse(self.menu.dictcandidates[id].pos[0],self.menu.dictcandidates[id].pos[1],self.menu.candidateColor,winnerpointsize)


    
    
    



    
