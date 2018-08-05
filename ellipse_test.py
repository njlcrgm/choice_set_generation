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

class EllipseTest(QDialog):
    def __init__(self, size, scale, mode, parent):
        super(EllipseTest, self).__init__(parent)
        self.size = size
        self.scale = scale
        ######################
        self.N = None
        self.OD = None
        self.S = None
        ######################
        self.end = int(math.floor((self.size**2 - 1)/2))
        self.pivot = int(self.end - math.floor(self.size/2) + 1)
        self.start = int(self.end - math.floor(self.size) + 1)
        ######################
        self.folder = 'ellipse_test'
        self.figname = "Ellipse_Test"
        self.mode = mode
        ######################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running Ellipse Test: ' + str(self.size) + '-' + str(self.scale))
        self.progress = QProgressBar(self)
        self.layout.addWidget(self.progress, 0, 0)
        self.progress.setMaximum(self.size)

    def create_ellipse(self, i):
        plt.clf()
        node = i + self.start

        if node != self.pivot and node <= self.end:
            plt.clf()

            self.N = Network(self.size, self.scale)
            self.N.creategrid()
            self.N.drawnetwork(self.figname)

            self.OD = ODPair(self.N, self.pivot, node)
            self.OD.create_pair()
            self.OD.draw_pair(self.figname)

            self.S = Subnetwork(self.N, self.OD)
            self.S.reducenetwork()
            self.S.drawnetwork(self.figname)
            self.progress.setValue(i+1)
            QApplication.processEvents()

    def create_ellipse_slanted(self, i):
        plt.clf()
        z = i + 1
        o = (z - 1) * (self.size + 1)
        d = (self.size - z) * (self.size + 1)

        self.N = Network(self.size, self.scale)
        self.N.creategrid()
        self.N.drawnetwork(self.figname)

        self.OD = ODPair(self.N, o, d)
        self.OD.create_pair()
        self.OD.draw_pair(self.figname)

        self.S = Subnetwork(self.N, self.OD)
        self.S.reducenetwork()
        self.S.drawnetwork(self.figname)
        self.progress.setValue(i + 1)
        QApplication.processEvents()

    def test(self):
        self.show()

        fig = plt.figure(self.figname, figsize=(12, 12))

        if self.mode == "straight":
            video = anim.FuncAnimation(fig, self.create_ellipse, frames=self.size, interval=100, blit=False)
        elif self.mode == "slanted":
            video = anim.FuncAnimation(fig, self.create_ellipse_slanted, frames = self.size, interval = 100, blit = False)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        video.save(self.folder + '/' + str(self.size) + '_' + str(self.scale) + 'km' + '.mp4', writer = 'ffmpeg')

        plt.clf()
        self.close()