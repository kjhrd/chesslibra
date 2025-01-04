import math

class ChessPiece:
    def __init__(self, color, type):
        self.color = color
        self.type = type

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Rook")

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Knight")


class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Bishop")


class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Queen")


class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "King")


class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color, "Pawn")


class Board:
    def __init__(self, board=None, whomove="White", captured=None):
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

    def get(self):
        pr_board = []
        for i in range(8):
            pr_board.append(str(8 - i))
            for j in range(8):
                piece = ""
                if self.board[i][j] is None:
                    piece = " "
                else:
                    match self.board[i][j].type:
                        case "Rook":
                            piece = "♖" if self.board[i][j].color == "White" else "♜"
                        case "Knight":
                            piece = "♘" if self.board[i][j].color == "White" else "♞"
                        case "Bishop":
                            piece = "♗" if self.board[i][j].color == "White" else "♝"
                        case "Queen":
                            piece = "♕" if self.board[i][j].color == "White" else "♛"
                        case "King":
                            piece = "♔" if self.board[i][j].color == "White" else "♚"
                        case "Pawn":
                            piece = "♙" if self.board[i][j].color == "White" else "♟"
                        case None:
                            piece = " "
                pr_board.append(piece)
            pr_board.append("\n")
        pr_board = "".join(pr_board)
        lines = pr_board.split('\n')
        reversed_lines = lines[::-1]
        reversed_lines.append(" abcdefgh")
        return '\n'.join(reversed_lines)


    def Move(self, fromx, fromy, tox, toy):
        mark = True
        if self.board[fromx][fromy] is None:
            return [False, None]
        else:
            match self.board[fromx][fromy].type:
                case "Rook":
                    if tox != fromx and toy != fromy:
                        mark = "Wrong move for rook"
                case "Knight":
                    if (math.fabs(tox - fromx)!=2 and math.fabs(toy - fromy)!=1) or (math.fabs(tox - fromx)!=1 and math.fabs(toy - fromy)!=2):
                        mark = "Wrong move for knight"
                case "Bishop":
                    if math.fabs(tox - fromx) != math.fabs(toy - fromy):
                        mark = "Wrong move for bishop"
                case "Queen":
                    if tox != fromx and toy != fromy and math.fabs(tox - fromx) != math.fabs(toy - fromy):
                        mark = "Wrong move for queen"
                case "King":
                    if math.fabs(tox - fromx) > 1 or math.fabs(toy - fromy) > 1:
                        mark = "Wrong move for king"
                case "Pawn":
                    if tox != fromx and toy != fromy:
                        mark = "Wrong move for pawn"
            if self.board[tox][toy] is not None:
                if self.board[tox][toy].color == self.whomove:
                    mark="Captures your own piece"
            if self.board[fromx][fromy].color != self.whomove:
                mark = "Moves opponent's piece"
            if mark==True:
                pre_board = self.board
                to_ = self.board[tox][toy]
                self.board[tox][toy] = self.board[fromx][fromy]
                self.board[fromx][fromy] = None
                if self.isChecked() == self.whomove:
                    self.board = pre_board
                    mark = "This move puts you in check"
                if mark:
                    self.whomove = "White" if self.whomove == "Black" else "Black"
                    if to_ is not None:
                        self.captured.append(to_)
            return [mark, self.isChecked()]
