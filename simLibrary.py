from __future__ import division  # Simplify division

import sys
import csv

from queueLibrary import Customer
from queueLibrary import Queue
from queueLibrary import Server
from queueLibrary import getPoissonProb


class Sim():

    def __init__(self, fileID, T, verbose, cockroachSimulation, permutation):
        self.T = T
        self.customers = []
        self.verbose = verbose
        self.cockroachSimulation = cockroachSimulation
        if self.cockroachSimulation==1:
            self.verbose = False
        if len(permutation)>1:
            self.permutation=permutation

        self.lastQueue =  Queue("Out",None)
        networkFile=csv.reader(open("networkStructure"+str(fileID)+".csv","r"))

        self.listOfQueues=[]
        self.listOfServers=[]

        for row in networkFile:
            if row[0]=='Q':
                self.listOfQueues.append(Queue("Q"+row[1],self.getServers(row[3])))
            else:
                self.listOfServers.append(Server("S"+row[1],int(row[2]),self.getQueues(row[3])))

        self.listOfQueues=sorted(self.listOfQueues,key=lambda Queue: Queue.queueID)
        self.listOfServers=sorted(self.listOfServers,key=lambda Server: Server.serverID)

        self.firstQueue = self.listOfQueues[0]
        self.lastID = -1

        self.routes = []
        routesFile=csv.reader(open("routes"+str(fileID)+".csv","r"))

        for row in routesFile:
            self.routes.append(self.getServers(row[0]))

        if len(permutation)>1:
            for i in self.permutation:
                self.newCustomer(self.routes[i])
        else:
            for route in self.routes:
                self.newCustomer(route)



    def getQueues(self,list):
        list2=[]
        list=list.split(';')
        # print list
        if list[0]=='-1':
            # print("Queue last"+self.lastQueue.queueID)
            return [self.lastQueue]
        else:
            for i in list:
             for queue in self.listOfQueues:
                if queue.queueID=="Q"+i:
                    # print("Queue "+queue.queueID)
                    list2.append(queue)
        return list2

    def getServers(self,list):
        list2=[]
        list=list.split(';')
        for i in list:
            for server in self.listOfServers:
                if server.serverID=="S"+i:
                    list2.append(server)
                    # print("Server "+server.serverID)
        return list2

    def newCustomer(self, route):
        self.lastID += 1
        newID = self.lastID
        self.customers.append(Customer(newID, route))

    def printProgressToScreen(self, t):
        sys.stdout.write('\r%.2f%% of simulation completed (t=%s of %s)\n' % (100 * t/self.T, t, self.T))
        sys.stdout.flush()

    def printCustomersForKubis(self):
        for customer in self.customers:
            print "{"+str(customer.customerID)+","+str(customer.currentPlace)+"},",
        print "\n"

    def run(self):
        t = 0

        for customer in self.customers:
            self.firstQueue.addCustomer(customer)
        whileLoopCondition=True
        while whileLoopCondition:
            t += 1
            if self.T!=0:
                whileLoopCondition = t<self.T
            else:
                whileLoopCondition = len(self.lastQueue.customers)!=len(self.routes)

            # self.verbose=False
            if self.verbose:
                print "------ t=",t, "---------"

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


            # if self.cockroachSimulation==0:
                # self.printCustomersForKubis()

        if self.cockroachSimulation==0:
            self.getStatistics()
        else:
            return self.getCockroachOutput()

    def getStatistics(self):
        for queue in self.listOfQueues:
            history = queue.historyCustomerAsKey
            historyT = queue.historyTAsKey
            totalTime = 0
            totalLength = 0
            for key in historyT.keys():
                if historyT[key]!=0:
                    totalTime +=1
                    totalLength+=historyT[key]

            if len(history)>0:
                averageWaitingTime = sum(history.values())/len(history)
                averageLength = totalLength/totalTime
                print "average time in queue ",queue.queueID, " : ", averageWaitingTime
                print "average length of queue ", queue.queueID, " : ", averageLength

        for server in self.listOfServers:
            history = server.historyCustomerAsKey
            if len(history)>0:
                averageServiceTime = sum(history.values())/len(history)
                print "serverID: ", server.serverID, " mu: ", server.mu
                print "average service time for server ",server.serverID, " : ", averageServiceTime

        totalTimeInSystem = 0
        for customer in self.customers:
            totalTimeInSystem += len(customer.historyTAsKey)
        averageTimeInSystem = totalTimeInSystem/len(self.customers)
        print "average time in system: ", averageTimeInSystem

    def getCockroachOutput(self):
        totalTimeInSystem = 0
        for customer in self.customers:
            totalTimeInSystem += len(customer.historyTAsKey)
        averageTimeInSystem = totalTimeInSystem/len(self.customers)
        return averageTimeInSystem
