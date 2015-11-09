from __future__ import division  # Simplify division
from turtle import Turtle, mainloop, setworldcoordinates  # Commands needed from Turtle
import random
import sys

def getRandomExpTime(mu):
    return int(random.expovariate(1/mu))

def getPoissonProb(lambd):
    return 1 - 2.7183**(-1/lambd)

def mean(lst):
    if len(lst) > 0:
        return sum(lst) / len(lst)
    return False

def movingaverage(lst):
    return [mean(lst[:k]) for k in range(1 , len(lst) + 1)]


class Customer():

    def __init__(self, customerID):
        # Turtle.__init__(self)  # Initialise all base Turtle attributes
        self.queue = None
        self.server = None
        self.customerID = customerID
        self.isServed = False
        self.historyTAsKey = {}
        self.historyEventAsKey = {}

    def updateHistory(self, t, event):
        self.historyTAsKey[t] = event
        self.historyEventAsKey[event] = t

    def printHistory(self):
        print(self.history)


class Queue():
    def __init__(self, queueID, lambd, connectedServers):
        self.customers = []
        self.queueID = queueID
        self.lambd = lambd
        self.connectedServers = connectedServers
        self.historyTAsKey = {}
        self.historyCustomerAsKey = {}

    def __len__(self):
        return len(self.customers)

    def addCustomer(self, customer):
        self.customers.append(customer)

    def sendCustomerToServer(self, index, targetServer):
        self.customers[index].isServed=True

        targetServer.startService(self.customers[index])
        self.customers.pop(index)

    def maintenance(self, t):

        for person in self.customers:
            person.updateHistory(t,self.queueID)
            if person.customerID in self.historyCustomerAsKey:
                self.historyCustomerAsKey[person.customerID] += 1
            else:
                self.historyCustomerAsKey[person.customerID] = 1

        self.historyTAsKey[t] = self.customers

        for server in self.connectedServers:
            if server.checkIfFree() and len(self.customers)!=0:
                self.sendCustomerToServer(-1, server)


    def printQueueState(self):
        sys.stdout.write('%s: number of customers in queue %s \n' % (len(self.customers), self.queueID))


class Server():
    def __init__(self, serverID, mu, outgoingQueues):
        self.customers = []
        self.serverID = serverID
        self.mu = mu
        self.outgoingQueues = outgoingQueues
        self.timeLeft = 0
        self.historyTAsKey = {}
        self.historyCustomerAsKey = {}


    def __iter__(self):
        return iter(self.customers)

    def __len__(self):
        return len(self.customers)

    def startService(self,customer):
        self.customers.append(customer)
        self.timeLeft = getRandomExpTime(self.mu)


    def endService(self, index):
        #TODO: procedura losowania kolejki
        targetQueue = self.outgoingQueues[0]

        targetQueue.addCustomer(self.customers[index])
        self.customers.pop(index)

    def checkIfFree(self):
        return len(self.customers) == 0

    def maintenance(self, t):

        for person in self.customers:
            person.updateHistory(t,self.serverID)
            if person.customerID in self.historyCustomerAsKey:
                self.historyCustomerAsKey[person.customerID] += 1
            else:
                self.historyCustomerAsKey[person.customerID] = 1

        self.historyTAsKey[t] = self.customers


        if len(self.customers)!=0:
            self.timeLeft=self.timeLeft-1
            if self.timeLeft<=0:
                self.endService(0)



    def printServerState(self):
        sys.stdout.write('%s: time left in server %s \n' % (self.timeLeft, self.serverID))
