from piece_types import Color, Piece
from piece_types import CHAR_TO_PIECE


class Position:
    start_position_sfen = (
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1"
    )
    BOARD_SIZE = 9  # 盤面の一辺のマス数

    def __init__(self):
        self.side_to_move = Color.BLACK  # 初期手番は先手
        # 盤面初期化
        self.board = [
            [Piece.NO_PIECE] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)
        ]
        self.hand_piece = [0] * Piece.NUM_PIECES.value  # 持ち駒の初期化
        self.play = 1  # 初期手数
        self.black_king_file = 0
        self.black_king_rank = 0
        self.white_king_file = 0
        self.white_king_rank = 0

    def __str__(self):
        result = []

        # ボードの状態を表示
        result.append("+----+----+----+----+----+----+----+----+----+\n")
        for rank in range(self.BOARD_SIZE):
            result.append("|")
            for file in range(self.BOARD_SIZE - 1, -1, -1):
                result.append(self.board[file][rank].to_human_readable_string())
                result.append("|")
            result.append("\n")
            result.append("+----+----+----+----+----+----+----+----+----+\n")

        # 持ち駒の状態を表示
        result.append("先手 手駒: ")
        for piece_value in range(Piece.BLACK_PAWN.value, Piece.WHITE_PAWN.value):
            for _ in range(self.hand_piece[piece_value]):
                result.append(Piece(piece_value).to_human_readable_string().strip()[0])

        result.append(" , 後手 手駒: ")
        for piece_value in range(Piece.WHITE_PAWN.value, Piece.NUM_PIECES.value):
            for _ in range(self.hand_piece[piece_value]):
                result.append(Piece(piece_value).to_human_readable_string().strip()[0])

        result.append("\n")

        # 手番を表示
        result.append(
            f"手番 = {'先手' if self.side_to_move == Color.BLACK else '後手'}\n"
        )
        return "".join(result)

    def set_position(self, sfen):
        self.side_to_move = Color.BLACK
        self.board = [
            [Piece.NO_PIECE] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)
        ]
        self.hand_piece = [0] * Piece.NUM_PIECES.value  # 持ち駒の初期化
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
                    self.board[file][rank] = Piece.NO_PIECE
                    file -= 1
            else:
                piece = CHAR_TO_PIECE.get(c, None)
                assert piece is not None
                if promotion:
                    piece = piece.as_promoted()
                    promotion = False
                self.board[file][rank] = piece

                if piece == Piece.BLACK_KING:
                    self.black_king_file = file
                    self.black_king_rank = rank
                elif piece == Piece.WHITE_KING:
                    self.white_king_file = file
                    self.white_king_rank = rank

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
            piece = CHAR_TO_PIECE.get(c, None)
            assert piece is not None
            self.hand_piece[piece.value] = max(1, count)
            count = 0

        # 手数のパース
        index += 1
        self.play = int(sfen[index:])

    def put_piece(self, file: int, rank: int, piece: Piece) -> None:
        assert self.board[file][rank] == Piece.NO_PIECE  # すでに駒がある場合はエラー
        self.board[file][rank] = piece

    def remove_piece(self, file: int, rank: int) -> None:
        assert self.board[file][rank] != Piece.NO_PIECE  # 駒がない場合はエラー
        self.board[file][rank] = Piece.NO_PIECE

    def put_hand_piece(self, piece: Piece) -> None:
        # 持ち駒に駒を加える
        self.hand_piece[piece.value] += 1

    def remove_hand_piece(self, piece: Piece) -> None:
        # 持ち駒から駒を取り除く
        assert self.hand_piece[piece.value] > 0
        self.hand_piece[piece.value] -= 1

    def do_move(self, move):
        """与えられた指し手に従い、局面を1手進める"""
        assert self.side_to_move == move.side_to_move
        assert (
            move.drop or self.board[move.file_from][move.rank_from] == move.piece_from
        )
        assert move.drop or self.board[move.file_to][move.rank_to] == move.piece_to

        # 相手の駒を取る
        if move.piece_to != Piece.NO_PIECE:
            self.remove_piece(move.file_to, move.rank_to)
            self.put_hand_piece(move.piece_to.as_opponent_hand_piece())

        if move.drop:
            # 持ち駒を打つ
            self.remove_hand_piece(move.piece_from)
        else:
            # 盤面の駒を移動
            self.remove_piece(move.file_from, move.rank_from)

        # 駒を配置（成り判定）
        self.put_piece(
            move.file_to,
            move.rank_to,
            move.piece_from.as_promoted() if move.promotion else move.piece_from,
        )

        if move.piece_from == Piece.BLACK_KING:
            self.black_king_file = move.file_to
            self.black_king_rank = move.rank_to
        if move.piece_from == Piece.WHITE_KING:
            self.white_king_file = move.file_to
            self.white_king_rank = move.rank_to

        self.side_to_move = self.side_to_move.to_opponent()
        self.play += 1
        self.last_move = move

    def undo_move(self, move) -> None:
        """与えられた指し手に従い、局面を1手戻す"""
        assert self.side_to_move != move.side_to_move

        self.play -= 1
        self.side_to_move = self.side_to_move.to_opponent()

        if move.piece_from == Piece.BLACK_KING:
            self.black_king_file = move.file_from
            self.black_king_rank = move.rank_from
        if move.piece_from == Piece.WHITE_KING:
            self.white_king_file = move.file_from
            self.white_king_rank = move.rank_from

        self.remove_piece(move.file_to, move.rank_to)

        if move.drop:
            # 持ち駒を打った場合
            self.put_hand_piece(move.piece_from)
        else:
            # 盤面の駒を戻す
            self.put_piece(move.file_from, move.rank_from, move.piece_from)

        # 取った駒を戻す
        if move.piece_to != Piece.NO_PIECE:
            self.remove_hand_piece(move.piece_to.as_opponent_hand_piece())
            self.put_piece(move.file_to, move.rank_to, move.piece_to)

    def is_in_checked(self, color) -> bool:
        """指定した手番の王が王手されているかどうかを返す"""
        king = Piece.BLACK_KING if color == Color.BLACK else Piece.WHITE_KING
        for file_from in range(self.BOARD_SIZE):
            for rank_from in range(self.BOARD_SIZE):
                piece_from = self.board[file_from][rank_from]
                if piece_from == Piece.NO_PIECE:
                    # 駒がない場合はスキップ
                    continue
                if piece_from.to_color() == color:
                    # 自分の駒の場合はスキップ
                    continue
                for move_direction in piece_from.move_directions():
                    max_distance = 8 if move_direction.is_long else 1
                    file_to = file_from
                    rank_to = rank_from
                    for distance in range(max_distance):
                        file_to += move_direction.direction.delta_file
                        rank_to += move_direction.direction.delta_rank
                        if not (
                            0 <= file_to < Position.BOARD_SIZE
                            and 0 <= rank_to < Position.BOARD_SIZE
                        ):
                            # 盤外に出たので何もしない
                            continue

                        piece_to = self.board[file_to][rank_to]
                        if piece_to == king:
                            return True
                        if piece_to != Piece.NO_PIECE:
                            # 王以外の駒がある
                            break
        return False
