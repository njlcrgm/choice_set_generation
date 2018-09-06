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

import csv
import random
import copy
import math
import os


class PaperA_Test(QDialog):
    def __init__(self, alpha, network, parent, **kwargs):
        super(PaperA_Test, self).__init__(parent)
        self.N = network
        self.OD = None
        self.S = None
        self.F = None
        self.x = []
        self.y = []
        self.alpha = alpha
        self.graph_mode = kwargs['graph']

        if len(kwargs) != 0:
            self.draw_mode = kwargs['draw_mode']
            self.output_mode = kwargs['output_mode']
        else:
            self.draw_mode = None
            self.output_mode = None

        self.figname = 'PaperA_Test'
        ############################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running PaperA Test: ' + str(self.N.size) + '-' + str(self.N.scale) + 'm_' + str(self.alpha))
        self.progress = QProgressBar(self)
        self.layout.addWidget(self.progress, 0, 0)

    def initialize_test(self):
        if self.graph_mode == 'grid':
            self.OD = ODPair(self.N, 0, self.N.size**2 - 1)
        else:
            self.OD = ODPair(self.N, 0, self.N.size - 1)

        self.OD.create_pair()

        self.S = Subnetwork(self.N, self.OD)
        self.S.reducenetwork()
        self.S.compute_affinities()

        if self.draw_mode == 'draw_output':
            self.N.drawnetwork(self.figname)
            self.OD.draw_pair(self.figname)
            self.S.drawnetwork(self.figname)

    def filter_nlargest(self, n):
        self.F = FilteredNetwork(self.N, self.S)
        self.F.filter(n)
        self.F.clear_edges()

        if self.draw_mode == 'draw_output':
            self.F.drawnodes(self.figname)

        H = HillClimb(self.alpha, self.N, self.S, self.F.filterednodes, 1, self.figname)

        if self.draw_mode == 'draw_output':
            H.multiple_trials(self.draw_mode, self.output_mode)
        else:
            H.multiple_trials()

        self.x.append(n)
        self.y.append(H.optimaltv)

    def test(self, runs, interval):
        self.progress.setMaximum(runs)
        self.show()

        size_tag = str(self.N.size) + '-'
        scale_tag = str(self.N.scale) + 'm'

        for i in range(runs+1):
            self.initialize_test()
            if i == 0:
                self.filter_nlargest(1)
            else:
                self.filter_nlargest(i * interval)

            if self.draw_mode == 'draw_output':
                save_image(str(self.alpha) + size_tag + scale_tag, str(i) + '_' + interval + '_nodes')

            self.progress.setValue(i+1)
            QApplication.processEvents()
            plt.clf()

        plt.plot(self.x, self.y, '-o')

        axes = plt.gca()

        axes.set_xlabel('Number of nodes in V_f (f)')
        axes.set_ylabel('Objective Function Value')

        # txtname = 'paperA_test/no_drawing_' + size_tag + scale_tag + '/' + str(self.alpha) + 'node-obj_plot.csv'

        if self.draw_mode == 'draw_output':
            save_image(str(self.alpha) + size_tag + scale_tag, 'node-obj plot')
        else:
            save_image('paperA_test/no_drawing_' + size_tag + scale_tag, str(self.alpha) + 'node-obj plot')

        # with open(txtname, mode='w') as node_obj_plot:
        #     writer = csv.writer(node_obj_plot, delimiter=',')
        #
        #     writer.writerow(['f', 'obj'])
        #     for i in range(len(self.x)):
        #         writer.writerow([str(self.x[i]), str(self.y[i])])

        plt.clf()
        self.close()

        if self.alpha != 1.00:
            return find_saturation(self.x, self.y)

        else:
            return 0

