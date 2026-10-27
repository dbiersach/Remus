#!/usr/bin/env -S uv run
"""station_match.py

Measure how much one enhancement station adds. A station's Remus plays a match
against Remus-WHITE (the finished Day 9 Remus with no enhancements), or against
another station, with python-chess as the referee. Every game is added to the class games file, games/remus_games.pgn
at the top of the Remus folder, and the script turns the score into an Elo gap.
This is a teacher tool: the engine itself never imports python-chess.

Usage:
    uv run station_match.py RED            Remus-RED against Remus-WHITE
    uv run station_match.py RED BLUE       Remus-RED against Remus-BLUE
    uv run station_match.py RED --games 20

Colors match the start of a station folder name, so "RED" finds
"RED - Transposition table".
"""

import argparse
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import chess
import chess.engine
import chess.pgn

STATIONS = Path(__file__).parent
# The top Remus folder is the one that holds pyproject.toml
REPOSITORY = next(
    (
        folder
        for folder in Path(__file__).parents
        if (folder / "pyproject.toml").exists()
    ),
    Path(__file__).parent,
)
GAMES_PATH = REPOSITORY / "games" / "remus_games.pgn"  # Every game any script plays
YARDSTICK = "WHITE"  # Remus-WHITE, with no enhancements, measures every station
MINUTES = 1.0  # Each side's clock
INCREMENT = 0.6  # Seconds added after each move
GAMES_AT_ONCE = 2  # Each game runs two engine processes


def find_player(color: str) -> tuple[str, Path]:
    """Return a player's name, such as "Remus-RED", and its station folder."""
    for folder in sorted(STATIONS.iterdir()):
        if folder.is_dir() and folder.name.upper().startswith(color.upper() + " "):
            return f"Remus-{folder.name.split(' - ')[0]}", folder
    sys.exit(f"No station folder starts with {color!r}")


def elo_gap(points: float, games: int) -> float:
    """
    Return the Elo gap that the Elo formula expects from a match score.

    Parameters
    ----------
    points : float
        The first player's points.
    games : int
        The games played.

    Returns
    -------
    float
        Positive when the first player is stronger. A score of 75 percent gives
        about +191. A perfect or a zero score counts as half a point short of it,
        so the gap stays a finite bound.
    """
    share = min(max(points, 0.5), games - 0.5) / games
    return -400 * math.log10(1 / share - 1)


def play_game(
    white: tuple[str, Path], black: tuple[str, Path], event: str
) -> chess.pgn.Game:
    """Play one game on a chess clock and return it as PGN, with the result set."""
    engines = [
        chess.engine.SimpleEngine.popen_uci(
            [sys.executable, str(folder / "uci_engine.py")], cwd=folder
        )
        for _, folder in (white, black)
    ]
    board = chess.Board()
    clocks = [MINUTES * 60, MINUTES * 60]  # Seconds left for White, then Black
    result, reason = None, ""
    try:
        while not board.is_game_over(claim_draw=True):
            side = 0 if board.turn == chess.WHITE else 1
            limit = chess.engine.Limit(
                white_clock=clocks[0],
                black_clock=clocks[1],
                white_inc=INCREMENT,
                black_inc=INCREMENT,
            )
            start = time.perf_counter()
            try:
                move = engines[side].play(board, limit).move
            except chess.engine.EngineError as error:
                move, reason = None, f"engine error: {error}"
            clocks[side] -= time.perf_counter() - start
            if move is None or move not in board.legal_moves:
                reason = reason or f"illegal move {move}"
            elif clocks[side] < 0:
                reason = "lost on time"
            else:
                board.push(move)
                clocks[side] += INCREMENT
                continue
            result = "0-1" if side == 0 else "1-0"  # The side to move loses
            break
    finally:
        for engine in engines:
            engine.quit()
    game = chess.pgn.Game.from_board(board)
    game.headers["Event"] = event
    game.headers["Date"] = date.today().strftime("%Y.%m.%d")
    game.headers["White"], game.headers["Black"] = white[0], black[0]
    game.headers["TimeControl"] = f"{MINUTES * 60:.0f}+{INCREMENT}"
    game.headers["Result"] = result or board.result(claim_draw=True)
    if reason:
        game.headers["Termination"] = reason
    return game


def main():
    parser = argparse.ArgumentParser(description="Measure an enhancement station.")
    parser.add_argument("first", help='a station color, such as "RED"')
    parser.add_argument("second", nargs="?", default=YARDSTICK)
    parser.add_argument("--games", type=int, default=20, help="games in the match")
    options = parser.parse_args()
    first = find_player(options.first)
    second = find_player(options.second)
    event = f"Station match {first[0]} vs {second[0]}"

    print(f"{event}: {options.games} games at {MINUTES:g} min + {INCREMENT} s")
    print(f"Adding every game to {GAMES_PATH}")
    GAMES_PATH.parent.mkdir(exist_ok=True)
    # The first player takes White in the even games and Black in the odd ones
    pairings = [
        (first, second) if number % 2 == 0 else (second, first)
        for number in range(options.games)
    ]
    points = 0.0
    start = time.perf_counter()
    with ThreadPoolExecutor(GAMES_AT_ONCE) as pool:
        jobs = [
            pool.submit(play_game, white, black, event) for white, black in pairings
        ]
        for number, job in enumerate(jobs, start=1):
            game = job.result()
            with GAMES_PATH.open("a") as file:
                print(game, end="\n\n", file=file)
            white_points = {"1-0": 1.0, "0-1": 0.0}.get(game.headers["Result"], 0.5)
            points += (
                white_points if game.headers["White"] == first[0] else 1 - white_points
            )
            ending = game.headers.get("Termination", "")
            print(
                f"  Game {number}: {game.headers['White']} vs {game.headers['Black']}: "
                f"{game.headers['Result']} {ending}"
            )
    print(f"{first[0]} scored {points:g} / {options.games} against {second[0]}")
    print(f"Elo gap: {elo_gap(points, options.games):+.0f} for {first[0]}")
    print(f"Total run time (sec): {time.perf_counter() - start:.3f}")


if __name__ == "__main__":
    main()
