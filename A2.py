# Assignment 2
# CMPT 317
# Chad A. Woitas


class board:

    def __init__(self):
        self.x = 5
        self.y = 5


class queen:

    @staticmethod
    def display():
        return 'q'


class dragon:

    @staticmethod
    def display():
        return 'd'


class pawn:

    @staticmethod
    def display():
        return 'p'


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