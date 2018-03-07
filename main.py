import chess
import sys
from zobrist import ZobristHash

def reversal(actList):
    replList = [[0 for x in range(8)] for y in range(8)]

    for i in range(0, 8):
        for j in range(0, 8):
            replList[i][j] = 0 - actList[7-i][j]

    return replList

def readPstTxt(filename):
    pst = []
    with open(filename, "r") as f:
        for line in f:
            arr = line.split(",")
            for i in range(len(arr)):
                arr[i] = int(arr[i])
            pst.insert(0, arr)
    return pst

def flatten(l):
    newList = []
    for i in l:
        for elem in i:
            newList.append(elem)
    return newList

def eval(board):
    if board.is_checkmate() and not board.turn:
        return -sys.maxint
    elif board.is_checkmate() and board.turn:
        return sys.maxint
    elif board.is_stalemate():
        return 0
    else:
        total = 0
        for i in chess.SQUARES:
            total = total + getPieceVal(board, i)
        return total

def clearZobristHash(oldNew, zobristHashTable, count):
    if len(zobristHashTable) >= 20000:
        zobristHashTable = {}
        oldNew = {}
        count = 0

def getPieceVal(board, i):
    if board.piece_at(i) == None:
        return 0

    piece = board.piece_at(i).symbol()
    if piece == "R":
        return pieceVals[piece] + whiteRook[i]
    elif piece == "B":
        return pieceVals[piece] + whiteBishop[i]
    elif piece == "K":
        return pieceVals[piece] + whiteKing[i]
    elif piece == "P":
        return pieceVals[piece] + whitePawn[i]
    elif piece == "N":
        return pieceVals[piece] + whiteKnight[i]
    elif piece == "Q":
        return pieceVals[piece] + whiteQueen[i]
    if piece == "r":
        return pieceVals[piece] + blackRook[i]
    elif piece == "b":
        return pieceVals[piece] + blackBishop[i]
    elif piece == "k":
        return pieceVals[piece] + blackKing[i]
    elif piece == "p":
        return pieceVals[piece] + blackPawn[i]
    elif piece == "n":
        return pieceVals[piece] + blackKnight[i]
    elif piece == "q":
        return pieceVals[piece] + blackQueen[i]

def alpha_beta(board, isMaximizing, alpha, beta, depth, zobrist, oldNew, zobristHashTable, count):
    if depth == 0 or board.legal_moves.count() == 0:
        return eval(board)

    if isMaximizing:
        bestVal = -sys.maxint
        for move in board.legal_moves:
            hash = zobrist.recomputeHash(board, move)

            if hash in zobristHashTable and zobristHashTable[hash][1] >= depth and zobristHashTable[hash][2] == False:
                zobrist.recomputeHash(board, move)
                bestVal = max(bestVal, zobristHashTable[hash][0])
                continue

            board.push(move)

            x = alpha_beta(board, False, alpha, beta, depth-1, zobrist, oldNew, zobristHashTable, count)
            bestVal = max(x, bestVal)
            zobristHashTable[hash] = [x, depth, False]
            oldNew[count] = hash
            count += 1
            board.pop()
            zobrist.recomputeHash(board, move)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal
    else:
        bestVal = sys.maxint
        for move in board.legal_moves:
            hash = zobrist.recomputeHash(board, move)

            if hash in zobristHashTable and zobristHashTable[hash][1] >= depth and zobristHashTable[hash][2] == True:
                zobrist.recomputeHash(board, move)
                bestVal = min(bestVal, zobristHashTable[hash][0])
                continue

            board.push(move)
            x = alpha_beta(board, True, alpha, beta, depth-1, zobrist, oldNew, zobristHashTable, count)
            bestVal = min(x, bestVal)
            zobristHashTable[hash] = [x, depth, True]
            oldNew[count] = hash
            count += 1
            board.pop()
            zobrist.recomputeHash(board, move)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal

def getBestMove(board, zobrist, oldNew, zobristHashTable, count, depth):
    bestVal = -sys.maxint
    bestMove = None

    alpha = -sys.maxint
    beta = sys.maxint

    moves = []

    for move in board.legal_moves:
        # clearZobristHash(oldNew, zobristHashTable, count)
        hash = zobrist.recomputeHash(board, move)

        if hash in zobristHashTable and zobristHashTable[hash][1] >= depth and zobristHashTable[hash][2] == False:
            zobrist.recomputeHash(board, move)
            if bestVal < zobristHashTable[hash][0]:
                bestVal = zobristHashTable[hash][0]
                bestMove = move
                continue

        board.push(move)
        x = alpha_beta(board, False, alpha, beta, depth - 1, zobrist, oldNew, zobristHashTable, count)
        board.pop()
        zobrist.recomputeHash(board, move)
        zobristHashTable[hash] = [x, depth, False]
        oldNew[count] = hash
        count += 1

        if beta <= alpha:
            moves.append([bestVal, move])
            bestVal = x
            bestMove = move
            break
        if bestVal < x:
            bestVal = x
            bestMove = move
    return bestMove

pieceVals = {
    "P": -100,
    "N": -280,
    "B": -320,
    "R": -479,
    "Q": -929,
    "K": -60000,
    "p": 100,
    "n": 280,
    "b": 320,
    "r": 479,
    "q": 929,
    "k": 60000
}

whiteKing = readPstTxt("./PieceSquareTables/King_mid.txt")
blackKing = reversal(whiteKing)
whiteKing = flatten(whiteKing)
blackKing = flatten(blackKing)

whiteQueen = readPstTxt("./PieceSquareTables/Queen.txt")
blackQueen = reversal(whiteQueen)
whiteQueen = flatten(whiteQueen)
blackQueen = flatten(blackQueen)

whiteBishop = readPstTxt("./PieceSquareTables/Bishop.txt")
blackBishop = reversal(whiteBishop)
whiteBishop = flatten(whiteBishop)
blackBishop = flatten(blackBishop)

whiteKnight = readPstTxt("./PieceSquareTables/Knight.txt")
blackKnight = reversal(whiteKnight)
whiteKnight = flatten(whiteKnight)
blackKnight = flatten(blackKnight)

whiteRook = readPstTxt("./PieceSquareTables/Rook.txt")
blackRook = reversal(whiteRook)
whiteRook = flatten(whiteRook)
blackRook = flatten(blackRook)

whitePawn = readPstTxt("./PieceSquareTables/Pawn.txt")
blackPawn = reversal(whitePawn)
whitePawn = flatten(whitePawn)
blackPawn = flatten(blackPawn)

depth = 4
zobrist = ZobristHash()
board = chess.Board()
oldNew = {0: zobrist.hashBoard(board)}
zobristHashTable = {zobrist.hashBoard(board): [0, depth, True]}
count = 1

while 1:
    if board.is_checkmate():
        print "Checkmate!"
        print board
        break
    if board.is_stalemate():
        print "Stalemate!"
        print board
        break

    if board.turn:
        print board
        move = raw_input("Please enter a move in algebraic notation\n")
        try:
            board.push_san(move)
        except ValueError:
            print "Invalid move try again"
            continue
    else:
        move = getBestMove(board, zobrist, oldNew, zobristHashTable, count, depth)
        zobrist.recomputeHash(board, move)
        board.push(move)
