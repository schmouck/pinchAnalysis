#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import fmin

def main():
    l = [[1, 20, 200, 100],
         [1, 40, 150,  60],
         [1, 80,  80, 120],
         [1, 15,  50, 220]]

    write_file('default.tsv', l)
    l = read_file('default.tsv')

    # => Adding heat capacity flow rate
    _l = []
    for curr in l:
        curr.append(curr[0]*curr[1]*abs(curr[2]-curr[3]))
        _l.append(curr)
    l = _l

    print(l)

    # => Splitting units by type
    hot_curr = []
    cold_curr = []
    for curr in l:
        if curr[2] > curr[3]:
            hot_curr.append(curr)
        elif curr[2] < curr[3]:
            cold_curr.append(curr)

    # => Breakpoint list
    hot_bp = set()
    for curr in hot_curr:
        hot_bp.add(curr[2])
        hot_bp.add(curr[3])
    hot_bp = list(sorted(hot_bp))

    cold_bp = set()
    for curr in cold_curr:
        cold_bp.add(curr[2])
        cold_bp.add(curr[3])
    cold_bp = list(sorted(cold_bp))

    # => Corresponding heat capacity list
    hot_hc = [0]*len(hot_bp)
    cold_hc = [0]*len(cold_bp)

    # => Calculation of heat capacity
    cold_hc = calc_curr(cold_curr, cold_hc, cold_bp)
    hot_hc = calc_curr(hot_curr, hot_hc, hot_bp)

    print(cold_hc)
    print(hot_hc)

    # => Creation of numpy array
    hot_C = np.array([])
    for i in range(len(hot_hc)-1):
        tmp = np.linspace(hot_bp[i], hot_bp[i+1], hot_hc[i+1]-hot_hc[i])
        hot_C = np.concatenate((hot_C, tmp), axis=0)
    hot_hc = np.linspace(0, len(hot_C), len(hot_C)+1)

    cold_C = np.array([])
    for i in range(len(cold_hc) - 1):
        tmp = np.linspace(cold_bp[i], cold_bp[i + 1], cold_hc[i + 1] - cold_hc[i])
        cold_C = np.concatenate((cold_C, tmp), axis=0)
    cold_hc = np.linspace(0, len(cold_C), len(cold_C)+1)

    # => Calculating pinch point
    for jj in range(5, 100):
        objective = jj
        eval = 0
        i = 0
        while eval < objective:
            i += 1
            inter = np.intersect1d(cold_hc[:-1]+(i+1), hot_hc[:-1]).astype(int)[:-1]
            old_eval = eval
            eval = min(hot_C[inter] - cold_C[inter-(i+1)])
            min_index = np.argmin(hot_C[inter] - cold_C[inter-(i+1)])

        # => Plotting
        #plot_curr(hot_hc[:-1], hot_C, cold_hc[:-1]+(i+1), cold_C)

        # => Plotting pinch point
        #plot_curr_pinch(hot_hc[:-1], hot_C, cold_hc[:-1]+(i+1), cold_C, [min_index+i, min_index+i], [hot_C[min_index+i], cold_C[min_index]])

        # => Heating and cooling energy
        h_cooling = i
        h_heating = abs(max(cold_hc+i) - max(hot_hc))

        # => Calculate price
        cost_cooling = 1.3
        cost_heating = 1.5
        cost_installation = 3000000

        total_cost = h_cooling*cost_cooling + h_heating*cost_heating + cost_installation/(jj+150)

        print('delta T : {jj}, h_cool : {h_cool}, h_heat : {h_heat}, total_cost : {total_cost}'.format(jj=jj, h_cool=h_cooling, h_heat=h_heating, total_cost=total_cost))


# => Plotting pinch point
    #plot_curr_pinch(hot_hc[:-1], hot_C, cold_hc[:-1] + (i + 1), cold_C, [min_index + i, min_index + i],
    #            [hot_C[min_index + i], cold_C[min_index]])


def calc_curr(currents, hc, bp):
    for curr in currents:
        n_hc = [0]*len(hc)
        # Finding temperature interval
        temp_int = abs(curr[2] - curr[3])
        # Finding start and stop index
        start_index = bp.index(min(curr[2:4]))
        stop_index = bp.index(max(curr[2:4]))
        for i in range(start_index, stop_index + 1):
            n_hc[i] += curr[4] / temp_int * (bp[i] - bp[start_index])
        for j in range(stop_index + 1, len(bp)):
            n_hc[j] += n_hc[stop_index]
        print('n_hc :', n_hc)
        hc = [x + y for x, y in zip(hc, n_hc)]
    return hc


def plot_curr(x1, y1, x2, y2):
    """ Outputs basic hot/cold current plot """
    plt.plot(x1, y1, 'r')
    plt.plot(x2, y2, 'b')
    plt.show()


def plot_curr_pinch(x1, y1, x2, y2, x_pinch, y_pinch):
    plt.plot(x1, y1, 'r')
    plt.plot(x2, y2, 'b')
    plt.plot(x_pinch, y_pinch, 'k')
    plt.show()


def read_file(fname):
    """ Reads a .tsv file with one unit per line """
    f = open(fname, 'r')
    l = []
    for line in f:
        l.append([int(i) for i in line.split('\t')[:-1]])
    return l


def write_file(fname, file):
    f = open(fname, 'w')
    for l in file:
        for item in l:
            f.write(str(item) + '\t')
        f.write('\n')
    f.close()

main()
