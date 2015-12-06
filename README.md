# Introduction

This project is a simulation of queue network written in python 2.7. It is loosely based on [the code from dr Vince Knight] (https://github.com/drvinceknight/Simulating_Queues). 
It was written as a project for classes on queues networks at AGH University of Science and Technology, Cracow. The topic of the project was "Optimization of customers scheduling in queue network using cockroach swarm algorithm", so besides the queues we implemented also the cockroach swarm optimization algorithm (CSO)

# Structure:
Core consist of four parts:
* queueLibrary.py, containing definitions of servers, queues and customers.
* simLibrary.py - loads necessary files and creates a single simulation
* cockroachLibrary.py - implements CSO
* runQueue.py - main - runs single simulation or CSO

Besides that there are:
* config files (networkStructure.csv and routes.csv)
* GUI - written in .Net .
* documentation - in the form of a report. It also includes some tests of the CSO.

# Running simulation

To run the simulation you have to run script runQueue.py .
It can be used with following flags:

* -T: time of simulation. If 0, simulation runs as long as necessary to serve all the customers. 0 is default.

* -v: verbose. 0 or 1, 0 is default

* -s: cockroach simulation. 0 - normal simulation, without CSO. 1 - simulation using CSO.

* -p: permutation of customers. If [0], customers are sorted (default). It is used by the CSO.

* -f: file ID, default 1. It concerns routes.csv and networkStructure.csv

# Important notes:

- this version doesn't implement the simplest behaviour of randomly generated customers. It takes as the input the predefined list of the customers. However it shouldn't be hard to add.

- there is no instruction for running gui and I have no idea how to run it (my friend wrote this part). I hope it is straightforward for anyone with .Net experience. 

- I have no intention of developing this code further. Feel free to use, modify or clean it. If any of that happens, I would be happy to know about it.

- theoretical part of the documentation is generally copied from articles in the references.

- sorry for the mess in commits and the fact, that most of them are in polish. But I really think noone will ever need that.

- for any further information read the documentation or contact me: michal.stechly@gmail.com

# License

As I mentioned, the code is loosely based on the work of dr Vince Knight, so it inherits its license:

## License Information
This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/us/) license.  You are free to:

* Share: copy, distribute, and transmit the work,
* Remix: adapt the work

Under the following conditions:

* Attribution: You must attribute the work in the manner specified by the author or licensor (but not in any way that suggests that they endorse you or your use of the work).
* Share Alike: If you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.
