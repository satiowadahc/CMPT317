# Assignment 2
# CMPT 317
# Chad A. Woitas and Brandon Bachynski
import time as time
from copy import deepcopy
import math

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

    maxPly = 50
    humanPlayer = None
    AI = None
    # TODO standardize to P1 and P2
    # 1 - Queens
    # 2 - Wights
    player1Win = 1
    player2Win = -1
    draw = 0

    player1score = 0
    player2score = 0

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

        self.whoseTurn = 1

        self.initialBoard()
        self.selectPlayer()

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
        # TODO change for ai player
        return self.whoseTurn == 2

    def isMaxNode(self):
        return self.whoseTurn == 1

    def Max(self):
        if self.whoseTurn == 2:
            return self.player2score
        else:
            return self.player1score

    def Min(self):
        if self.whoseTurn == 2:
            return self.player1score
        else:
            return self.player2score

    # Find the successor nodes
    def successors(self):
        successor = []

        player = self.whoseTurn
        self.togglePlayer()

        if player == 1:
            for i in range(self.y):
                for j in range(self.x):
                    if isinstance(self.board[j][i], token):
                        if self.board[j][i].isPawn():
                            m1 = (j, i)
                            states = [self.makeMove(m1 , k) for k in self.moveAIPlayer(m1)]
                            filterStates = list(filter(lambda x: x is not False , states))
                            successor.append(deepcopy(s) for s in filterStates)
                            # nextMoves.append(self.moveAIPlayer(m1))
                            # for k in nextMoves[0]:
                            #     newBoard = deepcopy(self)
                            #     successor.append(newBoard.makeMove(m1, k))


        else:
            for i in range(self.y):
                for j in range(self.x):
                    if isinstance(self.board[j][i], token):
                        if self.board[j][i].isDragon() or self.board[j][i].isQueen():
                            m1 = (j, i)
                            states = [self.makeMove(m1,k) for k in self.moveAIPlayer(m1)]
                            filterStates = list(filter(lambda x: x is not False, states))
                            successor.append(deepcopy(s) for s in filterStates)
                            # nextMoves.append(self.moveAIPlayer(m1))
                            # for k in nextMoves[0]:
                            #     newBoard = deepcopy(self)
                            #     successor.append(newBoard.makeMove(m1, k))

        return successor

    def isTerminal(self):
        return  self.utility() == self.player1Win or self.player2Win

    def utility(self):
        if self.q == 4:
            return self.player1Win

        elif self.q.alive is False:
            return self.player2Win

        else:
            return self.draw



    # Used for switching player
    def togglePlayer(self):
        if self.whoseTurn == 2:
            self.whoseTurn = 1
        else:
            self.whoseTurn = 2

    def nextAvailableMoves(self, m):
        x1 = m[0]
        y1 = m[1]
        # 1 Free Movement
        if 0 < x1 < 4 and 0 < y1 < 4:
            return {(x1, y1 - 1), (x1 - 1, y1), (x1 + 1, y1), (x1, y1 + 1),
                    (x1 - 1, y1 - 1), (x1 - 1, y1 + 1), (x1 + 1, y1 - 1), (x1 + 1, y1 + 1)}
        # 2 Can't Go NegX
        elif x1 == 0 and 0 < y1 < 4:
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
            print('Somethings not right')
            return {()}

    # Return allowed moves
    def moveAIPlayer(self, m1):
        moves = self.nextAvailableMoves(m1)
        thing = self.board[m1[0]][m1[1]]
        # TODO Remove 0's
        nextMove = ['0']
        if thing.isQueen() or thing.isDragon():
            for i in moves:
                if 5 > i[0] >= 0 and 5 > i[1] >= 0:
                    gs = self.board[i[0]][i[1]]
                    if self.isPlayer(gs):
                        if thing.isEnemy(gs):
                            nextMove.append(i)
                    else:
                        nextMove.append(i)
            nextMove.remove('0')
            return nextMove
        elif thing.isPawn():
            for i in moves:
                if 4 >= i[0] >= 0 and 4 >= i[1] >= 0:
                    gs = self.board[i[0]][i[1]]
                    if self.isDiagonalMove(m1, i):
                        if thing.isEnemy(gs):
                            nextMove.append(i)
                    elif not self.isPlayer(gs):
                            nextMove.append(i)
            nextMove.remove('0')
            return nextMove

    # @params - two locations
    # @return - false if invalid move taken
    #         - board if taken
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
                    return self
                else:
                    return False
            elif self.isDiagonalMove(m1, m2):
                if enemy == 1:
                    self.attack(p1, p2)
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = 0
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
                    if p1.isQueen() and (abs(m1[1] - m2[1]) == 1):
                        self.player2score += 1
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = 0
                    return self
                elif enemy == 1:
                    if p1.isQueen() and (abs(m1[1] - m2[1]) == 1):
                        self.player2score += 1
                    self.attack(p1, p2)
                    self.board[m2[0]][m2[1]] = self.board[m1[0]][m1[1]]
                    self.board[m1[0]][m1[1]] = 0
                    return self
                else:
                    return False
            else:
                return False
        else:
            return False
        # end player movement

    def isDiagonalMove(self, m1, m2):
        if (abs(m1[0]-m2[0]) == 1) and (abs(m1[1]-m2[1]) == 1):
            return True
        else:
            return False

    def attack(self, attacker, defender):
        if attacker.isPawn():
            if not defender.isPawn():
                if self.isPlayer(defender):
                    defender.alive = False
                    self.player1score += 1
                    return True
                else:
                    return False
        elif attacker.isQueen() or attacker.isDragon():
            if defender.isPawn():
                if self.isPlayer(defender):
                    self.player2score += 1
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

    def selectPlayer(self):
        player = input("Select P1 or P2: ")

        if player == "P1":
            self.humanPlayer = 1

        elif player == "P2":
            self.humanPlayer = 2

    def inputMove(self):
        legalMove = False
        while legalMove:
            start = tuple(int(x.strip()) for x in input("Who do you want to move? ").split(','))
            end = tuple(int(x.strip()) for x in input("Where do you want to move them?").split(','))


            legalMove = self.makeMove(start, end)

            if isinstance(legalMove, board):
                self.togglePlayer()
                return legalMove


def minimax(start):
    transpositionTable = dict()

    def do_minimax(node, depth, alpha, beta):

        s = node.str()
        if s in transpositionTable:
            return transpositionTable[s]
        elif node.isTerminal():
            u = node.utility()
        else:
            vs = [do_minimax(c, depth+1, alpha, beta) for c in node.successors()]
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


def playGame():
    b = board()
    while  b.utility() != (1,0,-1):
        print(b.humanPlayer)
        print(b.whoseTurn)
        if b.humanPlayer == b.whoseTurn:
            b = b.inputMove()
        m = minimax(b)



# Begin Testing --------------------------------------------------
print(math.inf)
playGame()
