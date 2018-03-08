# Assignment 2
# CMPT 317
# Chad A. Woitas
import time as time
import numpy as np

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
            return foe.isPawn()
        elif self.isDragon() or self.isQueen():
            return foe.isDragon()
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

    pawns = list()
    pawns.append(p1)
    pawns.append(p2)
    pawns.append(p3)
    pawns.append(p4)
    pawns.append(p5)

    def __init__(self, state, player):

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
            self.cachedWin = False
            self.cachedWinner = None

        self.q = self.gameState.q

        self.d1 = self.gameState.d1
        self.d2 = self.gameState.d2
        self.d3 = self.gameState.d3

        self.p1 = self.gameState.p1
        self.p2 = self.gameState.p2
        self.p3 = self.gameState.p3
        self.p4 = self.gameState.p4
        self.p5 = self.gameState.p5



    @staticmethod
    def isPlayer(thing):
        return isinstance(thing, token)

    def isMinNode(self):
        return self.whoseTurn == 0

    def isMaxNode(self):
        return self.whoseTurn == 1

    def allBlanks(self):
        return[v for v in self.gameState if self.gameState[v] == ' ']

    # Find the successor nodes
    def successors(self):

        blanks = self.allBlanks()
        next = self.togglePlayer(self.whoseTurn)
        states = map(lambda v: self.move(v,self.whoseTurn),blanks)
        nodes  = [(m,board(s,next)) for m,s in states]
        return nodes

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

    # Return allowed moves
    def moveAIPlayer(self, thing):
        moves = thing.nextAvailableMoves
        nextMove = []

        if thing.isQueen() or thing.isDragon():
            for i in moves:
                gs = self.gameState[i[0]][i[1]]
                if self.isPlayer(gs):
                    if thing.isEnemy(gs):
                        nextMove.append(i)
                else:
                    nextMove.append(i[0], i[1])
            return nextMove
        elif thing.isPawn():
            for i in moves:
                gs = self.gameState[i[0]][i[1]]
                if self.isDiagonalMove(thing.getCurrentLocaiton,i):
                    if thing.isEnemy(gs):
                        nextMove.append(i)
                else:
                    if not thing.isEnemy(gs):
                        nextMove.append(i)
            return nextMove


    @staticmethod
    def isDiagonalMove(m1, m2):
        if (abs(m1[0]-m2[0]) == 1) and (abs(m1[0]-m2[0]) == 1):
            return True
        else:
            return False

    def display(self):
        print('')
        for i in range(self.x):
            for j in range(self.y):
                if self.isPlayer(i, j):
                    print(self.board[i][j].display(), end='')
                else:
                    print(self.board[i][j], end='')
            print('')

    def move(self, token, where):

        gs = self.gameState.copy()
        gs[where] = token
        return (where,token),gs


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


initState = np.zeros((5,5),str)

initialState = [[0 for x in range(5)] for y in range(5)]

initState[2][0] = 'q'

initState[1][1] = 'd1'
initState[2][1] = 'd2'
initState[3][1] = 'd3'

initState[0][4] = 'p1'
initState[1][4] = 'p2'
initState[2][4] = 'p3'
initState[3][4] = 'p4'
initState[4][4] = 'p5'

a = board(initState, player=1)

print(a.whoseTurn)

print(initState)
#while not a.isTerminal():
    # start = time.process_time()
    # result = minimax(a)
    # end = time.process_time()
    # print('Took', end-start, 'seconds to determine the minimax value', result[0], 'for move', result[1])
    # result[2].display()
    # a = result[2]


