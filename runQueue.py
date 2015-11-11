from __future__ import division  # Simplify division
from turtle import Turtle, mainloop, setworldcoordinates  # Commands needed from Turtle

import sys
import time
import random

from queueLibrary import Customer
from queueLibrary import Queue
from queueLibrary import Server
from queueLibrary import getPoissonProb


class Sim():

    def __init__(self, T, lambd, verbose):
        self.T = T
        self.customers = []
        self.lambd = lambd
        self.verbose = verbose

        OutputQueue = Queue("Q3",None)
        Server3 = Server("S3", 2, [OutputQueue])
        Queue2 = Queue("Q2", [Server3])
        Server2 = Server("S2", 4, [Queue2])
        Server1 = Server ("S1", 5, [Queue2])
        Queue1 = Queue("Q1",[Server1, Server2])

        self.firstQueue = Queue1
        self.lastQueue = OutputQueue
        self.lastID = -1
        self.listOfQueues = [Queue1, Queue2]
        self.listOfServers = [Server1, Server2, Server3]

        route1 = [Server1, Server3]
        route2 = [Server2, Server3]

        for i in range(30):
            if i%2==0:
                self.newCustomer(route1)
            else:
                self.newCustomer(route2)
        # self.newCustomer(route2)

    def newCustomer(self, route):
        self.lastID += 1
        newID = self.lastID
        self.customers.append(Customer(newID, route))

    def printProgressToScreen(self, t):
        sys.stdout.write('\r%.2f%% of simulation completed (t=%s of %s)\n' % (100 * t/self.T, t, self.T))
        sys.stdout.flush()

    def run(self):
        t = 0
        # self.newCustomer()  # Create a new player
        # nextplayer = self.customers[self.lastID]
        # self.firstQueue.addCustomer(nextplayer)

        for customer in self.customers:
            self.firstQueue.addCustomer(customer)

        while t < self.T:
            t += 1
            self.verbose=False
            if self.verbose:
                print "-------------------"

            for queue in self.listOfQueues:
                if self.verbose:
                    queue.printQueueState()
                queue.maintenance(t)
                if self.verbose:
                    queue.printQueueState()

            for server in self.listOfServers:
                if self.verbose:
                    server.printServerState()
                server.maintenance(t)
                if self.verbose:
                    server.printServerState()



            # self.lastQueue.printQueueState()
            # self.printProgressToScreen(t)

            # if random.random()<getPoissonProb(self.lambd):
            #     self.newCustomer()
            #     nextplayer = self.customers[self.lastID]
            #     self.firstQueue.addCustomer(nextplayer)

            # time.sleep(0.01)

        # for customer in self.lastQueue.customers:
        #     customer.printHistory()

        # self.getStatistics()

    def getStatistics(self):
        for queue in self.listOfQueues:
            history = queue.historyCustomerAsKey
            # print history
            averageWaitingTime = sum(history.values())/len(history)
            print "average time in queue ",queue.queueID, " : ", averageWaitingTime

        for server in self.listOfServers:
            history = server.historyCustomerAsKey
            # print history
            averageServiceTime = sum(history.values())/len(history)
            print "average service time for server ",server.serverID, " : ", averageServiceTime

        totalTimeInSystem = 0
        for customer in self.customers:
            totalTimeInSystem += len(customer.historyTAsKey)
        averageTimeInSystem = totalTimeInSystem/len(self.customers)
        print "average time in system: ", averageTimeInSystem




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="A simulation of a queue.")
    parser.add_argument('-T', action="store", dest="T", type=float, help='The overall simulation time', default=100)
    parser.add_argument('-l', action="store", dest="lambd", type=float, help='Lambda', default=2)
    parser.add_argument('-v', action="store", dest="verbose", type=bool, help='Verbose', default=False)


    inputs = parser.parse_args()
    T = inputs.T
    l = inputs.lambd
    v = inputs.verbose

    q = Sim(T, 4, v)
    q.run()