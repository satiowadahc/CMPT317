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

# city = nx.grid_graph(dim=[10, 10])

# plt.subplot()
# nx.draw(city, font_size=1)

# plt.show()


class Package:

    def __init__(self, source, destination, pid):
        self.source = source
        self.destination = destination
        self.location = source
        self.id = pid


class Vehicle:

    def __init__(self, g):
        self.location = g
        self.packageLimit = 1
        self.cargo = []

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


# TODO: Implement
class ProblemState:
    # Next do this

    def __init__(self, vehicles, packages):
        self.vehicles = vehicles
        self.packages = packages

    def displayState(self):
        print("Trucks:")
        print("-------")
        print(self.vehicles.location, self.vehicles.cargo)
        print("Packages:")
        print("-------")
        print(self.packages.location, self.packages.source, self.packages.destination)


class Problem:

    def __init__(self):
        global truck, p1
        G = nx.grid_graph([10])

        for i in range(G.number_of_nodes()):
            G.add_node(i, node=i)

        truck = Vehicle(G.node[0])
        p1 = Package(G.node[rng.randint(1, 9)], G.node[rng.randint(1, 9)], 1)
        print("Truck Starting at", truck.location)
        print("Package 1 Starting", p1.source, "Destination", p1.destination, "Current Location", p1.location)


# packages at destination
    def isGoal(self):
        return True

    def successors(self):
        return True


# Begin Algorithm

problem = Problem()

problemState = ProblemState(truck, p1)

problemState.displayState()
