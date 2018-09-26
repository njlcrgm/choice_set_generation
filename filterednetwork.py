from utilities import detourfunction
from utilities import euclideandist
from heapq import nlargest

import networkx as nx
import matplotlib.pyplot as plt

class FilteredNetwork():
    def __init__(self, network, subnetwork):
        self.graph = nx.Graph()
        self.subnetwork = subnetwork
        self.network = network
        self.filternumber = 0
        self.filterednodes = []
        self.options = {'node_color': 'black', 'edge_color': 'green', 'node_size': 50, 'width': 0.5}
        self.randomnode = 0

    def filter(self, *args):
        nodalaffs = self.subnetwork.nodalaffs

        shortpath = nx.shortest_path(self.subnetwork.graph, self.subnetwork.origin, self.subnetwork.destination, weight = 'w')

        if len(args) == 0:
            filternumber = len(shortpath) - 2
        else:
            filternumber = args[0]

        self.filterednodes = nlargest(filternumber, nodalaffs, key=nodalaffs.get)
        self.graph = nx.subgraph(self.subnetwork.graph, self.filterednodes).copy()

    def clear_edges(self):
        erredges = []

        for edge in self.graph.edges:
            erredges.append(edge)

        self.graph.remove_edges_from(erredges)

    def constructgraph(self):

        for node in self.graph.nodes:
            self.connect_node(node)

    def connect_node(self, node):
        o = self.subnetwork.origin
        i = node
        d = self.subnetwork.destination

        pos = self.network.pos

        for k in self.graph.nodes:
            if k != i:
                oi = euclideandist(o, i, pos)
                ok = euclideandist(o, k, pos)
                ki = euclideandist(k, i, pos)
                id = euclideandist(i, d, pos)
                ik = euclideandist(i, k, pos)
                kd = euclideandist(k, d, pos)
                detour = detourfunction(self.subnetwork.od)
                if ((ok + ki) / oi <= detour) and ((ik + kd) / id <= detour):
                    self.graph.add_edge(i, k)
            else:
                pass

    def drawgraph(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw(self.graph, self.network.pos, **self.options)

    def drawnodes(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw_networkx_nodes(self.graph, self.network.pos, **self.options)
