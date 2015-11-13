from __future__ import division  # Simplify division

from simLibrary import Sim

numbersOfIterationsForOneCockroach = 100
timeOfSimulationForOneCockroach = 200


def assessOneCockroach(sequenceMatrix):
    cockroachFit = 0
    for i in range(numbersOfIterationsForOneCockroach):
        q = Sim(timeOfSimulationForOneCockroach, 0, 1, sequenceMatrix)
        simResult=q.run()
        cockroachFit += simResult

    return cockroachFit/numbersOfIterationsForOneCockroach

def initializeCSO():
    a=1

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="A simulation of a queue.")
    parser.add_argument('-T', action="store", dest="T", type=float, help='The overall simulation time', default=100)
    parser.add_argument('-v', action="store", dest="verbose", type=int, help='Verbose', default=0)
    parser.add_argument('-s', action="store", dest="cockroachSimulation", type=int, help='Is it a simulation for the cockroaches.', default=0)
    parser.add_argument('-p', action="store", dest="permutation", type=list, help='Permutation of Cockroaches', default=[0])

    inputs = parser.parse_args()
    T = inputs.T
    v = inputs.verbose
    s = inputs.cockroachSimulation
    p = inputs.permutation

    if s==0:
        q = Sim(T, v, s, p)
        q.run()

    if s==1:
        testSequence1 = [0,10,1,11,2,12,3,13,4,14,5,15,6,16,7,17,8,18,9,19]
        print assessOneCockroach(testSequence1)
        print assessOneCockroach(range(10))

