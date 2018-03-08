# Assignment 2
# CMPT 317
# Chad A. Woitas


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

    def __init__(self, state, player, numMoves):

        self.x = 5
        self.y = 5
        self.moves = numMoves
        if state is None:
            self.gameState = dict()
            for r in range(1,5):
                for c in range(1,5):
                    self.gameState[r,c] = None
        else:
            self.gameState = state
            self.whoseTurn = player
            self.chachedWin = False
            self.chachedWinner = None

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

    # Find the successor nodes
    def successors(self):
        global tree
        nodes  = [board(s,) for s in tree]

    def isTerminal(self):
        return self.winFor(0) or self.winFor(1) or self.moves == 50

    def winFor(self, player):
        if self.chachedWin is False:
            if player == 0:
                if self.q.y == 4:
                    self.chachedWin = True
                    self.chachedWinner = player
                    return True

                for val in self.pawns:
                    if val.x != None or val.y !=None:
                        return False
                    else:
                        self.chachedWin = True
                        self.chachedWinner = player
                        return True
            if player == 1:
                if self.q.x == None and self.q.y == None:
                    self.chachedWin = True
                    self.chachedWinner = player
                    return True
        else:
            return player == self.chachedWinner

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


    def makeMove(self, m1, m2):
        p1 = self.gameState(m1)
        p2 = self.gameState(m2)
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

        if p1.isPawn():
            # Check if move is 1 square in Straight line
            if ((abs(m1[0] - m2[0]) == 1) and not (abs(m1[1] - m2[1]) == 1)) or \
                    (not (abs(m1[0] - m2[0]) == 1) and (abs(m1[1] - m2[1]) == 1)):
                if enemy == 2:
                    self.gameState[m2[0]][m2[1]] = self.gameState[m1[0]][m1[1]]
                    self.gameState[m1[0]][m1[1]] = ''
                    return True
                else:
                    return False
            elif self.isDiagonalMove(m1,m2):
                if enemy == 1:
                    # TODO make kill function
                    self.gameState[m2[0]][m2[1]] = self.gameState[m1[0]][m1[1]]
                    self.gameState[m1[0]][m1[1]] = ''
                    return True
                else:
                    return False
            else:
                return False
        elif p1.isQueen() or p1.isDragon():
            # Check for not moving
            if (abs(m1[0] - m2[0]) <= 1) and (abs(m1[1] - m2[1]) <= 1):
                if enemy == 2:
                    self.gameState[m2[0]][m2[1]] = self.gameState[m1[0]][m1[1]]
                    self.gameState[m1[0]][m1[1]] = ''
                    return True
                elif enemy == 1:
                    # TODO MAKE KILL function
                    self.gameState[m2[0]][m2[1]] = self.gameState[m1[0]][m1[1]]
                    self.gameState[m1[0]][m1[1]] = ''
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False



        elif
        # elif p1.isPawn():
        #     if (abs(m1[0]-m2[0]) <= 1) or (abs(m1[1]-m2[1]) <= 1):
        #         if p1.isEnemy(p2):
        #             if self.isDiagonalMove(m1, m2):
        #                 p2.alive = False
        #                 self.gameState[m2[0]][m2[1]] = p1
        #                 self.gameState[m1[0]][m1[1]] = ' '
        #         else:
        #             p1.x = m2[0]
        #             p2.y = m2[1]
        # elif p1.isDragon() or p1.isQueen():
        #     if (abs(m1[0] - m2[0]) <= 1) or (abs(m1[1] - m2[1]) <= 1):
        #         if self.isPlayer(p2)
        #
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

    def move(self, who, where):

        gs = self.gameState.copy()
        gs[where] = who
        return gs






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

state = [[0 for i in range(5)] for j in range(5)]

for i in range(5):
    state[i][4] = token('pawn', i, 4)
state[2][0] = token('queen', 2, 0)
state[1][1] = token('dragon', 1, 1)
state[2][1] = token('dragon', 2, 1)
state[3][1] = token('dragon', 3, 1)

# b = board(state, 0, 0)

p = token('pawn', 0, 0)
print(p.isQueen())
print(p.isDragon())
print(p.isPawn())
p.display()
print(p.alive)
