#!/usr/bin/python

from random import random
import sys

def genrand(p, start):
    if p < 0.0 or p > 1.0:
        raise RuntimeError('p should be in [0,1]')
    k = start
    while True:
        if random() <= p: yield(k)
        k = k + 1

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: genrand <n> <probability> <start_number>'
        sys.exit(-1)
    n, p, start_number = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
    gen = genrand(p, start_number)
    for k in range(n):
        print '%06d' % gen.next()

