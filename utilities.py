import math
import copy
import os
import matplotlib.pyplot as plt

def detourfunction(dist):
    a = 1.209549
    b = 10896.21
    c = 0.6267842
    return  a + b * math.exp(-1 * c * dist)

def euclideandist(o, d, pos):
    dist = math.sqrt(((pos[o][0] - pos[d][0]) ** 2) + ((pos[o][1] - pos[d][1]) ** 2))
    return dist

def scorescale(node, network, scalelength, lowestscore):
    # A = float(len(network.edges(node)))
    # # A = 4
    # B = 2
    # scorelist = {}
    #
    # for i in range(scalelength):
    #     scorelist[i+1] = float(0)
    #
    # scorelist[1] = float(lowestscore)
    #
    # for i in range(1, scalelength):
    #     scorelist[i+1] += A*scorelist[i]/B
    #     for k in range(i):
    #         scorelist[i+1] += (-1*(A-B)/float(scalelength))*scorelist[k+1]/B

    # maxvalue = max(scorelist.values())
    # for i in range(scalelength):
    #     a = scorelist[i+1]
    #     scorelist[i+1] = 10*a/maxvalue

    ########################################

    scorelist = {}

    for i in range(scalelength):
        scorelist[i+1] = float(0)

    scorelist[1] = float(lowestscore)

    for i in range(1, scalelength):
        scorelist[i+1] += lowestscore
        for k in range(i):
            scorelist[i+1] += scorelist[k+1]/(i)

    # maxvalue = max(scorelist.values())
    # for i in range(scalelength):
    #     a = scorelist[i+1]
    #     scorelist[i+1] = 10*a/maxvalue

    return scorelist

def truncatelist(item, array):
    a = copy.copy(array)
    pivot = array.index(item)
    del a[:pivot]

    return a

def bisect_list(sequence):
    bisection = []
    for i in range(len(sequence)-1):
        midpoint = (sequence[i] + sequence[i+1])/2
        bisection.append(midpoint)

    return bisection

def fractalize(sequence):
    length = len(sequence)
    size_edge = int(2 ** (length - 1))

    corridors = {}
    buffer = []

    corridors[sequence[0]] = [int(0), size_edge]
    buffer += corridors[sequence[0]]

    for i in range(1, length):
        corr = bisect_list(buffer)
        corridors[sequence[i]] = corr
        buffer += corr
        buffer = sorted(buffer)

    return corridors

def save_image(folder, filename):
    if not os.path.exists(folder):
        os.mkdir(folder)

    plt.savefig(folder + '/' + filename + '.png')








