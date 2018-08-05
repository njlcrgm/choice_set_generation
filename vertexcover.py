import networkx as nx
import matplotlib.pyplot as plt
import random
import operator

class VertexCover():
    def __init__(self, network, subnetwork, filterednetwork, vctrials):
        self.network = network
        self.subnetwork = subnetwork
        self.filterednetwork = filterednetwork
        ########################
        self.cover = []
        self.dummycover = []
        ########################
        self.graph = nx.Graph()
        self.dummygraph = nx.Graph()
        ########################
        self.vctrials = vctrials
        self.options = {'node_color': 'brown', 'node_size': 60, 'width': 1}
        self.foptions = {'node_color': 'black', 'edge_color': 'green', 'node_size': 20, 'width': 0.5}

    def find_best_vc(self):
        VCscores = {}

        for i in range(self.vctrials):
            vc = self.find_2approx_vc()

            vcscore = self.evaluateVC(vc)

            VCscores[tuple(vc)] = vcscore

        maxvalue = max(VCscores.iteritems(), key=operator.itemgetter(1))[0]

        self.cover = list(maxvalue)

    def find_2approx_vc(self):
        self.dummygraph = self.filterednetwork.graph.copy()
        cover = []

        while len(self.dummygraph.edges) != 0:
            edge = random.choice(self.dummygraph.edges.keys())
            result = self.remove_neighbors(edge)
            cover += result

        return cover

    def remove_neighbors(self, edge):
        edgenodes = list(edge)

        A = set(list(self.dummygraph.nodes.keys()))

        for node in edgenodes:
            A = A - set(edgenodes) - set(self.dummygraph.neighbors(node))

        remainingnodes = list(A)
        self.dummygraph = nx.subgraph(self.dummygraph, remainingnodes).copy()

        return edgenodes

    def evaluateVC(self, VC):
        nodalaffs = self.subnetwork.nodalaffs

        VCscore = 0

        for i in range(len(VC)):
            VCscore += nodalaffs[VC[i]]
            for node in self.filterednetwork.graph.neighbors(VC[i]):
                VCscore += nodalaffs[node]

        score = VCscore/len(VC)

        return score

    def draw_dummy_graph(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw(self.dummygraph, self.network.pos, **self.foptions)

    def constructgraph(self):
        self.graph = nx.subgraph(self.filterednetwork.graph, self.cover)

    def drawgraph(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw_networkx_nodes(self.graph, self.network.pos, **self.options)









