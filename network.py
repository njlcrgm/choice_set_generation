from utilities import euclideandist, truncatelist

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import copy
import math
import random

class Network():
    def __init__(self, size, scale):
        # Graph
        self.experimentalnodes = []
        self.graph = nx.Graph()
        self.size = size
        self.scale = scale
        self.pos = {}

        # Tables of Hierarchy, Signalization and PT
        self.Hlist = ['Motorway', 'Trunk', 'Primary', 'Secondary', 'Tertiary', 'Residential', 'Service']
        self.Plist = ['Bus-UV', 'Jeep', 'None']
        self.Hspeedlimit = {'Motorway': 100, 'Trunk': 90, 'Primary': 80, 'Secondary': 70, 'Tertiary': 60,
                            'Residential': 50,
                            'Service': 40}
        self.phases = [2, 3, 4, 5, 6]

        # Drawing Settings
        self.options = {'node_color': 'blue', 'edge_color': 'blue', 'node_size': 20, 'width': 0.5}
        self.expoptions = {'node_color': 'blue', 'edge_color': 'black', 'node_size': 20, 'width': 2}

    def creategrid(self):
        G = self.graph
        n = self.size

        for i in range(n ** 2):
            G.add_node(i)

        for i in range(n ** 2):
            self.pos[i] = (self.scale*(i % n), self.scale*(math.floor(i / n)))

        for i in range(n ** 2):
            if (i in G.nodes) and (i + 1 in G.nodes) and (i % n != n - 1):
                G.add_edge(i, i + 1)
            if (i in G.nodes) and (i + n in G.nodes):
                G.add_edge(i, i + n)
            if (i in G.nodes) and (i - n in G.nodes):
                G.add_edge(i - n, i)
            if (i in G.nodes) and (i - 1 in G.nodes) and (i % n != 0):
                G.add_edge(i - 1, i)

        self.graph = G

        # print "\n\tGrid created with size " + str(self.size) + " and scale " + str(self.scale) + "."

    def randomize_atts(self, attribute, limit):
        if attribute == 'h':
            h_set = truncatelist(limit, self.Hlist)
            for edge in self.graph.edges:
                self.graph.add_edge(*edge, h=random.choice(h_set))

            # print "\tHierarchy attributes randomly assigned to links in the grid w/", limit, "being the highest."

        if attribute == 'p':
            p_set = truncatelist(limit, self.Plist)
            for edge in self.graph.edges:
                self.graph.add_edge(*edge, p=random.choice(p_set))

            # print "\tPT attributes randomly assigned to links in the grid w/", limit, "being the highest."

        if attribute == 's':
            for node in self.graph.nodes:
                cycletime = round(random.uniform(limit[0], limit[1]), 0)
                phasesnumber = float(random.choice(self.phases))
                c_p = random.choice([float(0), cycletime / phasesnumber])
                self.graph.add_node(node, c=cycletime)
                self.graph.add_node(node, ph=phasesnumber)
                self.graph.add_node(node, s=c_p)

            # print "\tSignalization attributes randomly assigned to nodes in the grid w/ c in " + str(limit) + "."

    def randomize_atts_corridors(self, attribute, limit):
        if attribute == 'h':
            h_set = truncatelist(limit, self.Hlist)
            self.create_corridor(attribute, h_set, 'column', [i for i in range(self.size)])
            self.create_corridor(attribute, h_set, 'row', [i for i in range(self.size)])

            # print "\tHierarchy attributes randomly assigned to corridors in the grid with", limit, "being the highest."

        if attribute == 'p':
            p_set = truncatelist(limit, self.Plist)
            self.create_corridor(attribute, p_set, 'column', [i for i in range(self.size)])
            self.create_corridor(attribute, p_set, 'row', [i for i in range(self.size)])

            # print "\tPT attributes randomly assigned to links and nodes in the grid with", limit, "being the highest."

    def same_atts(self, attribute, value):
        if attribute == 'h':
            for edge in self.graph.edges:
                self.graph.add_edge(*edge, h=value)

            # print "\tAll hierarchy attributes set to", value, "."

        if attribute == 'p':
            for edge in self.graph.edges:
                self.graph.add_edge(*edge, p=value)

            # print "\tAll PT attributes set to " + str(value) + "."

        if attribute == 's':
            for node in self.graph.nodes:
                c_p = float(value[0]) / float(value[1])
                self.graph.add_node(node, c = value[0])
                self.graph.add_node(node, p = value[1])
                self.graph.add_node(node, s = c_p)

            # print "\tAll signalization attributes set to " + str(round(c_p, 2)) + "."

    def fractal_atts(self, attribute, corridors):
        for key in corridors:
            self.create_corridor(attribute, [key], 'column', corridors[key])
            self.create_corridor(attribute, [key], 'row', corridors[key])

        # print "\tExperimental fractal grid created.\n"

    def create_corridor(self, attribute, value_list, orientation, positions):
        orientation_keys = {'column': 0, 'row': 1}
        key = orientation_keys[orientation]
        corr_values = {}
        for item in positions:
            corr_values[item] = random.choice(value_list)

        if attribute == 'h':
            for edge in self.graph.edges:
                if self.pos[edge[0]][key] == self.pos[edge[1]][key] and int(self.pos[edge[1]][key]/self.scale) in positions:
                    value = corr_values[int(self.pos[edge[1]][key]/self.scale)]
                    self.graph.add_edge(*edge, h=value)

        if attribute == 'p':
            for edge in self.graph.edges:
                if self.pos[edge[0]][key] == self.pos[edge[1]][key] and int(self.pos[edge[1]][key]/self.scale) in positions:
                    value = corr_values[int(self.pos[edge[1]][key] / self.scale)]
                    self.graph.add_edge(*edge, p=value)

        if attribute == 's':
            for node in self.graph.nodes:
                if int(self.pos[node][key]/self.scale) in positions:
                    c = float(corr_values[int(self.pos[node][key]/self.scale)][0])
                    p = float(corr_values[int(self.pos[node][key]/self.scale)][1])
                    value = c/p
                    self.graph.nodes[node]['s'] = value

    def assign_edge_weights(self):
        for edge in self.graph.edges:
                length = euclideandist(edge[0], edge[1], self.pos)
                speed = float(self.Hspeedlimit[self.graph.edges[edge]['h']])
                self.graph.add_edge(*edge, w = length/speed)

    def realize_network(self, origin, destination):
        dummy_graph = self.graph.copy()
        elim = 0

        while nx.has_path(dummy_graph, origin, destination) and (float(len(dummy_graph.nodes))/float(self.size**2) > 0.5):
            elim = random.choice(list(dummy_graph.nodes))
            if elim not in [origin, destination]:
                dummy_graph.remove_node(elim)

        include_nodes = list(dummy_graph.nodes) + [elim]
        new_graph = nx.subgraph(self.graph, include_nodes).copy()

        self.graph = new_graph

        # opts = [True, False]
        # include_nodes = [origin]
        # current = origin
        #
        # while destination not in include_nodes:
        #     neigh = [n for n in self.graph.neighbors(current)]
        #     for node in neigh:
        #         stay = np.random.choice(opts, p=[0.5, 0.5])
        #         if (stay or (node in [origin, destination])) and (node not in include_nodes):
        #             include_nodes.append(node)
        #
        #     current = random.choice(neigh)
        #
        # new_graph = nx.subgraph(self.graph, include_nodes).copy()
        #
        # for snodes in new_graph.nodes:
        #     if new_graph.edges(snodes) == 0:
        #         new_graph.remove_node(snodes)
        #
        # self.graph = new_graph

        # dummy_graph = self.graph.copy()
        # include_nodes = [origin, destination]
        #
        # while nx.has_path(dummy_graph, origin, destination):
        #     path = nx.shortest_path(dummy_graph, origin, destination)
        #     for i in path:
        #         if i not in include_nodes:
        #             include_nodes.append(i)
        #             dummy_graph.remove_node(i)
        #
        # new_graph = nx.subgraph(self.graph, include_nodes).copy()
        # self.graph = new_graph

    def drawnetwork(self, figname):
        plt.figure(figname, figsize=(12, 12))
        nx.draw(self.graph, self.pos, **self.options)

    def drawwith(self, figname, attribute):
        if attribute not in ['s', 'c', 'ph']:
            edge_labels = nx.get_edge_attributes(self.graph, attribute)
            plt.figure(figname, figsize=(12, 12))
            nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels)

        else:
            node_labels = nx.get_node_attributes(self.graph, attribute)
            plt.figure(figname, figsize=(12, 12))
            nx.draw_networkx_labels(self.graph, self.pos, node_labels)

    def draw_corridor(self, figname, orientation, position):
        orientation_keys = {'column': 0, 'row': 1}
        key = orientation_keys[orientation]
        nodeset = set()

        for edge in self.graph.edges:
            if self.pos[edge[0]][key] == self.pos[edge[1]][key] and int(self.pos[edge[1]][key] / self.scale) == position:
                nodeset.add(edge[0])
                nodeset.add(edge[1])

        nodelist = list(nodeset)

        graph = nx.subgraph(self.graph, nodelist).copy()
        plt.figure(figname, figsize=(12, 12))
        nx.draw(graph, self.pos, **self.expoptions)

