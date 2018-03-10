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


def test():

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

    def __init__(self, board=[]):
        self.x = 5
        self.y = 5


        # Token Area
        self.q = token('queen')
        self.d = [token('dragon') for c in range(3)]
        self.p = [token('pawn') for c in range(5)]

        # Board area
        if board is []:
            self.board = self.initialBoard()
        else:
            self.board = board

        # Human and AI Player Area
        self.wights = 1
        self.queens = 2
        self.whoseTurn = self.wights
        self.wightsScore = 0
        self.queensScore = 0

        self.cachedWinner = False
        self.cachedWin = False

    # SETUP FUNCTIONS ---------------------------------
    def initialBoard(self):
        board = [[0 for y in range(5)] for x in range(5)]
        board[2][0] = self.q
        board[1][1] = self.d[1]
        board[2][1] = self.d[2]
        board[3][1] = self.d[0]

        board[0][4] = self.p[1]
        board[1][4] = self.p[2]
        board[2][4] = self.p[3]
        board[3][4] = self.p[4]
        board[4][4] = self.p[0]
        return board

    def initPlayers(self, Human=False):
        # TODO Add human Toggle
        if Human:
            return self.wights

    # Human Input Functions ----------------------------
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
        if self.q.Alive is False:
            self.cachedWin = True
            self.cachedWinner = self.wights
            return True
        else:
            for c in self.p:
                # Wights still fighting
                if c.alive:
                    return False
            self.cachedWin = True
            self.cachedWinner = self.queens
            return True

    def isTerminal(self):
        return self.utility() == self.winFor()

    def utility(self):
        # TODO: Correct Queen Y Coordinates
        if self.q.y == 4:
            return 1
        elif self.q.alive is False:
            return -1
        else:
            return 0



    #  DISPLAY FUNCTIONS -----------------------------
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
        t = test()

        if thing.isQueen() or thing.isDragon():
            for i in moves:
                if 5 > i[0] >= 0 and 5 > i[1] >= 0:
                    gs = self.board[i[0]][i[1]]
                    if t.isToken(gs):
                        if thing.isEnemy(gs):
                            nextMove.append(i)
                    else:
                        nextMove.append(i)
            return nextMove
        elif thing.isPawn():
            for i in moves:
                if 4 >= i[0] >= 0 and 4 >= i[1] >= 0:
                    gs = self.board[i[0]][i[1]]
                    if t.isDiagonalMove(m1, i):
                        if thing.isEnemy(gs):
                            nextMove.append(i)
                    elif not t.isPlayer(gs):
                            nextMove.append(i)
            return nextMove

    def makeMove(self, m1, m2):
        x1 = m1[0]
        y1 = m1[1]
        x2 = m2[0]
        y2 = m2[1]

        p1 = self.board[x1][y1]
        p2 = self.board[x2][y2]
        t = test()

        # Check for players existence
        # TODO Clean Up
        if not t.isToken(p1):
            return False
        if t.isToken(p2):
            if t.isEnemy(p1, p2):
                enemy = 1
            else:
                enemy = 0
        else:
            enemy = 2

        # Check for player movement
        # TODO Add pawn score
        if p1.isPawn():
            # Check if move is 1 square in Straight line
            if t.isStraight(m1, m2):
                if enemy == 2:
                    self.board[x2][y2].alive = False
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = 0
                    return self
                else:
                    return False
            elif t.isDiagonalMove(m1, m2):
                if enemy == 1:
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = 0
                    return self
                else:
                    # Else friendly or not a one step move
                    return False
            else:
                return False
        elif p1.isQueen() or p1.isDragon():
            # Check for not moving
            if (abs(x1 - x2) <= 1) and (abs(y1 - y2) <= 1):
                if enemy == 2:
                    if p1.isQueen() and (abs(y1 - y2) == 1):
                        self.queensScore += 1
                    self.board[x2][y2] = self.board[x1][y1]
                    self.board[x1][y1] = 0
                    return self
                elif enemy == 1:
                    if p1.isQueen() and (abs(y1 - y2) == 1):
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
                    if isinstance(self.board[j][i], token):
                        if self.board[j][i].isPawn():
                            m1 = (j, i)
                            successor = [self.makeMove(m1, k) for k in self.moveAIPlayer(m1)]
        else:
            for i in range(self.y):
                for j in range(self.x):
                    if isinstance(self.board[j][i], token):
                        if self.board[j][i].isDragon() or self.board[j][i].isQueen():
                            m1 = (j, i)
                            successor = [self.makeMove(m1, k) for k in self.moveAIPlayer(m1)]
        for k in successor:
            if k == False:
                print('Removed False')
                successor.remove(False)
            if k == []:
                print("Removed None")
                successor.remove([])
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


    # G

    # Game Play -------------------------------------
def playGame():
    b = game()
    b.display()
    while b.utility() != (1 or 0 or -1):
        print("Player", b.whoseTurn, "Move")
        if b.humanPlayer == b.whoseTurn:
            b = b.inputMove()
        m = minimax(b)
        print(m)


playGame()