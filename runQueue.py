from __future__ import division  # Simplify division
from simLibrary import Sim
import csv
import random

numbersOfIterationsForOneCockroach = 100
timeOfSimulationForOneCockroach = 200

class Cockroach():

    def __init__(self, size):
        self.size = size
        singleRow = [0]*self.size
        self.matrix = [singleRow]*self.size
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j]=random.random()
        self.value=-1
        self.sequence = range(self.size)

    def assessOneCockroach(self):
        self.value = 0
        self.sequence = self.getSequence()
        for i in range(numbersOfIterationsForOneCockroach):
            q = Sim(timeOfSimulationForOneCockroach, 0, 1, self.sequence)
            simResult=q.run()
            self.value += simResult

        return cockroachFit/numbersOfIterationsForOneCockroach

    def getSequence(self):
        sequence = []
        singleRow = [0]*self.size
        matrixCopy = [singleRow]*self.size
        for i in range(self.size):
            for j in range(self.size):
                matrixCopy[i][j]=self.matrix[i][j]

        for row in matrixCopy:
            m=max(row)
            maxPos=[i for i,j in enumerate(row) if j==m]
            maxPos=maxPos[0]
            sequence.append(maxPos)
            for i in range(self.size):
                matrixCopy[i][maxPos]=0
        return sequence

def initializeCSO(numberOfCockroaches, numberOfIterations):
    routesFile=csv.reader(open("routes.csv","r"))
    numberOfCustomers=0

    for row in routesFile:
        numberOfCustomers+=1
    print "customers:", numberOfCustomers

    listOfCockroaches=[]
    for i in range(numberOfCustomers):
        listOfCockroaches.append(Cockroach())


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
    # initializeCSO(1,2)

    if s==0:
        q = Sim(T, v, s, p)
        q.run()

    if s==1:
        testSequence1 = [0,10,1,11,2,12,3,13,4,14,5,15,6,16,7,17,8,18,9,19]
        print assessOneCockroach(testSequence1)
        print assessOneCockroach(range(10))

