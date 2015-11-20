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


    def printCochroach(self, i):
        print "Cockroach: ", i
        print "sequence", self.sequence
        print "Fitness:", self.fitness

def runCSO(fileID, numberOfCockroaches, numberOfIterations):
    routesFile=csv.reader(open("routes"+str(fileID)+".csv","r"))
    numberOfCustomers=0

    for row in routesFile:
        numberOfCustomers+=1

    listOfCockroaches = []
    listOfValues = [0]*numberOfCockroaches
    print "Initialization"
    for i in range(numberOfCockroaches):
        newCockroach = Cockroach(fileID, numberOfCustomers)
        newCockroach.calculateFitness()
        listOfCockroaches.append(newCockroach)

    for iterationNumber in range(numberOfIterations):
        for i in range(numberOfCockroaches):
            listOfValues[i]=listOfCockroaches[i].fitness

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
                    if localBest.fitness>cockroach2.fitness:
                        localBest = cockroach2

            if localBest!=cockroach1:
                cockroach1.moveToward(localBest)
                if cockroach1.fitness<localBest.fitness:
                    localBest = cockroach1
                    for j in range(numberOfCockroaches):
                        cockroach2 = listOfCockroaches[j]
                        if i!=j and cockroach1.checkIfSee(cockroach2):
                            if localBest.fitness>cockroach2.fitness:
                                localBest = cockroach2

            if localBest==cockroach1 and cockroach1!=bestCockroach:
                if cockroach1.fitness<bestCockroach.fitness:
                    bestCockroach = localBest
                else:
                    cockroach1.moveToward(localBest)

        for i in range(numberOfCockroaches):
            givenCockroach = listOfCockroaches[i]
            if random.random()>0.75:
                randomCockroach = Cockroach(fileID, numberOfCustomers)
                randomCockroach.calculateFitness()
                givenCockroach.moveToward(randomCockroach)
            if givenCockroach.fitness<bestCockroach.fitness:
                bestCockroach = givenCockroach
            # givenCockroach.printCochroach(i)


        print '-----Iteration no.', iterationNumber, ' ------'
        print "Best Value: ", bestCockroach.fitness
        bestCockroach.printCochroach(1);
