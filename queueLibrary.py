from __future__ import division  # Simplify division
from turtle import Turtle, mainloop, setworldcoordinates  # Commands needed from Turtle
import random
import sys
import copy

def getRandomExpTime(mu):
    result = int(random.expovariate(1/mu))
    if result==0:
        result = 1
    return result

def getPoissonProb(lambd):
    return 1 - 2.7183**(-1/lambd)

def mean(lst):
    if len(lst) > 0:
        return sum(lst) / len(lst)
    return False


class Customer():

    def __init__(self, customerID, route):
        # Turtle.__init__(self)  # Initialise all base Turtle attributes
        self.queue = None
        self.server = None
        self.customerID = customerID
        self.isServed = False
        self.historyTAsKey = {}
        self.historyEventAsKey = {}
        self.route = route
        self.routePosition = 0
        self.currentPlace = "In"

    def updateHistory(self, t, event):
        self.historyTAsKey[t] = event
        self.historyEventAsKey[event] = t

    def printHistory(self):
        print(self.history)


class Queue():
    def __init__(self, queueID, connectedServers):
        self.customers = []
        self.queueID = queueID
        self.connectedServers = connectedServers
        self.historyTAsKey = {}
        self.historyCustomerAsKey = {}

    def addCustomer(self, customer):
        self.customers.append(customer)

    def sendCustomerToServer(self, index, targetServer):
        self.customers[index].isServed=True
        self.customers[index].routePosition +=1
        self.customers[index].currentPlace = targetServer.serverID
        targetServer.startService(self.customers[index])

    def maintenance(self, t):

        for person in self.customers:
            person.updateHistory(t,self.queueID)
            if person.customerID in self.historyCustomerAsKey:
                self.historyCustomerAsKey[person.customerID] += 1
            else:
                self.historyCustomerAsKey[person.customerID] = 1

        self.historyTAsKey[t] = self.customers

        customersToDrop =[]

        for i in range(len(self.customers)):
            currentCustomer = self.customers[i]
            targetServer = currentCustomer.route[currentCustomer.routePosition]
            if targetServer.checkIfFree():
                self.sendCustomerToServer(i, targetServer)
                customersToDrop.append(i)

        for i in range(len(customersToDrop)-1,-1,-1):
            self.customers.pop(customersToDrop[i])


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



    def startService(self,customer):
        self.customers.append(customer)
        self.timeLeft = getRandomExpTime(self.mu)

    def endService(self, index):
        #TODO: procedura losowania kolejki
        targetQueue = self.outgoingQueues[0]
        self.customers[index].currentPlace = targetQueue.queueID

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
            if self.timeLeft!=0:
                self.timeLeft=self.timeLeft-1
            if self.timeLeft<=0:
                self.endService(0)



    def printServerState(self):
        sys.stdout.write('%s: time left in server %s \n' % (self.timeLeft, self.serverID))
