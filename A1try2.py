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
        self.inTransit = False


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
        if package.inTransit:
            print("Package already Picked up")
        else:
            package.inTransit = True
            if len(self.packages) < self.capacity:
                self.packages.append(package)

    def deliverPackage(self,package):
            if package.destination == self.location:
                self.packages.remove(package)


class Search:
    def search(self, problem, initialState, queue):
        #queue.initialize()
        temp = ProblemState([],[])
        queue.add(initialState)
        while not queue.empty():
            here = queue.remove()
            temp = here
            if problem.isGoal(self,here):
                return here #+ some stats about run time costs
        else:
            next = problem.successors(self,temp)
            for s in next:
                queue.add(s)
        return "FAILED SEARCH + some stats about run time costs"


# Class SearchNodes()
#    - needs to store problem state information as well as search information
class StateQueue:

    def __init__(self):
        self.queue = q.Queue()

    def add(self, state):
        self.queue.put(state)

    def remove(self):
        return self.queue.get()

    def empty(self):
        return  self.queue.empty()

    def compare(self, state1, state2):
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
            while x == y:
                y = rng.randint(1, grid_x-1)
            self.packages.append(Package(x, x, y, i))

    def initProblemState(self):
        return ProblemState(self.trucks, self.packages)

    # True until proven False
    def isGoal(self, ps):
        Ptest = True
        Ttest = True

        for i in ps.packages:
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
        costLeft = cp.deepcopy(ps.cost)
        costRight = cp.deepcopy(ps.cost)
        packagesDropped = []

        for t in range(len(ps.trucks)):
            # Move Right if Possible Else Move Left
            currentTruck = cp.deepcopy(ps.trucks[0])
            if currentTruck.location == grid_x:
                currentTruck.moveTruckLeft()
                # Check to Pick up package
                if currentTruck.capacity > len(currentTruck.packages) and\
                    currentTruck.location == packagesRight[0].location:
                        currentTruck.pickupPackage(packagesRight[0])
                        packagesRight[0].inTransit=True
                        if len(currentTruck.packages) > 0:
                            print(t, "Picking up at:", currentTruck.packages[0].location)
                # Check to drop off Packages
                if len(currentTruck.packages) > 0 and\
                    currentTruck.location == currentTruck.packages[0].destination:
                        packagesDropped.append(currentTruck.packages[0])
                        currentTruck.deliverPackage(currentTruck.package[0])
                        print(t, "Dropping off at:", currentTruck.packages[0].location)
                        print("When Truck is at:", currentTruck.location)
                # End Package
                newTruckRight.append(currentTruck)
            else:
                currentTruck.moveTruckRight()
                # Check to Pick up package
                if currentTruck.capacity > len(currentTruck.packages) and\
                    currentTruck.location == packagesRight[0].location:
                        currentTruck.pickupPackage(packagesRight[0])
                        packagesRight[0].inTransit = True
                        if len(currentTruck.packages)>0:
                            print(t, "Picking up at:", currentTruck.packages[0].location)
                # Check to drop off Packages
                if len(currentTruck.packages) > 0 and\
                        currentTruck.location == currentTruck.packages[0].destination:
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

            # TODO: issue: packages need to be delivered
            newProblems.append(ProblemState(newTruckLeft, packagesLeft))
            newProblems.append(ProblemState(newTruckRight, packagesRight))

        print("this is the cost of going right: ", costRight)
        print("this is the cost of going left: ", costLeft)

        return newProblems


# Begin Execution
problem = Problem()

# Initialize Problem State
ps = problem.initProblemState()

# Initialize StateQueue

ps.display()
# Testing Below
test = problem.successors(ps)
queue = StateQueue()

for i in range(grid_x):
    test = problem.successors(test[1])

test[1].display()

    queue.add(test[1])


#testing the search function
search =  Search()
search.search(Problem,ps,queue)

