# Chad A. Woitas
# #11137533
# NSID: CAW724
# CMPT 317
# Michael Horcsh
# Due Date February 9
# Partner: Brandon B.

# Plan
# --------------------------------
# startSpace
# All Vehicles start at (0,0,0) y=3
# Packages are randomly distributed
# Delivery spots are random

# state
# vehicle location(s) = m
# package location(s) = n
# vehicleHasPackage

# successor function must move vehicle toward package
# or toward location

# ---------------------------------

import networkx as nx
import matplotlib.pyplot as plt

city = nx.grid_graph(dim=[10, 10])

plt.subplot()
nx.draw(city, font_size=1)

plt.show()


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
    def ProblemState(self):
        return True


# TODO: Implement
class Problem:

    def initialize(self):
        return True

    def isGoal(self):
        return True

    def successors(self):
        return True
