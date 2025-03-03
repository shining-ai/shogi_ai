from piece_types import Color, Piece
from piece_types import PIECE_TO_STR, CHAR_TO_PIECE, NON_PROMOTED_TO_PROMOTED


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
        # 盤面初期化
        self.board = [
            [Piece.NO_PIECE.value] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)
        ]
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
                result.append(self.to_human_readable_string(piece).strip()[0])

        result.append(" , 後手 手駒: ")
        for piece in range(Piece.WHITE_PAWN.value, Piece.NUM_PIECES.value):
            for _ in range(self.hand_piece[piece]):
                result.append(self.to_human_readable_string(piece).strip()[0])

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

        count = 0
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

    def put_piece(self, file, rank, piece):
        assert (
            self.board[file][rank] == Piece.NO_PIECE.value
        )  # すでに駒がある場合はエラー
        self.board[file][rank] = piece

    def remove_piece(self, file, rank):
        assert self.board[file][rank] != Piece.NO_PIECE.value  # 駒がない場合はエラー
        self.board[file][rank] = Piece.NO_PIECE.value

    def put_hand_piece(self, piece):
        self.hand_piece[piece] += 1

    def remove_hand_piece(self, piece):
        assert self.hand_piece[piece] > 0
        self.hand_piece[piece] -= 1

    def do_move(self, move):
        assert self.side_to_move == move.side_to_move
        assert (
            move.drop or self.board[move.file_from][move.rank_from] == move.piece_from
        )
        assert move.drop or self.board[move.file_to][move.rank_to] == move.piece_to

        # 相手の駒を取る
        if move.piece_to != Piece.NO_PIECE.value:
            self.remove_piece(move.file_to, move.rank_to)
            self.hand_pieces.put_hand_piece(move.piece_to.as_opponent_hand_piece())

        if move.drop:
            # 持ち駒を打つ
            self.hand_pieces.remove_hand_piece(move.piece_from)
        else:
            # 盤面の駒を移動
            self.remove_piece(move.file_from, move.rank_from)

        # 駒を配置（成り判定）
        self.put_piece(
            move.file_to,
            move.rank_to,
            move.piece_from.as_promoted() if move.promotion else move.piece_from,
        )

        self.side_to_move = self.side_to_move.to_opponent()
        self.play += 1
        self.last_move = move

    def undo_move(self, move) -> None:
        """与えられた指し手に従い、局面を1手戻す"""
        assert self.side_to_move != move.side_to_move

        self.play -= 1
        self.side_to_move = self.side_to_move.to_opponent()
        self.remove_piece(move.file_to, move.rank_to)

        if move.drop:
            # 持ち駒を打った場合
            self.hand_pieces.put_hand_piece(move.piece_from)
        else:
            # 盤面の駒を戻す
            self.put_piece(move.file_from, move.rank_from, move.piece_from)

        # 取った駒を戻す
        if move.piece_to != Piece.NO_PIECE:
            self.hand_pieces.remove_hand_piece(move.piece_to.as_opponent_hand_piece())
            self.put_piece(move.file_to, move.rank_to, move.piece_to)
