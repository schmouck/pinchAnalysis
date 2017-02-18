#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def main():
    l = [[50, 20, 100, 200],
         [50, 25,  45, 120],
         [50, 20, 150,  25],
         [50, 25, 240, 110]]
    write_file('default.tsv', l)
    l = read_file('default.tsv')

    # Adding heat capacity flow rate
    _l = []
    for curr in l:
        curr.append(curr[0]*curr[1])
        _l.append(curr)
    l = _l

    # Splitting units by type
    hot_curr = []
    cold_curr = []
    for curr in l:
        if curr[2] > curr[3]:
            hot_curr.append(curr)
        elif curr[2] < curr[3]:
            cold_curr.append(curr)

    # Breakpoint list
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

    # Corresponding heat capacity list
    hot_hc = [0]*len(hot_bp)
    cold_hc = [0]*len(cold_bp)

    for curr in hot_curr:
        print('This is curr')
        print(curr)
        # Finding temperature interval
        temp_int = abs(curr[2] - curr[3])
        # Finding start and stop index
        start_index = hot_bp.index(min(curr[2:4]))
        stop_index = hot_bp.index(max(curr[2:4]))
        for i in range(start_index, stop_index+1):
            hot_hc[i] += curr[4]/temp_int*(hot_bp[i]-hot_bp[start_index])
        print(hot_hc)
        for j in range(stop_index+1, len(hot_bp)):
            hot_hc[j] += hot_hc[stop_index]
        print(hot_hc)


def read_file(fname):
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
