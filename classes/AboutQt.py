import sys
import os
from PyQt5.QtCore import QRect, Qt 
from PyQt5.QtWidgets import  QWidget, QDialog, QApplication, QLabel, QPushButton,QDesktopWidget
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter, QBrush, QColor
class AboutQt(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.setStyleSheet("background-color: #ffffff;font: 14px;spacing: 8px;")
        self.setGeometry(QRect(0,0,720,610))
        self.setWindowTitle("About Qt")
        self.setWindowIcon(QIcon("./pictures/icons/icon.png")) 
        #Titre
        self.titre = QLabel (self)
        self.titre.setGeometry(QRect(90, 20, 720, 20))
        self.titre.setText("About Qt")
        self.titre.setStyleSheet("font-weight: bold; color: black; font-size:14pt")
        
        self.pix=(QPixmap("./pictures/icons/classic/iconQt.png")).scaledToHeight(60)
        self.image=QLabel(self)
        self.image.setStyleSheet("background-color: #ffffff;border: 1px solid;border-color: #dadfe5;")
        self.image.setGeometry(QRect(10,10,self.pix.width(),self.pix.height()))
        self.image.setPixmap(self.pix)
        self.image.setStyleSheet("border : none ")
        #Texte
        file=open("./doc/qt.txt","r", encoding="utf8")
        s=""
        for line in file.readlines():
            s+=line
        self.texte = QLabel(self)
        self.texte.setGeometry(QRect(90, 55, 720, 500))
        self.texte.setText(s)

        #Bouton ok
        self.button = QPushButton("Ok",self)
        self.button.setGeometry(QRect(550, 560, 160, 40))
        self.button.setStyleSheet("QPushButton{border: none; background-color: #70afea}QPushButton::hover{border: none; background-color:  #b2d2f0}")
        self.button.clicked.connect(self.close)

        #Personnalisation fenêtre

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()
    
    def showEvent(self, event):
        self.CenterOnScreen()

    def CenterOnScreen(self):
        screen=QDesktopWidget()
  
        screenGeom = QRect(screen.screenGeometry(self))
  
        screenCenterX = screenGeom.center().x()
        screenCenterY = screenGeom.center().y()
  
        self.move(int(screenCenterX - self.width () / 2),int (screenCenterY - self.height() / 2))

    def paintEvent(self, event):
        painter = QPainter(self)
        background=QBrush(QColor("white"))
        painter.setBrush(background)
        painter.setPen(Qt.NoPen )
        painter.drawRect(0, 0, self.width(), self.height())


if __name__ == '__main__':
    #print(QStyleFactory.keys()) 
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    aqt= AboutQt()
    sys.exit(app.exec_())