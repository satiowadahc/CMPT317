# Assignment 2
# CMPT 317
# Chad A. Woitas


class board:

    def __init__(self,state,player):
        self.x = 5
        self.y = 5

        if state is None:
            self.gameState = dict()
            for r in range(1,5):
                for c in range(1,5):
                    self.gameState[r,c] = None
        else:
            self.gameState = state
            self.whoseTurn = player

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

    # resets board to built in variables
    # does not move players
    def updateBoard(self):
        self.board = [[0 for x in range(self.x)] for y in range(self.y)]
        (m, n) = self.Q.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.Q
        (m, n) = self.D1.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.D1
        (m, n) = self.D2.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.D2
        (m, n) = self.D3.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.D3
        (m, n) = self.P1.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.P1
        (m, n) = self.P2.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.P2
        (m, n) = self.P3.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.P3
        (m, n) = self.P4.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.P4
        (m, n) = self.P5.getCurrentPosition()
        if isinstance(self.board[m][n], int):
            self.board[m][n] = self.P5

    def isQueen(self, x, y):
        return isinstance(self.board[x][y], queen)

    def isDragon(self, x, y):
        return isinstance(self.board[x][y], dragon)

    def isPawn(self, x, y):
        return isinstance(self.board[x][y], pawn)

    def isPlayer(self, x, y):
        return self.isDragon(x, y) or self.isPawn(x, y) or self.isQueen(x, y)

    def isMinNode(self):
        return self.whoseTurn == 0

    def isMaxNode(self):
        return self.whoseTurn == 1

    # Find the successor nodes
    def successors(self):
        global tree
        nodes  = [board(s) for s in tree]

    # Used for switching player
    def togglePlayer(self,p):
        if p == 0:
            return 1
        else:
            return 0

    # TODO Cross check with available moves
    def movePlayer(self, x1, y1, x2, y2):
        # Player Good and empty square
        if self.isPlayer(x1, y1) and not self.isPlayer(x2, y2):
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = 0
        elif self.isPawn(x1, y1) and self.isPawn(x2, y2):
            print("Friendly Fire")
        elif self.isPawn(x1, y1) and self.isDragon(x2, y2):
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = 0
            # Kill Dragon
        elif self.isPawn(x1, y1) and self.isQueen(x2, y2):
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = 0
            print('Winner Winner')
        elif self.isDragon(x1, y1) and self.isDragon(x2, y2):
            print('Friendly fire')
        elif self.isDragon(x1, y1) and self.isQueen(x2, y2):
            print('Friendly Fire')
        elif self.isDragon(x1, y1) and self.isPawn(x2, y2):
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = 0
            # Kill Pawn
        elif self.isQueen(x1, y1) and self.isDragon(x2, y2):
            print('Friendly Fire')
        elif self.isQueen(x1, y1) and self.isPawn(x2, y2):
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = 0
            # Kill Pawn
        else:
            print("Must not be a player there")

    def display(self):
        print('')
        for i in range(self.x):
            for j in range(self.y):
                if self.isPlayer(i, j):
                    print(self.board[i][j].display(), end='')
                else:
                    print(self.board[i][j], end='')
            print('')

    def move(self, who, where):

        gs = self.gameState.copy()
        gs[where] = who
        return gs

class token:

    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.alive = True

    def isDragon(self):
        return self.type == 'dragon'

    def isQueen(self):
        return self.type == 'queen'

    def isPawn(self):
        return self.type == 'pawn'

    # @param foe - type token
    def isEnemy(self, foe):
        if self.isPawn():
            return foe.isPawn()
        elif self.isDragon() or self.isQueen():
            return foe.isDragon();
        else:
            print('ERROR not a valid type')

    # @param foe - type token
    def nextAvailableMoves(self):
        # 1 Free Movement
        if 1 < self.x < 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 2 Can't Go back
        elif self.x == 0 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 5 Can't go forward
        elif self.x == 5 and 1 < self.y < 5:
            return {(self.x, self.y - 1), (self.x - 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1)}
        # 3 Can't go left
        elif 1 < self.x < 5 and self.y == 1:
            return {(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)}
        # 6 Can't go right
        elif 1 < self.x < 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y),
                    (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)}
        # 4 Can't go back or left
        elif self.x == 1 and self.y == 1:
            return {(self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y + 1)}
        # 7 Can't go forward or right
        elif self.x == 5 and self.y == 5:
            return {(self.x, self.y - 1), (self.x - 1, self.y),
                    (self.x - 1, self.y - 1)}
        # 8 Can't go forward or Left
        elif self.x == 5 and self.y == 1:
            return {(self.x - 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1)}
        # 9 Can't go back or right
        elif self.x == 1 and self.y == 5:
            return {(self.x, self.y - 1), (self.x + 1, self.y),
                    (self.x + 1, self.y - 1)}
        else:
            print("Somethings fucky")




# Begin unit tests
p = pawn(1, 2)

print(p.getCurrentPosition())
print(p.nextAvailableMoves())


def minimax(start):
    transpositionTable = dict()

    def do_minimax(node):
        s = node.str()
        if s in transpositionTable:
            return transpositionTable[s]
        elif node.isTerminal():
            u = node.utility()
        else:
            vs = [do_minimax(c) for c in node.successors()]
            if node.isMaxNode():
                u = max(vs)
            elif node.isMinNode():
                u = min(vs)
            else:
                print("Something went horribly wrong")
                return None
        transpositionTable[s] = u
        return u

    result = do_minimax(start)
    # print(transpositionTable)
    return result

b = board(None,player=1)
b.display()

b.movePlayer(0, 2, 0, 1)
b.display()

b.movePlayer(0, 1, 1, 1)
b.display()

b.movePlayer(1, 2, 2, 2)
b.display()

b.movePlayer(2, 2, 3, 2)
b.display()

b.movePlayer(3, 2, 4, 2)
b.display()

b.movePlayer(4, 2, 3, 2)
b.display()