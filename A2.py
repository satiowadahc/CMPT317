# Assignment 2
# CMPT 317
# Chad A. Woitas


class board:

    def __init__(self):
        self.x = 5
        self.y = 5


class queen:

    @staticmethod
    def display():
        return 'q'


class dragon:

    @staticmethod
    def display():
        return 'd'


class pawn:

    @staticmethod
    def display():
        return 'p'
