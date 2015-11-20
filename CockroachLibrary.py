from __future__ import division  # Simplify division
from simLibrary import Sim
import csv
import random

numbersOfSimulationsForOneCockroach = 2000

def getPermutation(L1, L2):

    if sorted(L1) != sorted(L2):
        raise ValueError("L2 must be permutation of L1 (%s, %s)" % (L1,L2))

    permutation = map(dict((v, i) for i, v in enumerate(L1)).get, L2)
    assert [L1[p] for p in permutation] == L2
    return permutation

def numberOfSwaps(permutation):
    # decompose the permutation into disjoint cycles
    nswaps = 0
    seen = set()
    for i in xrange(len(permutation)):
        if i not in seen:
           j = i # begin new cycle that starts with `i`
           while permutation[j] != i:
               j = permutation[j]
               seen.add(j)
               nswaps += 1

    return nswaps

class Cockroach():

    def __init__(self, fileID, size):
        self.size = size
        self.fileID = fileID
        self.sequence = random.sample(range(self.size),self.size)
        self.fitness=-1
        self.visual = int(size*0.6)


    def calculateFitness(self):
        cockroachFit = 0
        for i in range(numbersOfSimulationsForOneCockroach):
            q = Sim(self.fileID,0, 0, 1, self.sequence)
            simResult=q.run()
            cockroachFit += simResult
            # print cockroachFit / (i+1)

        self.fitness = cockroachFit/numbersOfSimulationsForOneCockroach
        return self.fitness

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
        self.calculateFitness()


    def printCochroach(self):
        print "sequence", self.sequence
        print "Fitness:", self.fitness

class CSO():

    def __init__(self, fileID, numberOfCockroaches, numberOfIterations):
        self.fileID = fileID
        self.numberOfCockroaches = numberOfCockroaches
        self.numberOfIterations = numberOfIterations

        routesFile=csv.reader(open("routes"+str(fileID)+".csv","r"))
        self.numberOfCustomers=0

        for row in routesFile:
            self.numberOfCustomers+=1

        self.listOfCockroaches = []
        self.listOfFitness = [0]*self.numberOfCockroaches
        self.bestCockroach = None
        # self.bestCockroach = new Cockroach(self.fileID, self.numberOfCustomers)

    def initialize(self):
        for i in range(self.numberOfCockroaches):
            newCockroach = Cockroach(self.fileID, self.numberOfCustomers)
            newCockroach.calculateFitness()
            self.listOfCockroaches.append(newCockroach)

        for i in range(self.numberOfCockroaches):
            self.listOfFitness[i]=self.listOfCockroaches[i].fitness

        self.bestValue = min(self.listOfFitness)
        self.bestCockroachIndex = [j for j,k in enumerate(self.listOfFitness) if k==self.bestValue]
        self.bestCockroachIndex = self.bestCockroachIndex[0]
        self.bestCockroach = self.listOfCockroaches[self.bestCockroachIndex]

    def moveCockroaches(self):
        for i in range(self.numberOfCockroaches):
            localBest = self.listOfCockroaches[i]
            cockroach1 = self.listOfCockroaches[i]
            for j in range(self.numberOfCockroaches):
                cockroach2 = self.listOfCockroaches[j]
                if i!=j and cockroach1.checkIfSee(cockroach2):
                    if localBest.fitness>cockroach2.fitness:
                        localBest = cockroach2

            if localBest!=cockroach1:
                cockroach1.moveToward(localBest)
                if cockroach1.fitness<localBest.fitness:
                    localBest = cockroach1
                    for j in range(self.numberOfCockroaches):
                        cockroach2 = self.listOfCockroaches[j]
                        if i!=j and cockroach1.checkIfSee(cockroach2):
                            if localBest.fitness>cockroach2.fitness:
                                localBest = cockroach2

            if localBest==cockroach1 and cockroach1!=self.bestCockroach:
                if cockroach1.fitness<self.bestCockroach.fitness:
                    self.bestCockroach = localBest
                else:
                    cockroach1.moveToward(localBest)

    def scatterCockroaches(self):
        for i in range(self.numberOfCockroaches):
            givenCockroach = self.listOfCockroaches[i]
            if random.random()>0.75:
                randomCockroach = Cockroach(self.fileID, self.numberOfCustomers)
                randomCockroach.calculateFitness()
                givenCockroach.moveToward(randomCockroach)
            if givenCockroach.fitness<self.bestCockroach.fitness:
                self.bestCockroach = givenCockroach

    def printBestCockroach(self):
        self.bestCockroach.printCochroach()

    def runCSO(self):
        self.initialize()
        for iterationNumber in range(self.numberOfIterations):
            self.moveCockroaches()
            self.scatterCockroaches()
            print "Iteration no. ", iterationNumber
            self.printBestCockroach()

