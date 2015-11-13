from __future__ import division  # Simplify division

from simLibrary import Sim

numbersOfIterationsForOneCockroach = 100
timeOfSimulationForOneCockroach = 100


def assessOneCockroach(sequenceMatrix):
    n = len(sequenceMatrix)
    cockroachFit = 0
    for i in range(numbersOfIterationsForOneCockroach):
        q = Sim(timeOfSimulationForOneCockroach, 0, 1)
        simResult=q.run()
        cockroachFit += simResult

    return cockroachFit/numbersOfIterationsForOneCockroach

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="A simulation of a queue.")
    parser.add_argument('-T', action="store", dest="T", type=float, help='The overall simulation time', default=100)
    parser.add_argument('-v', action="store", dest="verbose", type=int, help='Verbose', default=0)
    parser.add_argument('-s', action="store", dest="cockroachSimulation", type=int, help='Is it a simulation for the cockroaches.', default=0)

    inputs = parser.parse_args()
    T = inputs.T
    v = inputs.verbose
    s = inputs.cockroachSimulation

    if s==0:
        q = Sim(T, v, s)
        q.run()

    if s==1:
        print assessOneCockroach(range(10))

