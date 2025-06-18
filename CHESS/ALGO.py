import random

pieceScore = {"K":0 , "Q":8.1  , "R":5, "B":3.1 , "N":3, "p":1}
CHECKMATE=1000
STALEMATE = 0
DEPTH=3


knightScores = [
[1,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,1],
[1,1,3,3,3,3,2,1],
[1,1,2,3.2,3.2,2,2,1],
[1,2,3,3.1,3.1,3,2,1],
[1,2,3,3,3,3,2,1],
[1,2,2,2,2,2,2,1],
[1,1,1,1,1,1,2,1]

]

piecePositionScores = {"N":knightScores}



def findRandomMove(validMoves):
    if len(validMoves)!=0:
        return validMoves[random.randint(0,len(validMoves)-1)]
    else:
        return 10


def findBestMove(gs,validMoves):
    turnMultiplier = 1 if gs.whitetoMove else -1
    opponentMinMaxScore=CHECKMATE
    bestPlayerMove = None

    for playerMove in validMoves:
        gs.MakeMove(playerMove)
        opponentMoves=gs.getvalidmoves()
        opponentMaxScore = -CHECKMATE
        random.shuffle(validMoves)
        for opponentMove in opponentMoves:
            gs.MakeMove(opponentMove)
            if gs.checkmate:
              score = -turnMultiplier * CHECKMATE
            elif gs.stalemate:
                score=STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if(score > opponentMaxScore):
                opponentMaxScore=score

            gs.undo()

        if opponentMinMaxScore > opponentMaxScore:
            opponentMinMaxScore=opponentMaxScore
            bestPlayerMove=playerMove
        gs.undo()

    return bestPlayerMove

#Helper function to make the first recursive call
def findBestMoveMinMax(gs,validMoves):
    global nextMove
    random.shuffle(validMoves)
    nextMove=None
    findMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE, CHECKMATE ,1 if gs.whitetoMove else -1)
    #findMoveNegaMax(gs,validMoves,DEPTH,1 if gs.whitetoMove else -1)
    return nextMove


def findMoveMinMax(gs,validMoves,depth,whitetomove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whitetomove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.MakeMove(move)
            nextMoves=gs.getvalidmoves()
            score = findMoveMinMax(gs,nextMoves, depth - 1 ,False)
            if score > maxScore:
                maxScore=score
                if depth == DEPTH:
                    nextMove=move
            gs.undo()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.MakeMove(move)
            nextMoves=gs.getvalidmoves()
            score= findMoveMinMax(gs,nextMoves,depth-1,True)

            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undo()
        return minScore



def findMoveNegaMax(gs,validMoves,depth,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier* scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.MakeMove(move)
        nextMoves= gs.getvalidmoves()
        score = -findMoveNegaMax(gs,nextMoves,depth-1,-turnMultiplier)
        if score>maxScore:
            maxScore=score
            if depth == DEPTH:
                nextMove=move
        gs.undo()
    return maxScore




def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier* scoreBoard(gs)

    # move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.MakeMove(move)
        nextMoves= gs.getvalidmoves()
        score = -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if score>maxScore:
            maxScore=score
            if depth == DEPTH:
                nextMove=move
        gs.undo()
        if maxScore>alpha: # this is where pruning happens
            alpha = maxScore
        if alpha>= beta:
            break

    return maxScore







# positive score is good for white and negative score is good for black
def scoreBoard(gs ):
    if gs.checkmate:
        if gs.whitetoMove:     # black wins
            return -CHECKMATE
        else:                  # white wins
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square=gs.board[row][col]
            piecePositionScore=0
            if square!='--':
                if square[1] == "N":
                    piecePositionScore = piecePositionScores["N"][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]]+piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]]+piecePositionScore

    return score


# scoring the board based on materials
def scoreMaterial(board):
    score=0
    for row in board:
        for square in row:
            if square[0]=='w':
                score+=pieceScore[square[1]]
            elif square[0]=='b':
                score-=pieceScore[square[1]]

    return score
