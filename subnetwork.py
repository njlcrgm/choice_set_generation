from utilities import detourfunction
from utilities import euclideandist
from utilities import scorescale

import networkx as nx
import matplotlib.pyplot as plt

class Subnetwork():
    def __init__(self, network, ODpair):
        self.network = network
        # Graph
        self.graph = nx.Graph()
        self.nodesin = []
        # Choosing Ellipse
        self.origin = ODpair.origin
        self.destination = ODpair.destination
        self.od = 0
        # Scores and Penalties
        self.H_Base = {}
        self.S_Penalty = {}
        self.P_Penalty = {}
        self.hierarchy = {'Motorway': 7, 'Trunk': 6, 'Primary': 5, 'Secondary': 4, 'Tertiary': 3, 'Residential': 2,
                          'Service': 1}
        self.publictransport = {'Bus-UV': 2, 'Jeep': 1, 'None': 0}
        # Normalization
        self.normalS = {}
        self.normalP = {}
        # Final Weights
        self.nodalaffs = {}
        # Drawing Settings
        self.options = {'node_color': 'orange', 'edge_color': 'blue', 'node_size': 20, 'width': 0.5}

    def reducenetwork(self, *args):

        o = self.origin
        d = self.destination
        pos = self.network.pos

        self.od = euclideandist(o, d, pos)
        if len(args) == 0:
            detour = detourfunction(self.od)
        else:
            detour = args[0]

        # Determine nodes inside the ellipse

        for i in self.network.graph.nodes:
            oi = euclideandist(o, i, pos)
            id = euclideandist(i, d, pos)
            if (oi + id) / self.od < detour:
                self.nodesin.append(i)

        S = nx.subgraph(self.network.graph, self.nodesin).copy()

        self.graph = S

        # print "\tNetwork reduced to ellipse with detour factor " + str(detour) + "."

    def compute_affinities(self):

        for node in self.graph.nodes:
            self.H_Base[node] = 0
            self.S_Penalty[node] = self.network.graph.nodes[node]['s']
            self.P_Penalty[node] = 0

        # Average H-scores of adjacent edges for each node

        for node in self.graph.nodes:
            scorelist = scorescale(node, self.network.graph, 7, 1)
            for edge in self.network.graph.edges(node):  # Include weights from adjacent edges outside subnetwork
                n = len(self.network.graph.edges(node))
                hscore = self.network.graph.edges[edge]['h']
                pscore = self.network.graph.edges[edge]['p']
                self.H_Base[node] += float(scorelist[self.hierarchy[hscore]])/n
                self.P_Penalty[node] += float(self.publictransport[pscore])/n

        # Normalize scores of each penalty type

        maxS = float(max(self.S_Penalty.values()))
        maxP = float(max(self.P_Penalty.values()))

        for node in self.graph.nodes:
            if maxS != 0:
                self.normalS[node] = float(self.S_Penalty[node]) / maxS
            else:
                self.normalS[node] = 0

        for node in self.graph.nodes:
            if maxP != 0:
                self.normalP[node] = float(self.P_Penalty[node]) / maxP
            else:
                self.normalP[node] = 0

        # Calculate Nodal Affinity

        for node in self.graph.nodes:
            if node != self.origin and node != self.destination:
                self.nodalaffs[node] = self.nodal_aff(self.H_Base[node], self.normalS[node], self.normalP[node], 0.25, 0.25)
                self.graph.add_node(node, A=self.nodalaffs[node])

    def nodal_aff(self, H, S, P, alpha, beta):
        score = H - alpha * H * S - beta * H * P
        return score

    def drawnetwork(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw(self.graph, self.network.pos, **self.options)

    def drawwithA(self, figname):
        node_labels = nx.get_node_attributes(self.graph, 'A')
        plt.figure(figname, figsize=(12, 12))
        nx.draw_networkx_labels(self.graph, self.network.pos, node_labels)