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
import os

class Filter_Test(QDialog):
    def __init__(self, attribute, truncation, parent):
        super(Filter_Test, self).__init__(parent)
        self.attribute = attribute
        self.truncation = truncation
        self.attribute_list = ['h', 's', 'p']
        self.attribute_dict= {'h': ['Motorway', 'Trunk', 'Primary', 'Secondary', 'Tertiary', 'Residential', 'Service'],
                              'p': ['None', 'Jeep', 'Bus-UV'],
                              's': [(0,4), (20,4), (40,4), (60,4), (80,4), (100,4), (120,4)]}
        self.folder = "filter_test"
        self.figname = "Filter_Test"
        ######################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running Filter Test: ' + str(self.attribute) + '-' + str(self.truncation))
        self.progress = QProgressBar(self)
        self.layout.addWidget(self.progress, 0, 0)
        self.progress.setMaximum(4)

    def test(self):
        self.show()

        plt.figure(self.figname, figsize=(12,12))

        scale_list = truncatelist(self.truncation, self.attribute_dict[self.attribute])
        size = int(2**(len(scale_list) - 1)) + 1
        scale = 1

        ############################

        N = Network(size, scale)
        N.creategrid()
        corridors = fractalize(scale_list)

        N.fractal_atts(self.attribute, corridors)

        for att in self.attribute_list:
            if att != self.attribute:
                N.same_atts(att, random.choice(self.attribute_dict[att]))

        N.drawnetwork(self.figname)

        self.progress.setValue(1)
        QApplication.processEvents()

        ############################

        OD = ODPair(N, 0, size**2 - 1)
        OD.create_pair()
        OD.draw_pair(self.figname)

        self.progress.setValue(2)
        QApplication.processEvents()

        ############################

        S = Subnetwork(N, OD)
        S.reducenetwork()
        S.compute_affinities()

        S.drawnetwork(self.figname)

        self.progress.setValue(3)
        QApplication.processEvents()

        ############################

        F = FilteredNetwork(N, S)

        F.filter()
        F.clear_edges()
        F.constructgraph()

        F.drawnodes(self.figname)

        self.progress.setValue(4)
        QApplication.processEvents()

        label = str(self.attribute_dict[self.attribute].index(self.truncation))

        if self.attribute != 's':
            save_image(self.folder, self.attribute + label + "_" + str(self.truncation))
        else:
            save_image(self.folder, self.attribute + label + "_" + str(self.truncation[0]) + "-" + str(self.truncation[1]))

        plt.clf()
        self.close()