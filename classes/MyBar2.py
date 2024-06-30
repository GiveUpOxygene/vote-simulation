import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect,QSize,QPoint
from PyQt5.QtWidgets import QVBoxLayout,QStyle,QTextEdit,QToolButton,QStyle
from PyQt5.QtWidgets import QStatusBar,QToolButton,QMainWindow,QToolBar,QApplication,QFileDialog,QStyleFactory,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette,QKeySequence
from numpy import random
from Classes import *
from votes import *
from math import *

class MyBar(QWidget):
    clickPos = None
    def __init__(self, parent):
        super(MyBar, self).__init__(parent)
        self.resizable=True
        """self.setAutoFillBackground(True)
        
        self.setBackgroundRole(QPalette.Shadow)"""
        # alternatively:
        # palette = self.palette()
        # palette.setColor(palette.Window, Qt.black)
        # palette.setColor(palette.WindowText, Qt.white)
        # self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addStretch()

        self.title = QLabel("My Own Bar", self, alignment=Qt.AlignCenter)
        # if setPalette() was used above, this is not required
        #self.title.setForegroundRole(QPalette.Light)

        style = self.style()
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PM_ButtonMargin) * 2
        self.setMaximumHeight(ref_size + 2)

        btn_size = QSize(ref_size, ref_size)
        icons=dict()
        icons["min"]=QIcon("./pictures/icons/classic/iconMinimize.png")
        icons["normal"]=QIcon("./pictures/icons/classic/iconRestore.png")
        icons["max"]=QIcon("./pictures/icons/classic/iconRestore2.png")
        icons["close"]=QIcon("./pictures/icons/classic/iconClose2.png")

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
                    print(self.window().size().height())
                    print(self.height())
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