class token:

    def __init__(self, thing):
        self.type = thing
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


# Useful Functions -------------------
def isToken(thing):
    return isinstance(thing, token)


def isDragon(thing):
    if isToken(thing):
        return thing.type == 'dragon'
    else:
        return False


def isQueen(thing):
    if isToken(thing):
        return thing.type == 'queen'
    else:
        return False


def isPawn(thing):
    if isToken(thing):
        return thing.type == 'pawn'
    else:
        return False


def isEnemy(thing, foe):
    if isPawn(thing) and (isDragon(foe) or isQueen(foe)):
        return True
    elif isPawn(foe) and (isDragon(thing) or isQueen(thing)):
        return True
    else:
        return False


def isDiagonal(m1, m2):
    if (abs(m1[0] - m2[0]) == 1) and (abs(m1[1] - m2[1]) == 1):
        return True
    else:
        return False


def isStraight(m1, m2):
    if ((abs(m1[0] - m2[0]) == 1) and (abs(m1[1] - m2[1]) == 0)) or\
       ((abs(m1[0] - m2[0]) == 0) and (abs(m1[1] - m2[1]) == 1)):
        return True
    else:
        return False


class game:

    def __init__(self, board=[1]):
        self.x = 5
        self.y = 5

        # Token Area
        self.q = token('queen')
        self.d = [token('dragon') for c in range(3)]
        self.p = [token('pawn') for c in range(5)]

        # Board area
        if board[0] == 1:
            self.board = [[0 for y in range(5)] for x in range(5)]
            self.board[2][0] = self.q
            self.board[1][1] = self.d[1]
            self.board[2][1] = self.d[2]
            self.board[3][1] = self.d[0]

            self.board[0][4] = self.p[1]
            self.board[1][4] = self.p[2]
            self.board[2][4] = self.p[3]
            self.board[3][4] = self.p[4]
            self.board[4][4] = self.p[0]
        else:
            self.board = board

        # Human and AI Player Area
        self.wights = 1
        self.queens = 2
        self.whoseTurn = self.wights
        self.wightsScore = 0
        self.queensScore = 0
        self.humanPlayer = None
        self.AIPlayer = None

        self.cachedWinner = False
        self.cachedWin = False

    # SETUP FUNCTIONS ---------------------------------
    def initPlayers(self, Human=False):
        # TODO Add human Toggle
        if Human:
            return self.wights

    # Human Input Functions ----------------------------
    def selectPlayer(self):
        player = input("Select P1 or P2: ")

        if player == "P1":
            self.humanPlayer = 1
            self.AIPlayer = 2

        elif player == "P2":
            self.humanPlayer = 2
            self.AIPlayer = 1

    def inputMove(self):
        legalMove = False
        while legalMove:
            start = tuple(int(x.strip()) for x in input("Who do you want to move? ").split(','))
            end = tuple(int(x.strip()) for x in input("Where do you want to move them?").split(','))

            legalMove = self.makeMove(start, end)

            if isinstance(legalMove, game):
                self.togglePlayer()
                return legalMove

    # GAME PLAY FUNCTIONS ------------------------------
    def togglePlayer(self):
        if self.whoseTurn == 1:
            self.whoseTurn = 2
        else:
            self.whoseTurn = 1

    def isMinNode(self):
        if self.whoseTurn == 2:
            # player 1 min
            return True
        else:
            # player 2 min
            return False

    def isMaxNode(self):
        if self.whoseTurn == 1:
            # player 1 max
            return True
        else:
            # player 2 max
            return False

    def winFor(self):
        # Queen is Dead
        if self.q.alive is False:
            self.cachedWin = True
            self.cachedWinner = self.wights
            return -1
        else:
            x = False
            for i in range(5):
                if isQueen(self.board[i][4]):
                    x = True
            if x:
                self.cachedWin = True
                self.cachedWinner = self.queens
                return 1
            else:
                return 0

    def isTerminal(self):
        x = False
        for i in range(5):
            if isQueen(self.board[i][4]):
                x = True
        return not self.q.alive or x

    def utility(self):
        return self.winFor()

    def getBoard(self):
        return self.board()

    #  DISPLAY FUNCTIONS -----------------------------
    def display(self):
        print('')
        for i in range(5):
            for j in range(5):
                    print(self.board[j][i], end='')
            print('')

    def str(self):
        s = ''
        for i in range(self.y):
            for j in range(self.x):
                s += str(self.board[j][i])
        return s

    # MOVEMENT FUNCTIONS -----------------------------
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

    def nextLegalMoves(self, m1):
        moves = self.nextAvailableMoves(m1)
        thing = self.board[m1[0]][m1[1]]
        nextMove = []

        if isQueen(thing) or isDragon(thing):
            for i in moves:
                if 5 > i[0] >= 0 and 5 > i[1] >= 0:
                    gs = self.board[i[0]][i[1]]
                    if isToken(gs):
                        if isEnemy(gs, thing):
                            nextMove.append(i)
                    else:
                        nextMove.append(i)
            return nextMove
        elif isPawn(thing):
            for i in moves:
                if 4 >= i[0] >= 0 and 4 >= i[1] >= 0:
                    gs = self.board[i[0]][i[1]]
                    if isDiagonal(m1, i):
                        if isEnemy(gs,thing):
                            nextMove.append(i)
                    elif not isToken(gs):
                            nextMove.append(i)
            return nextMove

    def makeMove(self, m1, m2):
        x1 = m1[0]
        y1 = m1[1]
        x2 = m2[0]
        y2 = m2[1]

        p1 = self.board[x1][y1]
        p2 = self.board[x2][y2]

        enemy = -1

        # Check for players existence
        if not isToken(p1):
            return False
        else:
            if isEnemy(p1, p2):
                enemy = 1  # Enemy
            elif not isToken(p2):
                enemy = 2  # Blank
            else:
                enemy = 0  # Friendly

        # Check for player movement
        # TODO Add pawn score
        if isPawn(p1):
            # Check if move is 1 square in Straight line
            if isStraight(m1, m2):
                if enemy == 2:
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = 0
                    return self
                else:
                    return False
            elif isDiagonal(m1, m2):
                if enemy == 1:
                    self.board[x2][y2].alive = False
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = 0
                    return self
                else:
                    # Else friendly or not a one step move
                    return False
            else:
                return False
        elif isQueen(p1) or isDragon( p1):
            # Check for not moving
            if (abs(x1 - x2) <= 1) and (abs(y1 - y2) <= 1):
                if enemy == 2:
                    if isQueen(p1) and (abs(y1 - y2) == 1):
                        self.queensScore += 1
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = 0
                    return self
                elif enemy == 1:
                    if isQueen(p1) and (abs(y1 - y2) == 1):
                        self.queensScore += 1
                    self.board[x2][y2].alive = False
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = 0
                    return self
                else:
                    return False
            else:
                return False
        else:
            return False
        # end player movement

    # AI FUNCTIONS -----------------------------------
    def successors(self):
        successor = []

        player = self.whoseTurn
        self.togglePlayer()
        if player == 1:
            for i in range(self.y):
                for j in range(self.x):
                        if isPawn(self.board[j][i]):
                            m1 = (j, i)
                            states = [self.makeMove(m1, k) for k in self.nextLegalMoves(m1)]
                            successor = [game(s.getBoard()) for s in states]
        else:
            for i in range(self.y):
                for j in range(self.x):
                        if self.board[j][i].isDragon() or self.board[j][i].isQueen():
                            m1 = (j, i)
                            states = [self.makeMove(m1,k) for k in self.nextAvailableMoves(m1)]
                            successor = [game(s.getBoard()) for s in states]
        for k in successor:
            if k == False:
                print('Removed False')
                successor.remove(False)
            if k == []:
                print("Removed None")
                successor.remove([])
        print(successor)
        return successor


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
            print(vs)
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
    print(transpositionTable)
    return result


# Game Play -------------------------------------
def playGame():
    b = game()
    b.selectPlayer()
    while b.utility() != (1 or 0 or -1):
        print("Player", b.whoseTurn, "Move")
        if b.humanPlayer == b.whoseTurn:
            b = b.inputMove()
        m = minimax(b)
        print(m)

b = game()
b.selectPlayer()
b.display()
m = minimax(b)
print(m)