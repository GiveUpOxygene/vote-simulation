from PyQt5.QtCore import Qt,QRect,QPointF
from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor

class Drawing(QWidget):
    def __init__(self,parent):
        super().__init__(parent.tab1)
        self.parent=parent
        self.pix=(QPixmap("./pictures/axes.png")).scaledToHeight(800)
        self.image=QLabel(self)
        self.image.setStyleSheet("background-color: #ffffff;border: 1px solid;border-color: #dadfe5;")
        self.image.setGeometry(QRect(0,0,self.pix.width(),self.pix.height()))
        self.image.setPixmap(self.pix)

    def mousePressEvent(self,event):
        """Méthode appelée lors du click de la souris"""
        if event.buttons() == Qt.LeftButton :
            if not(self.parent.place_voters):
                self.parent.addCandidate(self.parent.randomParticipant(True,self.coord_to_pos(x=event.x()),self.coord_to_pos(y=event.y())))
            else:
                self.parent.addVoter(self.parent.randomParticipant(False,self.coord_to_pos(x=event.x()),self.coord_to_pos(y=event.y())))

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
        painter.drawEllipse(QPointF(x2,y2),size,size)
        painter.end()

    def reset(self):
        self.pix=(QPixmap("./pictures/axes.png")).scaledToHeight(800)
        self.image.setPixmap(self.pix)
    
    
    
            

    


