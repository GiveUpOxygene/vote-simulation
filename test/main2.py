import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect,QSize
from PyQt5.QtWidgets import QVBoxLayout,QDesktopWidget
from PyQt5.QtWidgets import QStatusBar,QMainWindow,QToolBar,QTabBar,QApplication,QLineEdit,QFileDialog,QStyleFactory,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox,QInputDialog
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette,QKeySequence
from numpy import random
import numpy as np
from math import *
import time
from Classes import *
from votes import *
from Mybar import *

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        #Change le style classic
        self.loadstyle()
        self.name="New_file.elct" #Nom du fichier
        self.filePath=os.path.realpath(os.path.dirname(__file__)) + "/files/New_file.elct" #Chemin d'accès du fichier
        #Création de la fenêtre principale
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + "/pictures/icons/icon.png"))   
        self.setGeometry(0,0,1450,985)

        #Création paramètres par défaut
        self.distribution="Uniform"
        self.candidateColor="#ff0000"
        self.voterColor="#70afea"
        self.backgroundColor="#ffffff"
        self.candidatePointsize=20
        self.voterPointsize=6
        self.att_budget=0.5
        self.def_budget=0.5

        self.resetParticipants() #Initialisation des candidats et votants
        self._createActions()  
        self._createMenuBar()#Création des menus
        self._connectActions()
        self._createToolBars()  #Création de la barre d'outil
        self._createStatusBar() #Création de la barre de statuts
        self._createtab1() #Création de la zone centrale
        self._connecttab1()
        self.show()

    def showEvent(self, event):
        self.CenterOnScreen()

    def CenterOnScreen(self):
        screen=QDesktopWidget()
  
        screenGeom = QRect(screen.screenGeometry(self))
  
        screenCenterX = screenGeom.center().x()
        #screenCenterY = screenGeom.center().y()
  
        #self.move(int(screenCenterX - self.width () / 2),int (screenCenterY - self.height() / 2))
        self.move(int(screenCenterX - self.width () / 2), 0)

    def reset(self):
        self.resetParticipants()
        self.pt=ParticipantTable(self.tab1,self.dictcandidates,self.dictvoters)
        self.image.reset()
        self.backgroundColor="#ffffff"
        self.tab1.setStyleSheet("background: "+self.backgroundColor)
        self.candidateColor="#ff0000"
        self.voterColor="#70afea"
        self.candidatePointsize=20
        self.voterPointsize=6
        self.update()
        
    #------Style------#

    def loadstyle(self,myStyle="classic"): #Style classic par défaut (bientôt un mode sombre)
        self.styleName=myStyle
        file=open(os.path.dirname(__file__) + "/styles/"+self.styleName+".txt","r")
        words=file.read().split("\n") #On copie le fichier classic.txt, puis on lui enleve ses sauts de lignes
        style=""    
        for w in words:
            style+=w
        self.setStyleSheet(style) #On charge le style

    #------End Style------#
    
    #-------Participant-------#
    def resetParticipants(self):
        self.dictcandidates = dict()
        self.dictvoters = dict()
        self.place_voters = False
        Candidate.idCounter=0
        Voter.idCounter=0
    #------End Participant------#

    #-------Central Area-------#
    def _createtab1(self):
        
        self.tabs=QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.resize(1450,985)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        
        # On crée une instance que l'on va mettre au centre de la fenêtre.
        self.tab1 = QWidget()
        # On met l'arrière-plan par défaut
        self.tab1.setStyleSheet("background: "+self.backgroundColor)
        # On injecte ce widget en tant que zone centrale.
        self.tabs.addTab(self.tab1,"Home")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide,None) #Pour que l'onglet Home ne soit pas fermable
        self.setCentralWidget(self.tabs)

        #Dessin
        self.pix=(QPixmap(os.path.dirname(__file__) + "/pictures/axes.png")).scaledToHeight(800)
        self.image=Drawing(self)
        
        #Fenêtre de Création de Participant
        self.pc=ParticipantCreator(self)
        self.pc.move(930,0)

        #Fenêtre de Génération de Participant
        self.pg = ParticipantGenerator(self)
        self.pg.move(1244,0)

        #Lancer Elections
        font = QFont()
        font.setPointSize(11)
        self.comboBoxVotingRules = QComboBox(self.tab1)
        self.comboBoxVotingRules.setGeometry(QRect(950, 175, 100, 23))
        self.comboBoxVotingRules.setFont(font)
        self.comboBoxVotingRules.addItems(["Plurality","Borda","Veto","Approval","Copeland","Simpson","Two-Round Majority","Alternative Vote","Nanson","Coombs"])
        self.ButtonGenerateVotes = QPushButton("Generate Votes",self.tab1)
        self.ButtonGenerateVotes.setGeometry(QRect(945, 215, 140, 23))
        self.ButtonGenerateVotes.setFont(font)
        self.ButtonResetScores = QPushButton("Reset Scores",self.tab1)
        self.ButtonResetScores.setGeometry(QRect(1105, 215, 115, 23))
        self.ButtonResetScores.setFont(font)

        #Tableau des Participants
        self.pt = ParticipantTable(self.tab1,self.dictcandidates,self.dictvoters)
        self.box1 = QCheckBox("Candidate",self.tab1)
        self.box1.move(1129,780)
        self.box1.setChecked(True)
        self.box2 = QCheckBox("Voter",self.tab1)
        self.box2.move(1229,780)
        self.box2.setChecked(True)
        self.ButtonrefreshTab = QPushButton("Refresh Tab",self.tab1)
        self.ButtonrefreshTab.setGeometry(QRect(1319,780,115,23))

    def _connecttab1(self):
        self.ButtonGenerateVotes.clicked.connect(self.generateVotes)
        self.ButtonResetScores.clicked.connect(self.resetScores)
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
        distribution=editMenu.addMenu("  Distribution")
        distribution.addAction(self.uniformAction)
        distribution.addAction(self.gaussianAction)
        editMenu.addSeparator()
        appearance = editMenu.addMenu(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconApparence.png"),"  Appearance")
        appearance.addAction(self.editcandidatecolor)
        appearance.addAction(self.editvotercolor)
        appearance.addAction(self.editbackgroundcolor)
        editPointsize = appearance.addMenu("Set point size")
        editPointsize.addAction(self.editCandidatePointsize)
        editPointsize.addAction(self.editVoterPointsize)
        editMenu.addSeparator()
        editMenu.addAction(self.deleteAction)
        # Lobbying menu
        lobbyingMenu = menuBar.addMenu("Lobbying")
        lobbyingMenu.addAction(self.lobbyingAction)
        lobbyingMenu.addAction(self.lobbyingOBOAction)
        lobbyingMenu.addSeparator()
        lobbyingMenu.addAction(self.attackAction)
        lobbyingMenu.addAction(self.attackOBOAction)
        lobbyingMenu.addSeparator()
        lobbyingMenu.addAction(self.defenseAction)
        lobbyingMenu.addAction(self.defenseOBOAction)
        lobbyingMenu.addSeparator()
        lobbyingMenu.addAction(self.defenseRangeAction)
        lobbyingMenu.addAction(self.defenseHideRangeAction)
        lobbyingMenu.addSeparator()
        lobbyingMenu.addAction(self.setBudgetRatioAction)
        lobbyingMenu.addAction(self.refreshBudgetAction)
        
        # Votes Rules menu
        votesMenu = menuBar.addMenu("Voting Rules")
        ## Calcul des scores
        scoresMenu = votesMenu.addMenu(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconPeople.png"),"  &Scoring Rules")
        scoresMenu.addAction(self.pluralityAction)
        scoresMenu.addAction(self.bordaAction)
        scoresMenu.addAction(self.vetoAction)
        scoresMenu.addAction(self.approvalAction)
        ## Condorcet
        condorcetMenu = votesMenu.addMenu(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconDuel.png"),"  &Condorcet")
        condorcetMenu.addAction(self.copelandAction)
        condorcetMenu.addAction(self.simpsonAction)
        ## Plusieurs tours
        turnMenu = votesMenu.addMenu("  &Multiple Round")
        turnMenu.addAction(self.maj2TurnsAction)
        turnMenu.addAction(self.avAction)
        turnMenu.addAction(self.nansonAction)
        turnMenu.addAction(self.coombsAction)
        
        
        ## Lancer toutes les Méthodes
        votesMenu.addAction(self.allMethodsAction)
        votesMenu.addSeparator()
        ##Reset Score
        votesMenu.addAction(self.resetScoresAction)
        # Help menu
        helpMenu = menuBar.addMenu("Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addSeparator()
        helpMenu.addAction(self.aboutAction)
        helpMenu.addAction(self.aboutQtAction)
        
    def _createActions(self):
        # Menu File
        self.newAction = QAction(QIcon(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/"+self.styleName+"/iconNew.png"),"  &New File", self)
        self.newAction.setShortcuts(QKeySequence("Ctrl+N"))
        self.openAction = QAction(QIcon(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/"+self.styleName+"/iconOpen.png"),"  &Open File...", self)
        self.openAction.setShortcuts(QKeySequence("Ctrl+O"))
        self.randomSetAction = QAction("  &New Random Set", self)
        self.randomSetAction.setShortcuts(QKeySequence("Ctrl+D"))
        self.saveAction = QAction(QIcon(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/"+self.styleName+"/iconSave.png"),"  &Save", self)
        self.saveAction.setShortcuts(QKeySequence("Ctrl+S"))
        self.saveAsAction = QAction("  &Save As...", self) 
        self.saveAsAction.setShortcuts(QKeySequence("Ctrl+Shift+S"))    
        self.exitAction = QAction(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconExit.png"),"  &Exit", self)
    
        # Menu Edit
        self.placeCandidateAction = QAction(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconCandidat.png"),"  &Candidate", self)
        self.placeCandidateAction.setShortcuts(QKeySequence("C"))
        self.placeVoterAction = QAction(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconVotant.png"),"  &Voter", self)
        self.placeVoterAction.setShortcuts(QKeySequence("V"))
        self.uniformAction = QAction("&Uniform",self)
        self.uniformAction.setShortcuts(QKeySequence("U"))
        self.gaussianAction = QAction("&Gaussian",self)
        self.gaussianAction.setShortcuts(QKeySequence("G"))
        self.editcandidatecolor = QAction("&Candidate Color",self)
        self.editvotercolor = QAction("&Voter Color",self)
        self.editbackgroundcolor = QAction("&Background Color",self)
        self.editCandidatePointsize = QAction("&Candidate Point Size",self)
        self.editVoterPointsize = QAction("&Voter Point Size",self)
        self.deleteAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconDelete.png"),"  &Delete", self)

        # Menu Lobbying
        self.lobbyingAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconLobbying.png"),"  &Launch Lobbying",self)
        self.lobbyingOBOAction = QAction("  &Launch Lobbying one by one",self)
        self.attackAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconAttack.png"), "  &Launch Attack", self)
        self.attackOBOAction = QAction("  &Launch Attack one by one",self)
        self.defenseAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconDefense.png"),"  &Launch Defense",self)
        self.defenseOBOAction = QAction("  &Launch Defense one by one",self)
        self.defenseRangeAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconRange.png"),"  &Show Defense Range")
        self.defenseHideRangeAction = QAction("  &Hide Defense Range")
        self.setBudgetRatioAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconRatio.png"),"  &Set Budget Ratio",self)
        self.refreshBudgetAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconCalculateBudget.png"),"  &Refresh Budget",self)

        # Menu Voting Rules
        self.pluralityAction = QAction("&Plurality",self)
        self.bordaAction = QAction("&Borda",self)
        self.vetoAction = QAction("&Veto",self)
        self.approvalAction = QAction("&Approval",self)
        self.copelandAction = QAction("&Copeland",self)
        self.simpsonAction = QAction("&Simpson",self)
        self.maj2TurnsAction = QAction("&Two-Round Majority",self)
        self.avAction = QAction("&Alternative Vote",self)
        self.nansonAction = QAction("&Nanson",self)
        self.coombsAction = QAction("&Coombs",self)

        
        self.allMethodsAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconElection.png"),"  &Launch All Voting Methods",self)
        self.allMethodsAction.setShortcuts(QKeySequence("Ctrl+A"))
        self.resetScoresAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconReset.png"),"  &Reset Scores",self)

        # Menu Help
        self.helpContentAction = QAction(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconHelp.png"),"  &Help Content", self)
        self.aboutAction = QAction("  &About...", self)
        self.aboutQtAction = QAction(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconQt.png"),"  &About Qt...", self)
        
    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.randomSetAction.triggered.connect(self.newSet)
        self.saveAction.triggered.connect(self.saveFile)
        self.saveAsAction.triggered.connect(self.saveAsFile)
        self.exitAction.triggered.connect(self.close)

        #Connect Lobbying actions
        self.lobbyingAction.triggered.connect(self.lobbyingContent)
        self.lobbyingOBOAction.triggered.connect(self.lobbyingOBOContent)
        self.attackAction.triggered.connect(self.attackContent)
        self.attackOBOAction.triggered.connect(self.attackOBOContent)
        self.defenseAction.triggered.connect(self.defenseContent)
        self.defenseOBOAction.triggered.connect(self.defenseOBOContent)
        self.defenseRangeAction.triggered.connect(self.defenseRangeContent)
        self.defenseHideRangeAction.triggered.connect(self.refreshImage)
        self.setBudgetRatioAction.triggered.connect(self.setBudgetRatioContent)
        self.refreshBudgetAction.triggered.connect(self.budgetContent)

        # Connect Votes Rules actions
        self.pluralityAction.triggered.connect(self.pluralityContent)
        self.bordaAction.triggered.connect(self.bordaContent)
        self.vetoAction.triggered.connect(self.vetoContent)
        self.approvalAction.triggered.connect(self.approvalContent)
        self.copelandAction.triggered.connect(self.copelandContent)
        self.simpsonAction.triggered.connect(self.simpsonContent)
        self.maj2TurnsAction.triggered.connect(self.maj2TurnsContent)
        self.avAction.triggered.connect(self.avContent)
        self.nansonAction.triggered.connect(self.nansonContent)
        self.coombsAction.triggered.connect(self.coombsContent)
        self.allMethodsAction.triggered.connect(self.allMethodsContent)
        self.resetScoresAction.triggered.connect(self.resetScores)
        # Connect Edit actions
        self.placeCandidateAction.triggered.connect(self.candidateContent)
        self.placeVoterAction.triggered.connect(self.voterContent)
        self.uniformAction.triggered.connect(self.uniformContent)
        self.gaussianAction.triggered.connect(self.gaussianContent)
        self.editcandidatecolor.triggered.connect(self.candidatecolorContent)
        self.editvotercolor.triggered.connect(self.votercolorContent)
        self.editbackgroundcolor.triggered.connect(self.backgroundcolorContent)
        self.editCandidatePointsize.triggered.connect(self.candidatePointsizeContent)
        self.editVoterPointsize.triggered.connect(self.voterPointsizeContent)
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
        pix1=(QPixmap(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/"+self.styleName+"/iconCandidat.png")).scaledToHeight(int(self.statusbar.height()/2))
        self.cc=QLabel()
        self.cc.setPixmap(pix1)
        self.statusbar.addPermanentWidget(self.cc)
        self.ccLabel = QLabel(f"Candidates : {len(self.dictcandidates)} \t")
        self.statusbar.addPermanentWidget(self.ccLabel)
        pix2=(QPixmap(os.path.realpath(os.path.dirname(__file__)) + "/pictures/icons/"+self.styleName+"/iconVotant.png")).scaledToHeight(int(self.statusbar.height()/2))
        self.vc=QLabel()
        self.vc.setPixmap(pix2)
        self.statusbar.addPermanentWidget(self.vc)
        self.vcLabel = QLabel(f"Voters : {len(self.dictvoters)} ")
        self.statusbar.addPermanentWidget(self.vcLabel)
    #------End Status Bar------#
    #-------Menus functions-------#
    
    ## File
        
    def newFile(self):
        # Logic for creating a new file goes here...
        self.name="New_file.elct" #Nom du fichier
        self.setWindowTitle(self.name)
        self.filePath=os.path.realpath(os.path.dirname(__file__)) + "/files/New_file.elct" #Chemin d'accès du fichier
        self.reset()

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Save File", os.path.dirname(__file__) + "/files","All Files(*.*) ")
        if filePath == "":
            return
        self.filePath=filePath
        words=filePath.split("/")
        self.name=words[len(words)-1]
        self.setWindowTitle(self.name)
        file=open(self.filePath,"r", encoding="utf8")
        self.reset()

        #Lecture des élements du style
        line=file.readline()
        assert(line=="<appearance>\n")
        line=file.readline()
        words=line.split("\n")
        self.backgroundColor=words[0]
        self.tab1.setStyleSheet("background: "+self.backgroundColor)
        line=file.readline()
        words=line.split("\n")
        self.candidateColor=words[0]
        line=file.readline()
        words=line.split("\n")
        self.voterColor=words[0]
        line=file.readline()
        words=line.split("\n")
        self.candidatePointsize=int(words[0])
        words=line.split("\n")
        line=file.readline()
        words=line.split("\n")
        self.voterPointsize=int(words[0])
        words=line.split("\n")
        line=file.readline()
        assert(line=="</appearance>\n")

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
        file.close()

    def saveFile(self):
        if os.path.exists(self.filePath):
            file=open(self.filePath, "w", encoding="utf8")
            file.write("<appearance>\n")
            file.write(self.backgroundColor+"\n")
            file.write(self.candidateColor+"\n")
            file.write(self.voterColor+"\n")
            file.write(str(self.candidatePointsize)+"\n")
            file.write(str(self.voterPointsize)+"\n")
            file.write("</appearance>\n")

            file.write("<voters>\n")
            for (_,v) in self.dictvoters.items():
                file.write(v.__repr__()+"\n")
            file.write("</voters>\n")

            file.write("<candidates>\n")
            for (_,v) in self.dictcandidates.items():
                file.write(v.__repr__()+"\n")
            file.write("</candidates>\n")

            file.close()
        else :
            self.saveAsFile()


    def saveAsFile(self):
        # Logic for saving an existing file goes here...
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", os.path.dirname(__file__) + "/files","(*.elct)")
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
        file=open(filePath, "w", encoding="utf8")
        file.close()
        self.saveFile()

    def newSet(self):
        self.reset()
        nb_candidates = 15
        nb_voters = 500
        #répartir aléatoirement avec numpy les candidats sur l'écran (en fonction de la taille de l'écran)
        for _ in range(nb_voters):
            newVoter=self.randomParticipant(False,mode=self.distribution)
            self.addVoter(newVoter)
        for _ in range(nb_candidates):
            newCandidate=self.randomParticipant(True,mode=self.distribution)
            self.addCandidate(newCandidate)
        self.refreshMU()
        self.refreshTab()
        self.refreshStatusBar()
    
    def refreshImage(self):
        self.image.reset()
        for (_,v) in self.dictvoters.items():
            self.image.drawEllipse(v.pos[0],v.pos[1],self.voterColor,self.voterPointsize)
        for (_,v) in self.dictcandidates.items():
            self.image.drawEllipse(v.pos[0],v.pos[1],self.candidateColor,self.candidatePointsize)
            
     
    #------End Menu functions------#
    #-------Others functions-------#

    def addnewTab(self,tab,name):
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i)==name:
                self.tabs.removeTab(i)
        self.tabs.addTab(tab,name)

    def generateVotes(self):
        self.winners=set()
        n=1
        if (self.comboBoxVotingRules.currentText()=="Plurality"):
            self.pluralityContent()
        elif(self.comboBoxVotingRules.currentText()=="Borda"):
            self.bordaContent()
        elif(self.comboBoxVotingRules.currentText()=="Veto"):
            self.vetoContent()
        elif(self.comboBoxVotingRules.currentText()=="Approval"):
            self.approvalContent()
        elif(self.comboBoxVotingRules.currentText()=="Copeland"):
            self.copelandContent()
        elif(self.comboBoxVotingRules.currentText()=="Simpson"):
            self.simpsonContent()
        elif(self.comboBoxVotingRules.currentText()=="Two-Round Majority"):
            self.maj2TurnsContent()
        elif(self.comboBoxVotingRules.currentText()=="Alternative Vote"):
            self.avContent()
        elif(self.comboBoxVotingRules.currentText()=="Nanson"):
            self.nansonContent()
        elif(self.comboBoxVotingRules.currentText()=="Coombs"):
            self.coombsContent()
            #Le gagnant est celui avec le nombre de vote le plus élevé
            n=-1
        self.refreshTab()
        #On affiche le(s) gagnant(s) des élections
        self.refreshImage()
        winnerpointsize=max(self.candidatePointsize*2,self.candidatePointsize+30)
        if n==1:
            self.winners=winners(self.dictcandidates)
        for id in self.winners:
            self.image.drawEllipse(self.dictcandidates[id].pos[0],self.dictcandidates[id].pos[1],self.candidateColor,winnerpointsize)

    def resetScores(self):
        resetElections(self.dictcandidates)
        self.refreshImage()
        self.refreshTab()


    def refreshTab(self):
        if (self.box1.isChecked() and self.box2.isChecked()):
            self.pt=ParticipantTable(self.tab1,self.dictcandidates,self.dictvoters)
        elif (self.box1.isChecked()):
            self.pt=ParticipantTable(self.tab1,self.dictcandidates,self.dictvoters,"Candidate")
        elif (self.box2.isChecked()):
            self.pt=ParticipantTable(self.tab1,self.dictcandidates,self.dictvoters,"Voter")

    def refreshStatusBar(self):
        self.statusbar.removeWidget(self.ccLabel)
        self.statusbar.removeWidget(self.vcLabel)
        self.statusbar.insertPermanentWidget(1,self.cc)
        self.ccLabel = QLabel(f"Candidates : {len(self.dictcandidates)} \t")
        self.statusbar.addPermanentWidget(self.ccLabel)
        self.statusbar.addPermanentWidget(self.vc)
        self.vcLabel = QLabel(f"Voters : {len(self.dictvoters)} ")
        self.statusbar.addPermanentWidget(self.vcLabel)
    
    def refreshMU(self):
        for (_,c) in self.dictcandidates.items():
            c.calculate_mu(self.dictvoters)
        
    def randomParticipant(self,is_candidate,x=None,y=None,mode="Uniform"):
        if x==None or y==None:
            if mode=="Uniform":
                x=random.randint(-400, 400)
                y=random.randint(-400, 400)
            elif mode=="Gaussian":
                x=gaussienne()
                y=gaussienne()
        firstname=firstNameGenerator()
        lastname=lastNameGenerator()
        if is_candidate==True:
            return Candidate(firstname,lastname,x,y)
        else:
            return Voter(firstname,lastname,x,y)
            
    def addCandidate(self,candidate):
        self.dictcandidates[candidate.id] = candidate
        self.image.drawEllipse(candidate.pos[0],candidate.pos[1],self.candidateColor,self.candidatePointsize)
        self.update()

    def addVoter(self,voter):
        self.dictvoters[voter.id] = voter
        self.image.drawEllipse(voter.pos[0],voter.pos[1],self.voterColor,self.voterPointsize)
        self.update()

    ## End File
    ## Edit

    def candidateContent(self):
        self.place_voters = False

    def voterContent(self):
        self.place_voters = True

    def uniformContent(self):
        self.distribution="Uniform"
    
    def gaussianContent(self):
        self.distribution="Gaussian"

    def candidatecolorContent(self):
        self.candidateColor=(QColorDialog.getColor()).name()
        self.refreshImage()

    def votercolorContent(self):
        self.voterColor=(QColorDialog.getColor()).name()
        self.refreshImage()

    def backgroundcolorContent(self):
        color = QColorDialog.getColor()
        self.backgroundColor=color.name()
        self.tab1.setStyleSheet("background: "+self.backgroundColor)

    def candidatePointsizeContent(self):
        self.candidatePointsize,_=QInputDialog.getInt(self,"Change Candidate Point Size","Point Size :", min = 1, max = 200, step = 1)
        self.refreshImage()

    def voterPointsizeContent(self):
        self.voterPointsize,_=QInputDialog.getInt(self,"Change Voter Point Size","Point Size :", min = 1, max = 200, step = 1)
        self.refreshImage()

    def deleteContent(self):
        self.reset()
        
    ## End Edit
    ## Lobbying

    def lobbyingContent(self):
        self.attackContent()
        self.defenseContent()
    
    def lobbyingOBOContent(self):
        self.attackOBOContent()
        self.defenseOBOContent()
    
    def attackContent(self):
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.att_budget=c.budget*self.att_budget
            c.attack(self.dictcandidates)
        self.refreshImage()
        self.refreshMU()
        self.refreshTab()
        
    
    def attackOBOContent(self):
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.att_budget=c.budget*self.att_budget
            if(c.attack(self.dictcandidates)):
                self.refreshImage()
                self.image.repaint()
                time.sleep(0.5)
        self.refreshMU()
        self.refreshTab()

    def defenseContent(self):
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.def_budget=c.budget*self.def_budget
            c.defend(self.dictcandidates,self.dictvoters)
        self.refreshImage()
        self.refreshMU()
        self.refreshTab()

    def defenseOBOContent(self):
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.def_budget=c.budget*self.def_budget
            c.defend(self.dictcandidates,self.dictvoters)
            self.refreshImage()
            self.image.repaint()
            time.sleep(0.5)
        self.refreshMU()
        self.refreshTab()
    
    def defenseRangeContent(self):
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.def_budget=c.budget*self.def_budget
            pos_r_set(c.pos[0],c.pos[1],int(c.def_budget),show=True,menu=self)

    def setBudgetRatioContent(self):
        #Lancement d'une fenêtre de dialogue pour récupérer le ratio attack/defense (en %)
        self.att_budget,_=QInputDialog.getInt(self,"Change Budget Ratio","Attack Budget (%) :", min = 0, max = 100, step = 1)
        self.att_budget/=100
        self.def_budget=1-self.att_budget
        self.refreshImage()
    
    
    def budgetContent(self):
        for _,c in self.dictcandidates.items():
            c.calculate_budget(self.dictcandidates)
        
    ## End Lobbying
    ## Votes Rules

    def pluralityContent(self):
        resetElections(self.dictcandidates)
        plurality(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Plurality")

    def bordaContent(self):
        resetElections(self.dictcandidates)
        borda(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab, "Borda")
    
    def vetoContent(self):
        resetElections(self.dictcandidates)
        veto(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Veto")
    
    def approvalContent(self,threshold=None):
        resetElections(self.dictcandidates)
        if threshold==None:
            self.appprovalThreshold,_=QInputDialog.getInt(self,"Approval Threshold","Threshold:", min = 1, max = 15, step = 1)
        else:
            self.appprovalThreshold=threshold
        approval(self.dictcandidates,self.dictvoters,self.appprovalThreshold)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Approval ("+str(self.appprovalThreshold)+")")
    
    def copelandContent(self):
        resetElections(self.dictcandidates)
        copeland(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Copeland")
    
    def simpsonContent(self):
        resetElections(self.dictcandidates)
        simpson(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Simpson")
    
    #Plusieurs Tours
    def maj2TurnsContent(self):
        resetElections(self.dictcandidates)
        maj2Turns(self,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)

    def avContent(self):
        resetElections(self.dictcandidates)
        newtab=QTabWidget()
        self.addnewTab(newtab,"Alternative Vote")
        av(self,newtab,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
    
    def nansonContent(self):
        resetElections(self.dictcandidates)
        newtab=QTabWidget()
        self.addnewTab(newtab,"Nanson")
        nanson(self,newtab,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
    
    def coombsContent(self):
        resetElections(self.dictcandidates)
        newtab=QTabWidget()
        self.addnewTab(newtab,"Coombs")
        c=coombs(self,newtab,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)


    
    
    
    def allMethodsContent(self):
        self.pluralityContent()
        self.bordaContent()
        self.vetoContent()
        self.approvalContent(ceil(len(self.dictcandidates)/2))
        self.copelandContent()
        self.simpsonContent()
        self.maj2TurnsContent()
        self.avContent()
        self.nansonContent()
        self.coombsContent()
        self.resetScores()

    ## End Votes

    
    ## Help

    def helpContent(self):
        print("Les votants sont en rouge, les candidats en bleu\n")

    def about(self):
        # Logic for showing an about dialog content goes here...
        print("<b>Help > About...</b> clicked")
    
    def aboutQt(self):
        self.qt=AboutQt()
    ## End Help
        
if __name__ == '__main__':
    #print(QStyleFactory.keys()) 
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainMenu = Menu()
    sys.exit(app.exec_())