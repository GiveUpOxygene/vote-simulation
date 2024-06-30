from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton,QHBoxLayout,QLineEdit,QDialog


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