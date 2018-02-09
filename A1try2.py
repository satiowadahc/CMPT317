import random as rng

number_of_trucks = 1
number_of_packs = 1
truck_capacity = 1
grid_x = 10
grid_y = 1


class Package:

    def __init__(self, location, source, destination):
        self.location = location
        self.source = source
        self.destination = destination


class Truck:
    location = 0
    capacity = 0
    packages = []

    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.packages = [None] * capacity

    def moveTruckRight(self):
        self.location += 1
        # TODO issue - uninitialized has object type - nonetype
        # for item in self.packages:
        #     item.location = self.location

    def moveTruckLeft(self):
        self.location -= 1
        # TODO issue - uninitialized has object type - nonetype
        # for item in self.packages:
        #     item.location = self.location

    def pickupPackage(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)

    def deliverPackage(self):
        for package in self.packages:
            if package.destination == self.location:
                self.packages.remove(package)

# class Search:
#
#   function search(problem, initialState, queue)
#      queue.initialize()
#      queue.add(initialState)
#      while !queue.empty()
#         here = queue.remove()
#         if problem.isGoal(here)
#            return here + some stats about run time costs
#         else
#            next = problem.successors(here)
#            for s in next
#                queue.add(s)
#         end if
#      end while
#      return FAILED SEARCH + some stats about run time costs
#
# Class SearchNodes()
#    - needs to store problem state information as well as search information
#
# class StateQueue:
#    function initialize()
#    function remove()
#    function add(state)
#    -- needs to be able to compare states!
#    -- store heuristic information in the state itself!

# PASS BY FUCKING REFERENCE
class ProblemState:
    def __init__(self, trucks, packages):
        self.trucks = trucks
        self.packages = packages

    #testing only
    def display(self):
        print("P state -----")
        print("trucks")
        for i in range(len(self.trucks)):
            print(self.trucks[i].location)
        print("packages")
        for i in range(len(self.packages)):
            print(self.packages[i].location)
        print("-----")


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
            self.packages.append(Package(x, x, y))

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
        newPacksLeft = []
        # newPacksRight = []

        # TODO: Issue trucks are changing original problem state
        currentTruck = ps.trucks[0]
        print(ps.trucks[0].location)  # testing --------------
        # Move Right if Possible Else Move Left
        if currentTruck.location == grid_x:
            currentTruck.moveTruckLeft()
            newTruckRight.append(currentTruck)
        else:
            currentTruck.moveTruckRight()
            newTruckRight.append(currentTruck)
        print(ps.trucks[0].location)  # testing --------------

        # Move Left if possible else move right
        currentTruck = ps.trucks[0]
        if currentTruck.location == 0:
            currentTruck.moveTruckRight()
            newTruckLeft.append(currentTruck)
        else:
            currentTruck.moveTruckLeft()
            newTruckLeft.append(currentTruck)
        print(ps.trucks[0].location)  # testing --------------

        # TODO: issue: packages aren't updated in problem state Maybe?
        for j in range(len(ps.packages)):
            newPacksLeft.append(ps.packages[j])
        print(ps.trucks[0].location)  # testing --------------
        print("Left", newTruckLeft[0].location)  # testing --------------
        print("Right", newTruckRight[0].location)  # testing --------------

        newProblems.append(ProblemState(newTruckLeft, newPacksLeft))
        newProblems.append(ProblemState(newTruckRight, newPacksLeft))

        newProblems[0].display()
        return newProblems


# Begin Execution
problem = Problem()

# Initialize Problem State
ps = problem.initProblemState()

# Initialize StateQueue

# Testing Below
# ps.display()
# test = problem.successors(ps)
# print(test)
# # test[1].display()
# print("2nd move--------------------")
# test2 = problem.successors(test[1])
# # test2[1].display()
