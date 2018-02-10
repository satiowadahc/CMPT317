# Assignment 1 for CMPT 317 A.I.
# Written by Chad Woitas and Brandon Bachynski
# Due Sunday Feb 11
# Current code at https://github.com/satiowadahc/CMPT317
#
# All libraries are published under open source
# https://opensource.org/licenses/Python-2.0

# Algorithm to learn the best path for a delivery truck to
# pick up and deliver all packages, then return to its start point

import random as rng
import copy as cp
import queue as q

# Set Parameters
number_of_trucks = 1
number_of_packs = 1
truck_capacity = 1
grid_x = 10
# Currently code is for linear search
# grid_y = 1


# Package objects
# Zero function on the world around them
# Can be manipulated
class Package:

    def __init__(self, location, source, destination, pid):
        self.location = location
        self.source = source
        self.destination = destination
        self.id = pid
        self.inTransit = False


# Truck objects
# Can move itself and any packages on board
# Will only carry as many packages as listed above
class Truck:
    location = 0
    capacity = 0
    packages = []

    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.packages = []*capacity

    def moveTruckRight(self):
        self.location += 1
        for item in self.packages:
            item.location = self.location

    def moveTruckLeft(self):
        self.location -= 1
        for item in self.packages:
            item.location = self.location

    # return to garage if no packages are on board
    def goHome(self):
        if len(self.packages) == 0:
            self.location = 0
        else:
            print("Still got work to do!")

    def pickupPackage(self, package):
        if package.inTransit:
            print("Package already Picked up")
        else:
            package.inTransit = True
            if len(self.packages) < self.capacity:
                self.packages.append(package)

    def deliverPackage(self, package):
            if package.destination == self.location:
                self.packages.remove(package)


# Function for Scanning the effects of a truck moving left or right
class Search:
    @staticmethod
    def search(currentProblem, initialPState, stateQueue):
        stateQueue.add(initialPState)
        count = 0
        while not stateQueue.empty():
            count += 1
            print(count)
            here = stateQueue.remove()
            if currentProblem.isGoal(here):
                return here
            else:
                nextState = currentProblem.successors(here)
                for s in nextState:
                    stateQueue.add(s)
        return "FAILED SEARCH"


# Class SearchNodes()
class StateQueue:

    def __init__(self):
        self.queue = q.Queue()

    def add(self, state):
        self.queue.put(state)

    def remove(self):
        return self.queue.get()

    def empty(self):
        return self.queue.empty()

    @staticmethod
    def compare(state1, state2):
        if state1.cost < state2.cost:
            return state1.cost
        else:
            return state2.cost


class ProblemState:

    cost = 0

    def __init__(self, trucks, packages):
        self.trucks = trucks
        self.packages = packages

    def getCost(self):
        return self.cost

    def setGoal(self):
        for item in self.packages:
            item.location = item.destination
        for t in self.trucks:
            t.location = 0

    # testing only
    def display(self):
        print("Problem state -----")
        for i in range(len(self.trucks)):
            print("Problem State Truck", i, "at", self.trucks[i].location)
        for i in range(len(self.packages)):
            print("Problem State Package", self.packages[i].id, "at", self.packages[i].location)
            print("Problem State Package", self.packages[i].id, "goes to", self.packages[i].destination)
        print("-------------------")


class Problem:
    trucks = []
    packages = []
    grid = []

    def __init__(self):
        for i in range(number_of_trucks):
            self.trucks.append(Truck(0, truck_capacity))
        for i in range(number_of_packs):
            x = rng.randint(1, grid_x-1)
            y = rng.randint(1, grid_x-1)
            while x < y:
                y = rng.randint(1, grid_x-1)
            self.packages.append(Package(x, x, y, i))

    def initProblemState(self):
        return ProblemState(self.trucks, self.packages)

    # True until proven False
    @staticmethod
    def isGoal(gps):
        PackTest = True
        TruckTest = True

        for i in gps.packages:
            if i.location == i.destination-1:
                PackTest = True
                for j in gps.trucks:
                    j.goHome()
            else:
                return False
        for i in gps.trucks:
            if i.location == 0:
                TruckTest = True
            else:
                return False
        return PackTest and TruckTest

    # Return 2 problem states for each truck in problem state
    @staticmethod
    def successors(ps):
        newProblems = []
        newTruckRight = []
        newTruckLeft = []
        packagesRight = cp.copy(ps.packages)
        packagesLeft = cp.copy(ps.packages)
        # For Adding cost analysis later on
        # costLeft = cp.deepcopy(ps.cost)
        # costRight = cp.deepcopy(ps.cost)
        packagesDropped = []

        # need to add loops for packages and mulitple directions
        for t in range(len(ps.trucks)):
            # Move Right if Possible Else Move Left
            currentTruck = cp.deepcopy(ps.trucks[0])
            if currentTruck.location == grid_x:
                currentTruck.moveTruckLeft()

                # Check to Pick up package
                if(currentTruck.capacity > len(currentTruck.packages) and
                    currentTruck.location == packagesRight[0].location
                   ):
                        currentTruck.pickupPackage(packagesRight[0])
                        packagesRight[0].inTransit = True
                        if len(currentTruck.packages) > 0:
                            print(t, "Picking up at:", currentTruck.packages[0].location)
                # Check to drop off Packages
                if(len(currentTruck.packages) > 0 and
                   currentTruck.location == currentTruck.packages[0].destination
                   ):
                        packagesDropped.append(currentTruck.packages[0])
                        currentTruck.deliverPackage(currentTruck.package[0])
                        print(t, "Dropping off at:", currentTruck.packages[0].location)
                        print("When Truck is at:", currentTruck.location)
                # End Package
                newTruckRight.append(currentTruck)
            else:
                currentTruck.moveTruckRight()
                # Check to Pick up package
                if(currentTruck.capacity > len(currentTruck.packages) and
                   currentTruck.location == packagesRight[0].location
                   ):
                        currentTruck.pickupPackage(packagesRight[0])
                        packagesRight[0].inTransit = True
                        if len(currentTruck.packages) > 0:
                            print(t, "Picking up at:", currentTruck.packages[0].location)
                # Check to drop off Packages
                if(len(currentTruck.packages) > 0 and
                   currentTruck.location == currentTruck.packages[0].destination
                   ):
                        packagesDropped.append(currentTruck.packages[0])
                        print(t, "Dropping off at:", currentTruck.packages[0].location)
                        print("When Truck is at:", currentTruck.location)
                        currentTruck.deliverPackage(currentTruck.packages[0])
                # End Package
                newTruckRight.append(currentTruck)

            for item in currentTruck.packages:
                for pack in packagesRight:
                    if item.id == pack.id:
                        pack.location = item.location
            if len(packagesDropped) > 0:
                print(packagesDropped[0].location)
            for item in packagesDropped:
                for pack in packagesLeft:
                    if item.id == pack.id:
                        pack.location += item.location

            # Move Left if possible else move right
            currentTruck = cp.deepcopy(ps.trucks[0])
            if currentTruck.location == 0:
                currentTruck.moveTruckRight()
                # Check to Pick up package
                if(currentTruck.capacity > len(currentTruck.packages) and
                    currentTruck.location == packagesLeft[0].location
                   ):
                        currentTruck.pickupPackage(packagesLeft[0])
                        packagesLeft[0].inTransit = True
                        if len(currentTruck.packages) > 0:
                            print(t, "Picking up at:", currentTruck.packages[0].location)
                # Check to drop off Packages
                if len(currentTruck.packages) > 0 and\
                        currentTruck.location == currentTruck.packages[0].destination:
                            print(t, "Dropping off at:", currentTruck.packages[0].location)
                            print("When Truck is at:", currentTruck.location)
                            packagesDropped.append(currentTruck.packages[0])
                            currentTruck.deliverPackage(currentTruck.packages[0])

                # End Package
                newTruckLeft.append(currentTruck)
            else:
                currentTruck.moveTruckLeft()
                # Check to Pick up package
                if currentTruck.capacity > len(currentTruck.packages) and\
                   currentTruck.location == packagesLeft[0].location:
                        currentTruck.pickupPackage(packagesLeft[0])
                        packagesLeft[0].inTransit = True
                        if len(currentTruck.packages) > 0:
                            print(t, "Picking up at:", currentTruck.packages[0].location)
                # Check to drop off Packages
                if len(currentTruck.packages) > 0 and\
                   currentTruck.location == currentTruck.packages[0].destination:
                    print(t, "Dropping off at:", currentTruck.packages[0].location)
                    print("When Truck is at:", currentTruck.location)
                    packagesDropped.append(currentTruck.packages[0])
                    currentTruck.deliverPackage(currentTruck.packages[0])

                # End Package)
                newTruckLeft.append(currentTruck)

            for item in currentTruck.packages:
                for pack in packagesLeft:
                    if item.id == pack.id:
                        pack.location = item.location
            if len(packagesDropped) > 0:
                print(packagesDropped[0].location)
            for item in packagesDropped:
                for pack in packagesLeft:
                    if item.id == pack.id:
                        pack.location += item.location

            newProblems.append(ProblemState(newTruckLeft, packagesLeft))
            newProblems.append(ProblemState(newTruckRight, packagesRight))

        return newProblems


# Begin Execution
problem = Problem()

# Initialize Problem State
ps = problem.initProblemState()

# Initialize StateQueue
queue = StateQueue()

# testing the search function
search = Search()
search.search(Problem, ps, queue)
print(problem.isGoal(ps))
