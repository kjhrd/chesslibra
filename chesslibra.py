import math

class ChessPiece:
    def __init__(self, color, type):
        self.color = color
        self.type = type

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Rook")

    def __str__(self):
        return f"{self.color} R"

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Knight")

    def __str__(self):
        return f"{self.color} N"

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Bishop")

    def __str__(self):
        return f"{self.color} B"

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Queen")

    def __str__(self):
        return f"{self.color} Q"

class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "King")

    def __str__(self):
        return f"{self.color} K"

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Pawn")

    def __str__(self):
        return f"{self.color} P"

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
    def __init__(self, board=None, whomove=Side.White, captured=None):
        if captured is None:
            captured = []
        if board is None:
            board = [[Rook("White"), Knight("White"), Bishop("White"),
                      Queen("White"), King("White"), Bishop("White"),
                      Knight("White"), Rook("White")],
                     [Pawn("White") for _ in range(8)],
                     [None for _ in range(8)],
                     [None for _ in range(8)],
                     [None for _ in range(8)],
                     [None for _ in range(8)],
                     [Pawn("Black") for _ in range(8)],
                     [Rook("Black"), Knight("Black"), Bishop("Black"),
                      Queen("Black"), King("Black"), Bishop("Black"),
                      Knight("Black"), Rook("Black")]
                     ]
        self.board = board
        self.whomove = whomove
        self.captured = captured

    def isChecked(self):
        def is_attacked(y, x, attacker_color):
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
                    if piece and piece.color == attacker_color and piece.type == "Pawn":
                        return True

            # Check for rook, bishop, and queen attacks
            for dx, dy in directions:
                step = 1
                while 0 <= x + step * dx < 8 and 0 <= y + step * dy < 8:
                    piece = self.board[x + step * dx][y + step * dy]
                    if piece:
                        if piece.color == attacker_color:
                            if piece.type == "Rook" and (dx == 0 or dy == 0):
                                return True
                            if piece.type == "Bishop" and (dx != 0 and dy != 0):
                                return True
                            if piece.type == "Queen":
                                return True
                        break
                    step += 1

            # Check for knight attacks
            for dx, dy in knight_moves:
                if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                    piece = self.board[x + dx][y + dy]
                    if piece and piece.color == attacker_color and piece.type == "Knight":
                        return True

            # Check for king attacks
            for dx, dy in directions:
                if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                    piece = self.board[x + dx][y + dy]
                    if piece and piece.color == attacker_color and piece.type == "King":
                        return True

            return False

        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.type == "King":
                    if piece.color == "White" and is_attacked(y, x, "Black"):
                        return "White"
                    if piece.color == "Black" and is_attacked(y, x, "White"):
                        return "Black"
        return None

    def __str__(self):
        pr_board = []
        for i in self.board:
            for j in i:
                piece = ""
                if j is None:
                    piece = " "
                else:
                    match j.type:
                        case "Rook":
                            piece = "♖" if j.color == "White" else "♜"
                        case "Knight":
                            piece = "♘" if j.color == "White" else "♞"
                        case "Bishop":
                            piece = "♗" if j.color == "White" else "♝"
                        case "Queen":
                            piece = "♕" if j.color == "White" else "♛"
                        case "King":
                            piece = "♔" if j.color == "White" else "♚"
                        case "Pawn":
                            piece = "♙" if j.color == "White" else "♟"
                        case None:
                            piece = " "
                pr_board.append(piece)
            pr_board.append("\n")
        pr_board = "".join(pr_board)
        lines = pr_board.split('\n')
        reversed_lines = lines[::-1]
        return '\n'.join(reversed_lines)


    def Move(self, fromx, fromy, tox, toy):
        mark = True
        if self.board[fromx][fromy] is None:
            return [False, None]
        else:
            match self.board[fromx][fromy].type:
                case "Rook":
                    if tox != fromx and toy != fromy:
                        mark = False
                case "Knight":
                    if (math.fabs(tox - fromx)!=2 and math.fabs(toy - fromy)!=1) or (math.fabs(tox - fromx)!=1 and math.fabs(toy - fromy)!=2):
                        mark = False
                case "Bishop":
                    if math.fabs(tox - fromx) != math.fabs(toy - fromy):
                        mark = False
                case "Queen":
                    if tox != fromx and toy != fromy and math.fabs(tox - fromx) != math.fabs(toy - fromy):
                        mark = False
                case "King":
                    if math.fabs(tox - fromx) > 1 or math.fabs(toy - fromy) > 1:
                        mark = False
                case "Pawn":
                    if tox != fromx and toy != fromy:
                        mark = False
            if self.board[tox][toy] is not None:
                if self.board[tox][toy].color == self.whomove:
                    mark=False
            if self.board[fromx][fromy].color != self.whomove:
                mark = False
            if mark:
                pre_board = self.board
                to_ = self.board[tox][toy]
                self.board[tox][toy] = self.board[fromx][fromy]
                self.board[fromx][fromy] = None
                if self.isChecked() == self.whomove:
                    self.board = pre_board
                    mark = False
                if mark:
                    self.whomove = "White" if self.whomove == "Black" else "Black"
                    if to_ is not None:
                        self.captured.append(to_)
            return [mark, self.isChecked()]
