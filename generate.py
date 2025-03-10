from position import Position
from piece_types import Piece, Color
from move import Move


def is_pawn_exist(board, file, pawn) -> bool:
    for rank in range(Position.BOARD_SIZE):
        if board[file][rank] == pawn:
            return True
    return False


# 指し手生成関数
def generate(position):
    side_to_move = position.side_to_move
    board = position.board
    hand_pieces = position.hand_piece
    non_capture_promotion_moves = []
    non_capture_non_promotion_moves = []

    # 駒を移動する指し手
    for file_from in range(Position.BOARD_SIZE):
        for rank_from in range(Position.BOARD_SIZE):
            piece_from = board[file_from][rank_from]
            if piece_from == Piece.NO_PIECE:
                # 駒がないので何もしない
                continue
            if piece_from.to_color() != side_to_move:
                # 手番の駒でないので何もしない
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

                    piece_to = board[file_to][rank_to]
                    if (
                        piece_to != Piece.NO_PIECE
                        and piece_to.to_color() == side_to_move
                    ):
                        # 自分の駒があるので何もしない
                        break

                    # 成る指し手
                    if piece_from.can_promote() and (
                        (side_to_move == Color.BLACK and rank_to <= 2)
                        or (side_to_move == Color.WHITE and rank_to >= 6)
                        or (side_to_move == Color.BLACK and rank_from <= 2)
                        or (side_to_move == Color.WHITE and rank_from >= 6)
                    ):
                        move = Move(
                            file_from,
                            rank_from,
                            piece_from,
                            file_to,
                            rank_to,
                            piece_to,
                            False,
                            True,
                            side_to_move,
                        )

                        if move.piece_to != Piece.NO_PIECE:
                            # 駒を取る指し手
                            yield move
                        else:
                            # 駒を取らない指し手
                            non_capture_promotion_moves.append(move)

                    # 成らない指し手
                    if piece_from.can_put_without_promotion(rank_to):
                        move = Move(
                            file_from,
                            rank_from,
                            piece_from,
                            file_to,
                            rank_to,
                            piece_to,
                            False,
                            False,
                            side_to_move,
                        )

                        if move.piece_to != Piece.NO_PIECE:
                            # 駒を取る指し手
                            yield move
                        else:
                            # 駒を取らない指し手
                            non_capture_non_promotion_moves.append(move)

                    if piece_to != Piece.NO_PIECE:
                        # 相手の駒があるのでここで利きが止まる
                        break

    # 駒を取らない、成る指し手
    for move in non_capture_promotion_moves:
        yield move

    # 駒を取らない、成らない指し手
    for move in non_capture_non_promotion_moves:
        yield move

    # 駒を打つ指し手
    min_piece = Piece.BLACK_PAWN if side_to_move == Color.BLACK else Piece.WHITE_PAWN
    max_piece = Piece.BLACK_ROOK if side_to_move == Color.BLACK else Piece.WHITE_ROOK
    for piece_from_val in range(min_piece.value, max_piece.value + 1):
        if hand_pieces[piece_from_val] == 0:
            continue
        piece_from = Piece(piece_from_val)

        for file_to in range(Position.BOARD_SIZE):
            for rank_to in range(Position.BOARD_SIZE):
                if board[file_to][rank_to] != Piece.NO_PIECE:
                    continue

                if not piece_from.can_put_without_promotion(rank_to):
                    continue

                if (
                    piece_from == Piece.BLACK_PAWN or piece_from == Piece.WHITE_PAWN
                ) and is_pawn_exist(board, file_to, piece_from):
                    # 2歩
                    continue

                yield Move(
                    file_from=-1,
                    rank_from=-1,
                    piece_from=piece_from,
                    file_to=file_to,
                    rank_to=rank_to,
                    piece_to=Piece.NO_PIECE,
                    drop=True,
                    promotion=False,
                    side_to_move=side_to_move,
                )
