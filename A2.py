# Assignment 2
# CMPT 317
# Chad A. Woitas and Brandon Bachynski
import time as time
import numpy as np
from copy import deepcopy


class token:

    def __init__(self, thing):
        self.type = thing
        self.x = 0
        self.y = 0
        self.alive = True

    def __str__(self):
        if self.type == 'dragon':
            return 'D'
        elif self.type == 'queen':
            return 'Q'
        elif self.type == 'pawn':
            return 'P'
        else:
            return '0'

    def isDragon(self):
        return self.type == 'dragon'

    def isQueen(self):
        return self.type == 'queen'

    def isPawn(self):
        return self.type == 'pawn'

    # @param foe - type token
    def isEnemy(self, foe):
        if isinstance(foe, token):
            if self.isPawn():
                return foe.isDragon() or foe.isQueen()
            elif self.isDragon() or self.isQueen():
                return foe.isPawn()
            else:
                print('ERROR not a valid type')


class board:

    q = token('queen')

    d1 = token('dragon')
    d2 = token('dragon')
    d3 = token('dragon')

    p1 = token('pawn')
    p2 = token('pawn')
    p3 = token('pawn')
    p4 = token('pawn')
    p5 = token('pawn')

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

        self.board = [[0 for i in range(5)] for j in range(5)]

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

        self.board[2][0] = self.q
        self.board[1][1] = self.d1
        self.board[2][1] = self.d2
        self.board[3][1] = self.d3

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
    def successors(self, player):
        successor = []
        nextMoves = []

        if player == 1:
            for i in range(self.y):
                for j in range(self.x):
                    if isinstance(self.board[j][i], token):
                        if self.board[j][i].isPawn():
                            m1 = (j, i)
                            nextMoves.append(self.moveAIPlayer(m1))
                            for k in nextMoves[0]:
                                newBoard = deepcopy(self)
                                successor.append(newBoard.makeMove(m1, k))
                            nextMoves = []
        else:
            for i in range(self.y):
                for j in range(self.x):
                    if isinstance(self.board[j][i], token):
                        if self.board[j][i].isDragon() or self.board[j][i].isQueen():
                            m1 = (j, i)
                            nextMoves.append(self.moveAIPlayer(m1))
                            for k in nextMoves[0]:
                                newBoard = deepcopy(self)
                                successor.append(newBoard.makeMove(m1, k))
                            nextMoves = []
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

    def winFor(self, player):
        if self.cachedWin is False:
            if player == 0:
                if self.q.y == 4:
                    self.cachedWin = True
                    self.cachedWinner = player
                    return True

                for val in self.pawns:
                    if val.alive:
                        return False
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
    # def h1(self, board):

    def nextAvailableMoves(self, m):
        x1 = m[0]
        y1 = m[1]
        # 1 Free Movement
        if 0 < x1 < 4 and 0 < y1 < 4:
            return {(x1, y1 - 1), (x1 - 1, y1), (x1 + 1, y1), (x1, y1 + 1),
                    (x1 - 1, y1 - 1), (x1 - 1, y1 + 1), (x1 + 1, y1 - 1), (x1 + 1, y1 + 1)}
        # 2 Can't Go NegX
        elif x1 == 0 and 1 < y1 < 4:
            return {(x1, y1 - 1), (x1 + 1, y1), (x1, y1 + 1), (x1 + 1, y1 - 1), (x1 + 1, y1 + 1)}
        # 3 Can't go PosX
        elif x1 == 4 and 0 < y1 < 4:
            return {(x1, y1 - 1), (x1 - 1, y1), (x1, y1 + 1), (x1 - 1, y1 - 1), (x1 - 1, y1 + 1)}
        # 4 Can't go NegY
        elif 0 < x1 < 4 and y1 == 0:
            return {(x1 - 1, y1), (x1 + 1, y1), (x1, y1 + 1), (x1 - 1, y1 + 1), (x1 + 1, y1 + 1)}
        # 5 Can't go PosY
        elif 0 < x1 < 4 and y1 == 4:
            return {(x1, y1 - 1), (x1 - 1, y1), (x1 + 1, y1), (x1 - 1, y1 - 1), (x1 + 1, y1 - 1)}
        # 6 Can't go NegX or NegY
        elif x1 == 0 and y1 == 0:
            return {(x1 + 1, y1), (x1, y1 + 1), (x1 + 1, y1 + 1)}
        # 7 Can't go NegX or PosY
        elif x1 == 0 and y1 == 4:
            return {(x1, y1 - 1), (x1 + 1, y1), (x1 + 1, y1 - 1)}
        # 8 Can't go PosX or PosY
        elif x1 == 4 and y1 == 4:
            return {(x1, y1 - 1), (x1 - 1, y1), (x1 - 1, y1 - 1)}
        # 9 Can't go PosX or NegY
        elif x1 == 4 and y1 == 0:
            return {(x1 - 1, y1), (x1, y1 + 1), (x1 - 1, y1 + 1)}
        else:
            return {()}

    # Return allowed moves
    def moveAIPlayer(self, m1):
        moves = self.nextAvailableMoves(m1)
        thing = self.board[m1[0]][m1[1]]
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
                if self.isDiagonalMove(m1, i):
                    if thing.isEnemy(gs):
                        nextMove.append(i)
                else:
                    if not thing.isEnemy(gs):
                        nextMove.append(i)
            return nextMove

    # @params - two locations
    # @return - true if valid move taken
    def makeMove(self, m1, m2):
        p1 = self.board[m1[0]][m1[1]]
        p2 = self.board[m2[0]][m2[1]]

        # Check for players existence
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
                    self.board[m1[0]][m1[1]] = 0
                    self.utility()
                    return self
                else:
                    return False
            elif self.isDiagonalMove(m1, m2):
                if enemy == 1:
                    # TODO make kill function
                    print(self.attack(p1, p2))
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = 0
                    self.utility()
                    return self
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
                    self.board[m1[0]][m1[1]] = 0
                    self.utility()
                    return self
                elif enemy == 1:
                    # TODO MAKE KILL function
                    print(self.attack(p1, p2))
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = 0
                    self.utility()
                    return self
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

    def attack(self, attacker, defender):
        if attacker.isPawn():
            if not defender.isPawn():
                if self.isPlayer(defender):
                    defender.alive = False
                    return True
                else:
                    return False
        elif attacker.isQueen() or attacker.isDragon():
            if defender.isPawn():
                if self.isPlayer(defender):
                    defender.alive = False
                    return True
                else:
                    return False
        else:
            return False

    def display(self):
        print('')
        for i in range(self.y):
            for j in range(self.x):
                    print(self.board[j][i], end='')
            print('')

    def str(self):
        s = ''
        for i in range(self.y):
            for j in range(self.x):
                s += str(self.board[j][i])
        return s

def minimax(start):
    transpositionTable = dict()

    def do_minimax(node):
        s = node.str()
        if s in transpositionTable:
            return transpositionTable[s]
        elif node.isTerminal():
            u = node.utility()
        else:
            vs = [do_minimax(c) for c in node.successors(0)]
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
# p = token('pawn')
# q = token('queen')
# d = token('dragon')
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
# print(b.nextAvailableMoves())
# print(b.moveAIPlayer(m))
# b.makeMove(m, b.moveAIPlayer(m)[1])
# print(b.successors(1))
# b.display()
# attack tested
# b.makeMove(s1, s2)
# b.display()
# print(b.makeMove(s2, s3))
# b.display()
# print(b.makeMove(s3, s4))
# b.display()
# print(b.makeMove(s3, s5))
# b.display()
# print(b.makeMove(s4, s3))
# b.display()
# print(b.makeMove(s5, s4))
# b.display()
# print(b.makeMove(s4, s6))
# b.display()

b = board()
b.display()

tree = b.successors(1)
print(len(tree))
for i in range(len(tree)):
    print(tree[i].display())
# s1 = (3, 4)
# s2 = (3, 3)
# s3 = (3, 2)
# s4 = (3, 1)
# s5 = (2, 1)
# s6 = (2, 0)

# start = time.process_time()
# result = minimax(b)
# end = time.process_time()
