import numpy as np

class ChessBoard(object):
    def __init__(self):
        self.pieces = np.zeros((2,6), dtype=np.uint64) # 2 sides, 6 piece bitboards per side
        self.combined_color = np.zeros(2, dtype=np.uint64) # Combined bitboard for all pieces of given color
        self.combined_all = np.uint64(0) # Combined bitboard for all pieces on the board


class Square(object):
    def __init__(self, index):
        self.index = np.uint8(index)

class Piece(IntEnum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

class Move(object):
    def __init__(self, src, dest, promo=None):
        """
        src is Square representing source square
        dst is Square representing destination square
        promo is Piece representing promotion
        """
        self.src = src
        self.dest = dest
        self.promo = promo