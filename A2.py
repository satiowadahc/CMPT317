# Assignment 2
# CMPT 317
# Chad A. Woitas


class Board:

    def __init__(self):
        self.x = 5
        self.y = 5

        self.Q = queen(1, 3)

        self.D1 = dragon(2, 2)
        self.D2 = dragon(2, 3)
        self.D3 = dragon(2, 4)

        self.P1 = pawn(5, 1)
        self.P2 = pawn(5, 2)
        self.P3 = pawn(5, 3)
        self.P4 = pawn(5, 4)
        self.P5 = pawn(5, 5)

    # def display(self):


class queen:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def nextAvailableMoves(self):
        # 1 Free Movement
        if 1 < self.x < 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x+1, self.y), (self.x, self.y+1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 2 Can't Go back
        elif self.x == 1 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 3 Can't go left
        elif 1 < self.x < 5 and self.y == 1:
            return {(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)}
        # 4 Can't go back or left
        elif self.x == 1 and self.y == 1:
            return {(self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y + 1)}
        # 5 Can't go forward
        elif self.x == 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1)}
        # 6 Can't go right
        elif 1 < self.x < 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x + 1, self.y),
                    (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)}
        # 7 Can't go forward or right
        elif self.x == 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x-1, self.y),
                    (self.x - 1, self.y - 1)}
        # 8 Can't go forward or Left
        elif self.x == 5 and self.y == 1:
            return {(self.x-1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1)}
        # 9 Can't go back or right
        elif self.x == 1 and self.y == 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y),
                    (self.x + 1, self.y - 1)}
        else:
            print("Somethings fucky")

    @staticmethod
    def display():
        return 'q'


class dragon:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def nextAvailableMoves(self):
        # 1 Free Movement
        if 1 < self.x < 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x+1, self.y), (self.x, self.y+1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 2 Can't Go back
        elif self.x == 1 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 3 Can't go left
        elif 1 < self.x < 5 and self.y == 1:
            return {(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)}
        # 4 Can't go back or left
        elif self.x == 1 and self.y == 1:
            return {(self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y + 1)}
        # 5 Can't go forward
        elif self.x == 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1)}
        # 6 Can't go right
        elif 1 < self.x < 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x + 1, self.y),
                    (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)}
        # 7 Can't go forward or right
        elif self.x == 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x-1, self.y),
                    (self.x - 1, self.y - 1)}
        # 8 Can't go forward or Left
        elif self.x == 5 and self.y == 1:
            return {(self.x-1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1)}
        # 9 Can't go back or right
        elif self.x == 1 and self.y == 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y),
                    (self.x + 1, self.y - 1)}
        else:
            print("Somethings fucky")

    @staticmethod
    def display():
        return 'd'


class pawn:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def nextAvailableMoves(self):
        # 1 Free Movement
        if 1 < self.x < 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x+1, self.y), (self.x, self.y+1)}
        # 2 Can't Go back
        elif self.x == 1 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y), (self.x, self.y + 1)}
        # 3 Can't go left
        elif 1 < self.x < 5 and self.y == 1:
            return {(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1)}
        # 4 Can't go back or left
        elif self.x == 1 and self.y == 1:
            return {(self.x + 1, self.y), (self.x, self.y + 1)}
        # 5 Can't go forward
        elif self.x == 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x, self.y + 1)}
        # 6 Can't go right
        elif 1 < self.x < 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x-1, self.y), (self.x + 1, self.y)}
        # 7 Can't go forward or right
        elif self.x == 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x-1, self.y)}
        # 8 Can't go forward or Left
        elif self.x == 5 and self.y == 1:
            return {(self.x-1, self.y), (self.x, self.y + 1)}
        # 9 Can't go back or right
        elif self.x == 1 and self.y == 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y)}
        # 10 probably could throw an error
        else:
            print("somethings fucky")

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


p = pawn(1, 5)
print(p.x, p.y)

print(p.nextAvailableMoves())
