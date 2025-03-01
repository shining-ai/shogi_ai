import sys
from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1
    NUM_COLORS = 2


class Piece(Enum):
    NO_PIECE = 0
    BLACK_PAWN = 1
    BLACK_LANCE = 2
    BLACK_KNIGHT = 3
    BLACK_SILVER = 4
    BLACK_GOLD = 5
    BLACK_BISHOP = 6
    BLACK_ROOK = 7
    BLACK_KING = 8
    BLACK_PROMOTED_PAWN = 9
    BLACK_PROMOTED_LANCE = 10
    BLACK_PROMOTED_KNIGHT = 11
    BLACK_PROMOTED_SILVER = 12
    BLACK_HORSE = 13
    BLACK_DRAGON = 14
    WHITE_PAWN = 15
    WHITE_LANCE = 16
    WHITE_KNIGHT = 17
    WHITE_SILVER = 18
    WHITE_GOLD = 19
    WHITE_BISHOP = 20
    WHITE_ROOK = 21
    WHITE_KING = 22
    WHITE_PROMOTED_PAWN = 23
    WHITE_PROMOTED_LANCE = 24
    WHITE_PROMOTED_KNIGHT = 25
    WHITE_PROMOTED_SILVER = 26
    WHITE_HORSE = 27
    WHITE_DRAGON = 28
    NUM_PIECES = 29


PIECE_TO_STR = [
    "    ",
    " 歩 ",
    " 香 ",
    " 桂 ",
    " 銀 ",
    " 金 ",
    " 角 ",
    " 飛 ",
    " 王 ",
    " と ",
    " 杏 ",
    " 圭 ",
    " 全 ",
    " 馬 ",
    " 龍 ",
    " 歩↓",
    " 香↓",
    " 桂↓",
    " 銀↓",
    " 金↓",
    " 角↓",
    " 飛↓",
    " 王↓",
    " と↓",
    " 杏↓",
    " 圭↓",
    " 全↓",
    " 馬↓",
    " 龍↓",
    None,
]

CHAR_TO_PIECE = {
    "K": Piece.BLACK_KING,
    "k": Piece.WHITE_KING,
    "R": Piece.BLACK_ROOK,
    "r": Piece.WHITE_ROOK,
    "B": Piece.BLACK_BISHOP,
    "b": Piece.WHITE_BISHOP,
    "G": Piece.BLACK_GOLD,
    "g": Piece.WHITE_GOLD,
    "S": Piece.BLACK_SILVER,
    "s": Piece.WHITE_SILVER,
    "N": Piece.BLACK_KNIGHT,
    "n": Piece.WHITE_KNIGHT,
    "L": Piece.BLACK_LANCE,
    "l": Piece.WHITE_LANCE,
    "P": Piece.BLACK_PAWN,
    "p": Piece.WHITE_PAWN,
}

NON_PROMOTED_TO_PROMOTED = {
    Piece.BLACK_PAWN: Piece.BLACK_PROMOTED_PAWN,
    Piece.BLACK_LANCE: Piece.BLACK_PROMOTED_LANCE,
    Piece.BLACK_KNIGHT: Piece.BLACK_PROMOTED_KNIGHT,
    Piece.BLACK_SILVER: Piece.BLACK_PROMOTED_SILVER,
    Piece.BLACK_BISHOP: Piece.BLACK_HORSE,
    Piece.BLACK_ROOK: Piece.BLACK_DRAGON,
    Piece.WHITE_PAWN: Piece.WHITE_PROMOTED_PAWN,
    Piece.WHITE_LANCE: Piece.WHITE_PROMOTED_LANCE,
    Piece.WHITE_KNIGHT: Piece.WHITE_PROMOTED_KNIGHT,
    Piece.WHITE_SILVER: Piece.WHITE_PROMOTED_SILVER,
    Piece.WHITE_BISHOP: Piece.WHITE_HORSE,
    Piece.WHITE_ROOK: Piece.WHITE_DRAGON,
}


def as_promoted(piece: Piece) -> Piece:
    """成り駒に変換する（成れる場合のみ変換）"""
    return NON_PROMOTED_TO_PROMOTED.get(piece, piece)


class Position:
    start_position_sfen = (
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1"
    )
    BOARD_SIZE = 9  # 盤面の一辺のマス数

    def __init__(self):
        self.side_to_move = Color.BLACK  # 初期手番は先手
        self.board = [
            [Piece.NO_PIECE.value] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)
        ]  # 盤面初期化
        self.hand_piece = [0] * len(Piece)  # 持ち駒の初期化
        self.play = 1  # 初期手数

    def __str__(self):
        result = []

        # ボードの状態を表示
        result.append("+----+----+----+----+----+----+----+----+----+\n")
        for rank in range(self.BOARD_SIZE):
            result.append("|")
            for file in range(self.BOARD_SIZE - 1, -1, -1):
                result.append(self.to_human_readable_string(self.board[file][rank]))
                result.append("|")
            result.append("\n")
            result.append("+----+----+----+----+----+----+----+----+----+\n")

        # 持ち駒の状態を表示
        result.append("先手 手駒: ")
        for piece in range(Piece.BLACK_PAWN.value, Piece.WHITE_PAWN.value):
            for _ in range(self.hand_piece[piece]):
                result.append(self.to_human_readable_string(Piece(piece)).strip()[0])

        result.append(" , 後手 手駒: ")
        for piece in range(Piece.WHITE_PAWN.value, Piece.NUM_PIECES.value):
            for _ in range(self.hand_piece[piece]):
                result.append(self.to_human_readable_string(Piece(piece)).strip()[0])

        result.append("\n")

        # 手番を表示
        result.append(
            f"手番 = {'先手' if self.side_to_move == Color.BLACK else '後手'}\n"
        )
        return "".join(result)

    def to_human_readable_string(self, piece):
        if not 0 <= piece < len(PIECE_TO_STR):
            return " "
        return PIECE_TO_STR[piece]

    def set_position(self, sfen):
        self.side_to_move = Color.BLACK
        self.board = [
            [Piece.NO_PIECE.value] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)
        ]
        self.hand_piece = [0] * len(Piece)
        self.play = 1

        file = self.BOARD_SIZE - 1
        rank = 0
        index = 0
        promotion = False

        # 盤面のパース
        while index < len(sfen):
            c = sfen[index]
            index += 1
            if c == " ":
                break
            elif c == "/":
                file = self.BOARD_SIZE - 1
                rank += 1
            elif c == "+":
                promotion = True
            elif c.isdigit():
                empty_sequnce = int(c)
                for _ in range(empty_sequnce):
                    self.board[file][rank] = Piece.NO_PIECE.value
                    file -= 1
            else:
                piece = CHAR_TO_PIECE.get(c)
                assert piece is not None
                if promotion:
                    piece = as_promoted(piece)
                    promotion = False
                self.board[file][rank] = piece.value
                file -= 1

        # 手番のパース
        if sfen[index] == "b":
            self.side_to_move = Color.BLACK
        else:
            self.side_to_move = Color.WHITE
        index += 2

        # 持ち駒のパース
        while index < len(sfen):
            if sfen[index] == " ":
                break
            c = sfen[index]
            index += 1
            if c == " ":
                break
            if c == "-":
                continue
            if c.isdigit():
                count = count * 10 + int(c)
                continue
            piece = CHAR_TO_PIECE.get(c)
            assert piece is not None
            self.hand_piece[piece.value] = max(1, count)
            count = 0

        # 手数のパース
        index += 1
        self.play = int(sfen[index:])


def main():
    position = Position()
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            continue

        command = line.split()[0]
        match command:
            case "usi":
                print("id name SimpleShogiEngine")
                print("id author YourName")
                print("usiok")
                sys.stdout.flush()
            case "isready":
                print("readyok")
                sys.stdout.flush()
            case "position":
                assert len(line.split()) >= 2
                if line.split()[1] == "sfen":
                    position.set_position(" ".join(line.split()[2:]))
                    next_index = 6
                elif line.split()[1] == "startpos":
                    position.set_position(Position.start_position_sfen)
                    next_index = 2
                else:
                    print("不正なコマンドです")
            case "go":
                print("bestmove resign")
                sys.stdout.flush()
            case "quit":
                break
            case "d":
                print(position)
                sys.stdout.flush()


if __name__ == "__main__":
    main()
