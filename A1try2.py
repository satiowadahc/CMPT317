import random as rng

number_of_trucks=1
number_of_packs=1
truck_capacity=1
grid_x=10
grid_y=1


class Package:

    def __init__(self, location, source, destination):
        self.location = location
        self.source = source
        self.destination = destination


class Truck:

    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.packages = [None] * capacity

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


class ProblemState:
     def __init__(self,trucks,packages):
        self.trucks = trucks
        self.packages = packages


class Problem:
    trucks = []
    packages = []
    grid = []

    def __init__(self):
        for i in range(number_of_trucks):
            self.trucks.append(Truck(0,truck_capacity))
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
                self.Ptest = True
            else:
                return False
        for i in ps.trucks:
            if i.location == 0:
                self.Ttest = True
            else:
                return False
        return self.Ptest and self.Ttest


    def successors(self, ps):
        newProblems = []
        newTrucks = []
        newPacks = []

        for i in ps.trucks:
            if i.location == 0:
                newTrucks += i.moveRight
            else:
                newTrucks += i.moveLeft
            for j in ps.trucks:
                if j.location == 0:
                    newTrucks += j.moveRight
                elif j.location == grid_x:
                    newTrucks += j.moveLeft
                else:
                    newTrucks += j.moveRight
            # Add Packages from trucks
            # TODO: Add packages

        newProblems += ProblemState(newTrucks, newPacks)
        return newProblems

# Begin Execution

problem = Problem()

ps = problem.initProblemState()

ps.packages


