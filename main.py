import sys
from typing import Generator
from piece_types import PieceTypes, Piece, Color
from piece_types import PIECE_TO_STR, CHAR_TO_PIECE, NON_PROMOTED_TO_PROMOTED
from position import Position


def to_color(piece):
    """駒の色を判定する"""
    if piece == Piece.NO_PIECE:
        return None  # 無駄な計算を避ける
    return Color.BLACK if piece < 15 else Color.WHITE


class Move:
    RankToKanjiLetters = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
    ToHumanReadableString = ["☗", "☖"]
    # 静的インスタンス
    Resign = None
    Win = None
    NoneMove = None

    def __init__(
        self,
        file_from,
        rank_from=None,
        piece_from=None,
        file_to=None,
        rank_to=None,
        piece_to=None,
        drop=False,
        promotion=False,
        side_to_move=None,
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
            f"{self.ToHumanReadableString[self.side_to_move.value]} "
            f"{chr(ord('１') + self.file_to)}"
            f"{self.RankToKanjiLetters[self.rank_to]}"
            f"{PIECE_TO_STR[self.piece_from]}{"成" if self.promotion else "  "}"
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
            usi_string += self.piece_from.to_usi_char().upper()
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
            move.piece_from = CHAR_TO_PIECE[move_string[0]]
            if position.side_to_move == Color.White:
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


def can_promote(piece):
    return piece in NON_PROMOTED_TO_PROMOTED


def can_put_without_promotion(piece_from: Piece, rank_to: int) -> bool:
    return (
        (piece_from == Piece.BLACK_PAWN.value and rank_to >= 1)
        or (piece_from == Piece.BLACK_LANCE.value and rank_to >= 1)
        or (piece_from == Piece.BLACK_KNIGHT.value and rank_to >= 2)
        or (piece_from == Piece.WHITE_PAWN.value and rank_to <= 7)
        or (piece_from == Piece.WHITE_LANCE.value and rank_to <= 7)
        or (piece_from == Piece.WHITE_KNIGHT.value and rank_to <= 6)
        or (
            piece_from
            not in {
                Piece.BLACK_PAWN.value,
                Piece.BLACK_LANCE.value,
                Piece.BLACK_KNIGHT.value,
                Piece.WHITE_PAWN.value,
                Piece.WHITE_LANCE.value,
                Piece.WHITE_KNIGHT.value,
            }
        )
    )


def is_pawn_exist(board, file, pawn) -> bool:
    for rank in range(Position.BOARD_SIZE):
        if board[file][rank] == pawn:
            return True
    return False


# 指し手生成関数
def generate(position) -> Generator[Move, None, None]:
    side_to_move = position.side_to_move
    board = position.board
    hand_pieces = position.hand_piece
    non_capture_promotion_moves = []
    non_capture_non_promotion_moves = []

    # 駒を移動する指し手
    for file_from in range(Position.BOARD_SIZE):
        for rank_from in range(Position.BOARD_SIZE):
            piece_from = board[file_from][rank_from]
            if piece_from == Piece.NO_PIECE.value:
                continue
            if to_color(piece_from) != side_to_move:
                continue

            for move_direction in PieceTypes.MoveDirections[int(piece_from)]:
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
                        continue

                    piece_to = board[file_to][rank_to]
                    if (
                        piece_to != Piece.NO_PIECE.value
                        and to_color(piece_to) == side_to_move
                    ):
                        break

                    if can_promote(piece_from) and (
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

                        if move.piece_to != Piece.NO_PIECE.value:
                            yield move
                        else:
                            non_capture_promotion_moves.append(move)

                    if can_put_without_promotion(piece_from, rank_to):
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

                        if move.piece_to != Piece.NO_PIECE.value:
                            yield move
                        else:
                            non_capture_non_promotion_moves.append(move)

                    if piece_to != Piece.NO_PIECE.value:
                        break

    # 駒を取らない、成る指し手
    for move in non_capture_promotion_moves:
        yield move

    # 駒を取らない、成らない指し手
    for move in non_capture_non_promotion_moves:
        yield move

    # 駒を打つ指し手
    min_piece = (
        Piece.BLACK_PAWN.value
        if side_to_move == Color.BLACK
        else Piece.WHITE_PAWN.value
    )
    max_piece = (
        Piece.BLACK_ROOK.value
        if side_to_move == Color.BLACK
        else Piece.WHITE_ROOK.value
    )
    for piece_from in range(min_piece, max_piece + 1):
        if hand_pieces[piece_from] == 0:
            continue

        for file_to in range(Position.BOARD_SIZE):
            for rank_to in range(Position.BOARD_SIZE):
                if board[file_to][rank_to] != Piece.NO_PIECE.value:
                    continue

                if not can_put_without_promotion(piece_from, rank_to):
                    continue

                if (
                    piece_from == Piece.BLACK_PAWN or piece_from == Piece.WHITE_PAWN
                ) and is_pawn_exist(board, file_to, piece_from):
                    continue

                yield Move(
                    -1,
                    -1,
                    piece_from,
                    file_to,
                    rank_to,
                    Piece.NO_PIECE.value,
                    True,
                    False,
                    side_to_move,
                )


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
                    print(f"不正なコマンド: {line}")

                # 指し手を適用
                for move_string in line.split()[next_index:]:
                    if move_string == "moves":
                        continue
                    move = Move.from_usi_string(position, move_string)
                    position.do_move(move)

            case "generatemove":
                count = 0
                for move in generate(position):
                    print(move)
                    sys.stdout.flush()
                    count += 1
                print(f"合計 {count} 通り")
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
