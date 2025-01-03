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

    def isChecked(self):
        def is_attacked(x, y, attacker_color):
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
            knight_moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]

            # Check for pawn attacks
            if attacker_color == "White":
                pawn_directions = [(1, -1), (1, 1)]
            else:
                pawn_directions = [(-1, -1), (-1, 1)]

            for dx, dy in pawn_directions:
                if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                    piece = self.board[x + dx][y + dy]
                    if piece and piece.color == attacker_color and piece.Pawn():
                        return True

            # Check for rook, bishop, and queen attacks
            for dx, dy in directions:
                step = 1
                while 0 <= x + step * dx < 8 and 0 <= y + step * dy < 8:
                    piece = self.board[x + step * dx][y + step * dy]
                    if piece:
                        if piece.color == attacker_color:
                            if piece.Rook() and (dx == 0 or dy == 0):
                                return True
                            if piece.Bishop() and (dx != 0 and dy != 0):
                                return True
                            if piece.Queen():
                                return True
                        break
                    step += 1

            # Check for knight attacks
            for dx, dy in knight_moves:
                if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                    piece = self.board[x + dx][y + dy]
                    if piece and piece.color == attacker_color and piece.Knight():
                        return True

            # Check for king attacks
            for dx, dy in directions:
                if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                    piece = self.board[x + dx][y + dy]
                    if piece and piece.color == attacker_color and piece.King():
                        return True

            return False

        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.King():
                    if piece.color == "White" and is_attacked(x, y, "Black"):
                        return
                    if piece.color == "Black" and is_attacked(x, y, "White"):
                        return "Black"
        return None

    def __str__(self):
        return f"{self.board}"

    def Move(self, fromx, fromy, tox, toy):
        mark = True
        match self.board[fromx][fromy]:
            case ChessPiece.Rook(_):
                if tox != fromx and toy != fromy:
                    mark = False
            case ChessPiece.Knight(_):
                if (math.fabs(tox - fromx)!=2 and math.fabs(toy - fromy)!=1) or (math.fabs(tox - fromx)!=1 and math.fabs(toy - fromy)!=2):
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
            self.board[tox][toy] = self.board[fromx][fromy]
            self.board[fromx][fromy] = None
