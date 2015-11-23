from __future__ import division  # Simplify division
from simLibrary import Sim
import csv
import random

numbersOfSimulationsForOneCockroach = 1500

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


        self.fitness = cockroachFit/numbersOfSimulationsForOneCockroach
        return self.fitness

    def setSequence(self, givenSequence):
        self.sequence = givenSequence

    def calculateDistance(self, secondCockroach):
        sequence1 = self.sequence
        sequence2 = secondCockroach.sequence
        perm = getPermutation(sequence1, sequence2)
        return numberOfSwaps(perm)

    def checkIfInVisual(self, secondCockroach):
        distance = self.calculateDistance(secondCockroach)
        if distance<= self.visual:
            return True
        else:
            return False

    def moveToward(self, secondCockroach, numberOfSteps):
        targetSequence = secondCockroach.sequence
        for step in range(numberOfSteps):
            for k in random.sample(range(self.size),self.size):
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

    def __init__(self, fileID, numberOfCockroaches, numberOfIterations, printToFile):
        self.fileID = fileID
        self.numberOfCockroaches = numberOfCockroaches
        self.numberOfIterations = numberOfIterations
        self.numberOfSteps = 2
        self.printToFile = printToFile

        routesFile=csv.reader(open("routes"+str(fileID)+".csv","r"))
        self.numberOfCustomers=0

        for row in routesFile:
            self.numberOfCustomers+=1

        self.listOfCockroaches = []
        self.listOfFitness = [0]*self.numberOfCockroaches
        self.bestCockroach = None

    def initialize(self):
        for i in range(self.numberOfCockroaches):
            newCockroach = Cockroach(self.fileID, self.numberOfCustomers)
            newCockroach.calculateFitness()
            self.listOfCockroaches.append(newCockroach)

        for i in range(self.numberOfCockroaches):
            self.listOfFitness[i]=self.listOfCockroaches[i].fitness

        self.bestValue = min(self.listOfFitness)
        bestCockroachIndex = [j for j,k in enumerate(self.listOfFitness) if k==self.bestValue]
        bestCockroachIndex = bestCockroachIndex[0]
        self.bestCockroach = self.listOfCockroaches[bestCockroachIndex]

    def moveCockroaches(self):
        for i in range(self.numberOfCockroaches):
            localBest = self.listOfCockroaches[i]
            cockroach1 = self.listOfCockroaches[i]
            for j in range(self.numberOfCockroaches):
                cockroach2 = self.listOfCockroaches[j]
                if i!=j and cockroach1.checkIfInVisual(cockroach2):
                    if cockroach2.fitness<localBest.fitness:
                        localBest = cockroach2

            if localBest!=cockroach1:
                cockroach1.moveToward(localBest, self.numberOfSteps)
                self.listOfFitness[i]=cockroach1.fitness
                if cockroach1.fitness<localBest.fitness:
                    localBest = cockroach1
                    for j in range(self.numberOfCockroaches):
                        cockroach2 = self.listOfCockroaches[j]
                        if i!=j and cockroach1.checkIfInVisual(cockroach2):
                            if cockroach2.fitness<localBest.fitness:
                                localBest = cockroach2

            if localBest==cockroach1 and cockroach1!=self.bestCockroach:
                if cockroach1.fitness<self.bestCockroach.fitness:
                    self.bestCockroach = cockroach1
                else:
                    cockroach1.moveToward(localBest, self.numberOfSteps)
                    self.listOfFitness[i]=cockroach1.fitness

    def scatterCockroaches(self):
        for i in range(self.numberOfCockroaches):
            givenCockroach = self.listOfCockroaches[i]
            if random.random()>0.75 and givenCockroach!=self.bestCockroach:
                randomCockroach = Cockroach(self.fileID, self.numberOfCustomers)
                randomCockroach.calculateFitness()
                givenCockroach.moveToward(randomCockroach, 1)
                givenCockroach.calculateFitness()
                self.listOfFitness[i]=givenCockroach.fitness
            if givenCockroach.fitness<self.bestCockroach.fitness:
                self.bestCockroach = givenCockroach

    def printBestCockroach(self):
        self.bestCockroach.printCochroach()

    def runCSO(self):
        resultFile=open('CSO/CSO_'+str(self.fileID)+"_0"+str(self.numberOfCockroaches)+"_"+str(self.numberOfIterations)+'.dat', 'w+')
        self.initialize()
        bestSameCounter = 0
        prevBest = self.bestCockroach.fitness
        lastIteration = 0
        for iterationNumber in range(self.numberOfIterations):
            lastIteration = iterationNumber + 1
            self.moveCockroaches()
            self.scatterCockroaches()
            print "Iteration no. ", iterationNumber
            if self.printToFile:
                for fit in self.listOfFitness:
                    resultFile.write(str(fit)+" ")
                resultFile.write("\n")
            if prevBest==self.bestCockroach.fitness:
                bestSameCounter += 1
            else:
                bestSameCounter = 0
                prevBest=self.bestCockroach.fitness
            if bestSameCounter==5:
                break


        resultFile.close()
        print "Best sequence: ", self.bestCockroach.sequence, "in ", lastIteration, " iterations"
        return self.bestCockroach.sequence
