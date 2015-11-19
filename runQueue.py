from __future__ import division  # Simplify division
from simLibrary import Sim
import csv
import random
from CockroachLibrary import getPermutation
from CockroachLibrary import numberOfSwaps

numbersOfSimulationsForOneCockroach = 400

class Cockroach():

    def __init__(self, fileID, size):
        self.size = size
        self.fileID = fileID
        self.visual = int(size*0.6)
        self.value=-1
        self.sequence = random.sample(range(self.size),self.size)


    def actualizeCockroach(self):
        cockroachFit = 0
        for i in range(numbersOfSimulationsForOneCockroach):
            q = Sim(self.fileID,0, 0, 1, self.sequence)
            simResult=q.run()
            cockroachFit += simResult
            # print cockroachFit / (i+1)

        self.value = cockroachFit/numbersOfSimulationsForOneCockroach
        return self.value

    def setSequence(self, givenSequence):
        self.sequence = givenSequence

    def calculateDistance(self, secondCockroach):
        sequence1 = self.sequence
        sequence2 = secondCockroach.sequence
        perm = getPermutation(sequence1, sequence2)
        return numberOfSwaps(perm)

    def checkIfSee(self, secondCockroach):
        distance = self.calculateDistance(secondCockroach)
        if distance<= self.visual:
            return True
        else:
            return False

    def moveToward(self, secondCockroach):
        numberOfSteps = 1
        targetSequence = secondCockroach.sequence
        perm = getPermutation(self.sequence, targetSequence)
        for k in range(self.size):
            if self.sequence[k]!=targetSequence[k]:
                elem1 = self.sequence[k]
                elem2 = targetSequence[k]
                pos = [i for i,j in enumerate(self.sequence) if j==elem2]
                pos = pos[0]
                self.sequence[k] = elem2
                self.sequence[pos] = elem1
            break
        self.actualizeCockroach()


    def printCochroach(self, i):
        print "Cockroach: ", i
        print "sequence", self.sequence
        print "Value:", self.value

def initializeCSO(fileID, numberOfCockroaches, numberOfIterations):
    routesFile=csv.reader(open("routes"+str(fileID)+".csv","r"))
    numberOfCustomers=0

    for row in routesFile:
        numberOfCustomers+=1

    listOfCockroaches = []
    listOfValues = [0]*numberOfCockroaches
    print "Initialization"
    for i in range(numberOfCockroaches):
        newCockroach = Cockroach(fileID, numberOfCustomers)
        newCockroach.actualizeCockroach()
        listOfCockroaches.append(newCockroach)

    for iterationNumber in range(numberOfIterations):
        for i in range(numberOfCockroaches):
            listOfValues[i]=listOfCockroaches[i].value

        bestValue = min(listOfValues)
        bestCockroachIndex = [i for i,j in enumerate(listOfValues) if j==bestValue]
        bestCockroachIndex = bestCockroachIndex[0]
        bestCockroach = listOfCockroaches[bestCockroachIndex]

        print "Optimization start"
        for i in range(numberOfCockroaches):

            localBest = listOfCockroaches[i]
            cockroach1 = listOfCockroaches[i]
            for j in range(numberOfCockroaches):
                cockroach2 = listOfCockroaches[j]
                if i!=j and cockroach1.checkIfSee(cockroach2):
                    if localBest.value>cockroach2.value:
                        localBest = cockroach2

            if localBest!=cockroach1:
                cockroach1.moveToward(localBest)
                if cockroach1.value<localBest.value:
                    localBest = cockroach1
                    for j in range(numberOfCockroaches):
                        cockroach2 = listOfCockroaches[j]
                        if i!=j and cockroach1.checkIfSee(cockroach2):
                            if localBest.value>cockroach2.value:
                                localBest = cockroach2

            if localBest==cockroach1 and cockroach1!=bestCockroach:
                if cockroach1.value<bestCockroach.value:
                    bestCockroach = localBest
                else:
                    cockroach1.moveToward(localBest)

        for i in range(numberOfCockroaches):
            givenCockroach = listOfCockroaches[i]
            if random.random()>0.75:
                randomCockroach = Cockroach(fileID, numberOfCustomers)
                randomCockroach.actualizeCockroach()
                givenCockroach.moveToward(randomCockroach)
            if givenCockroach.value<bestCockroach.value:
                bestCockroach = givenCockroach
            # givenCockroach.printCochroach(i)


        print '-----Iteration no.', iterationNumber, ' ------'
        print "Best Value: ", bestCockroach.value
        bestCockroach.printCochroach(1);


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
        newCockroach1=Cockroach(3,12)
        newCockroach1.setSequence(range(12))
        newCockroach2=Cockroach(3,12)
        newCockroach2.setSequence(range(11,-1,-1))
        print "Worst Cockroach time is:"
        print newCockroach1.actualizeCockroach()
        print "Best Cockroach time is:"
        print newCockroach2.actualizeCockroach()


        initializeCSO(f,50,20)

