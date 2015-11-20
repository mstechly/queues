from __future__ import division  # Simplify division
from simLibrary import Sim
import csv
import random

from CockroachLibrary import Cockroach
from CockroachLibrary import runCSO

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="A simulation of a queue.")
    parser.add_argument('-T', action="store", dest="T", type=float, help='The overall simulation time', default=0)
    parser.add_argument('-v', action="store", dest="verbose", type=int, help='Verbose', default=0)
    parser.add_argument('-s', action="store", dest="cockroachSimulation", type=int, help='Is it a simulation for the cockroaches.', default=0)
    parser.add_argument('-p', action="store", dest="permutation", type=list, help='Permutation of Cockroaches', default=[0])
    parser.add_argument('-f', action="store", dest="fileID", type=int, help='File ID', default=1)


    inputs = parser.parse_args()
    T = inputs.T
    v = inputs.verbose
    s = inputs.cockroachSimulation
    p = inputs.permutation
    f = inputs.fileID

    if s==0:
        q = Sim(f, T, v, s, p)
        q.run()

    if s==1:

        runCSO(f,5,5)

