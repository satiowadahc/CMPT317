# Chad A. Woitas
# CMPT 317 A1
# Due Date February 9
#

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

# successor function must

# ---------------------------------

import networkx as nx
import matplotlib.pyplot as plt

city = nx.grid_graph(dim=[3, 4])

# pos = nx.spring_layout(city, iterations=100)

plt.subplot()
nx.draw(city, font_size=8)

plt.show()
