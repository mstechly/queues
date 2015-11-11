from __future__ import division  # Simplify division
from turtle import Turtle, mainloop, setworldcoordinates  # Commands needed from Turtle

import sys
import time
import random
import csv

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

        self.lastQueue =  Queue("OutputQueue",None)
        plik=csv.reader(open("test.csv","r"))

        self.listOfQueues=[]
        self.listOfServers=[]

        for row in plik:
            if row[0]=='Q':
                self.listOfQueues.append(Queue("Q"+row[1],self.getServers(row[3])))
            else:
                self.listOfServers.append(Server("S"+row[1],int(row[2]),self.getQueues(row[3])))

        self.listOfQueues=sorted(self.listOfQueues,key=lambda Queue: Queue.queueID)
        self.listOfServers=sorted(self.listOfServers,key=lambda Server: Server.serverID)

        self.firstQueue = self.listOfQueues[0]
        self.lastID = -1

        route1 = [self.listOfServers[0], self.listOfServers[2]]
        route2 = [self.listOfServers[1], self.listOfServers[2]]

        for i in range(30):
            if i%2==0:
                self.newCustomer(route1)
            else:
                self.newCustomer(route2)


    def getQueues(self,list):
        list2=[]
        list=list.split(';')
        print list
        if list[0]=='-1':
            print("Queue last"+self.lastQueue.queueID)
            return [self.lastQueue]
        else:
            for i in list:
             for queue in self.listOfQueues:
                if queue.queueID=="Q"+i:
                    print("Queue "+queue.queueID)
                    list2.append(queue)
        return list2

    def getServers(self,list):
        list2=[]
        list=list.split(';')
        for i in list:
            for server in self.listOfServers:
                if server.serverID=="S"+i:
                    list2.append(server)
                    print("Server "+server.serverID)
        return list2

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