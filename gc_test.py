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


class Graph_Const_Test(QDialog):
    def __init__(self, size, scale, parent):
        super(Graph_Const_Test, self).__init__(parent)
        self.size = size
        self.scale = scale
        self.N = Network(self.size, self.scale)
        self.OD = None
        self.S = None
        self.F = None
        self.nodes_list = []
        self.figname = 'Graph_Construction'
        self.folder = 'graph_construction_test'
        ######################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running Graph Construction Test: ' + str(self.size) + '-' + str(self.scale))
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
        self.F.drawnodes(self.figname)

        self.nodes_list = copy.copy(list(self.F.graph.nodes))

    def node_graph(self, i):
        node = self.nodes_list[i]
        self.F.connect_node(node)

        self.F.drawgraph(self.figname)

        self.progress.setValue(i + 1)
        QApplication.processEvents()

    def test(self):
        self.filter()

        frames = len(self.nodes_list)
        self.progress.setMaximum(frames)
        self.show()

        fig = plt.figure(self.figname, figsize=(12, 12))

        video = anim.FuncAnimation(fig, self.node_graph, frames=frames, interval=500, blit=False)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        video.save(self.folder + '/' + str(self.size) + '_' + str(self.scale) + 'km' + '.mp4', writer='ffmpeg')

        plt.clf()
        self.close()