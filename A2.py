# Assignment 2
# CMPT 317
# Chad A. Woitas


class board:

    def __init__(self):
        self.x = 5
        self.y = 5

        self.board = [[0 for x in range(self.x)] for y in range(self.y)]

        self.Q = queen(0, 2)

        self.D1 = dragon(1, 1)
        self.D2 = dragon(1, 2)
        self.D3 = dragon(1, 3)

        self.P1 = pawn(4, 0)
        self.P2 = pawn(4, 1)
        self.P3 = pawn(4, 2)
        self.P4 = pawn(4, 3)
        self.P5 = pawn(4, 4)

        self.updateBoard()

    def updateBoard(self):
        (m, n) = self.Q.getCurrentPosition()
        self.board[m][n] = self.Q

        (m, n) = self.D1.getCurrentPosition()
        self.board[m][n] = self.D1
        (m, n) = self.D2.getCurrentPosition()
        self.board[m][n] = self.D2
        (m, n) = self.D3.getCurrentPosition()
        self.board[m][n] = self.D3

        (m, n) = self.P1.getCurrentPosition()
        self.board[m][n] = self.P1
        (m, n) = self.P2.getCurrentPosition()
        self.board[m][n] = self.P2
        (m, n) = self.P3.getCurrentPosition()
        self.board[m][n] = self.P3
        (m, n) = self.P4.getCurrentPosition()
        self.board[m][n] = self.P4
        (m, n) = self.P5.getCurrentPosition()
        self.board[m][n] = self.P5

    def display(self):
        for i in range(self.x):
            for j in range(self.y):
                if isinstance(self.board[i][j], queen) or \
                   isinstance(self.board[i][j], dragon) or \
                   isinstance(self.board[i][j], pawn):
                    print(self.board[i][j].display(), end='')
                else:
                    print(self.board[i][j], end='')
            print('')


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

    def getCurrentPosition(self):
        return self.x, self.y

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

    def getCurrentPosition(self):
        return self.x, self.y

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

    def getCurrentPosition(self):
        return self.x, self.y

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


# Begin unit tests
p = pawn(1, 2)

print(p.getCurrentPosition())
print(p.nextAvailableMoves())

b = board()
b.display()