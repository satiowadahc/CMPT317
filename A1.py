# Chad A. Woitas
# #11137533
# NSID: CAW724
# CMPT 317
# Michael Horcsh
# Due Date February 9
# Partner: Brandon Bachynski.

# Plan
# --------------------------------
# startSpace
# All Vehicles start at 0 (Garage)
# Packages are randomly distributed
# Delivery spots are random

# Vehicles and Packages are separate objects from nodes
# Graph traversal will check with objects

# ---------------------------------

import networkx as nx
import random as rng
import matplotlib.pyplot as plt


# PARAMETERS ----------------------------------
trucksNum = 1
packsNum = 1
# gridy = 1
gridx = 10
# PARAMETERS ----------------------------------

class Package:

    def __init__(self, source, destination, pid):
        self.source = source
        self.destination = destination
        self.location = source
        self.id = pid


class Vehicle:
    location = nx.Graph()
    cargo = []
    vid = 0

    def __init__(self, g, vid):
        global location, cargo
        self.location = g
        self.packageLimit = 1
        self.cargo = []
        self.vid = vid

    def pickupPackage(self, package):
        if self.cargo.count() < self.packageLimit:
            self.cargo.append(package)
            package.delete

    def moveVehicle(self, g):
        self.location = g

    def deliverPackage(self, currNode):
        for i in self.cargo:
            if self.cargo[i].destination == currNode:
                self.cargo[i].location = currNode
                self.cargo[i].pop


# TODO: Implement
class Search:
    def search(self):
        return True


# TODO: Implement
class SearchNodes:
    def searchNodes(self):
        return True


# TODO: Implement
class StateQueue:
    def initialize(self):
        return True

    def remove(self):
        return True

    def add(self):
        return True


class ProblemState:
    # Next do this
    vehicles = []
    packages = []

    def __init__(self, newvehicles, newpacks):
        self.vehicles = newvehicles
        self.packages = newpacks

    def displayState(self):
        print("Trucks:")
        print("-------")
        for i in range(len(self.vehicles)):
            current = self.vehicles
            if len(current[i].cargo) > 0:
                print(current[i].location, current[i].cargo)
            else:
                print(current[i].location)
        print()

        print("Packages:")
        print("-------")
        for i in range(len(self.packages)):
            current = self.packages
            print(current[i].location,
                  current[i].source,
                  current[i].destination)


class Problem:
    trucks = []
    packs = []

    def __init__(self):
        global trucks, packs
        trucks = []
        packs = []
        # Graph Creation
        G = nx.grid_graph([gridx])
        for i in range(G.number_of_nodes()):
            G.add_node(i, node=i)

        # Trucks Creation
        for i in range(trucksNum):
            newTruck = Vehicle(G.node[1], i)
            trucks.append(newTruck)

        # Packages Creation
        for i in range(packsNum):
            x = rng.randint(1, G.number_of_nodes()-1)
            y = rng.randint(1, G.number_of_nodes()-1)
            while x == y:
                y = rng.randint(1, G.number_of_nodes())
            newPack = Package(G.node[x], G.node[y], 1)
            packs.append(newPack)

# packages at destination
    def isGoal(self):
        test = 0

        for i in range(len(packs)):
            if packs[i].location == packs[i].destination:
                test += 1

        print("Goal Completion:", test*100/len(packs), "%")

        if test == len(packs):
            return True
        else:
            return False

    def successors(self):
        return True


# Begin Algorithm

problem = Problem()

problemState = ProblemState(trucks, packs)

problemState.displayState()

problem.isGoal()
