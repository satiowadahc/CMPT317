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

    def movePackage(self,g):
        self.location = g


class Vehicle:
    location = nx.Graph()
    adjacent = nx.Graph()
    cargo = []
    vid = 0

    def __init__(self, g, adj, vid):
        self.location = g
        self.adjacent = adj
        self.packageLimit = 1
        self.cargo = []
        self.vid = vid

    def pickupPackage(self, package):
        if len(self.cargo) < self.packageLimit:
            self.cargo.append(package)

    def moveVehicle(self, g):
        current = False
        for i in self.adjacent:
            if G.node[i] == g:
                self.location = g
                self.adjacent = G[i]
                for j in self.cargo:
                    j.movePackage(g)
                current = True
        if not current:
            print("Cant Move There")

    def deliverPackage(self, currNode):
        for i in self.cargo:
            if self.cargo[i].destination == currNode:
                self.cargo[i].location = currNode
                self.cargo[i].pop


# TODO: Implement
class Search:
    node = nx.Graph()
    # 1 for forward
    # -1 for backward
    travelDirection = 1

    def __init__(self, ps):

        if(ps.packageEvaluate() == 100.0) and (ps.truckEvaluate() == 100.0):
            print("Complete")
        else:
            print("Packages Left", 100.0-ps.packageEvaluate(),
                  "Trucks Left", 100.0-ps.truckEvaluate())
            self.search()

    def search(self):
        for i in range(len(trucks)):

            # test for package pick up
            for j in range(len(packs)):
                if (trucks[i].location == packs[j].location) and\
                        (packs[j].location != packs[j].destination):
                    trucks[i].pickupPackage(packs[j])
                    print("Truck", i, "Has picked up package", j)

            # test for current packages
            if len(trucks[i].cargo) > 0:
                left = trucks[i].adjacent[0]
                right = trucks[i].adjacent[1]
                currentDestination = trucks[i].cargo[0].destination
                if trucks[i].location > currentDestination:
                    trucks[i].moveVehicle(left)
                else:
                    trucks[i].moveVehicle(right)
            # move towards package destination

            # move to adjency


# # TODO: Implement
# class SearchNodes:
#     def searchNodes(self):
#         return True


class StateQueue:
    problemQueue = []

    def __init__(self,ps):
        self.problemQueue.append(ps)

    def remove(self):
        return self.problemQueue.pop()

    def add(self, ps):
        self.problemQueue.append(ps)


class ProblemState:
    vehicles = []
    packages = []

    def __init__(self, newVehicles, newPacks):
        self.vehicles = newVehicles
        self.packages = newPacks

    # Percentage of Packages at goals
    # Returns Percentage
    def packageEvaluate(self):
        test = 0
        for i in range(len(self.packages)):
            current = self.packages
            if current[i].location == current[i].destination:
                test += 1
        return test*100/len(self.packages)

    # Percentage of Trucks in Garage
    # Returns Percentage
    def truckEvaluate(self):
        test = 0
        g = nx.grid_graph([1])
        g.add_node(0, node=0)
        for i in range(len(self.vehicles)):
            current = self.vehicles
            if current[i].location == g.node[0]:
                test += 1
        return test*100/len(self.vehicles)

    # Displays Current State to console
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
    G = nx.Graph()

    def __init__(self):
        global trucks, packs, G
        trucks = []
        packs = []
        # Graph Creation
        self.G = nx.grid_graph([gridx])
        for i in range(self.G.number_of_nodes()):
            self.G.add_node(i, node=i)

        # Trucks Creation
        for i in range(trucksNum):
            newTruck = Vehicle(self.G.node[0], self.G[0], i)
            trucks.append(newTruck)

        # Packages Creation
        for i in range(packsNum):
            x = rng.randint(1, self.G.number_of_nodes()-1)
            y = rng.randint(1, self.G.number_of_nodes()-1)
            while x == y:
                y = rng.randint(1, self.G.number_of_nodes()-1)
            newPack = Package(self.G.node[x], self.G.node[y], 1)
            packs.append(newPack)

        G = self.G

    # packages at destination
    @staticmethod
    def isGoal():
        test = 0

        for i in range(len(packs)):
            if packs[i].location == packs[i].destination:
                test += 1

        print("Goal Completion:", test*100/len(packs), "%")

        if test == len(packs):
            return True
        else:
            return False

    # returns next (Vehicle Id, possible nodes)
    @staticmethod
    def successors():
        successArray = []
        current = []
        for i in range(len(trucks)):
            current += trucks[i].adjacent
            nextT = [trucks[i].vid]
            for j in range(len(current)):
                nextT.append(current[j])
            successArray.append(nextT)
            current = []
        print("successors:")
        print("-----------")
        print(successArray)
        return successArray


# Begin Main Execution
# initialize problem
problem = Problem()


# Test initial problem state
problemState = ProblemState(trucks, packs)

# problemState.displayState()

print(problemState.truckEvaluate(), problemState.packageEvaluate())

# Test percentage towards end
# problem.isGoal()

# test Truck moving
# problem.successors()
# trucks[0].moveVehicle(problem.G.node[1])
# problem.successors()
# packs[0].location = G.node[1]
#
# trucks[0].pickupPackage(packs[0])
#
# print(trucks[0].cargo[0].location)
# trucks[0].moveVehicle(problem.G.node[0])
# problem.successors()
# print(trucks[0].cargo[0].location)

problemState.displayState()
Search(problemState)
problemState.displayState()