import networkx as nx
import matplotlib.pyplot as plt

class ODPair():
    def __init__(self, network, origin, destination):
        self.graph = nx.Graph()
        self.network = network
        self.origin = origin
        self.destination = destination
        self.options = {'node_color': 'black', 'node_size': 110, 'width': 1}

        # print '\tODPair created with origin at node ' + str(self.origin) + ' and destination at node ' + str(self.destination) + '.'

    def create_pair(self):
        pair = [self.origin, self.destination]
        self.graph = nx.subgraph(self.network.graph, pair)

    def draw_pair(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw(self.graph, self.network.pos, **self.options)
