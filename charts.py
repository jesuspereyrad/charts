import sys

import pandas as pd
import math

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class ScrollableWindow(QtWidgets.QMainWindow):
    """
    A class used to render scrollable windows

    ...

    Attributes
    ----------
    QtWidgets : QT5 Object
        
   
    Methods
    -------
    __init__(self, fig)
        Render scrollable windows
    """
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])

        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.show()
        exit(self.qapp.exec_())


def charts(source, windows, x=20, y=8):
     """
    Render line charts using matplotlib .

    If the argument `x` isn't passed in, the default x is 20
    If the argument `y` isn't passed in, the default y is 8
    
    Parameters
    ----------
    source : str
        The path of the file
    windows : int
        The number to split the graphs
    x : int
        The widht of the render chart
    y : int
        The height of the render chart
    """
    df = pd.read_csv(source)
    i = df.shape[0]/windows
    i = i if df.shape[0] % windows == 0 else math.ceil(i)
    fig, axs = plt.subplots(i, figsize=(x,y * i), constrained_layout=False)
    plt.subplots_adjust(hspace=0.5)
    for j in range(i):
        start = windows * j
        end = windows * (j+1)
        end = end if end < df.shape[0] else (start + (df.shape[0] % windows))
        axs[j].plot(df.iloc[start:end, 0], df.iloc[start:end, 1], label = df.columns[1])
        axs[j].plot(df.iloc[start:end, 0], df.iloc[start:end, 2], label = df.columns[2])
        axs[j].set_xlabel(df.columns[0], fontsize=12)
        axs[j].tick_params(labelrotation=90)
        axs[j].set_title(df.columns[1] + ' vs ' + df.columns[2] + ' from ' + df.iloc[:, 0][start] + ' to ' + df.iloc[:,0][end-1],  pad=12, fontsize=24)
        axs[j].legend()
    ScrollableWindow(fig)


# TODO ADD inline data

if __name__ == '__main__':
    if len(sys.argv) > 3:
        charts(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    charts(sys.argv[1], int(sys.argv[2]))

