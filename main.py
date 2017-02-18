#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


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
        curr.append(curr[0]*curr[1])
        _l.append(curr)
    l = _l

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

    # => Plotting
    #plot_curr(hot_hc, hot_bp, cold_hc, cold_bp)

    # => Calculating pinch point
    cold_hc, cold_temp, hot_hc, hot_temp = filling_bp_for_hc(hot_hc, hot_bp, cold_hc, cold_bp)
    pinchdar(cold_hc, cold_temp, hot_hc, hot_temp)

    # => Some graph to verify the outputs
    plot_curr(hot_hc, hot_temp, cold_hc, cold_temp)


def calc_curr(currents, hc, bp):
    for curr in currents:
        # Finding temperature interval
        temp_int = abs(curr[2] - curr[3])
        # Finding start and stop index
        start_index = bp.index(min(curr[2:4]))
        stop_index = bp.index(max(curr[2:4]))
        for i in range(start_index, stop_index + 1):
            hc[i] += curr[4] / temp_int * (bp[i] - bp[start_index])
        for j in range(stop_index + 1, len(bp)):
            hc[j] += hc[stop_index]
    return hc


def min_dist(cold_hc, cold_temp, hot_hc, hot_temp):
    f_hc = clist(cold_hc, hot_hc)

    # Find max shared index
    max_indx_hot = f_hc.index(max(hot_hc))
    max_indx_cold = f_hc.index(max(cold_hc))
    max_indx = min(max_indx_hot, max_indx_cold)

    dist = []
    for i in range(max_indx+1):
        dist.append(hot_temp[i]-cold_temp[i])
        print(dist)


def filling_bp_for_hc(hot_hc, hot_bp, cold_hc, cold_bp):
    f_hc = clist(hot_hc, cold_hc)
    nhot_c = hot_bp[:]
    ncold_c = cold_bp[:]

    # Check number of points not in both currents
    nrej_hot = len(f_hc) - f_hc.index(max(hot_hc))
    nrej_cold = len(f_hc) - f_hc.index(max(cold_hc))

    if nrej_hot == nrej_cold:
        if nrej_hot:
            max_it = f_hc[:-nrej_hot]
        else:
            max_it = f_hc[:]
    else:
        max_it = f_hc[:-abs(nrej_hot-nrej_cold)]

    for hc in max_it:
        if hc not in hot_hc:
            hc_index = list(sorted(set(hot_hc[:] + [hc]))).index(hc)
            c_int = hot_bp[hc_index] - hot_bp[hc_index-1]
            hc_int = hot_hc[hc_index] - hot_hc[hc_index-1]
            nhot_c.append(c_int/hc_int * (hc - hot_hc[hc_index-1]) + hot_bp[hc_index-1])
        if hc not in cold_hc:
            hc_index = list(sorted(set(cold_hc[:] + [hc]))).index(hc)
            c_int = cold_bp[hc_index] - cold_bp[hc_index-1]
            hc_int = cold_hc[hc_index] - cold_hc[hc_index-1]
            ncold_c.append(c_int/hc_int * (hc - cold_hc[hc_index-1]) + cold_bp[hc_index-1])

    if len(ncold_c) > len(nhot_c):
        return f_hc, lsort(ncold_c), f_hc[:-abs(nrej_hot-nrej_cold)], lsort(nhot_c)
    elif len(ncold_c) < len(nhot_c):
        return f_hc[:-abs(nrej_hot-nrej_cold)], lsort(ncold_c), f_hc, lsort(nhot_c)
    else:
        return f_hc, lsort(ncold_c), f_hc, lsort(nhot_c)


def clist(hc1, hc2):
    """ Combines and sort two list """
    return lsort(hc1 + hc2)


def lsort(l):
    """ Returns a sorted version of a list """
    return list(sorted(set(l)))


def pinchdar(cold_hc, cold_temp, hot_hc, hot_temp):
    min_dist(cold_hc, cold_temp, hot_hc, hot_temp)


def plot_curr(x1, y1, x2, y2):
    """ Outputs basic hot/cold current plot """
    plt.plot(x1, y1, 'r')
    plt.plot(x2, y2, 'b')
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
