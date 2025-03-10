import sys
from position import Position
from generate import generate
from move import Move

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
                case "go":
                    moves = generate(position)
                    if not moves:
                        print("bestmove resign")
                        sys.stdout.flush()
                    else:
                        move = random.choice(list(moves))
                        print(f"bestmove {move.to_usi_string()}")
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
