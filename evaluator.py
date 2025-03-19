from piece_types import Color, Piece


class Evaluator:
    PIECE_VALUES = {
        Piece.NO_PIECE: 0,
        Piece.BLACK_PAWN: 90,
        Piece.BLACK_LANCE: 315,
        Piece.BLACK_KNIGHT: 405,
        Piece.BLACK_SILVER: 495,
        Piece.BLACK_GOLD: 540,
        Piece.BLACK_BISHOP: 855,
        Piece.BLACK_ROOK: 945,
        Piece.BLACK_KING: 15000,
        Piece.BLACK_PROMOTED_PAWN: 540,
        Piece.BLACK_PROMOTED_LANCE: 540,
        Piece.BLACK_PROMOTED_KNIGHT: 540,
        Piece.BLACK_PROMOTED_SILVER: 540,
        Piece.BLACK_HORSE: 945,
        Piece.BLACK_DRAGON: 1395,
        Piece.WHITE_PAWN: -90,
        Piece.WHITE_LANCE: -315,
        Piece.WHITE_KNIGHT: -405,
        Piece.WHITE_SILVER: -495,
        Piece.WHITE_GOLD: -540,
        Piece.WHITE_BISHOP: -855,
        Piece.WHITE_ROOK: -945,
        Piece.WHITE_KING: -15000,
        Piece.WHITE_PROMOTED_PAWN: -540,
        Piece.WHITE_PROMOTED_LANCE: -540,
        Piece.WHITE_PROMOTED_KNIGHT: -540,
        Piece.WHITE_PROMOTED_SILVER: -540,
        Piece.WHITE_HORSE: -945,
        Piece.WHITE_DRAGON: -1395,
    }

    @staticmethod
    def evaluate(position):
        value = 0

        # 盤上の駒の評価値を合算
        for board_row in position.board:
            for piece in board_row:
                value += Evaluator.PIECE_VALUES[piece]

        # 持ち駒の評価値を合算
        for piece_type, num_piece in enumerate(position.hand_piece):
            value += Evaluator.PIECE_VALUES[Piece(piece_type)] * num_piece

        # 後手の場合は評価値を反転
        if position.side_to_move == Color.WHITE:
            value = -value

        return value
