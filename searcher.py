from move import Move
from generate import generate
from evaluator import Evaluator
from piece_types import Piece


class BestMove:
    def __init__(self, move, value):
        self.move = move
        self.value = value


class Searcher:
    @staticmethod
    def search(position, depth, nodes):
        if depth == 0:
            return BestMove(None, Evaluator.evaluate(position))

        best_value = float("-inf")
        best_move = Move.Resign

        # 合法手を列挙
        moves = list(generate(position))
        ok_moves = []
        for move in moves:
            position.do_move(move)
            if not position.is_in_checked(position.side_to_move.to_opponent()):
                ok_moves.append(move)
            position.undo_move(move)

        for move in moves:
            # 相手の玉を取る手なら、early return
            if move.piece_to in {Piece.BLACK_KING, Piece.WHITE_KING}:
                return BestMove(move, float("inf"))

            nodes += 1  # nodes をリストで渡してミュータブルに
            position.do_move(move)
            child_best_move = Searcher.search(position, depth - 1, nodes)
            position.undo_move(move)

            if best_value < -child_best_move.value:
                best_value = -child_best_move.value
                best_move = move

        return BestMove(best_move, best_value)
