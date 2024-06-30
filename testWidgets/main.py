import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect
from PyQt5.QtWidgets import QMainWindow,QApplication,QStyleFactory,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette    
from numpy import random
import time
from Classes import *
from votes import *

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        #Création de la fenêtre principale
        self.name="New_file"
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon("./pictures/icon.png"))
        self.setGeometry(135,50,1600, 900)

        #Création style par défaut
        self.backgroundColor="#ffffff"
        self.candidateColor=QColor(255,0,0)
        self.voterColor=QColor(0,0,255)
        self.pointsize=5

        self.resetParticipants() #Initialisation des candidats et votants
        

        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self._createCentralArea()
        self._connectCentralArea()
        self.show()



    def reset(self):
        self.resetParticipants()
        self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        self.nbCandidat.setText("Number of candidates : "+str(len(self.dictcandidates)))
        self.nbVoter.setText("Number of voters : "+str(len(self.dictvoters)))
        self.pix=QPixmap("./pictures/axes.png")
        self.image.setPixmap(self.pix)
        self.backgroundColor="#ffffff"
        self.centralArea.setStyleSheet("background: "+self.backgroundColor)
        self.candidateColor=QColor(255,0,0)
        self.voterColor=QColor(0,0,255)
        self.pointsize=5
        self.update()
        
    #-------Events-------#
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pix)
        self.image.setPixmap(self.pix)
        

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and (int(event.x())<=self.pix.width() and int(event.y())<=self.pix.height()):
            if not(self.place_voters):
                self.addCandidate(self.randomParticipant(True,x=event.x(),y=event.y()-20))
                self.IdCandidates += 1
            else:
                self.addVoter(self.randomParticipant(False,x=event.x(),y=event.y()-20))
                self.IdVoters += 1

    #-------End Events-------#
    #-------Reset Participant-------#
    def resetParticipants(self):
        self.dictcandidates = dict()
        self.IdCandidates = 0
        self.dictvoters = dict()
        self.IdVoters = 0
        self.place_voters = False
        Participant.idCounter=0
    #-------Central Area-------#
    def _createCentralArea(self):
                # Le type QWidget représente un conteneur de widgets (et il est lui-même un widget).
        # On crée une instance que l'on va mettre au centre de la fenêtre.
        self.centralArea = QWidget()
        # On met l'arrière-plan en blanc 
        self.centralArea.setStyleSheet("background: "+self.backgroundColor)
        # On injecte ce widget en tant que zone centrale.
        self.setCentralWidget(self.centralArea)
        

        #Dessin
        self.pix=QPixmap("./pictures/axes.png")
        self.image=QLabel(self.centralArea)
        self.image.setGeometry(QRect(0,0,self.pix.width(),self.pix.height()))
        self.image.setPixmap(self.pix)
    
        #Creation Participant
        self.cp=CreateParticipant(self)
        self.cp.move(930,60)
        self.Buttoncreate = QPushButton("Create",self.centralArea)
        self.Buttoncreate.setGeometry(QRect(1140, 215, 80, 23))
        font = QFont()
        font.setPointSize(11)
        self.Buttoncreate.setFont(font)

        #Lancer Elections
        font = QFont()
        font.setPointSize(11)
        self.comboBoxVotingRules = QComboBox(self.centralArea)
        self.comboBoxVotingRules.setGeometry(QRect(950, 215, 100, 23))
        self.comboBoxVotingRules.setFont(font)
        self.comboBoxVotingRules.addItems(["Plurality","Borda","Veto","Approval"])
        self.ButtonGenerateVotes=QPushButton("Generate Votes",self.centralArea)
        self.ButtonGenerateVotes.setGeometry(QRect(945, 255, 140, 23))
        self.ButtonGenerateVotes.setFont(font)
        self.ButtonResetVotes=QPushButton("Reset Votes",self.centralArea)
        self.ButtonResetVotes.setGeometry(QRect(1105, 255, 115, 23))
        self.ButtonResetVotes.setFont(font)



        #Table View
        self.table = tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        self.nbCandidat=QLabel("Number of candidates : "+str(len(self.dictcandidates)),self.centralArea)
        self.nbCandidat.setGeometry(940,831,200,20)
        self.nbVoter=QLabel("Number of voters : "+str(len(self.dictvoters)),self.centralArea)
        self.nbVoter.setGeometry(1125,831,200,20)
        self.box1 = QCheckBox("Candidate",self.centralArea)
        self.box1.move(1300,828)
        self.box1.setChecked(True)
        self.box2 = QCheckBox("Voter",self.centralArea)
        self.box2.move(1400,828)
        self.box2.setChecked(True)
        self.ButtonrefreshTab = QPushButton("Refresh Tab",self.centralArea)
        self.ButtonrefreshTab.move(1480,828) 


    def _connectCentralArea(self):
        self.Buttoncreate.clicked.connect(self.create)
        self.ButtonGenerateVotes.clicked.connect(self.generateVotes)
        self.ButtonResetVotes.clicked.connect(self.resetVotes)
        self.ButtonrefreshTab.clicked.connect(self.refreshTab)
        
  
    
    #-------End Central Area-------#

    #-------Menus-------#


    def _createMenuBar(self):
        menuBar = self.menuBar()
        # File menu
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.randomSetAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.editbackgroundcolor)
        editMenu.addAction(self.editcandidatecolor)
        editMenu.addAction(self.editvotercolor)
        editMenu.addAction(self.editpointsize)
        editMenu.addAction(self.placeCandidateAction)
        editMenu.addAction(self.placeVoterAction)
        editMenu.addAction(self.deleteAction)
        # Votes menu
        votesMenu = menuBar.addMenu("&Méthodes de vote")
        ## Calcul des scores
        scoresMenu = votesMenu.addMenu("&Calcul des scores")
        scoresMenu.addAction(self.bordaAction)
        scoresMenu.addAction(self.pluralityAction)
        scoresMenu.addAction(self.vetoAction)
        scoresMenu.addAction(self.approbAction)
        ## Condorcet
        condorcetMenu = votesMenu.addMenu("&Condorcet")
        condorcetMenu.addAction(self.copelandAction)
        condorcetMenu.addAction(self.SimpsonAction)
        ## Plusieurs tours
        turnMenu = votesMenu.addMenu("&Plusieurs tours")
        turnMenu.addAction(self.VAAction)
        turnMenu.addAction(self.maj2TurnsAction)
        # Help menu
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)
        
    def _createActions(self):
        # Menu Résultats
        self.newAction = QAction("&New File", self)
        self.openAction = QAction("&Open File...", self)
        self.saveAction = QAction("&Save", self)
        self.saveAsAction = QAction("&Save As...", self)
        

        self.randomSetAction = QAction("&New Random Set (TO-DO)", self)
        self.exitAction = QAction("&Exit", self)
        # Menu Méthodes de vote
        self.bordaAction = QAction("&Borda",self)
        self.pluralityAction = QAction("&Plurality",self)
        self.vetoAction = QAction("&Veto",self)
        self.approbAction = QAction("&Approval",self)
        self.copelandAction = QAction("&Copeland",self)
        self.SimpsonAction = QAction("&Simpson",self)
        self.VAAction = QAction("&Vote alternatif",self)
        self.maj2TurnsAction = QAction("&Majorité à 2 tours",self)
        
        # Menu Edit
        self.editbackgroundcolor = QAction("&Background Color",self)
        self.editcandidatecolor = QAction("&Candidate Color",self)
        self.editvotercolor = QAction("&Voter Color",self)
        self.editpointsize = QAction("&Point Size",self)
        self.placeCandidateAction = QAction("&\U0001F534 Candidate", self)
        self.placeVoterAction = QAction("&\U0001F535 Voter", self)
        self.deleteAction = QAction("&Delete", self)
        # Menu Help
        self.helpContentAction = QAction("&Help Content (TO-DO)", self)
        self.aboutAction = QAction("&About (TO-DO)", self)
        
    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.saveAsAction.triggered.connect(self.saveAsFile)
        self.randomSetAction.triggered.connect(self.newSet)
        self.exitAction.triggered.connect(self.close)
        # Connect Votes actions
        self.bordaAction.triggered.connect(self.bordaContent)
        self.pluralityAction.triggered.connect(self.pluralityContent)
        self.vetoAction.triggered.connect(self.vetoContent)
        self.approbAction.triggered.connect(self.approbContent)
        self.copelandAction.triggered.connect(self.copelandContent)
        self.SimpsonAction.triggered.connect(self.SimpsonContent)
        self.VAAction.triggered.connect(self.VAContent)
        self.maj2TurnsAction.triggered.connect(self.maj2TurnsContent)
        # Connect Edit actions
        self.editbackgroundcolor.triggered.connect(self.backgroundcolorContent)
        self.editcandidatecolor.triggered.connect(self.candidatecolorContent)
        self.editvotercolor.triggered.connect(self.votercolorContent)
        self.editpointsize.triggered.connect(self.pointsizeContent)
        self.placeCandidateAction.triggered.connect(self.candidateContent)
        self.placeVoterAction.triggered.connect(self.voterContent)
        self.deleteAction.triggered.connect(self.deleteContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)
        

    #-------End Menus-------#
    
    #-------Menus functions-------#
    
    ## File
        
    def newFile(self):
        # Logic for creating a new file goes here...
        self.name="New_file"
        self.setWindowTitle(self.name)
        self.reset()
        print("<b>File > New</b> clicked")

    def openFile(self):
        # Logic for opening an existing file goes here...
        
        self.saisie("Open","recupName")
        file=open(self.name,"r")
        self.reset()

        #Lecture des élements du style
        line=file.readline()
        assert(line=="<style>\n")
        line=file.readline()
        words=line.split("\n")
        self.backgroundColor=words[0]
        self.centralArea.setStyleSheet("background: "+self.backgroundColor)
        line=file.readline()
        words=line.split("\n")
        self.candidateColor=QColor(words[0])
        line=file.readline()
        words=line.split("\n")
        self.voterColor=QColor(words[0])
        line=file.readline()
        words=line.split("\n")
        self.pointsize=int(words[0])
        line=file.readline()
        assert(line=="</style>\n")

        #Lecture des candidats
        line=file.readline()
        assert(line=="<candidates>\n")
        line=file.readline()
        while line!="</candidates>\n":
            words=line.split(" ")
            id=words[1]
            firstname=words[2]
            lastname=words[3]
            x=words[5]
            y=words[7]
            self.newCandidate=Candidate(firstname,lastname,x,y)
            self.addCandidate(self.newCandidate)
            line=file.readline()

        #Lecture des votants
        line=file.readline()
        assert(line=="<voters>\n")
        line=file.readline()    
        while line!="</voters>\n":
            words=line.split(" ")
            id=words[1]
            firstname=words[2]
            lastname=words[3]
            x=words[5]
            y=words[7]
            self.newVoter=Voter(firstname,lastname,x,y)
            self.addVoter(self.newVoter)
            line=file.readline()
        
        file.close()
        print("<b>File > Open...</b> clicked")

    def saveFile(self):
        if os.path.exists(self.name):
            file=open(self.name, "w")
            file.write("<style>\n")
            file.write(self.backgroundColor+"\n")
            file.write(self.candidateColor.name()+"\n")
            file.write(self.voterColor.name()+"\n")
            file.write(str(self.pointsize)+"\n")
            file.write("</style>\n")

            file.write("<candidates>\n")
            for (k,v) in self.dictcandidates.items():
                file.write(v.__repr__()+"\n")
            file.write("</candidates>\n")

            file.write("<voters>\n")
            for (k,v) in self.dictvoters.items():
                file.write(v.__repr__()+"\n")
            file.write("</voters>\n")

            file.close()
        else :
            self.saveAsFile()


    def saveAsFile(self):
        # Logic for saving an existing file goes here...
        self.saisie("Save","recupName")
        file=open(self.name, "w")
        file.close()
        self.saveFile()
        print("<b>File > Save As...</b> clicked")


    def newSet(self):
        self.reset()
        nb_candidates = 5
        nb_voters = 50
        #répartir aléatoirement avec numpy les candidats sur l'écran (en fonction de la taille de l'écran)
        for i in range(nb_candidates):
            newCandidate=self.randomParticipant(True)
            self.addCandidate(newCandidate)
        for i in range(nb_voters):
            newVoter=self.randomParticipant(False)
            self.addVoter(newVoter)
        print("<b>File > Save</b> clicked")

    def saisie(self,act,mode):
        """lancement de la fenêtre de dialogue pour la saisie de la tailrecupAle des points
        """
        self.dialog = Dialog(act)
        self.dialog.setGeometry(740,400,400,50)
        if(mode=="recupPointSize"):
            self.dialog.donnees.connect(self.recupPointSize) # prépare la récupération des données saisies
        elif(mode=="recupApprovalThreshold"):
            self.dialog.donnees.connect(self.recupApprovalThreshold)
        elif(mode=="recupName"):
            self.dialog.donnees.connect(self.recupName)

        self.dialog.exec_()

    def recupName(self, liste):
        """Récupération des infos
        """        
        # cache la fenêtre dialog encore affichée (elle sera fermée juste après)
        if liste!=[None]:
            self.name=liste[0]
            self.setWindowTitle(self.name)

    def recupPointSize(self, liste):
        """Récupération des infos
        """        
        # cache la fenêtre dialog encore affichée (elle sera fermée juste après)
        if liste!=[None]:
            self.pointsize=int(liste[0])

    def recupApprovalThreshold(self, liste):
        """Récupération des infos
        """        
        # cache la fenêtre dialog encore affichée (elle sera fermée juste après)
        if liste!=[None]:
            self.appprovalThreshold=int(liste[0])

    #-------Others functions-------#
    def create(self):
        firstname=self.cp.lineEditFirstname.text()
        lastname=self.cp.lineEditLastname.text()
        newx=self.cp.posx.text()
        newy=self.cp.posy.text()
        if ((firstname!="") and (lastname!="")) and ((newx!="") and (newy !="")) :
            if self.cp.comboBox.currentText()=="Candidate":
                self.newCandidate=Candidate(firstname,lastname,newx,newy)
                self.addCandidate(self.newCandidate)
            else:
                self.newVoter=Voter(firstname,lastname,newx,newy)
                self.addVoter(self.newVoter)
            firstname=""
            lastname=""
            newx=""
            newy=""
    def generateVotes(self):
        if (self.comboBoxVotingRules.currentText()=="Plurality"):
            plurality(self.dictcandidates,self.dictvoters)
            self.dictcandidates=rating(self.dictcandidates)
            self.refreshTab()
        elif(self.comboBoxVotingRules.currentText()=="Borda"):
            borda(self.dictcandidates,self.dictvoters)
            self.dictcandidates=rating(self.dictcandidates)
            self.refreshTab()
        elif(self.comboBoxVotingRules.currentText()=="Veto"):
            veto(self.dictcandidates,self.dictvoters)
            self.dictcandidates=rating(self.dictcandidates)
            self.refreshTab()
        elif(self.comboBoxVotingRules.currentText()=="Approval"):
            self.appprovalThreshold=1
            self.saisie("Set Threshold","recupApprovalThreshold")
            approval(self.dictcandidates,self.dictvoters,self.appprovalThreshold)
            self.dictcandidates=rating(self.dictcandidates)
            self.refreshTab()
    
    def resetVotes(self):
        resetElections(self.dictcandidates,self.dictvoters)
        self.refreshTab()


    def refreshTab(self):
        if (self.box1.isChecked() and self.box2.isChecked()):
            self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        elif (self.box1.isChecked()):
            self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters,"Candidat")
        elif (self.box2.isChecked()):
            self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters,"Voter")


    def randomParticipant(self,is_candidate,x=None,y=None):
            if x==None or y==None:
                x=random.randint(0, self.pix.width())
                y=random.randint(0, self.pix.width())
            firstname=firstNameGenerator()
            lastname=lastNameGenerator()
            if is_candidate==True:
                return Candidate(firstname,lastname,x,y)
            else:
                return Voter(firstname,lastname,x,y)
            
    def addCandidate(self,candidate):
        self.dictcandidates[candidate.id] = candidate
        self.IdCandidates += 1
        painter = QPainter(self.pix)
        painter.setPen(QPen(self.candidateColor, self.pointsize, Qt.SolidLine))
        painter.setBrush(self.candidateColor)
        painter.drawEllipse(candidate.pos[0],candidate.pos[1]-6,5,5)
        self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        self.nbCandidat.setText("Number of candidates : "+str(len(self.dictcandidates)))
        self.update()

    def addVoter(self,voter):
        self.dictvoters[voter.id] = voter
        self.IdVoters += 1
        painter = QPainter(self.pix)
        painter.setPen(QPen(self.voterColor, self.pointsize, Qt.SolidLine))
        painter.setBrush(self.voterColor)
        painter.drawEllipse(voter.pos[0],voter.pos[1],5,5)
        self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        self.nbVoter.setText("Number of voters : "+str(len(self.dictvoters)))
        self.update()

    def backgroundcolorContent(self):
        # opening color dialog
        color = QColorDialog.getColor()
        self.backgroundColor=color.name()
        self.centralArea.setStyleSheet("background: "+self.backgroundColor)
    
    def candidatecolorContent(self):
        self.candidateColor=QColorDialog.getColor()
        self.refreshImage()

    def votercolorContent(self):
        self.voterColor=QColorDialog.getColor()
        self.refreshImage()

    def pointsizeContent(self):
        self.saisie("Change Point Size","recupPointSize")
        self.refreshImage()
        
    
    def refreshImage(self):
        self.pix=QPixmap("./pictures/axes.png")
        for (k,v) in self.dictcandidates.items():
            painter = QPainter(self.pix)
            painter.setPen(QPen(self.candidateColor, self.pointsize, Qt.SolidLine))
            painter.setBrush(self.candidateColor)
            painter.drawEllipse(v.pos[0],v.pos[1],5,5)
            painter.end()
        for (k,v) in self.dictvoters.items():
            painter = QPainter(self.pix)
            painter.setPen(QPen(self.voterColor, self.pointsize, Qt.SolidLine))
            painter.setBrush(self.voterColor)
            painter.drawEllipse(v.pos[0],v.pos[1],5,5)
            painter.end()
        

    ## End File
    ## Votes
    def bordaContent(self):
        return
    
    def pluralityContent(self):
        return
    
    def vetoContent(self):
        return
    
    def approbContent(self):
        return
    
    def copelandContent(self):
        return
    
    def SimpsonContent(self):
        return
    
    def VAContent(self):
        return
    
    def maj2TurnsContent(self):
        return
    
    
    ## End Votes
    ## Edit

    def candidateContent(self):
        # Logic for pasting content goes here...
        self.place_voters = False
        print("Candidate clicked")

    def voterContent(self):
        # Logic for copying content goes here...
        self.place_voters = True
        print("Voter clicked")

    def deleteContent(self):
        self.reset()
        print("<b>Edit > Cut</b> clicked")
        
    ## End Edit
    ## Help

    def helpContent(self):
        print("Les votants sont en rouge, les candidats en bleu\n")

    def about(self):
        # Logic for showing an about dialog content goes here...
        print("<b>Help > About...</b> clicked")
    
    ## End Help
        
if __name__ == '__main__':
    #print(QStyleFactory.keys()) 
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainMenu = Menu()
    sys.exit(app.exec_())