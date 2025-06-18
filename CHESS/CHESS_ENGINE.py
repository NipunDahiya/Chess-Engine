class GameState():
    def __init__(self):
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--", "--", "--", "--","--", "--", "--","--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]

        self.whitetoMove=True

        self.Movelog = []
        self.WhiteKingLocation = (7,4)
        self.BlackKingLocation = (0,4)

        self.checkmate = False
        self.stalemate = False

        self.count = 1

        self.enpassantPossible=()  # location of the enpassant square in terms of the col and row (0-indexed)

        self.currentCastlingRight=CastleRights(True,True,True,True)
        self.castleRightLog=[CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]


    def MakeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.Movelog.append(move)
        self.whitetoMove = not self.whitetoMove

        if move.pieceMoved=="wK":
            self.WhiteKingLocation = (move.endRow,move.endCol)
        if move.pieceMoved=="bK":
            self.BlackKingLocation =(move.endRow,move.endCol)

        # if the move is pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.pieceMoved[0]+'Q'

        # if the move is enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol]="--" #capturing the pawn :)

        if move.pieceMoved[1]=='p' and abs(move.startRow-move.endRow)==2:
            self.enpassantPossible=((move.startRow+move.endRow)//2,move.startCol)
        else:
            self.enpassantPossible=()

        # if the move is castle
        if move.isCastleMove:
            if move.endCol-move.startCol==2: # king side castle move
                self.board[move.endRow][move.endCol-1]=self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1]='--'
            else:
                self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2]='--'


        #update castling rights
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs,
                     self.currentCastlingRight.bqs))




    def undo(self):
        if len(self.Movelog)!=0:
            move=self.Movelog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whitetoMove = not self.whitetoMove

            if move.pieceMoved == "wK":
                self.WhiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.BlackKingLocation = (move.startRow, move.startCol)

            #undo the enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol]='--'
                self.board[move.startRow][move.endCol]=move.pieceCaptured
                self.enpassantPossible=(move.endRow,move.endCol)

            #undo a 2 square pawn advance
            if move.pieceMoved[1]=='p' and abs(move.startRow-move.endRow)==2:
                self.enpassantPossible=()

            # undoing the castling rights
            self.castleRightLog.pop()
            self.currentCastlingRight = CastleRights(self.castleRightLog[-1].wks,self.castleRightLog[-1].bks,self.castleRightLog[-1].wqs,self.castleRightLog[-1].bqs)

            #undoing the castling move
            if move.isCastleMove:
                if move.endCol-move.startCol==2: # king side castle
                    self.board[move.endRow][move.endCol + 1] =self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1]='--' # Only have to reverse the rook move ---> the king move is taken care by the case undo logic

                else:# queen side castle
                    self.board[move.endRow][move.endCol-2]=self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1]='--'

        # to avoid some bugs in undoing the moves when playing vs the computer
        self.checkmate=False
        self.stalemate=False




    #update the castle rights after the move
    def updateCastleRights(self,move):
        if move.pieceMoved=='wK':
            self.currentCastlingRight.wks=False
            self.currentCastlingRight.wqs=False

        elif move.pieceMoved=='bK':

            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False

        elif move.pieceMoved=='wR':
            if move.startRow==7:
                if move.startCol==0:
                    self.currentCastlingRight.wqs=False
                elif move.startCol==7:
                    self.currentCastlingRight.wks=False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        elif move.pieceCaptured == 'bR':
            if move.endRow==0 and move.endCol==0:
                self.currentCastlingRight.bqs=False
            if move.endRow==0 and move.endCol==7:
                self.currentCastlingRight.bks=False

        elif move.pieceCaptured == 'wR':
            if move.endRow==7 and move.endCol==0:
                self.currentCastlingRight.wqs=False
            if move.endRow==7 and move.endCol==7:
                self.currentCastlingRight.wks=False






# that weird enpassant bug was occuring due to some errors in this funtion ----> Review for later maybe
    def getvalidmoves(self):
        tempEnpassantPossible=self.enpassantPossible
        tempCastlingRights=CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)
        moves=self.getallpossiblemoves()
        self.count+=1

        if self.whitetoMove:
            self.getCastleMoves(self.WhiteKingLocation[0],self.WhiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.BlackKingLocation[0],self.BlackKingLocation[1],moves)


        for i in range(len(moves)-1,-1,-1):
            self.MakeMove(moves[i])
            self.whitetoMove = not self.whitetoMove


            if self.inCheck():
                moves.remove(moves[i])

            self.whitetoMove = not self.whitetoMove
            self.undo()




        if len(moves)==0:
            if self.inCheck():
                self.checkmate=True
            else :
                self.stalemate=True

        else :
            self.checkmate=False
            self.stalemate=False


        self.enpassantPossible=tempEnpassantPossible
        self.currentCastlingRight=CastleRights(tempCastlingRights.wks,tempCastlingRights.bks,tempCastlingRights.wqs,tempCastlingRights.bqs)





        return moves


    # Tells whether or not the king is in check .... it it's white's turn then it tells us whether the white's king is in check or not ---> same is done for black
    def inCheck(self):
        if self.whitetoMove:
            return self.squareUnderAttack(self.WhiteKingLocation[0],self.WhiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.BlackKingLocation[0],self.BlackKingLocation[1])


    def squareUnderAttack(self,r,c):
        self.whitetoMove= not self.whitetoMove
        oppsMoves = self.getallpossiblemoves()
        self.whitetoMove = not self.whitetoMove
        for move in oppsMoves:
            if move.endRow==r and move.endCol==c:
                return True


        return False




# Loops through the entire board ---> if it's white's turn then gets all the white moves ---> if it's black's turn it gets all the black's moves
    def getallpossiblemoves(self):
        moves= [ ]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                if (color =='w' and self.whitetoMove) or (color == "b" and not self.whitetoMove):
                    piece=self.board[r][c][1]
                    if piece == "p":
                        self.getpawnMoves(r,c,moves)
                    elif piece=='R':
                        self.getRookMoves(r,c,moves)
                    elif piece=="N":
                        self.getKnightMoves(r,c,moves)
                    elif piece=="K":
                        self.getKingMoves(r,c,moves)
                    elif piece=="B":
                        self.getBishopMoves(r,c,moves)
                    elif piece == "Q":
                       self.getQueenMoves(r, c, moves)

        return moves


    def getpawnMoves(self,r,c,moves):
        if self.whitetoMove:
            if self.board[r-1][c]=="--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0]=='b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove=True))

            if c+1<=7:
                if self.board[r-1][c+1][0]=='b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        if not self.whitetoMove:
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board))

            if c-1>=0:
                if self.board[r+1][c-1][0]=="w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c+1<=7:
                if self.board[r+1][c+1][0]=="w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))



    def getRookMoves(self,r,c,moves):
        if self.whitetoMove:
            new_c=c-1
            while new_c>=0 and self.board[r][new_c]=="--":
                moves.append(Move((r,c),(r,new_c),self.board))
                new_c-=1
            if new_c>=0:
                if self.board[r][new_c][0]=="b":
                    moves.append(Move((r,c),(r,new_c),self.board))

            new_c = c + 1
            while new_c <= 7 and self.board[r][new_c] == "--":
                moves.append(Move((r, c), (r, new_c), self.board))
                new_c += 1
            if new_c <= 7:
                if self.board[r][new_c][0] == "b":
                    moves.append(Move((r, c), (r, new_c), self.board))



        if not self.whitetoMove:
            new_c=c+1
            while new_c<=7 and self.board[r][new_c]=="--":
                moves.append(Move((r,c),(r,new_c),self.board))
                new_c+=1
            if new_c<=7:
                if self.board[r][new_c][0]=="w":
                    moves.append(Move((r,c),(r,new_c),self.board))

            new_c = c - 1
            while new_c >= 0 and self.board[r][new_c] == "--":
                moves.append(Move((r, c), (r, new_c), self.board))
                new_c -= 1
            if new_c >= 0:
                if self.board[r][new_c][0] == "w":
                    moves.append(Move((r, c), (r, new_c), self.board))


        if self.whitetoMove:
            new_r=r-1
            while new_r>=0 and self.board[new_r][c]=="--":
                moves.append(Move((r,c),(new_r,c),self.board))
                new_r-=1
            if new_r>=0:
                if self.board[new_r][c][0]=="b":
                    moves.append(Move((r,c),(new_r,c),self.board))
            new_r = r + 1
            while new_r <= 7 and self.board[new_r][c] == "--":
                moves.append(Move((r, c), (new_r, c), self.board))
                new_r += 1
            if new_r <= 7:
                if self.board[new_r][c][0]== "b":
                    moves.append(Move((r, c), (new_r, c), self.board))

        if not self.whitetoMove:
            new_r=r+1
            while new_r<=7 and self.board[new_r][c]=="--":
                moves.append(Move((r,c),(new_r,c),self.board))
                new_r+=1
            if new_r<=7:
                if self.board[new_r][c][0]=="w":
                    moves.append(Move((r,c),(new_r,c),self.board))

            new_r = r - 1
            while new_r >= 0 and self.board[new_r][c] == "--":
                moves.append(Move((r, c), (new_r, c), self.board))
                new_r -= 1
            if new_r >= 0:
                if self.board[new_r][c][0]== "w":
                    moves.append(Move((r, c), (new_r, c), self.board))

    def getKnightMoves(self,r,c,moves):
        if self.whitetoMove:
            if c+2<=7 and r+1<=7:
                if self.board[r+1][c+2]=="--" or self.board[r+1][c+2][0]=="b":
                    moves.append(Move((r, c),(r+1,c+2),self.board))

            if c+2<=7 and r-1>=0:
                if self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == "b":
                    moves.append(Move((r, c),(r-1,c+2),self.board))

            if c-2 >= 0 and r +1 <=7:
                if self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == "b":
                    moves.append(Move((r, c), (r + 1, c -2), self.board))

            if c-2 >= 0 and r -1 >=0:
                if self.board[r - 1][c - 2] == "--" or self.board[r - 1][c- 2][0] == "b":
                    moves.append(Move((r, c), (r - 1, c -2), self.board))


            if r+2<=7 and c+1<=7:
                if self.board[r + 2][c + 1] == "--" or self.board[r + 2][c + 1][0] == "b":
                    moves.append(Move((r, c),(r+2,c+1),self.board))

            if r+2<=7 and c-1>=0:
                if self.board[r + 2][c - 1] == "--" or self.board[r + 2][c - 1][0]== "b":
                    moves.append(Move((r, c),(r+2,c-1),self.board))

            if r-2 >= 0 and c +1 <=7:
                if self.board[r - 2][c + 1] == "--" or self.board[r - 2][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 2, c +1), self.board))

            if r-2 >= 0 and c-1 >=0:
                if self.board[r - 2][c - 1] == "--" or self.board[r - 2][c - 1][0] == "b":
                    moves.append(Move((r, c), (r -2, c -1), self.board))

        else:
            if c+2<=7 and r+1<=7:
                if self.board[r+1][c+2]=="--" or self.board[r+1][c+2][0]=="w":
                    moves.append(Move((r, c),(r+1,c+2),self.board))

            if c+2<=7 and r-1>=0:
                if self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == "w":
                    moves.append(Move((r, c),(r-1,c+2),self.board))

            if c-2 >= 0 and r +1 <=7:
                if self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == "w":
                    moves.append(Move((r, c), (r + 1, c -2), self.board))

            if c-2 >= 0 and r -1 >=0:
                if self.board[r - 1][c - 2] == "--" or self.board[r - 1][c- 2][0] == "w":
                    moves.append(Move((r, c), (r - 1, c -2), self.board))


            if r+2<=7 and c+1<=7:
                if self.board[r + 2][c + 1] == "--" or self.board[r + 2][c + 1][0] == "w":
                    moves.append(Move((r, c),(r+2,c+1),self.board))

            if r+2<=7 and c-1>=0:
                if self.board[r + 2][c - 1] == "--" or self.board[r + 2][c - 1][0] == "w":
                    moves.append(Move((r, c),(r+2,c-1),self.board))

            if r-2 >= 0 and c +1 <=7:
                if self.board[r - 2][c + 1] == "--" or self.board[r - 2][c + 1][0] == "w":
                    moves.append(Move((r, c), (r - 2, c +1), self.board))

            if r-2 >= 0 and c-1 >=0:
                if self.board[r - 2][c - 1] == "--" or self.board[r - 2][c - 1][0] == "w":
                    moves.append(Move((r, c), (r -2, c -1), self.board))



    def getBishopMoves(self,r,c,moves):
        directions= ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor="b" if self.whitetoMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break



    def getKingMoves(self,r,c,moves):
        kingMoves =((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor='w' if self.whitetoMove else 'b'

        for i in range(8):
            endRow=r+kingMoves[i][0]
            endCol=c+kingMoves[i][1]

            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


    # gets all the castling moves for the ring at (r,c):
    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return
        if (self.whitetoMove and self.currentCastlingRight.wks) or (not self.whitetoMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r,c,moves)

        if (self.whitetoMove and self.currentCastlingRight.wqs) or (not self.whitetoMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r,c,moves)



    def getKingsideCastleMoves(self,r,c,moves):

        if self.board[r][c+1]=='--' and self.board[r][c+2]=='--':
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))


    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]=='--':
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))





    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)



class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs


class Move():
    ranksToRows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    RowsToranks={v:k for k,v in ranksToRows.items()}
    filesTocols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    ColsTofiles={v:k for k,v in filesTocols.items()}

    def GetchessNotation(self):
        return self.GetRankfile(self.startRow,self.startCol)+self.GetRankfile(self.endRow,self.endCol)

    def GetRankfile(self,r,c):
        return self.ColsTofiles[c]+self.RowsToranks[r]


    def __init__(self,start_sq,end_sq,board,isEnpassantMove=False,isCastleMove=False):
        self.startRow=start_sq[0]
        self.startCol=start_sq[1]
        self.endRow= end_sq[0]
        self.endCol=end_sq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion=False
        self.isEnpassantMove=isEnpassantMove
        self.isCastleMove=isCastleMove


        if self.isEnpassantMove:
            self.pieceCaptured='wp' if self.pieceMoved=='bp' else 'bp'

        if((self.pieceMoved=="wp" and self.endRow==0) or (self.pieceMoved=="bp" and self.endRow==7)):
            self.isPawnPromotion=True

        self.moveID = self.startRow*1000 + self.startCol*100+self.endRow*10+self.endCol


    def __eq__ (self,other):
        if isinstance(other,Move):
            if self.moveID==other.moveID:
                return True
            else:
                return False




