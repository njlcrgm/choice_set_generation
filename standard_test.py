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


class Standard_Test(QDialog):
    def __init__(self, parent, size, scale, **kwargs):
        super(Standard_Test, self).__init__(parent)
        self.size = size
        self.scale = scale
        ########################
        self.origin = kwargs['o']
        self.destination = kwargs['d']
        ########################
        self.random = kwargs['random']
        self.same = kwargs['same']
        self.random_c = kwargs['random_c']
        self.input = {'h': kwargs['h'], 'p': kwargs['p'], 's': kwargs['s']}
        self.exp_corridor = kwargs['exp_corridor']
        self.realize = kwargs['realize']
        ########################
        self.hctrials = kwargs['hctrials']
        self.mode = kwargs['mode']
        ########################
        self.figname = 'Standard_Test'
        self.folder = str(self.size) + '_' + str(self.scale) + 'km'
        ######################
        self.layout = QGridLayout(self)
        self.setGeometry(900, 100, 500, 60)
        self.setWindowTitle('Running Standard Test: ' + str(self.size) + '-' + str(self.scale))
        self.progress = QProgressBar(self)
        self.layout.addWidget(self.progress, 0, 0)
        self.progress.setMaximum(7)

    def test(self):

        self.show()

        N = Network(self.size, self.scale)
        N.creategrid()

        for i in self.random:
            N.randomize_atts(i, self.input[i])

        for i in self.same:
            N.same_atts(i, self.input[i])

        for i in self.random_c:
            N.randomize_atts_corridors(i, self.input[i])

        if self.exp_corridor:
            N.create_corridor('h', ['Motorway'], 'row', [int(self.size/2)])
            N.create_corridor('p', ['None'], 'row', [int(self.size / 2)])
            N.create_corridor('s', [(0,6)], 'row', [int(self.size / 2)])

            # N.create_corridor('h', ['Motorway'], 'column', [int(0)])
            # N.create_corridor('p', ['None'], 'column', [int(0)])
            # N.create_corridor('s', [(0, 6)], 'column', [int(0)])

            # N.create_corridor('h', ['Motorway'], 'column', [int(self.size - 1)])
            # N.create_corridor('p', ['None'], 'column', [int(self.size - 1)])
            # N.create_corridor('s', [(0, 6)], 'column', [int(self.size - 1)])

        if self.realize:
            N.realize_network(self.origin, self.destination)

        N.assign_edge_weights()

        N.drawnetwork(self.figname)

        print 'Network Created.'

        self.progress.setValue(1)
        QApplication.processEvents()

        #################################

        OD = ODPair(N, self.origin, self.destination)
        OD.create_pair()
        OD.draw_pair(self.figname)

        print 'OD Created'

        self.progress.setValue(2)
        QApplication.processEvents()

        #################################

        S = Subnetwork(N, OD)
        S.reducenetwork()
        S.compute_affinities()
        S.drawnetwork(self.figname)

        print 'Subnetwork Created'

        self.progress.setValue(3)
        QApplication.processEvents()

        #################################

        F = FilteredNetwork(N, S)
        F.filter(50)
        F.clear_edges()
        F.constructgraph()
        F.drawnodes(self.figname)

        self.progress.setValue(4)
        QApplication.processEvents()

        print 'Filter done'
        print len(F.filterednodes)

        #################################
        #
        # VC = VertexCover(N, S, F, len(F.filterednodes))
        # VC.find_best_vc()
        # VC.constructgraph()
        # VC.drawgraph(self.figname)
        #
        # self.progress.setValue(5)
        # QApplication.processEvents()
        #
        # print 'VC determined'

        #################################

        HC = HillClimb(0.5, N, S, F.filterednodes, self.hctrials, self.figname)
        HC.multiple_trials('draw_output', self.mode)

        self.progress.setValue(6)
        QApplication.processEvents()

        print 'Hill Climb done'

        #################################

        randomtags = str()
        sametags = str()

        for i in self.random:
            randomtags += i

        for j in self.random_c:
            randomtags += (j + '-')

        for k in self.same:
            sametags += k

        taglist = {'Motorway': 1, 'Trunk': 2, 'Primary': 3, 'Secondary': 4, 'Tertiary': 5,
                            'Residential': 6,
                            'Service': 7}
        htag = str(taglist[self.input['h']]) + '-' + str(self.input['h'])
        ptag = str(self.input['p'])
        stag = str(self.input['s'][0]) + '-' + str(self.input['s'][1])

        if not os.path.exists('standard_test/' + self.folder):
            os.mkdir('standard_test/' + self.folder)

        save_image('standard_test/' + self.folder + '/' + 'R' + randomtags + '_' + 'S' + sametags, '_' + htag + ptag + stag)

        self.progress.setValue(7)
        QApplication.processEvents()

        plt.clf()
        self.close()