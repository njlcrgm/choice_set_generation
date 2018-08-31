import math
import copy
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

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


def count_chances(guess_len, remaining):
    if guess_len == 1:
        remove_chances = 0
    else:
        remove_chances = guess_len

    add_chances = (guess_len + 1) * remaining
    change_chances = guess_len * remaining

    fact = math.factorial
    if guess_len != 1:
        swap_chances = fact(guess_len) / fact(guess_len - 2) / fact(2)
    else:
        swap_chances = 0

    total_chances = add_chances + remove_chances + change_chances + swap_chances

    return total_chances

def find_saturation(x, y, tolerance):
    # def func(t, a, b, c, h):
    #     return a*np.exp(-1*b*(t-h)) + c
    #
    # popt, pcov = curve_fit(func, x, y, maxfev=10000)
    #
    # afit, bfit, cfit, hfit = tuple(popt)
    #
    # xvalue = (-1/bfit)*np.log((-1/(afit*bfit))*(-1)*tolerance) + hfit
    #
    # return xvalue

    mean_error = [0 for i in range(len(y)-1)]

    for i in range(len(y)-1):
        error = 0

        for j in range(i+1, len(y)):
            error += y[j] - y[i]

        mean_error[i] = error/(len(y) - (i+1))

    candidates = []

    print mean_error

    for k in range(len(mean_error)):
        if abs(mean_error[k]) < tolerance:
            candidates.append(k)

    saturation_point = int(min(candidates))

    return x[saturation_point]


def save_image(folder, filename):
    if not os.path.exists(folder):
        os.mkdir(folder)

    plt.savefig(folder + '/' + filename + '.png')








