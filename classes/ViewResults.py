import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.cm as cm
import numpy as np

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class ViewResults(FigureCanvasQTAgg):

    def __init__(self, parent=None,candidates=None,voters=None,width=5, height=4, dpi=100):
        if candidates==None:
            candidates=parent.dictcandidates
        if voters==None:
            voters=parent.dictvoters
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
        
        
        

        