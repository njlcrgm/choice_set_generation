from network import Network
from subnetwork import Subnetwork
from odpair import ODPair
from filterednetwork import FilteredNetwork
from vertexcover import VertexCover
from hillclimbing import HillClimb

from utilities import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import matplotlib.pyplot as plt
import matplotlib.animation as anim

import random
import copy
import math
import time
import os


class HcPlotObjs(QDialog):
    def __init__(self, size, scale, parent):
        super(HcPlotObjs, self).__init__(parent)
        self.size = size
        self.scale = scale
        self.N = Network(self.size, self.scale)
        self.OD = None
        self.S = None
        self.F = None
        self.VC = None
        self.H = None
        self.figname = 'HC_plot_objs'
        self.folder = 'HC_plot_objs'
        #########################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running Hill Climbing Test: ' + str(self.size) + '-' + str(self.scale))
        self.progress = QProgressBar(self)
        self.progress.setMaximum(6)
        self.layout.addWidget(self.progress, 0, 0)

    def test(self):
        self.show()
        self.N.creategrid()
        self.N.randomize_atts('h', 'Motorway')
        self.N.same_atts('p', 'None')
        self.N.same_atts('s', (0, 6))

        self.progress.setValue(1)
        QApplication.processEvents()

        #########################

        self.OD = ODPair(self.N, 0, self.size ** 2 - 1)
        self.OD.create_pair()

        self.progress.setValue(2)
        QApplication.processEvents()

        #########################

        self.S = Subnetwork(self.N, self.OD)
        self.S.reducenetwork()
        self.S.compute_affinities()

        self.progress.setValue(3)
        QApplication.processEvents()

        #########################

        self.F = FilteredNetwork(self.N, self.S)
        self.F.filter()
        self.F.clear_edges()
        self.F.constructgraph()

        self.progress.setValue(4)
        QApplication.processEvents()

        #########################

        self.VC = VertexCover(self.N, self.S, self.F, len(self.F.filterednodes))
        self.VC.find_best_vc()
        self.VC.constructgraph()

        self.progress.setValue(5)
        QApplication.processEvents()

        #########################

        self.H = HillClimb(0.5, self.N, self.S, self.VC.cover, 1, self.figname)
        self.H.multiple_trials()

        self.progress.setValue(6)
        QApplication.processEvents()

        indexes = []

        for i in range(len(self.H.tv_list)):
            indexes.append(i + 1)

        hcplot, hcplotax = plt.subplots(1, 1, figsize=(12, 12))
        hcplotax.plot(indexes, self.H.tv_list, color='r', marker='o', ms=2, mfc='g', mec='g', lw=2)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        if not os.path.exists(self.folder + '/obj-plots'):
            os.mkdir(self.folder + '/obj-plots')

        hcplot.savefig(self.folder + '/obj-plots' + '/' + str(self.size) + '_' + str(self.scale))

        self.progress.setValue(7)
        QApplication.processEvents()

        plt.clf()
        self.close()
        return max(indexes), self.H.shortest_path_length




