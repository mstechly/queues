from __future__ import division  # Simplify division

from simLibrary import Sim

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="A simulation of a queue.")
    parser.add_argument('-T', action="store", dest="T", type=float, help='The overall simulation time', default=100)
    parser.add_argument('-l', action="store", dest="lambd", type=float, help='Lambda', default=4)
    parser.add_argument('-n', action="store", dest="numberOfCustomers", type=int, help='Number of customers', default=10)
    parser.add_argument('-v', action="store", dest="verbose", type=int, help='Verbose', default=0)
    parser.add_argument('-s', action="store", dest="cockroachSimulation", type=int, help='Is it run for the cockroach simulation.', default=0)

    inputs = parser.parse_args()
    T = inputs.T
    l = inputs.lambd
    v = inputs.verbose
    n = inputs.numberOfCustomers
    s = inputs.cockroachSimulation

    if s==0:
        q = Sim(T, l, n, v, s)
        q.run()

    if s==1:
        for i in range(5):
            q = Sim(T, l, n, v, s)
            oneSim=q.run()
            print oneSim