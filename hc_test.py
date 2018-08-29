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

class Hill_Climb_Test(QDialog):
    def __init__(self, size, scale, frames, mode, parent):
        super(Hill_Climb_Test, self).__init__(parent)
        self.size = size
        self.scale = scale
        self.N = Network(self.size, self.scale)
        self.OD = None
        self.S = None
        self.F = None
        self.VC = None
        self.H = None
        self.mode = mode
        self.frames = frames
        self.figname = 'Hill_Climb_Test'
        self.folder = 'hill_climb_test'
        #########################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running Hill Climbing Test: ' + str(self.size) + '-' + str(self.scale))
        self.progress = QProgressBar(self)
        self.layout.addWidget(self.progress, 0, 0)

    def filter(self):
        self.N.creategrid()
        self.N.randomize_atts('h', 'Motorway')
        self.N.same_atts('p', 'None')
        self.N.same_atts('s', (0, 6))

        self.N.drawnetwork(self.figname)

        #########################

        self.OD = ODPair(self.N, 0, self.size**2 - 1)
        self.OD.create_pair()
        self.OD.draw_pair(self.figname)

        #########################

        self.S = Subnetwork(self.N, self.OD)
        self.S.reducenetwork()
        self.S.compute_affinities()
        self.S.drawnetwork(self.figname)

        #########################

        self.F = FilteredNetwork(self.N, self.S)
        self.F.filter()
        self.F.clear_edges()
        self.F.constructgraph()
        self.F.drawnodes(self.figname)

        #########################

        self.VC = VertexCover(self.N, self.S, self.F, len(self.F.filterednodes))
        self.VC.find_best_vc()
        self.VC.constructgraph()

        #########################
        coverlen = len(self.VC.cover)
        self.frames = count_chances(coverlen, coverlen)
        self.progress.setMaximum(self.frames)

        self.H = HillClimb(0.5, self.N, self.S, self.VC.cover, 1, self.figname)
        self.H.init_hill_climb()

        self.H.optimalpath = self.H.iterations['guess'][0]
        self.H.optimaltv = self.H.iterations['guess'][1]

        if self.mode == 'simple':
            self.H.determine_simplified_optimal_path()
        else:
            self.H.determine_optimal_path()

        self.N.drawnetwork(self.figname)
        self.OD.draw_pair(self.figname)
        self.S.drawnetwork(self.figname)
        self.F.drawnodes(self.figname)
        self.VC.drawgraph(self.figname)
        self.H.draw_optimal_path(self.figname)

    def climb(self, i):
        plt.clf()
        self.N.drawnetwork(self.figname)
        self.OD.draw_pair(self.figname)
        self.S.drawnetwork(self.figname)
        self.F.drawnodes(self.figname)
        self.VC.drawgraph(self.figname)

        self.H.hill_climb(mode='animate', drawing=self.mode)

        self.progress.setValue(i+1)
        QApplication.processEvents()

    def test(self):
        self.filter()

        self.show()

        fig = plt.figure(self.figname, figsize=(12, 12))

        video = anim.FuncAnimation(fig, self.climb, frames=self.frames, interval=100, blit=False)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        video.save(self.folder + '/' + str(self.size) + '_' + str(self.scale) + 'km' + '.mp4', writer='ffmpeg')

        plt.clf()
        self.close()