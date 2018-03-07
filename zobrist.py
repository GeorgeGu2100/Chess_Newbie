import chess
import sys
import random

class ZobristHash(object):
    l = [[] for i in range(64)]

    def __init__(self):
        self.l = l = [{} for i in range(64)]
        self.hash = 0
        for pieces in self.l:
            self.initPieces(pieces)


    def initPieces(self, pieces):
        pieces["K"] = random.randint(0, sys.maxint)
        pieces["Q"] = random.randint(0, sys.maxint)
        pieces["R"] = random.randint(0, sys.maxint)
        pieces["B"] = random.randint(0, sys.maxint)
        pieces["P"] = random.randint(0, sys.maxint)
        pieces["N"] = random.randint(0, sys.maxint)
        pieces["k"] = random.randint(0, sys.maxint)
        pieces["q"] = random.randint(0, sys.maxint)
        pieces["r"] = random.randint(0, sys.maxint)
        pieces["b"] = random.randint(0, sys.maxint)
        pieces["p"] = random.randint(0, sys.maxint)
        pieces["n"] = random.randint(0, sys.maxint)

    def hashBoard(self, board):
        for i in range(64):
            hash = board.piece_at(i)
            if hash != None:
                self.hash ^= self.l[i][hash.symbol()]
        return self.hash

    def recomputeHash(self, board, move):
        if board.piece_at(move.to_square) != None:
            self.hash ^= self.l[move.to_square][board.piece_at(move.to_square).symbol()]
        piece = board.piece_at(move.from_square).symbol()

        self.hash ^= self.l[move.to_square][piece]
        self.hash ^= self.l[move.from_square][piece]
        return self.hash
