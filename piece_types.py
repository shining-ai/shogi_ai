from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1

    def to_opponent(self):
        return Color(1 - self.value)


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
    Piece.BLACK_PAWN.value: Piece.BLACK_PROMOTED_PAWN,
    Piece.BLACK_LANCE.value: Piece.BLACK_PROMOTED_LANCE,
    Piece.BLACK_KNIGHT.value: Piece.BLACK_PROMOTED_KNIGHT,
    Piece.BLACK_SILVER.value: Piece.BLACK_PROMOTED_SILVER,
    Piece.BLACK_BISHOP.value: Piece.BLACK_HORSE,
    Piece.BLACK_ROOK.value: Piece.BLACK_DRAGON,
    Piece.WHITE_PAWN.value: Piece.WHITE_PROMOTED_PAWN,
    Piece.WHITE_LANCE.value: Piece.WHITE_PROMOTED_LANCE,
    Piece.WHITE_KNIGHT.value: Piece.WHITE_PROMOTED_KNIGHT,
    Piece.WHITE_SILVER.value: Piece.WHITE_PROMOTED_SILVER,
    Piece.WHITE_BISHOP.value: Piece.WHITE_HORSE,
    Piece.WHITE_ROOK.value: Piece.WHITE_DRAGON,
}

PIECE_TO_OPPONENT_HANDPIECE = [
    Piece.NO_PIECE,
    Piece.WHITE_PAWN,
    Piece.WHITE_LANCE,
    Piece.WHITE_KNIGHT,
    Piece.WHITE_SILVER,
    Piece.WHITE_GOLD,
    Piece.WHITE_BISHOP,
    Piece.WHITE_ROOK,
    Piece.NO_PIECE,
    Piece.WHITE_PAWN,
    Piece.WHITE_LANCE,
    Piece.WHITE_KNIGHT,
    Piece.WHITE_SILVER,
    Piece.WHITE_BISHOP,
    Piece.WHITE_ROOK,
    Piece.BLACK_PAWN,
    Piece.BLACK_LANCE,
    Piece.BLACK_KNIGHT,
    Piece.BLACK_SILVER,
    Piece.BLACK_GOLD,
    Piece.BLACK_BISHOP,
    Piece.BLACK_ROOK,
    Piece.NO_PIECE,
    Piece.BLACK_PAWN,
    Piece.BLACK_LANCE,
    Piece.BLACK_KNIGHT,
    Piece.BLACK_SILVER,
    Piece.BLACK_BISHOP,
    Piece.BLACK_ROOK,
    Piece.NUM_PIECES,
]


class MoveDirection:
    def __init__(self, direction, is_long=False):
        self.direction = direction
        self.is_long = is_long


class Direction:
    def __init__(self, delta_file, delta_rank):
        self.delta_file = delta_file
        self.delta_rank = delta_rank


class PieceTypes:
    UpLeft = Direction(1, -1)
    Up = Direction(0, -1)
    UpRight = Direction(-1, -1)
    Left = Direction(1, 0)
    Right = Direction(-1, 0)
    DownLeft = Direction(1, 1)
    Down = Direction(0, 1)
    DownRight = Direction(-1, 1)

    MoveDirections = [
        # NoPiece
        None,
        # BlackPawn
        [
            MoveDirection(Up),
        ],
        # BlackLance
        [
            MoveDirection(Up, True),
        ],
        # BlackKnight
        [
            MoveDirection(Direction(-1, -2)),
            MoveDirection(Direction(1, -2)),
        ],
        # BlackSilver
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(DownLeft),
            MoveDirection(DownRight),
        ],
        # BlackGold
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(Down),
        ],
        # BlackBishop
        [
            MoveDirection(UpLeft, True),
            MoveDirection(UpRight, True),
            MoveDirection(DownLeft, True),
            MoveDirection(DownRight, True),
        ],
        # BlackRook
        [
            MoveDirection(Up, True),
            MoveDirection(Left, True),
            MoveDirection(Right, True),
            MoveDirection(Down, True),
        ],
        # BlackKing
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # BlackPromotedPawn
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(Down),
        ],
        # BlackPromotedLance
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(Down),
        ],
        # BlackPromotedKnight
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(Down),
        ],
        # BlackPromotedSilver
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(Down),
        ],
        # BlackHorse
        [
            MoveDirection(UpLeft, True),
            MoveDirection(Up),
            MoveDirection(UpRight, True),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft, True),
            MoveDirection(Down),
            MoveDirection(DownRight, True),
        ],
        # BlackDragon
        [
            MoveDirection(UpLeft),
            MoveDirection(Up, True),
            MoveDirection(UpRight),
            MoveDirection(Left, True),
            MoveDirection(Right, True),
            MoveDirection(DownLeft),
            MoveDirection(Down, True),
            MoveDirection(DownRight),
        ],
        # WhitePawn
        [
            MoveDirection(Down),
        ],
        # WhiteLance
        [
            MoveDirection(Down, True),
        ],
        # WhiteKnight
        [
            MoveDirection(Direction(1, 2)),
            MoveDirection(Direction(-1, 2)),
        ],
        # WhiteSilver
        [
            MoveDirection(UpLeft),
            MoveDirection(UpRight),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # WhiteGold
        [
            MoveDirection(Up),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # WhiteBishop
        [
            MoveDirection(UpLeft, True),
            MoveDirection(UpRight, True),
            MoveDirection(DownLeft, True),
            MoveDirection(DownRight, True),
        ],
        # WhiteRook
        [
            MoveDirection(Up, True),
            MoveDirection(Left, True),
            MoveDirection(Right, True),
            MoveDirection(Down, True),
        ],
        # WhiteKing
        [
            MoveDirection(UpLeft),
            MoveDirection(Up),
            MoveDirection(UpRight),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # WhitePromotedPawn
        [
            MoveDirection(Up),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # WhitePromotedLance
        [
            MoveDirection(Up),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # WhitePromotedKnight
        [
            MoveDirection(Up),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # WhitePromotedSilver
        [
            MoveDirection(Up),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft),
            MoveDirection(Down),
            MoveDirection(DownRight),
        ],
        # WhiteHorse
        [
            MoveDirection(UpLeft, True),
            MoveDirection(Up),
            MoveDirection(UpRight, True),
            MoveDirection(Left),
            MoveDirection(Right),
            MoveDirection(DownLeft, True),
            MoveDirection(Down),
            MoveDirection(DownRight, True),
        ],
        # WhiteDragon
        [
            MoveDirection(UpLeft),
            MoveDirection(Up, True),
            MoveDirection(UpRight),
            MoveDirection(Left, True),
            MoveDirection(Right, True),
            MoveDirection(DownLeft),
            MoveDirection(Down, True),
            MoveDirection(DownRight),
        ],
        # NumPieces
        None,
    ]
