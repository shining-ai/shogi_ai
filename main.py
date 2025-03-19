import sys
from position import Position
from generate import generate
from move import Move
from evaluator import Evaluator
import time
from searcher import Searcher

import random
import traceback


def main():
    position = Position()
    while True:
        try:
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
                case "okmove":
                    moves = list(generate(position))
                    ok_moves = []
                    for move in moves:
                        position.do_move(move)
                        if not position.is_in_checked(
                            position.side_to_move.to_opponent()
                        ):
                            ok_moves.append(move)
                        position.undo_move(move)
                    for move in ok_moves:
                        print(move)
                case "go":
                    depth = 3
                    begin_time = time.time()
                    nodes = 0
                    best_move = Searcher.search(position, depth, nodes)
                    end_time = time.time()
                    time_diff = end_time - begin_time
                    best_move_string = best_move.move.to_usi_string()
                    score_cp = best_move.value
                    nps = nodes / time_diff
                    print(
                        f"info score cp {score_cp} nodes {nodes} nps {nps} time {time_diff} pv {best_move_string}"
                    )
                    if best_move.value < -30000:
                        print("bestmove resign")
                    else:
                        print(f"bestmove {best_move_string}")
                    sys.stdout.flush()
                case "eval":
                    print(Evaluator.evaluate(position))
                case "check":
                    print(position.is_in_checked())
                    sys.stdout.flush()
                case "quit":
                    break
                case "d":
                    print(position)
                    sys.stdout.flush()

        except Exception as e:
            print(f"例外が発生しました: {e}")
            print(traceback.format_exc())
            print("bestmove resign")  # とりあえず投了してエンジンが落ちないようにする


if __name__ == "__main__":
    main()
