import math

class ChessPiece:
    def __init__(self, color, type):
        self.color = color
        self.type = type

    def __str__(self):
        return f"{self.color} {self.type}"

    def Rook(self):
        return self.type == "Rook"

    def Knight(self):
        return self.type == "Knight"

    def Bishop(self):
        return self.type == "Bishop"

    def Queen(self):
        return self.type == "Queen"

    def King(self):
        return self.type == "King"

    def Pawn(self):
        return self.type == "Pawn"

class Side:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"{self.color}"

    def White(self):
        return self.color == "White"

    def Black(self):
        return self.color == "Black"

class Board:
    def __init__(self, board=None, whomove=Side.White, captured=[]):
        if board is None:
            board = [[ChessPiece.Rook("Black"), ChessPiece.Knight("Black"), ChessPiece.Bishop("Black"),
                      ChessPiece.Queen("Black"), ChessPiece.King("Black"), ChessPiece.Bishop("Black"),
                      ChessPiece.Knight("Black"), ChessPiece.Rook("Black")],
                     [ChessPiece.Pawn("Black") for _ in range(8)],
                     [None for _ in range(8)],
                     [None for _ in range(8)],
                     [None for _ in range(8)],
                     [None for _ in range(8)],
                     [ChessPiece.Pawn("White") for _ in range(8)],
                     [ChessPiece.Rook("White"), ChessPiece.Knight("White"), ChessPiece.Bishop("White"),
                      ChessPiece.Queen("White"), ChessPiece.King("White"), ChessPiece.Bishop("White"),
                      ChessPiece.Knight("White"), ChessPiece.Rook("White")]
                     ]
        self.board = board
        self.whomove = whomove
        self.captured = captured

    def __str__(self):
        return f"{self.board}"

    def Move(self, fromx, fromy, tox, toy):
        mark = True
        match self.board[fromx][fromy]:
            case ChessPiece.Rook(_):
                if tox != fromx and toy != fromy:
                    mark = False
            case ChessPiece.Knight(_):
                if (math.fabs(tox - fromx)!=2 and math.fabs(toy - fromy)!=3) or (math.fabs(tox - fromx)!=3 and math.fabs(toy - fromy)!=2):
                    mark = False
            case ChessPiece.Bishop(_):
                if math.fabs(tox - fromx) != math.fabs(toy - fromy):
                    mark = False
            case ChessPiece.Queen(_):
                if tox != fromx and toy != fromy and math.fabs(tox - fromx) != math.fabs(toy - fromy):
                    mark = False
            case ChessPiece.King(_):
                if math.fabs(tox - fromx) > 1 or math.fabs(toy - fromy) > 1:
                    mark = False
            case ChessPiece.Pawn(_):
                if tox != fromx and toy != fromy:
                    mark = False
        if self.board[tox][toy].color == self.whomove:
            mark=False
        if mark:
            if self.board[tox][toy].color != self.whomove:
                self.captured.append(self.board[tox][toy])
            self.board[tox][toy] = self.board[fromx][fromy]
            self.board[fromx][fromy] = None
