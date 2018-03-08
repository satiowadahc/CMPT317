# Assignment 2
# CMPT 317
# Chad A. Woitas and Brandon Bachynski
import time as time
import numpy as np
from copy import deepcopy


class token:

    def __init__(self, thing, x, y):
        self.type = thing
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
            return foe.isDragon() or foe.isQueen()
        elif self.isDragon() or self.isQueen():
            return foe.isPawn()
        else:
            print('ERROR not a valid type')

    # @param foe - type token
    def nextAvailableMoves(self):
        # 1 Free Movement
        if 0 < self.x < 4 and 0 < self.y < 4:
            return {(self.x, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 2 Can't Go NegX
        elif self.x == 0 and 1 < self.y < 4:
            return {(self.x, self.y - 1), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)}
        # 3 Can't go PosX
        elif self.x == 4 and 0 < self.y < 4:
            return {(self.x, self.y - 1), (self.x - 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y - 1), (self.x - 1, self.y + 1)}
        # 4 Can't go NegY
        elif 0 < self.x < 4 and self.y == 0:
            return {(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)}
        # 5 Can't go PosY
        elif 0 < self.x < 4 and self.y == 4:
            return {(self.x, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y),
                    (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)}
        # 6 Can't go NegX or NegY
        elif self.x == 0 and self.y == 0:
            return {(self.x + 1, self.y), (self.x, self.y + 1),
                    (self.x + 1, self.y + 1)}
        # 7 Can't go NegX or PosY
        elif self.x == 0 and self.y == 4:
            return {(self.x, self.y - 1), (self.x + 1, self.y),
                    (self.x + 1, self.y - 1)}
        # 8 Can't go PosX or PosY
        elif self.x == 4 and self.y == 4:
            return {(self.x, self.y - 1), (self.x - 1, self.y),
                    (self.x - 1, self.y - 1)}
        # 9 Can't go PosX or NegY
        elif self.x == 4 and self.y == 0:
            return {(self.x - 1, self.y), (self.x, self.y + 1),
                    (self.x - 1, self.y + 1)}
        else:
            return None

    def display(self):
        if self.isPawn():
            print('p')
        elif self.isDragon():
            print('d')
        elif self.isQueen():
            print('q')


class board:

    q = token('queen', None, None)

    d1 = token('dragon', None, None)
    d2 = token('dragon', None, None)
    d3 = token('dragon', None, None)

    p1 = token('pawn', None, None)
    p2 = token('pawn', None, None)
    p3 = token('pawn', None, None)
    p4 = token('pawn', None, None)
    p5 = token('pawn', None, None)

    dragons = list()
    dragons.append(d1)
    dragons.append(d2)
    dragons.append(d3)

    pawns = list()
    pawns.append(p1)
    pawns.append(p2)
    pawns.append(p3)
    pawns.append(p4)
    pawns.append(p5)

    def __init__(self):

        self.x = 5
        self.y = 5

        self.board = [[" " for i in range(5)] for j in range(5)]

        # if state is None:
        #     self.board = dict()
        #     for r in range(1,5):
        #         for c in range(1,5):
        #             self.board[r,c] = None
        # else:
        #     self.board = state
        #     self.whoseTurn = player
        #     self.cachedWin = False
        #     self.cachedWinner = None

        self.whoseTurn = 1
        self.cachedWin = False
        self.cachedWinner = None

        self.initialBoard()

    def initialBoard(self):

        self.board[0][2] = self.q
        self.board[1][1] = self.d1
        self.board[1][2] = self.d2
        self.board[1][3] = self.d3

        self.board[0][4] = self.p1
        self.board[1][4] = self.p2
        self.board[2][4] = self.p3
        self.board[3][4] = self.p4
        self.board[4][4] = self.p5

    @staticmethod
    def isPlayer(thing):
        return isinstance(thing, token)

    def isMinNode(self):
        return self.whoseTurn == 0

    def isMaxNode(self):
        return self.whoseTurn == 1

    def allBlanks(self):
        return[v for v in self.board if self.board[v] == ' ']

    # Find the successor nodes
    def successors(self,player):
        successor = []

        if player == 0:
            successor += self.moveAIPlayer(self.q)

            for dragon in self.dragons:
                successor += self.moveAIPlayer(dragon)
        else:
            for pawn in self.pawns:
                successor += self.moveAIPlayer(pawn)

        return successor



    def isTerminal(self):
        return self.winFor(0) or self.winFor(1)

    def utility(self):
        if self.winFor(0):
            return 1
        elif self.winFor(1):
            return -1
        else:
            return 0


    def winFor(self,player):
        if self.cachedWin is False:
            if player == 0:
                if self.q.y == 4:
                    self.cachedWin = True
                    self.cachedWinner = player
                    return True

                for val in self.pawns:
                    if val.alive:
                        return False
                    else:
                        self.cachedWin = True
                        self.cachedWinner = player
                        return True
            if player == 1:
                if self.q.alive is False:
                    self.cachedWin = True
                    self.cachedWinner = player
                    return True
        else:
            return player == self.cachedWinner

    # Used for switching player
    def togglePlayer(self, p):
        if p == 0:
            return 1
        else:
            return 0

    # Heuristic function
    # def h1(self):

    # Return allowed moves
    def moveAIPlayer(self, thing):
        moves = thing.nextAvailableMoves
        nextMove = []

        if thing.isQueen() or thing.isDragon():
            for i in moves:
                gs = self.board[i[0]][i[1]]
                if self.isPlayer(gs):
                    if thing.isEnemy(gs):
                        nextMove.append(i)
                else:
                    nextMove.append(i)
            return nextMove
        elif thing.isPawn():
            for i in moves:
                gs = self.board[i[0]][i[1]]
                if self.isDiagonalMove(thing.getCurrentLocaiton,i):
                    if thing.isEnemy(gs):
                        nextMove.append(i)
                else:
                    if not thing.isEnemy(gs):
                        nextMove.append(i)
            return nextMove

    # @params - two locations
    # @return - true if valid move taken
    def makeMove(self, m1, m2):
        p1 = self.board(m1)
        p2 = self.board(m2)

        # Check for players existestance
        if not self.isPlayer(p1):
            return False
        if self.isPlayer(p2):
            if p1.isEnemy(p2):
                # Enemy
                enemy = 1
            else:
                # Friendly
                enemy = 0
        else:
            # Blank
            enemy = 2

        # Check for player movement
        if p1.isPawn():
            # Check if move is 1 square in Straight line
            if ((abs(m1[0] - m2[0]) == 1) and not (abs(m1[1] - m2[1]) == 1)) or \
                    (not (abs(m1[0] - m2[0]) == 1) and (abs(m1[1] - m2[1]) == 1)):
                if enemy == 2:
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = ''
                    return True
                else:
                    return False
            elif self.isDiagonalMove(m1, m2):
                if enemy == 1:
                    # TODO make kill function
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = ''
                    return True
                else:
                    # Else friendly or not a one step move
                    return False
            else:
                return False
        elif p1.isQueen() or p1.isDragon():
            # Check for not moving
            if (abs(m1[0] - m2[0]) <= 1) and (abs(m1[1] - m2[1]) <= 1):
                if enemy == 2:
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = ''
                    return True
                elif enemy == 1:
                    # TODO MAKE KILL function
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = ''
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        # end player movement

    def isDiagonalMove(self, m1, m2):
        if (abs(m1[0]-m2[0]) == 1) and (abs(m1[0]-m2[0]) == 1):
            return True
        else:
            return False

    def display(self):
        print('')
        for i in range(self.x):
            for j in range(self.y):
                print(self.board[i][j])
                # if self.isPlayer(self.board[i][j]):
                #     print(self.board[i][j], end='')
                # else:
                #     print(self.board[i][j], end='')
            print('')



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


# Begin Testing Below -------------------------------
p = token('pawn', 0, 0)
q = token('queen', 0, 0)
d = token('dragon', 0, 0)

# Completed Tests
# print(p.isPawn())
# print(p.isQueen())
# print(p.isDragon())
#
# print(p.isEnemy(q))
# print(p.isEnemy(d))
# print(p.isEnemy(p))
#
# print(d.isEnemy(q))
# print(d.isEnemy(d))
# print(d.isEnemy(p))
# print(p.nextAvailableMoves())

b = board()

b.display()


