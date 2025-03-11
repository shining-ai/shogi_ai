from piece_types import Color, Piece, CHAR_TO_PIECE


class Move:
    RankToKanjiLetters = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
    ToHumanReadableString = {Color.BLACK: "☗", Color.WHITE: "☖"}
    # 静的インスタンス
    Resign = None
    Win = None
    NoneMove = None

    def __init__(
        self,
        file_from: int,
        rank_from: int = None,
        piece_from: Piece = None,
        file_to: int = None,
        rank_to: int = None,
        piece_to: Piece = None,
        drop: bool = False,  # 駒打ちかどうか
        promotion: bool = False,
        side_to_move: Color = None,
    ):
        self.file_from = file_from
        self.rank_from = rank_from
        self.piece_from = piece_from
        self.file_to = file_to
        self.rank_to = rank_to
        self.piece_to = piece_to
        self.drop = drop
        self.promotion = promotion
        self.side_to_move = side_to_move

    def __str__(self):
        """指し手の文字列変換(デバッグ用)"""
        return (
            f"{self.ToHumanReadableString[self.side_to_move]} "
            f"{chr(ord('１') + self.file_to)}"
            f"{self.RankToKanjiLetters[self.rank_to]}"
            f"{self.piece_from.to_human_readable_string()}{"成" if self.promotion else "  "}"
        )

    def __eq__(self, other):
        # 比較関数
        if not isinstance(other, Move):
            return False
        return (
            self.file_from == other.file_from
            and self.rank_from == other.rank_from
            and self.piece_from == other.piece_from
            and self.file_to == other.file_to
            and self.rank_to == other.rank_to
            and self.piece_to == other.piece_to
            and self.drop == other.drop
            and self.promotion == other.promotion
            and self.side_to_move == other.side_to_move
        )

    def __hash__(self):
        # ハッシュ関数
        seed = 0
        seed ^= self.file_from + ((seed << 6) + (seed >> 2))
        seed ^= self.rank_from + ((seed << 6) + (seed >> 2))
        seed ^= hash(self.piece_from) + ((seed << 6) + (seed >> 2))
        seed ^= self.file_to + ((seed << 6) + (seed >> 2))
        seed ^= self.rank_to + ((seed << 6) + (seed >> 2))
        seed ^= hash(self.piece_to) + ((seed << 6) + (seed >> 2))
        seed ^= int(self.drop) + ((seed << 6) + (seed >> 2))
        seed ^= int(self.promotion) + ((seed << 6) + (seed >> 2))
        seed ^= hash(self.side_to_move) + ((seed << 6) + (seed >> 2))
        return seed

    def to_usi_string(self):
        if self == Move.Resign:
            return "resign"
        elif self == Move.Win:
            return "win"

        usi_string = ""
        if self.drop:
            usi_string += self.piece_from.to_char().upper()
            usi_string += "*"
        else:
            usi_string += chr(self.file_from + ord("1"))
            usi_string += chr(self.rank_from + ord("a"))

        usi_string += chr(self.file_to + ord("1"))
        usi_string += chr(self.rank_to + ord("a"))

        if self.promotion:
            usi_string += "+"

        return usi_string

    @staticmethod
    def from_usi_string(position, move_string):
        if move_string == "resign":
            return Move.Resign
        elif move_string == "win":
            return Move.Win
        elif move_string == "none":
            return Move.NoneMove

        move = Move(
            file_from=-1,
            rank_from=-1,
            piece_from=None,
            file_to=None,
            rank_to=None,
            piece_to=None,
        )
        if move_string[1] == "*":
            # 駒打ちの指し手
            move.file_from = -1
            move.rank_from = -1
            move.piece_from = Piece(CHAR_TO_PIECE[move_string[0]])
            if position.side_to_move == Color.WHITE:
                move.piece_from = move.piece_from.as_opponent_hand_piece()
            move.drop = True
        else:
            # 駒を移動する指し手
            move.file_from = ord(move_string[0]) - ord("1")
            move.rank_from = ord(move_string[1]) - ord("a")
            move.piece_from = position.board[move.file_from][move.rank_from]
            move.drop = False

        move.file_to = ord(move_string[2]) - ord("1")
        move.rank_to = ord(move_string[3]) - ord("a")
        move.piece_to = position.board[move.file_to][move.rank_to]

        move.promotion = len(move_string) == 5
        move.side_to_move = position.side_to_move
        return move


# 静的なインスタンス定義
Move.Resign = Move(file_from=2, file_to=2)
Move.Win = Move(file_from=3, file_to=3)
Move.NoneMove = Move(file_from=4, file_to=4)
