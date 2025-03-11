from enum import Enum, unique


class Color(Enum):
    BLACK = 0
    WHITE = 1

    def to_opponent(self):
        return Color(1 - self.value)


@unique
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

    def is_black(self):
        return Piece.BLACK_PAWN.value <= self.value < Piece.WHITE_PAWN.value

    def is_white(self):
        return Piece.WHITE_PAWN.value <= self.value < Piece.NUM_PIECES.value

    def to_human_readable_string(self):
        readable_string = PIECE_TO_READABLE.get(self, None)
        assert readable_string is not None
        return readable_string

    def as_promoted(self):
        assert self != Piece.NO_PIECE
        return NON_PROMOTED_TO_PROMOTED.get(self, self)

    def to_char(self):
        assert self != Piece.NO_PIECE
        return PIECE_TO_CHAR.get(self, None)

    def as_opponent_hand_piece(self):
        assert self != Piece.NO_PIECE
        return PIECE_TO_OPPONENT_PIECE.get(self, None)

    def to_color(self):
        if self == Piece.NO_PIECE:
            return None
        return Color.BLACK if self.is_black() else Color.WHITE

    def move_directions(self):
        return PieceTypes.MoveDirections[self]

    def can_promote(self):
        return self in NON_PROMOTED_TO_PROMOTED

    def can_put_without_promotion(self, rank_to):
        return (
            (self == Piece.BLACK_PAWN and rank_to >= 1)
            or (self == Piece.BLACK_LANCE and rank_to >= 1)
            or (self == Piece.BLACK_KNIGHT and rank_to >= 2)
            or (self == Piece.WHITE_PAWN and rank_to <= 7)
            or (self == Piece.WHITE_LANCE and rank_to <= 7)
            or (self == Piece.WHITE_KNIGHT and rank_to <= 6)
            or (
                self
                not in {
                    Piece.BLACK_PAWN,
                    Piece.BLACK_LANCE,
                    Piece.BLACK_KNIGHT,
                    Piece.WHITE_PAWN,
                    Piece.WHITE_LANCE,
                    Piece.WHITE_KNIGHT,
                }
            )
        )


PIECE_TO_READABLE = {
    Piece.NO_PIECE: "    ",
    Piece.BLACK_PAWN: " 歩 ",
    Piece.BLACK_LANCE: " 香 ",
    Piece.BLACK_KNIGHT: " 桂 ",
    Piece.BLACK_SILVER: " 銀 ",
    Piece.BLACK_GOLD: " 金 ",
    Piece.BLACK_BISHOP: " 角 ",
    Piece.BLACK_ROOK: " 飛 ",
    Piece.BLACK_KING: " 王 ",
    Piece.BLACK_PROMOTED_PAWN: " と ",
    Piece.BLACK_PROMOTED_LANCE: " 杏 ",
    Piece.BLACK_PROMOTED_KNIGHT: " 圭 ",
    Piece.BLACK_PROMOTED_SILVER: " 全 ",
    Piece.BLACK_HORSE: " 馬 ",
    Piece.BLACK_DRAGON: " 龍 ",
    Piece.WHITE_PAWN: " 歩↓",
    Piece.WHITE_LANCE: " 香↓",
    Piece.WHITE_KNIGHT: " 桂↓",
    Piece.WHITE_SILVER: " 銀↓",
    Piece.WHITE_GOLD: " 金↓",
    Piece.WHITE_BISHOP: " 角↓",
    Piece.WHITE_ROOK: " 飛↓",
    Piece.WHITE_KING: " 王↓",
    Piece.WHITE_PROMOTED_PAWN: " と↓",
    Piece.WHITE_PROMOTED_LANCE: " 杏↓",
    Piece.WHITE_PROMOTED_KNIGHT: " 圭↓",
    Piece.WHITE_PROMOTED_SILVER: " 全↓",
    Piece.WHITE_HORSE: " 馬↓",
    Piece.WHITE_DRAGON: " 龍↓",
}


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

PIECE_TO_CHAR = {
    Piece.BLACK_KING: "K",
    Piece.WHITE_KING: "k",
    Piece.BLACK_ROOK: "R",
    Piece.WHITE_ROOK: "r",
    Piece.BLACK_BISHOP: "B",
    Piece.WHITE_BISHOP: "b",
    Piece.BLACK_GOLD: "G",
    Piece.WHITE_GOLD: "g",
    Piece.BLACK_SILVER: "S",
    Piece.WHITE_SILVER: "s",
    Piece.BLACK_KNIGHT: "N",
    Piece.WHITE_KNIGHT: "n",
    Piece.BLACK_LANCE: "L",
    Piece.WHITE_LANCE: "l",
    Piece.BLACK_PAWN: "P",
    Piece.WHITE_PAWN: "p",
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

PIECE_TO_OPPONENT_PIECE = {
    Piece.BLACK_PAWN: Piece.WHITE_PAWN,
    Piece.BLACK_LANCE: Piece.WHITE_LANCE,
    Piece.BLACK_KNIGHT: Piece.WHITE_KNIGHT,
    Piece.BLACK_SILVER: Piece.WHITE_SILVER,
    Piece.BLACK_GOLD: Piece.WHITE_GOLD,
    Piece.BLACK_BISHOP: Piece.WHITE_BISHOP,
    Piece.BLACK_ROOK: Piece.WHITE_ROOK,
    Piece.BLACK_KING: Piece.WHITE_KING,
    Piece.BLACK_PROMOTED_PAWN: Piece.WHITE_PAWN,
    Piece.BLACK_PROMOTED_LANCE: Piece.WHITE_LANCE,
    Piece.BLACK_PROMOTED_KNIGHT: Piece.WHITE_KNIGHT,
    Piece.BLACK_PROMOTED_SILVER: Piece.WHITE_SILVER,
    Piece.BLACK_HORSE: Piece.WHITE_BISHOP,
    Piece.BLACK_DRAGON: Piece.WHITE_ROOK,
    Piece.WHITE_PAWN: Piece.BLACK_PAWN,
    Piece.WHITE_LANCE: Piece.BLACK_LANCE,
    Piece.WHITE_KNIGHT: Piece.BLACK_KNIGHT,
    Piece.WHITE_SILVER: Piece.BLACK_SILVER,
    Piece.WHITE_GOLD: Piece.BLACK_GOLD,
    Piece.WHITE_BISHOP: Piece.BLACK_BISHOP,
    Piece.WHITE_ROOK: Piece.BLACK_ROOK,
    Piece.WHITE_KING: Piece.BLACK_KING,
    Piece.WHITE_PROMOTED_PAWN: Piece.BLACK_PAWN,
    Piece.WHITE_PROMOTED_LANCE: Piece.BLACK_LANCE,
    Piece.WHITE_PROMOTED_KNIGHT: Piece.BLACK_KNIGHT,
    Piece.WHITE_PROMOTED_SILVER: Piece.BLACK_SILVER,
    Piece.WHITE_HORSE: Piece.BLACK_BISHOP,
    Piece.WHITE_DRAGON: Piece.BLACK_ROOK,
}


class MoveDirection:
    def __init__(self, direction, is_long=False):
        self.direction = direction
        self.is_long = is_long


class Direction:
    def __init__(self, delta_file, delta_rank):
        self.delta_file = delta_file
        self.delta_rank = delta_rank


class PieceTypes:
    UP_LEFT = Direction(1, -1)
    UP = Direction(0, -1)
    UP_RIGHT = Direction(-1, -1)
    LEFT = Direction(1, 0)
    RIGHT = Direction(-1, 0)
    DOWN_LEFT = Direction(1, 1)
    DOWN = Direction(0, 1)
    DOWN_RIGHT = Direction(-1, 1)
    MOVE_BLACK_GOLD = [
        MoveDirection(UP_LEFT),
        MoveDirection(UP),
        MoveDirection(UP_RIGHT),
        MoveDirection(LEFT),
        MoveDirection(RIGHT),
        MoveDirection(DOWN),
    ]
    MOVE_WHITE_GOLD = [
        MoveDirection(DOWN_LEFT),
        MoveDirection(DOWN),
        MoveDirection(DOWN_RIGHT),
        MoveDirection(LEFT),
        MoveDirection(RIGHT),
        MoveDirection(UP),
    ]

    MoveDirections = {
        Piece.NO_PIECE: None,
        Piece.BLACK_PAWN: [MoveDirection(UP)],
        Piece.BLACK_LANCE: [MoveDirection(UP, True)],
        Piece.BLACK_KNIGHT: [
            MoveDirection(Direction(-1, -2)),
            MoveDirection(Direction(1, -2)),
        ],
        Piece.BLACK_SILVER: [
            MoveDirection(UP_LEFT),
            MoveDirection(UP),
            MoveDirection(UP_RIGHT),
            MoveDirection(DOWN_LEFT),
            MoveDirection(DOWN_RIGHT),
        ],
        Piece.BLACK_GOLD: MOVE_BLACK_GOLD,
        Piece.BLACK_BISHOP: [
            MoveDirection(UP_LEFT, True),
            MoveDirection(UP_RIGHT, True),
            MoveDirection(DOWN_LEFT, True),
            MoveDirection(DOWN_RIGHT, True),
        ],
        Piece.BLACK_ROOK: [
            MoveDirection(UP, True),
            MoveDirection(LEFT, True),
            MoveDirection(RIGHT, True),
            MoveDirection(DOWN, True),
        ],
        Piece.BLACK_KING: [
            MoveDirection(UP_LEFT),
            MoveDirection(UP),
            MoveDirection(UP_RIGHT),
            MoveDirection(LEFT),
            MoveDirection(RIGHT),
            MoveDirection(DOWN_LEFT),
            MoveDirection(DOWN),
            MoveDirection(DOWN_RIGHT),
        ],
        Piece.BLACK_PROMOTED_PAWN: MOVE_BLACK_GOLD,
        Piece.BLACK_PROMOTED_LANCE: MOVE_BLACK_GOLD,
        Piece.BLACK_PROMOTED_KNIGHT: MOVE_BLACK_GOLD,
        Piece.BLACK_PROMOTED_SILVER: MOVE_BLACK_GOLD,
        Piece.BLACK_HORSE: [
            MoveDirection(UP_LEFT, True),
            MoveDirection(UP),
            MoveDirection(UP_RIGHT, True),
            MoveDirection(LEFT),
            MoveDirection(RIGHT),
            MoveDirection(DOWN_LEFT, True),
            MoveDirection(DOWN),
            MoveDirection(DOWN_RIGHT, True),
        ],
        Piece.BLACK_DRAGON: [
            MoveDirection(UP_LEFT),
            MoveDirection(UP, True),
            MoveDirection(UP_RIGHT),
            MoveDirection(LEFT, True),
            MoveDirection(RIGHT, True),
            MoveDirection(DOWN_LEFT),
            MoveDirection(DOWN, True),
            MoveDirection(DOWN_RIGHT),
        ],
        Piece.WHITE_PAWN: [MoveDirection(DOWN)],
        Piece.WHITE_LANCE: [MoveDirection(DOWN, True)],
        Piece.WHITE_KNIGHT: [
            MoveDirection(Direction(1, 2)),
            MoveDirection(Direction(-1, 2)),
        ],
        Piece.WHITE_SILVER: [
            MoveDirection(UP_LEFT),
            MoveDirection(UP),
            MoveDirection(UP_RIGHT),
            MoveDirection(DOWN_LEFT),
            MoveDirection(DOWN_RIGHT),
        ],
        Piece.WHITE_GOLD: MOVE_WHITE_GOLD,
        Piece.WHITE_BISHOP: [
            MoveDirection(UP_LEFT, True),
            MoveDirection(UP_RIGHT, True),
            MoveDirection(DOWN_LEFT, True),
            MoveDirection(DOWN_RIGHT, True),
        ],
        Piece.WHITE_ROOK: [
            MoveDirection(UP, True),
            MoveDirection(LEFT, True),
            MoveDirection(RIGHT, True),
            MoveDirection(DOWN, True),
        ],
        Piece.WHITE_KING: [
            MoveDirection(UP_LEFT),
            MoveDirection(UP),
            MoveDirection(UP_RIGHT),
            MoveDirection(LEFT),
            MoveDirection(RIGHT),
            MoveDirection(DOWN_LEFT),
            MoveDirection(DOWN),
            MoveDirection(DOWN_RIGHT),
        ],
        Piece.WHITE_PROMOTED_PAWN: MOVE_WHITE_GOLD,
        Piece.WHITE_PROMOTED_LANCE: MOVE_WHITE_GOLD,
        Piece.WHITE_PROMOTED_KNIGHT: MOVE_WHITE_GOLD,
        Piece.WHITE_PROMOTED_SILVER: MOVE_WHITE_GOLD,
        Piece.WHITE_HORSE: [
            MoveDirection(UP_LEFT, True),
            MoveDirection(UP),
            MoveDirection(UP_RIGHT, True),
            MoveDirection(LEFT),
            MoveDirection(RIGHT),
            MoveDirection(DOWN_LEFT, True),
            MoveDirection(DOWN),
            MoveDirection(DOWN_RIGHT, True),
        ],
        Piece.WHITE_DRAGON: [
            MoveDirection(UP_LEFT),
            MoveDirection(UP, True),
            MoveDirection(UP_RIGHT),
            MoveDirection(LEFT, True),
            MoveDirection(RIGHT, True),
            MoveDirection(DOWN_LEFT),
            MoveDirection(DOWN, True),
            MoveDirection(DOWN_RIGHT),
        ],
    }
