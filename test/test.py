import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect,QSize
from PyQt5.QtWidgets import QStatusBar,QMainWindow,QToolBar,QApplication,QFileDialog,QStyleFactory,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette,QKeySequence
from numpy import random
import time
from Classes import *
from votes import *

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        #Change le style classic
        self.loadstyle()
        self.name="New_file.elct" #Nom du fichier
        self.filePath="./files/New_file.elct" #Chemin d'accès du fichier
        #Création de la fenêtre principale
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon("./pictures/icons/icon.png"))
        self.setGeometry(0,0,1910,985)

        #Création paramètres par défaut
        self.backgroundColor="#dadfe5"
        self.candidateColor="#ff0000"
        self.voterColor="#70afea"
        self.pointsize=7

        self.resetParticipants() #Initialisation des candidats et votants
        self._createActions()   
        self._createMenuBar()   #Création des menus
        self._connectActions()
        self._createToolBars()  #Création de la barre d'outil
        self._createStatusBar() #Création de la barre de statuts
        self._createCentralArea() #Création de la zone centrale
        self._connectCentralArea()
        self.show()

    def reset(self):
        self.resetParticipants()
        self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        self.pix=QPixmap("./pictures/axes.png")
        self.image.setPixmap(self.pix)
        self.backgroundColor="#ffffff"
        self.centralArea.setStyleSheet("background: "+self.backgroundColor+";border: 1px solid;border-color: #dadfe5;")
        self.candidateColor="#ff0000"
        self.voterColor="#70afea"
        self.pointsize=7
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
    #------Style------#

    def loadstyle(self,myStyle="classic"): #Style classic par défaut (bientôt un mode sombre)
        self.styleName=myStyle
        file=open("./styles/"+self.styleName+".txt","r")
        words=file.read().split("\n") #On copie le fichier classic.txt, puis on lui enleve ses sauts de lignes
        style=""    
        for w in words:
            style+=w
        self.setStyleSheet(style) #On charge le style

    #------End Style------#
    
    #-------Participant-------#
    def resetParticipants(self):
        self.dictcandidates = dict()
        self.IdCandidates = 0
        self.dictvoters = dict()
        self.IdVoters = 0
        self.place_voters = False
        Participant.idCounter=0
    #------End Participant------#

    #-------Central Area-------#
    def _createCentralArea(self):
        # On crée une instance que l'on va mettre au centre de la fenêtre.
        self.centralArea = QWidget()
        # On met l'arrière-plan par défaut
        self.centralArea.setStyleSheet("background: "+self.backgroundColor)
        # On injecte ce widget en tant que zone centrale.
        self.setCentralWidget(self.centralArea)
        

        #Dessin
        self.pix=(QPixmap("./pictures/axes.png")).scaledToHeight(int(self.centralArea.height()))
        self.image=QLabel(self.centralArea)
        self.image.setStyleSheet("background: #ffffff")
        self.image.setGeometry(QRect(0,0,self.pix.width(),self.pix.height()))
        self.image.setPixmap(self.pix)
    
        #Fenêtre de Creation de Participant
        self.cp=CreateParticipant(self)
        self.cp.move(930,60)


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
        self.box1 = QCheckBox("Candidate",self.centralArea)
        self.box1.move(1300,828)
        self.box1.setChecked(True)
        self.box2 = QCheckBox("Voter",self.centralArea)
        self.box2.move(1400,828)
        self.box2.setChecked(True)
        self.ButtonrefreshTab = QPushButton("Refresh Tab",self.centralArea)
        self.ButtonrefreshTab.move(1480,828) 


    def _connectCentralArea(self):
        self.ButtonGenerateVotes.clicked.connect(self.generateVotes)
        self.ButtonResetVotes.clicked.connect(self.resetVotes)
        self.ButtonrefreshTab.clicked.connect(self.refreshTab)
        
  
    
    #-------End Central Area-------#

    #-------Menus-------#


    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.isNativeMenuBar()
        # File menu
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.randomSetAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.placeCandidateAction)
        editMenu.addAction(self.placeVoterAction)
        editMenu.addSeparator()
        appearance=editMenu.addMenu(QIcon("./pictures/icons/"+self.styleName+"/iconApparence.png"),"  Appearance")
        appearance.addAction(self.editcandidatecolor)
        appearance.addAction(self.editvotercolor)
        appearance.addAction(self.editbackgroundcolor)
        appearance.addAction(self.editpointsize)
        editMenu.addSeparator()
        editMenu.addAction(self.deleteAction)
        # Votes menu
        votesMenu = menuBar.addMenu("Méthodes de vote")
        ## Calcul des scores
        scoresMenu = votesMenu.addMenu(QIcon("./pictures/icons/"+self.styleName+"/iconCalculer.png"),"  &Calcul des scores")
        scoresMenu.addAction(self.bordaAction)
        scoresMenu.addAction(self.pluralityAction)
        scoresMenu.addAction(self.vetoAction)
        scoresMenu.addAction(self.approbAction)
        ## Condorcet
        condorcetMenu = votesMenu.addMenu("  &Condorcet")
        condorcetMenu.addAction(self.copelandAction)
        condorcetMenu.addAction(self.SimpsonAction)
        ## Plusieurs tours
        turnMenu = votesMenu.addMenu("  &Plusieurs tours")
        turnMenu.addAction(self.VAAction)
        turnMenu.addAction(self.maj2TurnsAction)
        # Help menu
        helpMenu = menuBar.addMenu("Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addSeparator()
        helpMenu.addAction(self.aboutAction)
        helpMenu.addAction(self.aboutQtAction)
        
    def _createActions(self):
        # Menu File
        self.newAction = QAction(QIcon("./pictures/icons/"+self.styleName+"/iconNew.png"),"  &New File", self)
        self.newAction.setShortcuts(QKeySequence("Ctrl+N"))
        self.openAction = QAction(QIcon("./pictures/icons/"+self.styleName+"/iconOpen.png"),"  &Open File...", self)
        self.openAction.setShortcuts(QKeySequence("Ctrl+O"))
        self.randomSetAction = QAction("  &New Random Set", self)
        self.saveAction = QAction(QIcon("./pictures/icons/"+self.styleName+"/iconSave.png"),"  &Save", self)
        self.saveAction.setShortcuts(QKeySequence("Ctrl+S"))
        self.saveAsAction = QAction("  &Save As...", self) 
        self.saveAsAction.setShortcuts(QKeySequence("Ctrl+Shift+S"))    
        self.exitAction = QAction("  &Exit", self)
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
        self.placeCandidateAction = QAction(QIcon("./pictures/icons/"+self.styleName+"/iconCandidat.png"),"  &Candidate", self)
        self.placeCandidateAction.setShortcuts(QKeySequence("C"))
        self.placeVoterAction = QAction(QIcon("./pictures/icons/"+self.styleName+"/iconVotant.png"),"  &Voter", self)
        self.placeVoterAction.setShortcuts(QKeySequence("V"))
        self.editcandidatecolor = QAction("&Candidate Color",self)
        self.editvotercolor = QAction("&Voter Color",self)
        self.editbackgroundcolor = QAction("&Background Color",self)
        self.editpointsize = QAction("&Point Size",self)
        self.deleteAction = QAction("  &Delete", self)
        # Menu Help
        self.helpContentAction = QAction(QIcon("./pictures/icons/"+self.styleName+"/iconHelp.png"),"  &Help Content (TO-DO)", self)
        self.aboutAction = QAction("  &About... (TO-DO)", self)
        self.aboutQtAction = QAction(QIcon("./pictures/icons/"+self.styleName+"/iconQt.png"),"  &About Qt... (TO-DO)", self)
        
    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.randomSetAction.triggered.connect(self.newSet)
        self.saveAction.triggered.connect(self.saveFile)
        self.saveAsAction.triggered.connect(self.saveAsFile)
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
        self.aboutQtAction.triggered.connect(self.aboutQt)

    #-------End Menus-------#
    #-------ToolBar-------#
    def _createToolBars(self):
        ToolBar = self.addToolBar("ToolBar")
        ToolBar.addAction(self.newAction)
        ToolBar.addAction(self.openAction)
        ToolBar.addAction(self.saveAction)
        ToolBar.addSeparator()
        ToolBar.addAction(self.placeCandidateAction)
        ToolBar.addAction(self.placeVoterAction)
    #-------End ToolBar-------#

    #------Status Bar------#

    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.setFixedHeight(36)
        pix1=(QPixmap("./pictures/icons/"+self.styleName+"/iconCandidat.png")).scaledToHeight(int(self.statusbar.height()/2))
        self.cc=QLabel()
        self.cc.setPixmap(pix1)
        self.statusbar.addPermanentWidget(self.cc)
        self.ccLabel = QLabel(f"Candidates : {len(self.dictcandidates)} \t")
        self.statusbar.addPermanentWidget(self.ccLabel)
        pix2=(QPixmap("./pictures/icons/"+self.styleName+"/iconVotant.png")).scaledToHeight(int(self.statusbar.height()/2))
        self.vc=QLabel()
        self.vc.setPixmap(pix2)
        self.statusbar.addPermanentWidget(self.vc)
        self.vcLabel = QLabel(f"Voters : {len(self.dictvoters)} ")
        self.statusbar.addPermanentWidget(self.vcLabel)

    #-------Menus functions-------#
    
    ## File
        
    def newFile(self):
        # Logic for creating a new file goes here...
        self.name="New_file.elct" #Nom du fichier
        self.setWindowTitle(self.name)
        self.filePath="./files/New_file.elct" #Chemin d'accès du fichier
        self.reset()
        print("<b>File > New</b> clicked")

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Save File", "./files","All Files(*.*) ")
        if filePath == "":
            return
        self.filePath=filePath
        words=filePath.split("/")
        self.name=words[len(words)-1]
        self.setWindowTitle(self.name)
        file=open(self.filePath,"r")
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
        if os.path.exists(self.filePath):
            file=open(self.filePath, "w")
            file.write("<style>\n")
            file.write(self.backgroundColor+"\n")
            file.write(self.candidateColor+"\n")
            file.write(self.voterColor+"\n")
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
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "./files","(*.elct)")
        # if file path is blank return back
        if filePath == "":
            return
        #On teste si le nom de fichier contient bien l'extension .elct sinon on la rajoute
        words=filePath.split(".")
        if(words[len(words)-1])!="elct":
            filePath+=".elct"

        self.filePath=filePath
        words=filePath.split("/")
        self.name=words[len(words)-1]
        self.setWindowTitle(self.name)
        file=open(filePath, "w")
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
    
    def saisie(self,act,mode):
        """lancement de la fenêtre de dialogue pour la saisie """
        self.dialog = Dialog(act)
        self.dialog.setGeometry(740,400,400,50)
        if(mode=="recupPointSize"):
            self.dialog.donnees.connect(self.recupPointSize) # prépare la récupération des données saisies
        elif(mode=="recupApprovalThreshold"):
            self.dialog.donnees.connect(self.recupApprovalThreshold)
            
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
    
    def refreshImage(self):
        self.pix=QPixmap("./pictures/axes.png")
        for (k,v) in self.dictcandidates.items():
            painter = QPainter(self.pix)
            painter.setPen(QPen(QColor(self.candidateColor), self.pointsize, Qt.SolidLine))
            painter.setBrush(QColor(self.candidateColor))
            painter.drawEllipse(v.pos[0],v.pos[1],5,5)
            painter.end()
        for (k,v) in self.dictvoters.items():
            painter = QPainter(self.pix)
            painter.setPen(QPen(QColor(self.voterColor), self.pointsize, Qt.SolidLine))
            painter.setBrush(QColor(self.voterColor))
            painter.drawEllipse(v.pos[0],v.pos[1],5,5)
            painter.end()
     
    #------End Menu functions------#
    #-------Others functions-------#

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

    def refreshStatusBar(self):
        self.statusbar.removeWidget(self.ccLabel)
        self.statusbar.removeWidget(self.vcLabel)
        self.statusbar.insertPermanentWidget(1,self.cc)
        self.ccLabel = QLabel(f"Candidates : {len(self.dictcandidates)} \t")
        self.statusbar.addPermanentWidget(self.ccLabel)
        self.statusbar.addPermanentWidget(self.vc)
        self.vcLabel = QLabel(f"Voters : {len(self.dictvoters)} ")
        self.statusbar.addPermanentWidget(self.vcLabel)
        
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
        painter.setPen(QPen(QColor(self.candidateColor), self.pointsize, Qt.SolidLine))
        painter.setBrush(QColor(self.candidateColor))
        painter.drawEllipse(candidate.pos[0],candidate.pos[1]-6,5,5)
        self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        self.refreshStatusBar()
        self.update()

    def addVoter(self,voter):
        self.dictvoters[voter.id] = voter
        self.IdVoters += 1
        painter = QPainter(self.pix)
        painter.setPen(QPen(QColor(self.voterColor), self.pointsize, Qt.SolidLine))
        painter.setBrush(QColor(self.voterColor))
        painter.drawEllipse(voter.pos[0],voter.pos[1],5,5)
        self.table=tableView(self.centralArea,self.dictcandidates,self.dictvoters)
        self.refreshStatusBar()
        self.update()

   

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
    
    def aboutQt(self):
        print("<b>Help > About Qt...</b> clicked")
    ## End Help
        
if __name__ == '__main__':
    #print(QStyleFactory.keys()) 
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainMenu = Menu()
    sys.exit(app.exec_())