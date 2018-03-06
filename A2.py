# Assignment 2
# CMPT 317
# Chad A. Woitas


class Board:

    def __init__(self):
        self.x = 5
        self.y = 5

        self.Q = queen(1,3)

        self.D1 = dragon(2,2)
        self.D2 = dragon(2,3)
        self.D3 = dragon(2,4)

        self.P1 = pawn(5, 1)
        self.P2 = pawn(5, 2)
        self.P3 = pawn(5, 3)
        self.P4 = pawn(5, 4)
        self.P5 = pawn(5, 5)

    # def display(self):


class queen:
    def __init__(self,x,y):
        self.x
        self.y

    @staticmethod
    def display():
        return 'q'


class dragon:
    def __init__(self,x,y):
        self.x
        self.y

    @staticmethod
    def display():
        return 'd'


class pawn:
    def __init__(self,x,y):
        self.x
        self.y
    def forward(self):
        if self.x!=5:
            self.x-=1

    def backward(self):
        if self.x!=1:
            self.x+=1

    def left(self):
        if self.y!=1:
            self.y-=1

    @staticmethod
    def display():
        return 'p'

# class search:
#
# class searchNodes:
#
# class problemState:
#
# class problem:
#     def __init__(self):
#         Board board = Board.__init__()