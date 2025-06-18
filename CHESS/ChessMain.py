from CHESS import CHESS_ENGINE
import pygame as py
import ALGO


py.init()
HEIGHT = WIDTH = 512
Dimension =8
SQ_size= HEIGHT // Dimension
MAX_FPS =15
Images ={ }

def load_images():
    pieces = ["wp","wR","wB","wN","wQ","wK","bp","bR","bB","bN","bQ","bK"]
    for piece in pieces:
        Images[piece]=py.transform.scale(py.image.load("images/"+piece+".png"),(SQ_size,SQ_size))


def main():
    screen = py.display.set_mode((WIDTH,HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color('white'))
    gs = CHESS_ENGINE.GameState()
    validMoves=gs.getvalidmoves()
    Movemade = False
    load_images()
    running = True
    sqSELECTED=()
    playerCLICKS=[]
    animate=False
    gameover=False
    playerOne=True # if human is playing white then true ---> if ai is playing then false
    playerTwo=False # same as above but for black

    while running:
        humanTurn= (gs.whitetoMove and playerOne) or (not gs.whitetoMove and playerTwo)
        for e in py.event.get():
            if e.type==py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                if not gameover:
                    location = py.mouse.get_pos()
                    col=location[0]//SQ_size
                    row=location[1]//SQ_size


                    if sqSELECTED==(row,col): #deselecting a square
                        sqSELECTED=()
                        playerCLICKS=[]

                    else:
                        sqSELECTED=(row,col)
                        playerCLICKS.append(sqSELECTED)


                    if len(playerCLICKS)==2 and humanTurn:
                        move=CHESS_ENGINE.Move(playerCLICKS[0],playerCLICKS[1],gs.board)
                        print(move.GetchessNotation())
                        for i in range(len(validMoves)):
                            if move ==validMoves[i]:
                                gs.MakeMove(validMoves[i])
                                Movemade=True
                                animate=True
                                sqSELECTED=()
                                playerCLICKS=[]

                        if not Movemade:
                            playerCLICKS=[sqSELECTED]

            elif e.type==py.KEYDOWN:
                if e.key==py.K_LEFT:
                    gs.undo()
                    gs.undo()
                    #humanTurn = (gs.whitetoMove and playerOne) or (not gs.whitetoMove and playerTwo)
                    animate=False
                    Movemade=True
                    gameover=False
                    validMoves = gs.getvalidmoves()

                if e.key==py.K_r:
                    gs=CHESS_ENGINE.GameState()
                    validMoves=gs.getvalidmoves()
                    sqSELECTED=()
                    playerCLICKS=[]
                    Movemade=False
                    animate=False
                    gameover=False

        # AI ALGO logic
        if not gameover and not humanTurn:
            AIMove = ALGO.findBestMoveMinMax(gs,validMoves)
            if AIMove is None: # if the ALGO/AI cannot find the best move --> maybe every valid move leads to a checkmate ?
                AIMove=ALGO.findRandomMove(validMoves)
            gs.MakeMove(AIMove)
            Movemade=True
            animate=True

        if Movemade:
            if animate:
                animateMove(gs.Movelog[-1],screen,gs.board,clock)
            validMoves=gs.getvalidmoves()
            Movemade=False
            animate=False


        drawGameState(screen,gs,validMoves,sqSELECTED)

        if gs.checkmate:
            gameover=True
            if gs.whitetoMove:
                drawText(screen,'BLACK WINS')
            else:
                drawText(screen,'WHITE WINS')

        elif gs.stalemate:
            gameover=True
            drawText(screen,'DRAW')



        clock.tick(MAX_FPS)
        py.display.flip()




def highlightSquares(screen,gs,validMoves,sqSELECTED):
    if sqSELECTED!=():
        r,c=sqSELECTED
        if gs.board[r][c][0]==('w' if gs.whitetoMove else 'b'):
            s=py.Surface((SQ_size,SQ_size))
            s.set_alpha(200) #transparency value ---> 0=transparent and 255=opaque
            s.fill(py.Color('Black'))
            screen.blit(s,(c*SQ_size,r*SQ_size))

            s.fill(py.Color('light green'))
            for move in validMoves:
                if move.startRow==r and move.startCol==c:
                    screen.blit(s,(SQ_size*move.endCol,SQ_size*move.endRow))







def drawGameState(screen,gs,validMoves,sqSELECTED):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSELECTED)
    drawPieces(screen,gs.board)


def drawBoard(screen):
    global colors
    colors=[py.Color('White'),py.Color('Gray')]
    for r in range(Dimension):
        for c in range(Dimension):
            color=colors[((r+c)%2)]
            py.draw.rect(screen,color,py.Rect(c*SQ_size,r*SQ_size,SQ_size,SQ_size))


def drawPieces(screen,board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece=board[r][c]
            if piece != "--":
                screen.blit(Images[piece],py.Rect(c*SQ_size,r*SQ_size,SQ_size,SQ_size))


def animateMove(move,screen,board,clock):
    global colors
    dR=move.endRow-move.startRow
    dC=move.endCol-move.startCol
    framesPerSquare=2
    frameCount = (abs(dR)+abs(dC))*framesPerSquare

    for frame in range(frameCount+1):
        r,c=((move.startRow + dR * frame/frameCount , move.startCol+ dC * frame/frameCount))
        drawBoard(screen)
        drawPieces(screen,board)
        color=colors[(move.endRow+move.endCol)%2]
        endSquare=py.Rect(move.endCol*SQ_size,move.endRow*SQ_size,SQ_size,SQ_size)
        py.draw.rect(screen,color,endSquare)
        if move.pieceCaptured!='--' and not move.isEnpassantMove:
           screen.blit(Images[move.pieceCaptured],endSquare)
        elif move.pieceCaptured == '--' and move.isEnpassantMove:
           temp = py.Rect(move.endCol*SQ_size,(move.endRow+1)*SQ_size,SQ_size,SQ_size)
           screen.blit(Images[move.pieceCaptured], endSquare)

        screen.blit(Images[move.pieceMoved],py.Rect(c*SQ_size,r*SQ_size,SQ_size,SQ_size))
        py.display.flip()
        clock.tick(120)


def drawText(screen,text):
    font=py.font.SysFont("Helvitca",32,True,False)
    textObject=font.render(text,0,py.Color('Gray'))
    textLocation=py.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2,HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject=font.render(text,0,py.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))


if __name__ == '__main__':
    main()





