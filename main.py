from PySide2.QtWidgets import *
from PySide2.QtCore import *
from utilities import *
from network import Network

from hc_plot_objs_test import *
from paperA_test import *
from standard_test import *
from hc_test import *
from vc_test import *
from gc_test import *
from filter_test import *
from ellipse_test import *

import matplotlib.pyplot as plt
import math
import sys
import os

class ProgressWindow(QWidget):
    def __init__(self):
        super(ProgressWindow, self).__init__()

        self.layout = QGridLayout(self)
        self.setGeometry(100, 100, 800, 360)
        self.setWindowTitle('Choice Set Generation')

        self.ellipse_button = QPushButton('Ellipse Test', self)
        self.filter_button = QPushButton('Filter Test', self)
        self.gc_button = QPushButton('Graph Construction Test', self)
        self.vc_button = QPushButton('Vertex Cover Test', self)
        self.hc_button = QPushButton('Hill Climb Test', self)
        self.hcwp_button = QPushButton('HC w/ Plot Test', self)
        self.standard_button = QPushButton('Standard Test', self)
        self.paperA_button = QPushButton('Paper A Test', self)

        self.ellipse_button.clicked.connect(self.test_ellipse)
        self.filter_button.clicked.connect(self.test_filter)
        self.gc_button.clicked.connect(self.test_graph_construction)
        self.vc_button.clicked.connect(self.test_vc)
        self.hc_button.clicked.connect(self.test_hill_climb)
        self.hcwp_button.clicked.connect(self.hc_test_with_plot)
        self.standard_button.clicked.connect(self.test_standard)
        self.paperA_button.clicked.connect(self.test_paperA)

        self.ellipse_progress = QProgressBar(self)
        self.filter_progress = QProgressBar(self)
        self.gc_progress = QProgressBar(self)
        self.vc_progress = QProgressBar(self)
        self.hc_progress = QProgressBar(self)
        self.hcwp_progress = QProgressBar(self)
        self.standard_progress = QProgressBar(self)
        self.paperA_progress = QProgressBar(self)

        self.layout.addWidget(self.ellipse_button, 0, 0)
        self.layout.addWidget(self.filter_button, 1, 0)
        self.layout.addWidget(self.gc_button, 2, 0)
        self.layout.addWidget(self.vc_button, 3, 0)
        self.layout.addWidget(self.hc_button, 4, 0)
        self.layout.addWidget(self.hcwp_button, 5, 0)
        self.layout.addWidget(self.standard_button, 6, 0)
        self.layout.addWidget(self.paperA_button, 7, 0)

        self.layout.addWidget(self.ellipse_progress, 0, 1)
        self.layout.addWidget(self.filter_progress, 1, 1)
        self.layout.addWidget(self.gc_progress, 2, 1)
        self.layout.addWidget(self.vc_progress, 3, 1)
        self.layout.addWidget(self.hc_progress, 4, 1)
        self.layout.addWidget(self.hcwp_progress, 5, 1)
        self.layout.addWidget(self.standard_progress, 6, 1)
        self.layout.addWidget(self.paperA_progress, 7, 1)

    def test_ellipse(self):
        size_iterations = [10, 50, 100]
        scale_iterations = [0.5, 5, 10]
        mode = 'slanted'

        self.ellipse_progress.setMaximum(len(size_iterations)*len(scale_iterations))

        for i in range(len(size_iterations)):
            for j in range(len(scale_iterations)):
                ellipse_test = EllipseTest(size_iterations[i], scale_iterations[j], mode, self)
                ellipse_test.test()
                self.ellipse_progress.setValue(i * len(scale_iterations) + j + 1)
                QApplication.processEvents()

    def test_filter(self):
        iterations = {'h': ['Motorway', 'Trunk', 'Primary', 'Secondary', 'Tertiary', 'Residential', 'Service'],
                      'p': ['None', 'Jeep', 'Bus-UV'],
                      's': [(0, 4), (20, 4), (40, 4), (60, 4), (80, 4), (100, 4), (120, 4)]}

        self.filter_progress.setMaximum(len(iterations['h']) + len(iterations['p']) + len(iterations['s']))

        counter = 0

        for key in iterations:
            for item in iterations[key]:
                filter_test = Filter_Test(key, item, self)
                filter_test.test()
                counter += 1
                self.filter_progress.setValue(counter)
                QApplication.processEvents()

    def test_graph_construction(self):
        iterations = [10, 20, 25, 50, 100]
        self.gc_progress.setMaximum(len(iterations))

        for i in range(len(iterations)):
            GC = Graph_Const_Test(iterations[i], int(100 / iterations[i]), self)
            GC.test()
            self.gc_progress.setValue(i + 1)
            QApplication.processEvents()

    def test_vc(self):
        iterations = [10, 20, 25, 50, 100]
        self.vc_progress.setMaximum(len(iterations))

        for i in range(len(iterations)):
            VC = Vertex_Cover_Test(iterations[i], int(100 / iterations[i]), self)
            VC.test()
            self.vc_progress.setValue(i + 1)
            QApplication.processEvents()

    def test_hill_climb(self):
        # iterations = [10, 20, 25, 50, 100]
        iterations = [100]
        self.hc_progress.setMaximum(len(iterations))

        for i in range(len(iterations)):
            H = Hill_Climb_Test(iterations[i], 1, 1000, 'simple', self)
            H.test()
            self.hc_progress.setValue(i + 1)
            QApplication.processEvents()

    def test_standard(self):
        size = 100
        scale = 0.5
        origin = 0
        destination = int(size ** 2 - 1)
        h_in_list = ['Motorway', 'Trunk', 'Primary', 'Secondary', 'Tertiary', 'Residential', 'Service']
        p_in = 'None'
        s_in = (0, 6)
        hctrials = 1

        self.standard_progress.setMaximum(len(h_in_list))

        if not os.path.exists('standard_test'):
            os.mkdir('standard_test')

        for item in h_in_list:
            ST = Standard_Test(self, size, scale, o=origin, d=destination, random=[], same=['s', 'p'], random_c=['h'],
                               h=item, p=p_in, s=s_in, hctrials=hctrials, mode='path_mode')
            ST.test()
            i = h_in_list.index(item)
            self.standard_progress.setValue(i+1)
            QApplication.processEvents()

    def test_paperA(self):
        iterations = [0.0, 0.25, 0.5, 0.75, 1]
        values = [0 for i in range(len(iterations))]

        self.paperA_progress.setMaximum(len(iterations))

        if not os.path.exists('paperA_test'):
            os.mkdir('paperA_test')

        N = Network(10, 5)
        N.creategrid()
        N.randomize_atts('h', 'Motorway')
        N.same_atts('p', 'None')
        N.same_atts('s', (0, 6))

        for i in range(len(iterations)):
            P = PaperA_Test(iterations[i], N, self)
            y = P.test(25, 4)
            values[i] = y
            self.paperA_progress.setValue(i + 1)
            QApplication.processEvents()

        plt.plot(iterations, values)
        size_tag = str(N.size) + '-'
        scale_tag = str(N.scale) + 'm'
        alpha_start_tag = str(iterations[0])
        alpha_end_tag = str(iterations[len(iterations)-1])
        save_image('paperA_test/alpha-fn_plots', size_tag + scale_tag + '-' + alpha_start_tag + '-' + alpha_end_tag)
        plt.clf()

    def hc_test_with_plot(self):
        sizes = [50]
        scales = [1]

        self.hcwp_progress.setMaximum(len(sizes)*len(scales))

        for i in range(len(sizes)):
            for j in range(len(scales)):
                hcwp = HcPlotObjs(sizes[i], scales[j], self)
                hcwp.test()
                self.hcwp_progress.setValue(i * len(scales) + j + 1)

def main():
    if not os.path.exists('tests'):
        os.mkdir('tests')

    os.chdir('tests')

    app = QApplication(sys.argv)
    P = ProgressWindow()

    P.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

