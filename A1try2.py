import random as rng
import copy as cp
import queue as q

number_of_trucks = 1
number_of_packs = 1
truck_capacity = 1
grid_x = 10
grid_y = 1


class Package:

    def __init__(self, location, source, destination, id):
        self.location = location
        self.source = source
        self.destination = destination
        self.id = id


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

    def pickupPackage(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)

    def deliverPackage(self):
        for package in self.packages:
            if package.destination == self.location:
                self.packages.remove(package)


class Search:
    def search(self, problem, initialState, queue):
        queue.initialize()
        queue.add(initialState)
        while not queue.empty():
            here = queue.remove()
            if problem.isGoal(here):
                return here #+ some stats about run time costs
        else:
            next = problem.successors(here)
            for s in next:
                queue.add(s)
        return "FAILED SEARCH + some stats about run time costs"


# Class SearchNodes()
#    - needs to store problem state information as well as search information
class StateQueue:

    queue = q.Queue()

    def add(self, state):
        self.queue.put(state)

    def remove(self):
        return self.queue.get()

    def compare(self, state1, state2):
        if state1.cost < state2.cost:
            return state1.cost
        else:
            return state2.cost


class ProblemState:

    def __init__(self, trucks, packages):
        self.trucks = trucks
        self.packages = packages

    # testing only
    def display(self):
        print("Problem state -----")
        for i in range(len(self.trucks)):
            print("Problem State Truck at", self.trucks[i].location)
        for i in range(len(self.packages)):
            print("Problem State Package at", self.packages[i].location)
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
            while x == y:
                y = rng.randint(1, grid_x-1)
            self.packages.append(Package(x, x, y, i))

    def initProblemState(self):
        return ProblemState(self.trucks, self.packages)

    # True until proven False
    def isGoal(self, ps):
        Ptest = True
        Ttest = True
        for i in ps.packs:
            if i.location == i.destination:
                Ptest = True
            else:
                return False
        for i in ps.trucks:
            if i.location == 0:
                Ttest = True
            else:
                return False
        return Ptest and Ttest

    # Return 2 problem states for each truck in problem state
    def successors(self, ps):
        newProblems = []
        newTruckRight = []
        newTruckLeft = []
        packagesRight = cp.deepcopy(ps.packages)
        packagesLeft = cp.deepcopy(ps.packages)

        # Move Right if Possible Else Move Left
        currentTruck = cp.deepcopy(ps.trucks[0])
        print(currentTruck.packages)
        if len(currentTruck.packages) != 0:
            print("Forwards Truck Pack", currentTruck.packages[0].location)
        if currentTruck.location == grid_x:
            currentTruck.moveTruckLeft()
            # Check to Pick up package
            if currentTruck.capacity > len(currentTruck.packages) and\
                currentTruck.location == packagesRight[0].location:
                    currentTruck.pickupPackage(packagesRight[0])
                    print("pickme")

            # End Package
            newTruckRight.append(currentTruck)
        else:
            currentTruck.moveTruckRight()
            # Check to Pick up package
            if currentTruck.capacity > len(currentTruck.packages) and\
                currentTruck.location == packagesRight[0].location:
                    currentTruck.pickupPackage(packagesRight[0])
                    print("pickme")
            # End Package
            newTruckRight.append(currentTruck)

        for item in currentTruck.packages:
            for pack in packagesRight:
                if item.id == pack.id:
                    pack.location = item.location

        # Move Left if possible else move right
        currentTruck = cp.deepcopy(ps.trucks[0])
        print(currentTruck.packages)
        if len(currentTruck.packages) != 0:
            print("Backwards Truck Pack", currentTruck.packages[0].location)
        if currentTruck.location == 0:
            currentTruck.moveTruckRight()
            # Check to Pick up package
            if currentTruck.capacity > len(currentTruck.packages) and\
                currentTruck.location == packagesLeft[0].location:
                    currentTruck.pickupPackage(packagesLeft[0])
                    print("pickme")
            # End Package
            newTruckLeft.append(currentTruck)
        else:
            currentTruck.moveTruckLeft()
            # Check to Pick up package
            if currentTruck.capacity > len(currentTruck.packages) and\
                currentTruck.location == packagesLeft[0].location:
                    currentTruck.pickupPackage(packagesLeft[0])
                    print("pickme")
            # End Package)
            newTruckLeft.append(currentTruck)

        for item in currentTruck.packages:
            for pack in packagesLeft:
                if item.id == pack.id:
                    pack.location = item.location

        # TODO: issue: packages need to be delivered
        newProblems.append(ProblemState(newTruckLeft, packagesLeft))
        newProblems.append(ProblemState(newTruckRight, packagesRight))

        return newProblems


# Begin Execution
problem = Problem()

# Initialize Problem State
ps = problem.initProblemState()


# Initialize StateQueue

ps.display()
# Testing Below
test = problem.successors(ps)

for i in range(grid_x):
    print("Step", i,i,i,i,i,i)
    print("Moving right")
    test[1].display()
    print("Moving left")
    test[0].display()
    test = problem.successors(test[1])


