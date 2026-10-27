#!/usr/bin/env -S uv run
"""play_match.py

Play a match between two Remus brains through UCI, with python-chess as the referee.
python-chess rejects any illegal move, so every match is also a rules test. Every
game is added to the class games file, games/remus_games.pgn at the top of the Remus
folder. This is a teacher tool: the engine itself never imports python-chess.

Usage: uv run play_match.py random greedy 20

Both players may use the same brain, such as "think think", for Remus against itself.
"""

import sys
from datetime import date
from pathlib import Path

import chess
import chess.engine
import chess.pgn

ENGINE_FILE = Path(__file__).parent / "uci_engine.py"  # The engine both players run
# The top Remus folder is the nearest folder above this one with pyproject.toml
REPOSITORY = Path(__file__).parent
for folder in Path(__file__).parents:
    if (folder / "pyproject.toml").exists():
        REPOSITORY = folder
        break
GAMES_PATH = REPOSITORY / "games" / "remus_games.pgn"  # Every game any script plays


def start_engine(brain: str) -> chess.engine.SimpleEngine:
    """Start one Remus process that plays with the named brain."""
    return chess.engine.SimpleEngine.popen_uci(
        [sys.executable, str(ENGINE_FILE), brain]
    )


def play_game(
    white: chess.engine.SimpleEngine, black: chess.engine.SimpleEngine
) -> chess.Board:
    """Play one game and return the board with every move on it."""
    board = chess.Board()
    while not board.is_game_over(claim_draw=True):
        engine = white if board.turn == chess.WHITE else black
        result = engine.play(board, chess.engine.Limit(time=1.0))
        if result.move is None:
            break  # The engine sent no move, so the game stops unfinished
        board.push(result.move)
    return board


def save_game(board: chess.Board, white: str, black: str) -> str:
    """Add one finished game to the class games file and return its result."""
    game = chess.pgn.Game.from_board(board)
    game.headers["Event"] = "Remus self-play match"
    game.headers["Date"] = date.today().strftime("%Y.%m.%d")
    game.headers["White"] = f"Remus {white}"
    game.headers["Black"] = f"Remus {black}"
    game.headers["Result"] = board.result(claim_draw=True)
    GAMES_PATH.parent.mkdir(exist_ok=True)
    with GAMES_PATH.open("a") as file:
        print(game, end="\n\n", file=file)
    return game.headers["Result"]


def main():
    first = sys.argv[1] if len(sys.argv) > 1 else "random"
    second = sys.argv[2] if len(sys.argv) > 2 else "greedy"
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    # Player 0 uses the first brain and player 1 the second, even when they match
    brains = [first, second]
    engines = [start_engine(first), start_engine(second)]
    points = [0.0, 0.0]
    print(f"Adding every game to {GAMES_PATH}")
    for number in range(games):
        white, black = (0, 1) if number % 2 == 0 else (1, 0)  # Take turns with White
        board = play_game(engines[white], engines[black])
        result = save_game(board, brains[white], brains[black])
        if result == "1-0":
            points[white] += 1
        elif result == "0-1":
            points[black] += 1
        else:
            points[white] += 0.5
            points[black] += 0.5
        print(f"Game {number + 1}: {brains[white]} vs {brains[black]}: {result}")
    for engine in engines:
        engine.quit()
    print(f"Final score: {first} {points[0]}, {second} {points[1]}")


if __name__ == "__main__":
    main()
