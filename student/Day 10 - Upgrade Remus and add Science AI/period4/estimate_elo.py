#!/usr/bin/env -S uv run
"""estimate_elo.py

Measure the playing strength of Remus. Remus plays Stockfish set to a fixed
strength (UCI_Elo), level after level, and the script turns the results into an
estimated Elo rating. python-chess is the referee, as in tournament.py, and every
finished game is added at once to the class games file, games/remus_games.pgn at
the top of the Remus folder, so no game is ever lost.
This is a teacher tool: the engine itself never imports python-chess.

Usage: uv run estimate_elo.py [--games 10] [--levels 1320 1500 1700] [--stockfish PATH]

Stockfish calibrates UCI_Elo at 60 seconds plus 0.6 seconds a move, anchored to the
CCRL 40/4 rating list, so the games use that clock by default. Without --stockfish,
the script looks for "stockfish" on the PATH and then in En Croissant's engine folder.
"""

import argparse
import math
import os
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import chess
import chess.engine
import chess.pgn

ENGINE_FILE = Path(__file__).parent / "uci_engine.py"
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
EN_CROISSANT_ENGINES = (
    Path.home() / "AppData" / "Roaming" / "org.encroissant.app" / "engines"
)  # Where En Croissant keeps the Stockfish it downloads on Windows
LEVELS = [1320, 1500, 1700]  # Stockfish strengths to play; 1320 is its weakest
MINUTES = 1.0  # Each side's clock, the clock Stockfish calibrates UCI_Elo with
INCREMENT = 0.6  # Seconds added after each move
ELO_SCALE = 400 / math.log(10)  # Turns a rating gap into the logistic curve's units


def find_stockfish() -> str:
    """Return the path to a Stockfish program, or stop with a message."""
    on_path = shutil.which("stockfish") or shutil.which("/usr/games/stockfish")
    if on_path:
        return on_path
    if EN_CROISSANT_ENGINES.exists():
        for candidate in sorted(EN_CROISSANT_ENGINES.rglob("stockfish*.exe")):
            return str(candidate)
    sys.exit("No Stockfish found. Give its path with --stockfish PATH.")


def expected_score(rating: float, opponent: float) -> float:
    """Return the points per game the Elo formula expects for a player against an opponent."""
    return 1 / (1 + 10 ** ((opponent - rating) / 400))


def estimate_rating(results: list[tuple[int, float]]) -> tuple[float, float]:
    """
    Find the rating that best explains the results, and its uncertainty.

    Parameters
    ----------
    results : list[tuple[int, float]]
        One (Stockfish UCI_Elo, Remus points) pair per game, where points are
        1 for a win, 0.5 for a draw, and 0 for a loss.

    Returns
    -------
    tuple[float, float]
        The rating whose expected total score equals Remus's real total score,
        and the half-width of its 95 percent confidence interval. After a
        perfect score the rating is a bound: an upper bound after all losses, a
        lower bound after all wins.
    """
    # A perfect score (all losses or all wins) fits any rating far enough away, so
    # count it as half a point off perfect to get a bound instead
    points = sum(score for _, score in results)
    points = min(max(points, 0.5), len(results) - 0.5)
    # The expected total grows with the rating, so halving the range finds the match
    low, high = 0.0, 3500.0
    for _ in range(60):
        middle = (low + high) / 2
        expected = sum(expected_score(middle, elo) for elo, _ in results)
        if expected < points:
            low = middle
        else:
            high = middle
    rating = (low + high) / 2
    # Each game tells us more when its result was hard to predict (p near 0.5)
    information = sum(
        expected_score(rating, elo) * (1 - expected_score(rating, elo))
        for elo, _ in results
    )
    margin = 1.96 * ELO_SCALE / math.sqrt(information) if information > 0 else 0.0
    return rating, margin


def play_game(
    stockfish_path: str, stockfish_elo: int, remus_white: bool
) -> chess.pgn.Game:
    """Play Remus against Stockfish at one strength, and return the game as PGN."""
    remus = chess.engine.SimpleEngine.popen_uci([sys.executable, str(ENGINE_FILE)])
    stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    stockfish.configure({"UCI_LimitStrength": True, "UCI_Elo": stockfish_elo})
    engines = [remus, stockfish] if remus_white else [stockfish, remus]
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
        remus.quit()
        stockfish.quit()
    game = chess.pgn.Game.from_board(board)
    stockfish_name = f"Stockfish {stockfish_elo}"
    game.headers["Event"] = "Remus strength test"
    game.headers["Date"] = date.today().strftime("%Y.%m.%d")
    game.headers["White"] = "Remus" if remus_white else stockfish_name
    game.headers["Black"] = stockfish_name if remus_white else "Remus"
    game.headers["WhiteElo" if not remus_white else "BlackElo"] = str(stockfish_elo)
    game.headers["TimeControl"] = f"{MINUTES * 60:.0f}+{INCREMENT}"
    game.headers["Result"] = result or board.result(claim_draw=True)
    if reason:
        game.headers["Termination"] = reason
    return game


def remus_points(game: chess.pgn.Game) -> float:
    """Return Remus's points from one game: 1, 0.5, or 0."""
    white_points = {"1-0": 1.0, "0-1": 0.0}.get(game.headers["Result"], 0.5)
    return white_points if game.headers["White"] == "Remus" else 1 - white_points


def main():
    parser = argparse.ArgumentParser(description="Estimate the Elo rating of Remus.")
    parser.add_argument("--games", type=int, default=10, help="games at each level")
    parser.add_argument("--levels", type=int, nargs="+", default=LEVELS)
    parser.add_argument("--stockfish", default=None, help="path to Stockfish")
    options = parser.parse_args()
    stockfish_path = options.stockfish or find_stockfish()
    games_at_once = max(1, (os.cpu_count() or 2) // 2)  # Each game runs two engines

    print(f"Stockfish: {stockfish_path}")
    print(f"Adding every game to {GAMES_PATH}")
    GAMES_PATH.parent.mkdir(exist_ok=True)
    print(f"Clock: {MINUTES:g} minute(s) + {INCREMENT} seconds a move per side")
    results = []
    start = time.perf_counter()
    for elo in options.levels:
        colors = [number % 2 == 0 for number in range(options.games)]  # Take turns
        with ThreadPoolExecutor(games_at_once) as pool:
            jobs = [
                pool.submit(play_game, stockfish_path, elo, white) for white in colors
            ]
            level_points = 0.0
            for job in jobs:
                game = job.result()
                with GAMES_PATH.open("a") as file:
                    print(game, end="\n\n", file=file)
                points = remus_points(game)
                level_points += points
                results.append((elo, points))
                ending = game.headers.get("Termination", "")
                print(
                    f"  {game.headers['White']} vs {game.headers['Black']}: "
                    f"{game.headers['Result']} {ending}"
                )
        print(f"Against Stockfish {elo}: {level_points:g} / {options.games}")

    rating, margin = estimate_rating(results)
    points = sum(score for _, score in results)
    print(f"Remus scored {points:g} / {len(results)}")
    if points == 0:
        print(f"Estimated Elo: below {rating:.0f} (Remus lost every game)")
    elif points == len(results):
        print(f"Estimated Elo: above {rating:.0f} (Remus won every game)")
    else:
        print(f"Estimated Elo: {rating:.0f} +/- {margin:.0f} (95 percent)")
    print(f"Total run time (sec): {time.perf_counter() - start:.3f}")


if __name__ == "__main__":
    main()
