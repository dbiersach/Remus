#!/usr/bin/env -S uv run
"""play_match.py

Play a match between two Remus brains through UCI, with python-chess as the referee.
python-chess rejects any illegal move, so every match is also a rules test. This is a
teacher tool: the engine itself never imports python-chess.

Usage: uv run play_match.py random greedy 20
"""

import sys
from pathlib import Path

import chess
import chess.engine

ENGINE_FILE = Path(__file__).parent / "uci_engine.py"  # The engine both players run


def start_engine(brain: str) -> chess.engine.SimpleEngine:
    """Start one Remus process that plays with the named brain."""
    return chess.engine.SimpleEngine.popen_uci(
        [sys.executable, str(ENGINE_FILE), brain]
    )


def play_game(
    white: chess.engine.SimpleEngine, black: chess.engine.SimpleEngine
) -> str:
    """Play one game and return its result, such as "1-0"."""
    board = chess.Board()
    while not board.is_game_over(claim_draw=True):
        engine = white if board.turn == chess.WHITE else black
        result = engine.play(board, chess.engine.Limit(time=1.0))
        board.push(result.move)
    return board.result(claim_draw=True)


def main():
    first = sys.argv[1] if len(sys.argv) > 1 else "random"
    second = sys.argv[2] if len(sys.argv) > 2 else "greedy"
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    engines = {first: start_engine(first), second: start_engine(second)}
    points = {first: 0.0, second: 0.0}
    for number in range(games):
        white, black = (first, second) if number % 2 == 0 else (second, first)
        result = play_game(engines[white], engines[black])
        if result == "1-0":
            points[white] += 1
        elif result == "0-1":
            points[black] += 1
        else:
            points[white] += 0.5
            points[black] += 0.5
        print(f"Game {number + 1}: {white} vs {black}: {result}")
    for engine in engines.values():
        engine.quit()
    print(f"Final score: {first} {points[first]}, {second} {points[second]}")


if __name__ == "__main__":
    main()
