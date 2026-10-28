#!/usr/bin/env -S uv run
"""station_elo.py

Rate every Remus version against Stockfish: Remus-WHITE, the ten color stations,
and Remus-GOLD.

Each version plays Stockfish at five strengths (UCI_Elo), from Stockfish's weakest
setting, 1320, up to 2500. At every strength a version plays 6 games, 3 as White
and 3 as Black, on a 10 minute clock. The script then finds each version's Elo
rating the way estimate_elo.py does, adds every game to games/remus_games.pgn, and
writes the table of ratings to docs/station_elo.md.

Before the first game, the script copies every station folder into a temporary
folder and runs the engines from that copy. A change to the station code during
the hours the games take then cannot change a version halfway through its games.

Remus is pure Python, so it plays weaker when it shares a processor core. Each
game needs about one core, because only one engine of a game thinks at a time:
keep --workers at or below the number of physical cores.

Usage:
    uv run station_elo.py --workers 16          all 12 versions, 360 games
    uv run station_elo.py --colors WHITE GOLD   only some versions
    uv run station_elo.py --report-only         only the ratings, from saved games
    uv run station_elo.py --niram               the same for Niram, in Rust

With --niram the games use Niram, the Rust copies of the same 12 versions in the
niram folder, which choose the same moves as Remus about 50 times faster. Build
them first with "cargo build --release" inside niram. Niram games are rated apart
from Remus games.

A game already in the games file is not played twice, so a run that stops
partway, such as when the computer restarts, picks up where it stopped.
This is a teacher tool: the engine itself never imports python-chess.
"""

import argparse
import math
import os
import shutil
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import chess
import chess.engine
import chess.pgn
from station_match import Player, all_players, engine_command

# The top Remus folder is the nearest folder above this one with pyproject.toml
REPOSITORY = Path(__file__).parent
for folder in Path(__file__).parents:
    if (folder / "pyproject.toml").exists():
        REPOSITORY = folder
        break
GAMES_PATH = REPOSITORY / "games" / "remus_games.pgn"  # Every game any script plays
REPORT_PATH = REPOSITORY / "docs" / "station_elo.md"  # The table of ratings
LUCAS_CHESS_ENGINES = (
    Path.home() / "AppData" / "Local" / "Programs" / "LucasChessR" / "bin" / "OS"
)  # Where Lucas Chess keeps the Stockfish it installs on Windows
EVENT = "Station Elo test"  # The Event header of every game this script plays
LEVELS = [1320, 1615, 1910, 2205, 2500]  # Stockfish strengths; 1320 is its weakest
GAMES_PER_LEVEL = 6  # Half with Remus as White, half with Remus as Black
MINUTES = 10.0  # Each side's clock
INCREMENT = 0.0  # Seconds added after each move
# Milliseconds Stockfish keeps in reserve on every move. The referee times each move
# from outside, and with many games running at once its own bookkeeping adds a few
# hundred milliseconds that Stockfish cannot see on its clock.
STOCKFISH_OVERHEAD = 1000
ELO_SCALE = 400 / math.log(10)  # Turns a rating gap into the logistic curve's units

Job = tuple[Player, int, int]  # (player, Stockfish UCI_Elo, game number at that level)


def freeze(players: list[Player]) -> list[Player]:
    """Copy every player's program into a new temporary folder and return the copies."""
    frozen_root = Path(tempfile.mkdtemp(prefix="remus_frozen_"))
    frozen = []
    for name, program in players:
        copy = frozen_root / program.name
        if program.is_file():
            shutil.copy2(program, copy)
        else:
            shutil.copytree(
                program, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pgn")
            )
        frozen.append((name, copy))
    print(f"Frozen copies of {len(frozen)} versions in {frozen_root}")
    return frozen


def find_stockfish() -> str:
    """Return the path to a Stockfish program, or stop with a message."""
    on_path = shutil.which("stockfish") or shutil.which("/usr/games/stockfish")
    if on_path:
        return on_path
    if LUCAS_CHESS_ENGINES.exists():
        for candidate in sorted(LUCAS_CHESS_ENGINES.rglob("stockfish*.exe")):
            return str(candidate)
    sys.exit("No Stockfish found. Give its path with --stockfish PATH.")


def expected_score(rating: float, opponent: float) -> float:
    """Return the points per game the Elo formula expects for the first player."""
    return 1 / (1 + 10 ** ((opponent - rating) / 400))


def estimate_rating(results: list[tuple[int, float]]) -> tuple[float, float]:
    """
    Find the rating that best explains the results, and its uncertainty.

    Parameters
    ----------
    results : list[tuple[int, float]]
        One (Stockfish UCI_Elo, Remus points) pair per game.

    Returns
    -------
    tuple[float, float]
        The rating whose expected total score equals the real total score, and
        the half-width of its 95 percent confidence interval. A perfect score
        counts as half a point short of perfect, so the rating stays a bound.
    """
    points = 0.0
    for _, score in results:
        points += score
    points = min(max(points, 0.5), len(results) - 0.5)
    # The expected total grows with the rating, so halving the range finds the match
    low, high = 0.0, 3500.0
    for _ in range(60):
        middle = (low + high) / 2
        expected = 0.0
        for elo, _ in results:
            expected += expected_score(middle, elo)
        if expected < points:
            low = middle
        else:
            high = middle
    rating = (low + high) / 2
    # A game tells us the most when its result was hard to predict (p near 0.5)
    information = 0.0
    for elo, _ in results:
        chance = expected_score(rating, elo)
        information += chance * (1 - chance)
    margin = 1.96 * ELO_SCALE / math.sqrt(information) if information > 0 else 0.0
    return rating, margin


def game_round(elo: int, number: int) -> str:
    """Return the Round header that names one game, such as "1615.4"."""
    return f"{elo}.{number}"


def play_game(player: Player, stockfish_path: str, elo: int, number: int):
    """
    Play one game of a Remus version against Stockfish and return it as PGN.

    Parameters
    ----------
    player : Player
        The Remus or Niram version's name and its frozen program.
    stockfish_path : str
        The Stockfish program.
    elo : int
        Stockfish's strength, its UCI_Elo.
    number : int
        The game number at this strength, from 1. Remus takes White in the odd games.
    """
    name, program = player
    remus_white = number % 2 == 1
    command, folder = engine_command(program)
    remus = chess.engine.SimpleEngine.popen_uci(command, cwd=folder)
    stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    stockfish.configure(
        {
            "Threads": 1,
            "Move Overhead": STOCKFISH_OVERHEAD,
            "UCI_LimitStrength": True,
            "UCI_Elo": elo,
        }
    )
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
    stockfish_name = f"Stockfish {elo}"
    game.headers["Event"] = EVENT
    game.headers["Date"] = date.today().strftime("%Y.%m.%d")
    game.headers["Round"] = game_round(elo, number)
    game.headers["White"] = name if remus_white else stockfish_name
    game.headers["Black"] = stockfish_name if remus_white else name
    game.headers["BlackElo" if remus_white else "WhiteElo"] = str(elo)
    game.headers["TimeControl"] = f"{MINUTES * 60:.0f}+{INCREMENT:g}"
    game.headers["Result"] = result or board.result(claim_draw=True)
    if reason:
        game.headers["Termination"] = reason
    return game


def read_results(engine: str = "Remus") -> dict[str, dict[int, list[float]]]:
    """
    Return every saved game of this script as points by version and level.

    The answer looks like {"Remus-RED": {1320: [1.0, 0.5, ...], ...}, ...}.
    Only the versions of one engine, "Remus" or "Niram", count.
    """
    results = {}
    if not GAMES_PATH.exists():
        return results
    points = {"1-0": 1.0, "0-1": 0.0, "1/2-1/2": 0.5}
    with GAMES_PATH.open() as file:
        while (headers := chess.pgn.read_headers(file)) is not None:
            if headers.get("Event") != EVENT or headers.get("Result") not in points:
                continue
            white_points = points[headers["Result"]]
            if headers["Black"].startswith("Stockfish"):
                name, remus_points = headers["White"], white_points
            else:
                name, remus_points = headers["Black"], 1 - white_points
            if not name.startswith(engine + "-"):
                continue
            elo = int(headers["Round"].split(".")[0])
            results.setdefault(name, {}).setdefault(elo, []).append(remus_points)
    return results


def played_games() -> set[tuple[str, str]]:
    """Return (version, Round) for every game of this script in the games file."""
    played = set()
    if not GAMES_PATH.exists():
        return played
    with GAMES_PATH.open() as file:
        while (headers := chess.pgn.read_headers(file)) is not None:
            if headers.get("Event") == EVENT:
                remus = headers["White"]
                if remus.startswith("Stockfish"):
                    remus = headers["Black"]
                played.add((remus, headers.get("Round", "")))
    return played


def play_all(players: list[Player], stockfish_path: str, workers: int) -> None:
    """Play every game not yet in the games file, workers games at a time."""
    played = played_games()
    # Game 1 of every version and level first, then game 2, and so on, so the
    # results stay balanced if the run stops partway
    jobs: list[Job] = []
    for number in range(1, GAMES_PER_LEVEL + 1):
        for elo in LEVELS:
            for player in players:
                if (player[0], game_round(elo, number)) not in played:
                    jobs.append((player, elo, number))
    total = len(players) * len(LEVELS) * GAMES_PER_LEVEL
    print(
        f"{total} games at {MINUTES:g} min + {INCREMENT:g} s, "
        f"{total - len(jobs)} already played, {workers} at a time"
    )
    print(f"Adding every game to {GAMES_PATH}")
    GAMES_PATH.parent.mkdir(exist_ok=True)
    frozen = dict(zip(players, freeze(players), strict=True))
    start = time.perf_counter()
    with ThreadPoolExecutor(workers) as pool:
        futures = []
        for player, elo, number in jobs:
            futures.append(
                pool.submit(play_game, frozen[player], stockfish_path, elo, number)
            )
        for done, future in enumerate(futures, start=1):
            game = future.result()
            with GAMES_PATH.open("a") as file:
                print(game, end="\n\n", file=file)
            minutes = (time.perf_counter() - start) / 60
            print(
                f"  [{done}/{len(jobs)}, {minutes:.0f} min] {game.headers['White']} "
                f"vs {game.headers['Black']}: {game.headers['Result']} "
                f"{game.headers.get('Termination', '')}",
                flush=True,
            )


def write_report(results: dict[str, dict[int, list[float]]]) -> str:
    """Return the Markdown table of every version's rating and score at each level."""
    rated = []
    for name, by_level in results.items():
        games = []
        for elo in by_level:
            for points in by_level[elo]:
                games.append((elo, points))
        rating, margin = estimate_rating(games)
        rated.append((rating, margin, name, by_level, games))
    rated.sort(reverse=True)
    head = "| Rank | Version | Elo | 95% margin | Score |"
    rule = "| ---: | --- | ---: | ---: | ---: |"
    for elo in LEVELS:
        head += f" SF {elo} |"
        rule += " :---: |"
    report = head + "\n" + rule + "\n"
    for rank, (rating, margin, name, by_level, games) in enumerate(rated, start=1):
        points = 0.0
        for _, score in games:
            points += score
        cells = ""
        for elo in LEVELS:
            scores = by_level.get(elo, [])
            if scores:
                cells += f" {sum(scores):g}/{len(scores)} |"
            else:
                cells += " - |"
        if points == 0:
            elo_text = f"below {rating:.0f}"
        elif points == len(games):
            elo_text = f"above {rating:.0f}"
        else:
            elo_text = f"{rating:.0f}"
        report += (
            f"| {rank} | {name} | {elo_text} | +/- {margin:.0f} | "
            f"{points:g}/{len(games)} |" + cells + "\n"
        )
    return report.rstrip("\n")


def main():
    parser = argparse.ArgumentParser(description="Rate every Remus version.")
    parser.add_argument("--colors", nargs="+", help="only these versions, like RED")
    parser.add_argument(
        "--workers", type=int, default=max(1, (os.cpu_count() or 2) // 2)
    )
    parser.add_argument("--stockfish", default=None, help="path to Stockfish")
    parser.add_argument("--report-only", action="store_true", help="skip the games")
    parser.add_argument(
        "--niram", action="store_true", help="play the Rust versions in niram/"
    )
    options = parser.parse_args()
    start = time.perf_counter()
    engine = "Niram" if options.niram else "Remus"
    players = all_players(engine)
    if options.colors:
        wanted = []
        for color in options.colors:
            wanted.append(f"{engine}-{color.upper()}")
        chosen = []
        for player in players:
            if player[0] in wanted:
                chosen.append(player)
        players = chosen
    if not options.report_only:
        stockfish_path = options.stockfish or find_stockfish()
        print(f"Stockfish: {stockfish_path}")
        play_all(players, stockfish_path, options.workers)
    table = write_report(read_results(engine))
    print(table)
    print(f"Total run time (sec): {time.perf_counter() - start:.3f}")


if __name__ == "__main__":
    main()
