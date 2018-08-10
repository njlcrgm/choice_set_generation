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


def find_inflection(x, y, tolerance):
    m = [float(0) for r in range(len(x))]
    m_forward = [float(0) for s in range(len(x))]
    zeros = []

    for i in range(len(x)):
        if i == 0:
            m[i] = (y[i+1] - y[i])/(x[i+1] - x[i])
        elif i == len(x) - 1:
            m[i] = (y[i] - y[i-1])/(x[i] - x[i-1])
        else:
            m[i] = (y[i + 1] - y[i-1]) / (x[i + 1] - x[i-1])

    for j in range(len(x)):
        splice = m[j:]
        average = sum(splice)/float(len(splice))
        m_forward[j] = average

    for l in range(len(m_forward)):
        if abs(m_forward[l]) < tolerance:
            zeros.append(l)

    if len(zeros) != 0:
        limit = x[min(zeros)]
        return limit

    else:
        new_tolerance = tolerance + 0.1
        find_inflection(x, y, new_tolerance)


def save_image(folder, filename):
    if not os.path.exists(folder):
        os.mkdir(folder)

    plt.savefig(folder + '/' + filename + '.png')








