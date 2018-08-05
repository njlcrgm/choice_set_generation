from utilities import euclideandist
from collections import Counter

import networkx as nx
import matplotlib.pyplot as plt
import random
import operator
import copy

class HillClimb():
    def __init__(self, alpha, network, subnetwork, vertexset, trials, figname):
        ##########################
        self.network = network
        self.subnetwork = subnetwork
        self.origin = subnetwork.origin
        self.destination = subnetwork.destination
        self.vertexset = vertexset
        self.alpha = alpha
        ##########################
        self.iterations = {}
        self.counter = 0
        self.consistency = 0
        self.consistencylimit = 100*len(vertexset)
        ##########################
        self.optimaltv = 0
        self.optimalpath = []
        self.optimalset = []
        ##########################
        self.buffer = {}
        self.frequencies = {}
        ##########################
        self.graph = nx.Graph()
        self.leaf = nx.Graph()
        ##########################
        self.trials = trials
        self.figname = figname
        self.nodeoptions = {'node_color': 'red', 'node_size': 50}
        self.pathoptions = {'node_color': 'brown', 'edge_color': 'brown', 'node_size': 1, 'width': 3}
        self.leafoptions = {'node_color': 'blue', 'edge_color': 'blue', 'node_size': 1, 'width': 3}

    def multiple_trials(self, *args):
        if len(self.vertexset) != 1:
            opt_tv_list = []

            for i in range(self.trials):
                self.init_hill_climb()
                opt_tv = self.hill_climb()
                opt_tv_list.append(opt_tv)

                if len(args) != 0 and args[0] == 'draw_output':
                    self.determine_optimal_path()
                    self.draw_optimal_nodes(self.figname)
                    if args[1] == 'leaf_mode':
                        self.draw_leaf(self.figname)
                    elif args[1] == 'path_mode':
                        self.draw_optimal_path(self.figname)

                optimalnodes = copy.copy(self.optimalpath)
                self.optimalset += optimalnodes

            self.optimaltv = sum(opt_tv_list)/len(opt_tv_list)
            self.frequencies = Counter(self.optimalset)

        else:
            self.optimalpath = self.vertexset
            self.optimaltv = self.findtvratio(self.vertexset, self.alpha)

            if len(args) != 0 and args[0] == 'draw_output':
                self.determine_optimal_path()
                self.draw_optimal_nodes(self.figname)
                if args[1] == 'leaf_mode':
                    self.draw_leaf(self.figname)
                elif args[1] == 'path_mode':
                    self.draw_optimal_path(self.figname)

            for i in range(self.trials):
                optimalnodes = copy.copy(self.optimalpath)
                self.optimalset += optimalnodes

            self.frequencies = Counter(self.optimalset)

    def init_hill_climb(self):
        self.iterations = {'guess': [[], 0], 'jump': [[], 0]}

        origindist = {}
        for node in self.vertexset:
            origindist[node] = euclideandist(self.origin, node, self.network.pos)

        initialtuples = sorted(origindist.items(), key=operator.itemgetter(1))

        initial = []

        for i in range(len(initialtuples)):
            initial.append(initialtuples[i][0])

        self.iterations['guess'][0] = copy.copy(initial)
        self.iterations['jump'][0] = copy.copy(initial)
        self.iterations['guess'][1] = self.findtvratio(self.iterations['guess'][0], self.alpha)
        self.iterations['jump'][1] = self.findtvratio(self.iterations['jump'][0], self.alpha)

    def hill_climb(self):
        while self.consistency <= self.consistencylimit:
            self.counter = self.climb_trial(self.counter)

        self.optimalpath = self.iterations['guess'][0]
        optimaltv = self.iterations['guess'][1]

        return optimaltv

    def climb_trial(self, i):
        status = self.checkstatus(self.iterations['guess'][0])
        guesscopy = copy.copy(self.iterations['guess'][0])
        jump = self.randomjump(status, guesscopy)
        whatif = self.findtvratio(guesscopy, self.alpha)

        self.iterations['jump'][0] = jump[0]
        self.iterations['jump'][1] = whatif

        if self.iterations['jump'][1] < self.iterations['guess'][1]:
            self.consistency = 0
            self.iterations['guess'][0] = copy.copy(self.iterations['jump'][0])
            self.iterations['guess'][1] = self.iterations['jump'][1]
        else:
            self.consistency += 1

        i += 1
        return i

    def checkstatus(self, jump):
        if len(jump) == 1:
            return 'empty'
        elif len(jump) == len(self.vertexset):
            return 'full'
        else:
            return 'filled'

    def randomjump(self, status, jump):
        move = {'full': [self.swapnode, self.removenode], 'empty': [self.addnode, self.changenode],
                'filled':[self.swapnode, self.addnode, self.removenode, self.changenode]}

        result = random.choice(move[status])(jump)

        return result

    def swapnode(self, jump):
            x = random.choice(range(len(jump)))
            y = random.choice(range(len(jump)))

            if x != y:
                temp = jump[x]
                jump[x] = jump[y]
                jump[y] = temp

            else:
                self.swapnode(jump)

            return [jump, 'swap', (x, y)]

    def addnode(self, jump):
            x = random.choice(range(len(jump)))
            node = random.choice(list(set(self.vertexset) - set(jump)))
            jump.insert(x, node)

            return [jump, 'add', x]

    def removenode(self, jump):
            x = random.choice(range(len(jump)))
            del jump[x]

            return [jump, 'remove', x]

    def changenode(self, jump):
            x = random.choice(range(len(jump)))
            node = random.choice(list(set(self.vertexset) - set(jump)))
            jump[x] = node

            return [jump, 'change', x]

    def findtvratio(self, path, alpha):
        o = self.origin
        d = self.destination

        T = 0
        v = len(path)

        T += self.tapbuffer(o, path[0])

        for i in range(len(path) - 1):
            T += self.tapbuffer(path[i], path[i+1])

        T += self.tapbuffer(path[len(path) - 1], d)

        objective = alpha*T + (1-alpha)*T/v

        return objective

    def tapbuffer(self, source, target):
        edge = (source, target)
        if edge in self.buffer.keys():
            return self.buffer[edge]
        else:
            value = nx.shortest_path_length(self.subnetwork.graph, source = source, target = target, weight = 'w')
            self.buffer[edge] = value
            return value

    def determine_optimal_path(self):
        path = [self.origin] + self.optimalpath + [self.destination]
        optimalpath = nx.subgraph(self.network.graph, path).copy()

        erredges = []

        for edge in optimalpath.edges:
            erredges.append(edge)

        optimalpath.remove_edges_from(erredges)

        edges = []

        for i in range(len(path)-1):
            shortestpath = nx.shortest_path(self.subnetwork.graph, source = path[i], target = path[i + 1], weight = 'w')
            for j in range(len(shortestpath)-1):
                edges.append((shortestpath[j], shortestpath[j+1]))

        optimalpath.add_edges_from(edges)

        self.graph = optimalpath

    def determine_simplified_optimal_path(self):
        path = [self.origin] + self.optimalpath + [self.destination]
        optimalpath = nx.subgraph(self.network.graph, path).copy()

        erredges = []

        for edge in optimalpath.edges:
            erredges.append(edge)

        optimalpath.remove_edges_from(erredges)

        edges = []

        for i in range(len(path)-1):
            edges.append((path[i], path[i+1]))

        optimalpath.add_edges_from(edges)

        self.graph = optimalpath

    def determine_choice_set(self):
        choiceset = nx.Graph()

        from_origin = []
        to_destination = []

        for i in range(len(self.optimalpath)):
            O_element = nx.shortest_path(self.subnetwork.graph, source = self.origin, target = self.optimalpath[i], weight = 'w')
            D_element = nx.shortest_path(self.subnetwork.graph, source = self.optimalpath[i], target = self.destination, weight = 'w')
            from_origin.append(O_element)
            to_destination.append(D_element)

        for node in range(len(self.optimalpath)):
            path_graph_from_o = nx.subgraph(self.network.graph, from_origin[node]).copy()
            path_graph_to_d = nx.subgraph(self.network.graph, to_destination[node]).copy()
            choiceset = nx.compose_all([path_graph_from_o, path_graph_to_d, choiceset])

        self.leaf = choiceset

    def count_hierarchies(self):
        frequencies = {'Motorway': 0, 'Trunk': 0, 'Primary': 0, 'Secondary': 0, 'Tertiary': 0, 'Residential': 0,
                     'Service': 0}

        for edge in self.graph.edges:
            h = self.network.graph.edges[edge]['h']
            frequencies[h] += 1

        return frequencies

    def draw_optimal_nodes(self, figname):
        graph = nx.subgraph(self.network.graph, self.optimalpath)
        plt.figure(figname, figsize=(12, 12))
        nx.draw_networkx_nodes(graph, self.network.pos, **self.nodeoptions)

    def draw_optimal_path(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw(self.graph, self.network.pos, **self.pathoptions)

    def draw_leaf(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw(self.leaf, self.network.pos, **self.leafoptions)

    def draw_frequencies(self, figname):
        graph = nx.subgraph(self.network.graph, self.frequencies.keys()).copy()

        for node in graph.nodes:
            graph.add_node(node, freq = self.frequencies[node])

        node_labels = nx.get_node_attributes(graph, 'freq')

        plt.figure(figname, figsize=(12, 12))
        nx.draw_networkx_nodes(graph, self.network.pos, **self.nodeoptions)
        nx.draw_networkx_labels(graph, self.network.pos, node_labels)







