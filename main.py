import chess
import sys

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

def alpha_beta(board, isMaximizing, alpha, beta, depth):
    if depth == 0 or board.legal_moves.count() == 0:
        return eval(board)

    if isMaximizing:
        bestVal = -sys.maxint
        for move in board.legal_moves:
            board.push(move)
            bestVal = max(bestVal, alpha_beta(board, not isMaximizing, alpha, beta, depth - 1))
            board.pop()
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal
    else:
        bestVal = sys.maxint
        for move in board.legal_moves:
            board.push(move)
            bestVal = min(bestVal, alpha_beta(board, not isMaximizing, alpha, beta, depth - 1))
            board.pop()
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal

def getBestMove(board):
    bestVal = -sys.maxint
    bestMove = None

    alpha = -sys.maxint
    beta = sys.maxint

    for move in board.legal_moves:
        board.push(move)
        x = alpha_beta(board, False, alpha, beta, 4)
        board.pop()
        if beta <= alpha:
            bestVal = x
            bestMove = move
            break
        if bestVal < x:
            bestVal = x
            bestMove = move

    return bestMove

pieceVals = {
    "P": -100,
    "N": -320,
    "B": -330,
    "R": -500,
    "Q": -900,
    "K": -20000,
    "p": 100,
    "n": 320,
    "b": 330,
    "r": 500,
    "q": 900,
    "k": 20000
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

board = chess.Board()

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
        move = getBestMove(board)
        board.push(move)
