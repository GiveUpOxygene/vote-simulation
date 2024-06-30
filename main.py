import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect,QSize
from PyQt5.QtWidgets import QVBoxLayout,QDesktopWidget,QToolButton,QStyle
from PyQt5.QtWidgets import QStatusBar,QMainWindow,QToolBar,QTabBar,QApplication,QLineEdit,QFileDialog,QStyleFactory,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox,QInputDialog
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette,QKeySequence,QFont
from numpy import random
import numpy as np
from math import *
import time
from Classes import *
from votes import *
"""Pour fonctionner correcterment ils est nécessaire d'avoir les fichiers votes.py Classes.py et les répertoirs styles/files/pictures dans le même répertoire que ce main.py"""

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.titleBar = MyBar(self)
        self.titleBar.resize(QSize(10,60))
        self.setContentsMargins(1, self.titleBar.height(), 1, 1)
        #Change le style classic
        self.loadstyle()
        self.name="New_file.elct" #Nom du fichier
        self.filePath=os.path.realpath(os.path.dirname(__file__)) + "/files/New_file.elct" #Chemin d'accès du fichier
        #Création de la fenêtre principale
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon("{}/pictures/icons/icon.png".format(os.path.dirname(__file__))))   
        self.setGeometry(0,0,1450,991+self.titleBar.height())

        #Création paramètres par défaut
        self.styleName="classic"
        self.candidateColor="#ff0000"
        self.voterColor="#70afea"
        self.backgroundColor="#ffffff"
        self.distribution="Uniform"
        self.candidatePointsize=18
        self.voterPointsize=2
        self.att_budget=0.5
        self.def_budget=0.5
        self.place_voters=False

        self.resetParticipants() #Initialisation des candidats et votants
        self._createActions()  
        self._createMenuBar()#f des menus
        self._connectActions()
        self._createToolBars()  #Création de la barre d'outil
        self._createStatusBar() #Création de la barre de statuts
        self._createhome() #Création de la zone centrale
        self._connecthome()
        self.show()

    def showEvent(self, event):
        self.CenterOnScreen()

    def CenterOnScreen(self):
        """Méthode pour placer la fenêtre au milieu de l'écran"""
        screen=QDesktopWidget()
  
        screenGeom = QRect(screen.screenGeometry(self))
  
        screenCenterX = screenGeom.center().x()
        #screenCenterY = screenGeom.center().y()
  
        #self.move(int(screenCenterX - self.width () / 2),int (screenCenterY - self.height() / 2))
        self.move(int(screenCenterX - self.width () / 2), 0)

    def reset(self):
        """Méthode pour Remettre à 0 touts les paramètres/participants"""
        self.resetParticipants()
        self.pt=ParticipantTable(self)
        self.candidateColor="#ff0000"
        self.voterColor="#70afea"
        self.backgroundColor="#ffffff"
        self.candidatePointsize=20
        self.voterPointsize=2
        self.image.reset()
        
    #------Style------#

    def loadstyle(self,myStyle="classic"): #Style classic par défaut (bientôt un mode sombre)
        """Méthode pour charger un style
        ici ne sert qu'à initialiser le style classic mais on pourrait imaginer l'ajout d'un style sombre 
        comme sur beaucoup d'applications"""
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
        """Méthode pour réinitialisé les participants (supprimer tous les participants/remmettre à 0 les id)"""
        self.dictcandidates = dict()
        self.dictvoters = dict()
        self.place_voters = False
        Candidate.idCounter=0
        Voter.idCounter=0
    #------End Participant------#

    #-------Central Area-------#
    def _createhome(self):
        """Création de la barre d'onglet"""
        self.tabs=QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.resize(1450,985)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        # On injecte ce widget en tant que zone centrale.
        self.setCentralWidget(self.tabs)
        
        # Création de l'onglet pricipal
        self.home = QWidget()
        # On l'ajout à la barre d'onglet
        self.tabs.addTab(self.home,"Home")
        # On fait en sorte que cet onglet ne soit pas fermable en cachant le bouton de fermeture
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide,None) 

        # On créer et injecte tous les widgets de l'onglet principal
        #Dessin (Plan dans lequel on dessinera tous les candidats/votants)
        self.image=Drawing(self)
        
        # Fenêtre de Création de Participant
        self.pc=ParticipantCreator(self)
        self.pc.move(930,0)

        # Fenêtre de Génération de Participant
        self.pg = ParticipantGenerator(self)
        self.pg.move(1244,0)

        # Fenêtre de Génération d'élection
        self.eg = ElectionGenerator(self)
        self.eg.move(945,175)

        # Tableau des Participants
        self.pt = ParticipantTable(self)
        self.box1 = QCheckBox("Candidate",self.home)
        self.box1.move(1129,780)
        self.box1.setChecked(True)
        self.box2 = QCheckBox("Voter",self.home)
        self.box2.move(1229,780)
        self.box2.setChecked(True)
        self.ButtonrefreshTab = QPushButton("Refresh Tab",self.home)
        self.ButtonrefreshTab.setGeometry(QRect(1319,780,115,23))

    def _connecthome(self):
        
        self.ButtonrefreshTab.clicked.connect(self.refreshTab)
  
    #-------End Central Area-------#
    #-------Menus-------#

    def _createMenuBar(self):
        """Méthode de création de la barre de menu"""
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
        distribution.addAction(self.elections2017Action)
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
        editMenu.addAction(self.deleteCandidatesAction)
        editMenu.addAction(self.deleteVotersAction)
        # Lobbying menu
        lobbyingMenu = menuBar.addMenu("Lobbying")
        lobbyingMenu.addAction(self.lobbyingOBOAction)
        lobbyingMenu.addAction(self.lobbyingAction)
        lobbyingMenu.addSeparator()
        lobbyingMenu.addAction(self.attackOBOAction)
        lobbyingMenu.addAction(self.attackAction)
        lobbyingMenu.addSeparator()
        lobbyingMenu.addAction(self.defenseOBOAction)
        lobbyingMenu.addAction(self.defenseAction)
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
        turnMenu.addAction(self.liquidDemocracyAction)
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
        """Méthode de création des actions des différents menus"""
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
        self.elections2017Action = QAction("&Elections 2017",self)
        self.editcandidatecolor = QAction("&Candidate Color",self)
        self.editvotercolor = QAction("&Voter Color",self)
        self.editbackgroundcolor = QAction("&Background Color",self)
        self.editCandidatePointsize = QAction("&Candidate Point Size",self)
        self.editVoterPointsize = QAction("&Voter Point Size",self)
        self.deleteAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconDelete.png"),"  &Delete", self)
        self.deleteCandidatesAction = QAction("  &Delete All Candidates", self)
        self.deleteVotersAction = QAction("  &Delete All Voters", self)
        # Menu Lobbying
        self.lobbyingOBOAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconLobbying.png"),"  &Launch Lobbying one by one",self)
        self.lobbyingAction = QAction("  &Launch Lobbying",self)
        self.attackOBOAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconAttack.png"),"  &Launch Attack one by one",self)
        self.attackAction = QAction("  &Launch Attack", self)
        self.defenseOBOAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconDefense.png"),"  &Launch Defense one by one",self)
        self.defenseAction = QAction("  &Launch Defense",self)
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
        self.maj2TurnsAction.setShortcuts(QKeySequence("E"))
        self.avAction = QAction("&Alternative Vote",self)
        self.nansonAction = QAction("&Nanson",self)
        self.coombsAction = QAction("&Coombs",self)
        self.liquidDemocracyAction = QAction("&Liquid Democracy",self)
        self.allMethodsAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconElection.png"),"  &Launch All Voting Methods",self)
        self.allMethodsAction.setShortcuts(QKeySequence("Ctrl+A"))
        self.resetScoresAction = QAction(QIcon(os.path.dirname(__file__)+ "/pictures/icons/"+self.styleName+"/iconReset.png"),"  &Reset Scores",self)

        # Menu Help
        self.helpContentAction = QAction(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconHelp.png"),"  &Help...", self)
        self.aboutAction = QAction("  &About...", self)
        self.aboutQtAction = QAction(QIcon(os.path.dirname(__file__) + "/pictures/icons/"+self.styleName+"/iconQt.png"),"  &About Qt...", self)
        
    def _connectActions(self):
        """Méthode de connection des actions"""
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.randomSetAction.triggered.connect(self.newSet)
        self.saveAction.triggered.connect(self.saveFile)
        self.saveAsAction.triggered.connect(self.saveAsFile)
        self.exitAction.triggered.connect(self.close)

        #Connect Lobbying actions
        self.lobbyingOBOAction.triggered.connect(self.lobbyingOBOContent)
        self.lobbyingAction.triggered.connect(self.lobbyingContent)
        self.attackOBOAction.triggered.connect(self.attackOBOContent)
        self.attackAction.triggered.connect(self.attackContent)
        self.defenseOBOAction.triggered.connect(self.defenseOBOContent)
        self.defenseAction.triggered.connect(self.defenseContent)
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
        self.liquidDemocracyAction.triggered.connect(self.liquidDemocracyContent)
        self.allMethodsAction.triggered.connect(self.allMethodsContent)
        self.resetScoresAction.triggered.connect(self.resetScores)
        # Connect Edit actions
        self.placeCandidateAction.triggered.connect(self.candidateContent)
        self.placeVoterAction.triggered.connect(self.voterContent)
        self.uniformAction.triggered.connect(self.uniformContent)
        self.gaussianAction.triggered.connect(self.gaussianContent)
        self.elections2017Action.triggered.connect(self.elections2017Content)
        self.editcandidatecolor.triggered.connect(self.candidatecolorContent)
        self.editvotercolor.triggered.connect(self.votercolorContent)
        self.editbackgroundcolor.triggered.connect(self.backgroundcolorContent)
        self.editCandidatePointsize.triggered.connect(self.candidatePointsizeContent)
        self.editVoterPointsize.triggered.connect(self.voterPointsizeContent)
        self.deleteAction.triggered.connect(self.deleteContent)
        self.deleteCandidatesAction.triggered.connect(self.deleteCandidatesContent)
        self.deleteVotersAction.triggered.connect(self.deleteVotersContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)
        self.aboutQtAction.triggered.connect(self.aboutQt)

    #-------End Menus-------#
    #-------ToolBar-------#
    def _createToolBars(self):
        """Méthode de création de la barre d'outil"""
        ToolBar = self.addToolBar("ToolBar")
        ToolBar.addAction(self.newAction)
        ToolBar.addAction(self.openAction)
        ToolBar.addAction(self.saveAction)
        ToolBar.addSeparator()
        ToolBar.addAction(self.placeCandidateAction)
        ToolBar.addAction(self.placeVoterAction)
        ToolBar.addAction(self.deleteAction)
        ToolBar.addSeparator()
        ToolBar.addAction(self.lobbyingOBOAction)
        ToolBar.addAction(self.attackOBOAction)
        ToolBar.addAction(self.defenseOBOAction)
        ToolBar.addSeparator()
        ToolBar.addAction(self.allMethodsAction)
    #-------End ToolBar-------#

    #------Status Bar------#

    def _createStatusBar(self):
        """Méthode de création de la barre de statuts"""
        self.statusbar = self.statusBar()
        self.statusbar.setFixedHeight(34)
        self.statusbar.setStyleSheet("font: 12px")
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
        """Méthode pour créer un nouveau fichier"""
        # Logic for creating a new file goes here...
        self.name="New_file.elct" #Nom du fichier
        self.setWindowTitle(self.name)
        self.filePath=os.path.realpath(os.path.dirname(__file__)) + "/files/New_file.elct" #Chemin d'accès du fichier
        self.reset()

    def openFile(self):
        """Méthode pour ouvrir un nouveau fichier"""
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
        self.candidateColor=words[0]
        line=file.readline()
        words=line.split("\n")
        self.voterColor=words[0]
        line=file.readline()
        words=line.split("\n")
        self.backgroundColor=words[0]
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
        self.image.setBackgroundColor()
        self.refreshMU()
        self.refreshTab()
        self.refreshStatusBar()
        

    def saveFile(self):
        """Méthode pour enregistrer un fichier existant"""
        if os.path.exists(self.filePath):
            file=open(self.filePath, "w", encoding="utf8")
            file.write("<appearance>\n")
            file.write(self.candidateColor+"\n")
            file.write(self.voterColor+"\n")
            file.write(self.backgroundColor+"\n")
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
        """Méthode pour enregistrer un nouveau fichier"""
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
        """Méthode pour générer une situation électorale aléatoire, en fonction de l'attribut distribution"""
        self.reset()
        nb_candidates = 11
        nb_voters = 1000
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
        """Méthode pour raffraichir le dessin"""
        self.image.reset()
        for (_,v) in self.dictvoters.items():
            self.image.drawEllipse(v.pos[0],v.pos[1],self.voterColor,self.voterPointsize)
        for (_,v) in self.dictcandidates.items():
            self.image.drawEllipse(v.pos[0],v.pos[1],self.candidateColor,self.candidatePointsize)
            
     
    #------End Menu functions------#
    #-------Others functions-------#

    def addnewTab(self,tab,name):
        """Méthode pour ajouter un nouvel onglet (si il y a déjà un onglet avec le même nom, celui-ci est supprimé)"""
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i)==name:
                self.tabs.removeTab(i)
        self.tabs.addTab(tab,name)

    

    def resetScores(self):
        """Méthode pour remmtre les scores à 0"""
        resetElections(self.dictcandidates)
        self.refreshImage() #On raffraichit l'image, pour qu'il n'y ai pas de gagnant affiché
        self.refreshTab()


    def refreshTab(self):
        """Méthode pour raffraichir le tableau des participants"""
        if (self.box1.isChecked() and self.box2.isChecked()):
            self.pt = ParticipantTable(self)
        elif (self.box1.isChecked()):
            self.pt = ParticipantTable(self,"Candidate")
        elif (self.box2.isChecked()):
            self.pt = ParticipantTable(self,"Voter")

    def refreshStatusBar(self):
        """Méthode pour raffraichir la barre de statuts"""
        self.statusbar.removeWidget(self.ccLabel)
        self.statusbar.removeWidget(self.vcLabel)
        self.statusbar.insertPermanentWidget(1,self.cc)
        self.ccLabel = QLabel(f"Candidates : {len(self.dictcandidates)} \t")
        self.statusbar.addPermanentWidget(self.ccLabel)
        self.statusbar.addPermanentWidget(self.vc)
        self.vcLabel = QLabel(f"Voters : {len(self.dictvoters)} ")
        self.statusbar.addPermanentWidget(self.vcLabel)
    
    def refreshMU(self):
        """Méthode pour raffraichir les métriques utilitaires des candidats"""
        for (_,c) in self.dictcandidates.items():
            c.calculate_mu(self.dictvoters)
        
    def randomParticipant(self,is_candidate,x=None,y=None,mode="Uniform"):
        """Méthode pour générer un partcipant, de position aléatoire ou non, (position générer selon le mode de distribution) """
        if x==None or y==None:
            if mode=="Uniform":
                x=random.randint(-400, 400)
                y=random.randint(-400, 400)
            elif mode=="Gaussian":
                x=gaussienne()
                y=gaussienne()
            elif mode=="Elections 2017":
                x,y=r2017()
        firstname=firstNameGenerator() # On génére un prénom aléatoire
        lastname=lastNameGenerator() # On génére un nom aléatoire
        if is_candidate==True: # Selon ce parametre le participant sera un candidat ou un votant
            return Candidate(firstname,lastname,x,y)
        else:
            return Voter(firstname,lastname,x,y)
            
    def addCandidate(self,candidate):
        """Méthode d'ajout d'un candidat :
        - ajout du candidat au dictionnaire
        - dessine le candidat
        """
        self.dictcandidates[candidate.id] = candidate
        self.image.drawEllipse(candidate.pos[0],candidate.pos[1],self.candidateColor,self.candidatePointsize)

    def addVoter(self,voter):
        """Méthode d'ajout d'un votant
        - ajout du votant au dictionnaire
        - dessine le votant
        """
        self.dictvoters[voter.id] = voter
        self.image.drawEllipse(voter.pos[0],voter.pos[1],self.voterColor,self.voterPointsize)

    ## End File
    ## Edit

    def candidateContent(self):
        """Mode placer  un candidat Activé : Un click sur le plan déclenche l'ajout d'un Candidat"""
        self.place_voters = False

    def voterContent(self):
        """Mode placer un votant Activé : Un click sur le plan déclenche l'ajout d'un Votant"""
        self.place_voters = True

    def uniformContent(self):
        """Change le mode distribution en Uniform"""
        self.distribution="Uniform"
    
    def gaussianContent(self):
        """Change le mode distribution en Gaussian"""
        self.distribution="Gaussian"
    
    def elections2017Content(self):
        """Change le mode distribution en Elections 2017"""
        self.distribution="Elections 2017"

    def candidatecolorContent(self):
        """Change la couleur des candidats sur le plan"""
        self.candidateColor=(QColorDialog.getColor()).name()
        self.refreshImage()

    def votercolorContent(self):
        """Change la couleur des votants sur le plan"""
        self.voterColor=(QColorDialog.getColor()).name()
        self.refreshImage()

    def backgroundcolorContent(self):
        """Change la couleur de fond du plan"""
        color = QColorDialog.getColor()
        self.backgroundColor=color.name()
        self.image.setBackgroundColor()

    def candidatePointsizeContent(self):
        """Change la taille des candidats sur le plan"""
        self.candidatePointsize,_=QInputDialog.getInt(self,"Change Candidate Point Size","Point Size :", min = 1, max = 200, step = 1)
        self.refreshImage()

    def voterPointsizeContent(self):
        """Change la taille des votants sur le plan"""
        self.voterPointsize,_=QInputDialog.getInt(self,"Change Voter Point Size","Point Size :", min = 1, max = 200, step = 1)
        self.refreshImage()

    def deleteContent(self):
        """Efface tous les participants"""
        self.resetParticipants()
        self.pt=ParticipantTable(self)
        self.image.reset()

    def deleteCandidatesContent(self):
        """Efface tous les candidats"""
        self.dictcandidates = dict()
        Candidate.idCounter=0
        self.pt=ParticipantTable(self)
        self.refreshImage()
    
    def deleteVotersContent(self):
        """Efface tous les votants"""
        self.dictvoters = dict()
        Voter.idCounter=0
        self.pt=ParticipantTable(self)
        self.refreshImage()

    ## End Edit
    ## Lobbying

    def lobbyingOBOContent(self):
        """Lance le lobbying (attaque + défense) pas à pas"""
        self.attackOBOContent()
        self.defenseOBOContent()

    def lobbyingContent(self):
        """Lance le lobbying """
        self.attackContent()
        self.defenseContent()
    
    def attackOBOContent(self):
        """Lance l'attaque pas à pas"""
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.att_budget=c.budget*self.att_budget
            if(c.attack(self.dictcandidates)):
                self.refreshImage()
                self.image.repaint()
                time.sleep(0.5)
        self.refreshMU()
        self.refreshTab()
    
    def attackContent(self):
        """Lance l'attaque"""
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.att_budget=c.budget*self.att_budget
            c.attack(self.dictcandidates)
        self.refreshImage()
        self.refreshMU()
        self.refreshTab()

    def defenseOBOContent(self):
        """Lance la défense pas à pas"""
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.def_budget=c.budget*self.def_budget
            c.defend(self.dictcandidates,self.dictvoters)
            self.refreshImage()
            self.image.repaint()
            time.sleep(0.5)
        self.refreshMU()
        self.refreshTab()

    def defenseContent(self):
        """Lance la défense"""
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.def_budget=c.budget*self.def_budget
            c.defend(self.dictcandidates,self.dictvoters)
        self.refreshImage()
        self.refreshMU()
        self.refreshTab()

    def defenseRangeContent(self):
        """Affiche la portée de défense des candidats"""
        self.budgetContent()
        for _,c in self.dictcandidates.items():
            c.def_budget=c.budget*self.def_budget
            pos_r_set(c.pos[0],c.pos[1],int(c.def_budget),show=True,menu=self)

    def setBudgetRatioContent(self):
        """Change le ration d'attaque/défense"""
        #Lancement d'une fenêtre de dialogue pour récupérer le ratio attack/defense (en %)
        self.att_budget,_=QInputDialog.getInt(self,"Change Budget Ratio","Attack Budget (%) :", min = 0, max = 100, step = 1)
        self.att_budget/=100
        self.def_budget=1-self.att_budget
        self.refreshImage()
    
    
    def budgetContent(self):
        """Met à jour les budgets de chaque candidats"""
        for _,c in self.dictcandidates.items():
            c.calculate_budget(self.dictcandidates)
        
    ## End Lobbying
    ## Votes Rules

    def pluralityContent(self):
        """Lance un vote de Pluralité, et créer un onglet avec les résultats sous la forme d'un graphique"""
        resetElections(self.dictcandidates)
        plurality(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Plurality")

    def bordaContent(self):
        """Lance un vote de Borda, et créer un onglet avec les résultats sous la forme d'un graphique"""
        resetElections(self.dictcandidates)
        borda(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab, "Borda")
    
    def vetoContent(self):
        """Lance un vote de Veto, et créer un onglet avec les résultats sous la forme d'un graphique"""
        resetElections(self.dictcandidates)
        veto(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates,n=-1)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Veto")
    
    def approvalContent(self,threshold=None):
        """Lance un vote d'approbation, et créer un onglet avec les résultats sous la forme d'un graphique"""
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
        """Lance un vote de Copeland, et créer un onglet avec les résultats sous la forme d'un graphique"""
        resetElections(self.dictcandidates)
        copeland(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Copeland")
    
    def simpsonContent(self):
        """Lance un vote de Simpson, et créer un onglet avec les résultats sous la forme d'un graphique"""
        resetElections(self.dictcandidates)
        simpson(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Simpson")
    
    #Plusieurs Tours
    def maj2TurnsContent(self):
        """Lance un vote majoriataire à 2 tours, et créer un onglet avec les résultats sous la forme d'un graphique"""
        if len(self.dictcandidates)<=0:
            return None
        resetElections(self.dictcandidates)
        maj2Turns(self,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)

    def avContent(self):
        """Lance un vote Alternatif, et créer un onglet avec les résultats sous la forme d'un graphique"""
        if len(self.dictcandidates)<=0:
            return None
        resetElections(self.dictcandidates)
        newtab=QTabWidget()
        self.addnewTab(newtab,"Alternative Vote")
        av(self,newtab,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
    
    def nansonContent(self):
        """Lance un vote de Nanson, et créer un onglet avec les résultats sous la forme d'un graphique"""
        if len(self.dictcandidates)<=0:
            return None
        resetElections(self.dictcandidates)
        newtab=QTabWidget()
        self.addnewTab(newtab,"Nanson")
        nanson(self,newtab,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
    
    def coombsContent(self):
        """Lance un vote de Coombs, et créer un onglet avec les résultats sous la forme d'un graphique"""
        if len(self.dictcandidates)<=0:
            return None
        resetElections(self.dictcandidates)
        newtab=QTabWidget()
        self.addnewTab(newtab,"Coombs")
        c=coombs(self,newtab,self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)


    def liquidDemocracyContent(self,distanceMin=None,prob=None,nbtours=None):
        """Lance un vote de pluralité, en appliquant les délégations de démocratie liquide, et créer un onglet avec les résultats sous la forme d'un graphique"""
        if distanceMin==None:
            distanceMin,_=QInputDialog.getInt(self,"Change Delegation Minimum Distance","Minimum Distance :", min = 0, max = 1131, step = 1)
        if prob==None:
            prob,_=QInputDialog.getInt(self,"Change Delegation Probability","Delegation Probability (%) :", min = 0, max = 100, step = 1)
        if nbtours==None:
            nbtours,_=QInputDialog.getInt(self,"Change Delegation Round","Delegation Round :", min = 1, max = 100, step = 1)
        delegate(self.dictcandidates,self.dictvoters,distanceMin,(prob/100),nbtours)
        pluralityWithWeight(self.dictcandidates,self.dictvoters)
        self.dictcandidates=rating(self.dictcandidates)
        newtab=ViewResults(self,width=5, height=4, dpi=100)
        self.addnewTab(newtab,"Liquid Democracy")
    
    
    def allMethodsContent(self):
        """Lance toutes les méthodes de votes et créer des onglets avec les résultats de chaque élections sous forme graphique"""
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
        self.liquidDemocracyContent(distanceMin=200,prob=30,nbtours=10)
        self.resetScores()

    ## End Votes
    ## Help

    def helpContent(self):
        """Affiche la fenêtre d'aide"""
        self.help=ShowTexte("Help","help","icons/icon.png")

    def about(self):
        """Affiche la fenêtre d'information sur l'application"""
        self.about=ShowTexte("About","about","icons/icon.png")
    
    def aboutQt(self):
        """Affiche la fenêtre d'information sur PyQt"""
        self.qt=ShowTexte("About Qt","qt","icons/classic/iconQt.png")
    ## End Help

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())
    

if __name__ == '__main__':
    #print(QStyleFactory.keys()) 
    #random.seed(42) utilisé Pour les tests, en générant toujours la même situation aléatoire
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainMenu = Menu()
    sys.exit(app.exec_())

