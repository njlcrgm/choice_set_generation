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


class Vertex_Cover_Test(QDialog):
    def __init__(self, size, scale, parent):
        super(Vertex_Cover_Test, self).__init__(parent)
        self.size = size
        self.scale = scale
        self.N = Network(self.size, self.scale)
        self.OD = None
        self.S = None
        self.F = None
        self.VC = None
        self.figname = 'Vertex_Cover_Test'
        self.folder = 'vertex_cover_test'
        #########################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running Vertex Cover Test: ' + str(self.size) + '-' + str(self.scale))
        self.progress = QProgressBar(self)
        self.layout.addWidget(self.progress, 0, 0)

    def filter(self):
        self.N.creategrid()
        self.N.randomize_atts('h', 'Motorway')
        self.N.randomize_atts('p', 'Bus-UV')
        self.N.randomize_atts('s', (60, 120))

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
        self.F.drawgraph(self.figname)

        #########################

        self.VC = VertexCover(self.N, self.S, self.F, len(self.F.filterednodes))
        self.VC.dummygraph = self.F.graph.copy()

    def vc_approximation(self, i):
        if len(list(self.VC.dummygraph.edges)) != 0 and i < int(math.ceil(len(list(self.F.graph.nodes))/2)) and i > 0:
            edge = random.choice(list(self.VC.dummygraph.edges))

            plt.clf()
            self.N.drawnetwork(self.figname)
            self.OD.draw_pair(self.figname)
            self.S.drawnetwork(self.figname)
            self.F.drawnodes(self.figname)

            self.VC.cover += self.VC.remove_neighbors(edge)

            self.VC.constructgraph()
            self.VC.drawgraph(self.figname)

            self.VC.draw_dummy_graph(self.figname)

            self.progress.setValue(i+1)
            QApplication.processEvents()

        else:
            self.progress.setValue(i + 1)
            QApplication.processEvents()
            pass

    def test(self):
        self.filter()

        frames = int(math.ceil(len(list(self.F.graph.nodes))/2))
        self.progress.setMaximum(frames)
        self.show()

        fig = plt.figure(self.figname, figsize=(12, 12))

        video = anim.FuncAnimation(fig, self.vc_approximation, frames=frames, interval=2000, blit=False)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        video.save(self.folder + '/' + str(self.size) + '_' + str(self.scale) + 'km' + '.mp4', writer='ffmpeg')

        plt.clf()
        self.close()