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

        self.tests = []

        self.ellipse_button = QPushButton('Ellipse Test', self)
        self.filter_button = QPushButton('Filter Test', self)
        self.gc_button = QPushButton('Graph Construction Test', self)
        self.vc_button = QPushButton('Vertex Cover Test', self)
        self.hc_button = QPushButton('Hill Climb Test', self)
        self.hcwp_button = QPushButton('HC w/ Plot Test', self)
        self.standard_button = QPushButton('Standard Test', self)
        self.paperA_button = QPushButton('Paper A Test', self)
        self.run_toggled_button = QPushButton('Run Toggled Tests', self)

        for btn in [self.ellipse_button, self.filter_button, self.gc_button, self.vc_button, self.hc_button,
                    self.hcwp_button, self.standard_button, self.paperA_button]:
            btn.setCheckable(True)

        self.ellipse_button.toggled.connect(lambda: self.add_remove_test(self.ellipse_button, self.test_ellipse))
        self.filter_button.toggled.connect(lambda: self.add_remove_test(self.filter_button, self.test_filter))
        self.gc_button.toggled.connect(lambda: self.add_remove_test(self.gc_button, self.test_graph_construction))
        self.vc_button.toggled.connect(lambda: self.add_remove_test(self.vc_button, self.test_vc))
        self.hc_button.toggled.connect(lambda: self.add_remove_test(self.hc_button, self.test_hill_climb))
        self.hcwp_button.toggled.connect(lambda: self.add_remove_test(self.hcwp_button, self.test_hc_with_plot))
        self.standard_button.toggled.connect(lambda: self.add_remove_test(self.standard_button, self.test_standard))
        self.paperA_button.toggled.connect(lambda: self.add_remove_test(self.paperA_button, self.test_paperA))
        self.run_toggled_button.clicked.connect(self.run_toggled_tests)

        self.ellipse_progress = QProgressBar(self)
        self.filter_progress = QProgressBar(self)
        self.gc_progress = QProgressBar(self)
        self.vc_progress = QProgressBar(self)
        self.hc_progress = QProgressBar(self)
        self.hcwp_progress = QProgressBar(self)
        self.standard_progress = QProgressBar(self)
        self.paperA_progress = QProgressBar(self)
        self.run_toggled_progress = QProgressBar(self)

        self.layout.addWidget(self.ellipse_button, 0, 0)
        self.layout.addWidget(self.filter_button, 1, 0)
        self.layout.addWidget(self.gc_button, 2, 0)
        self.layout.addWidget(self.vc_button, 3, 0)
        self.layout.addWidget(self.hc_button, 4, 0)
        self.layout.addWidget(self.hcwp_button, 5, 0)
        self.layout.addWidget(self.standard_button, 6, 0)
        self.layout.addWidget(self.paperA_button, 7, 0)
        self.layout.addWidget(self.run_toggled_button, 8, 0)

        self.layout.addWidget(self.ellipse_progress, 0, 1)
        self.layout.addWidget(self.filter_progress, 1, 1)
        self.layout.addWidget(self.gc_progress, 2, 1)
        self.layout.addWidget(self.vc_progress, 3, 1)
        self.layout.addWidget(self.hc_progress, 4, 1)
        self.layout.addWidget(self.hcwp_progress, 5, 1)
        self.layout.addWidget(self.standard_progress, 6, 1)
        self.layout.addWidget(self.paperA_progress, 7, 1)
        self.layout.addWidget(self.run_toggled_progress, 8, 1)

    def add_remove_test(self, button, test):
        if button.isChecked():
            self.tests.append(test)
        else:
            self.tests.remove(test)

    def test_ellipse(self):
        size_iterations = [30]
        scale_iterations = [5]
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
        iterations = [30]
        self.hc_progress.setMaximum(len(iterations))

        for i in range(len(iterations)):
            H = Hill_Climb_Test(iterations[i], 5, 1000, 'simple', self)
            H.test()
            self.hc_progress.setValue(i + 1)
            QApplication.processEvents()

    def test_hc_with_plot(self):
        sizes = [30]
        scales = [5]

        points = []

        self.hcwp_progress.setMaximum(len(sizes)*len(scales))

        for i in range(len(sizes)):
            for j in range(len(scales)):
                hcwp = HcPlotObjs(sizes[i], scales[j], self)
                value = hcwp.test()
                points.append(value)

                self.hcwp_progress.setValue(i * len(scales) + j + 1)

        coordinates = zip(*points)

        fig, ax = plt.subplots(1, 1, figsize=(12,12))
        ax.plot(list(coordinates[0]), list(coordinates[1]), '-ro')
        fig.savefig('HC_plot_objs/' + 'iter_vs_shortest.png')

    def test_standard(self):
        size = 30
        scale = 5
        origin = 0
        destination = int(size ** 2 - 1)
        # destination = size - 1
        h_in_list = ['Motorway', 'Trunk', 'Primary', 'Secondary', 'Tertiary', 'Residential', 'Service']
        p_in = 'None'
        s_in = (0, 6)
        hctrials = 1

        self.standard_progress.setMaximum(len(h_in_list))

        if not os.path.exists('standard_test'):
            os.mkdir('standard_test')

        for item in h_in_list:
            ST = Standard_Test(self, size, scale, o=origin, d=destination, random=['h'], same=['s', 'p'], random_c=[],
                               h=item, p=p_in, s=s_in, hctrials=hctrials, mode='leaf_mode', exp_corridor=False,
                               realize=False)
            ST.test()
            i = h_in_list.index(item)
            self.standard_progress.setValue(i+1)
            QApplication.processEvents()

    def test_paperA(self):
        sizes = [30]
        scales = [5]
        iterations = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        self.paperA_progress.setMaximum(len(sizes) * len(scales) * len(iterations))

        for z in range(len(sizes)):
            for c in range(len(scales)):
                values = [0 for k in range(len(iterations))]
                if not os.path.exists('paperA_test'):
                    os.mkdir('paperA_test')

                N = Network(sizes[z], scales[c])
                N.creategrid()
                N.randomize_atts('h', 'Motorway')
                N.same_atts('p', 'None')
                N.same_atts('s', (0, 6))
                N.assign_edge_weights()

                for i in range(len(iterations)):
                    P = PaperA_Test(iterations[i], N, self, graph='grid', draw_mode=None, output_mode=None)
                    y = P.test(int(round((sizes[z]**2)/10)), 10)
                    values[i] = y
                    self.paperA_progress.setValue(z*len(scales)*len(iterations) + c*len(iterations) + i + 1)
                    QApplication.processEvents()

                plt.plot(iterations, values, '-ro')

                axes = plt.gca()

                axes.set_xlabel('alpha')
                axes.set_ylabel('Candidate Nodes Saturation Point')

                size_tag = str(N.size) + '-'
                scale_tag = str(N.scale) + 'm'
                alpha_start_tag = str(iterations[0])
                alpha_end_tag = str(iterations[len(iterations)-1])
                filename = size_tag + scale_tag + '-' + alpha_start_tag + '-' + alpha_end_tag

                save_image('paperA_test/alpha-fn_plots', filename)

                txtname = 'paperA_test/alpha-fn_plots/' + filename + '.csv'

                with open(txtname, mode='w') as node_obj_plot:
                    writer = csv.writer(node_obj_plot, delimiter=',')

                    writer.writerow(['f', 'obj'])
                    for i in range(len(iterations)):
                        writer.writerow([str(iterations[i]), str(values[i])])

                plt.clf()

                N.drawnetwork('network')
                save_image('paperA_test/alpha-fn_plots', 'network')

    def run_toggled_tests(self):
        self.run_toggled_progress.setMaximum(len(self.tests))
        p = 0
        for test in self.tests:
            test()
            p += 1
            self.run_toggled_progress.setValue(p)

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

