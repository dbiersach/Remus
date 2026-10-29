#!/usr/bin/env -S uv run
"""version_elo.py

Rate every Remus version against Stockfish: Remus-WHITE, the ten color versions,
and Remus-GOLD.

Each version plays Stockfish at four strengths (UCI_Elo) near the strength where
Remus scores about half the points, because a game against a Stockfish that
always wins, or always loses, says almost nothing about a rating: 1650, 1800,
1950, and 2100. At every strength a version plays 12 games, 6 as White and 6 as
Black, on a 10 minute clock. The script then finds each version's Elo rating the
way estimate_elo.py does, adds every game to misc/games/remus_games.pgn, and
prints the table that misc/docs/engines/engines_elo.md reports.

With --niram-gold, Niram, the Rust copy of Remus-GOLD that chooses the same
moves about 50 times faster, plays too, at 2000, 2200, 2400, and 2600. Build it
first with "cargo build --release" inside its folder. Its games are rated apart
from the Remus games.

Before the first game, the script copies every version folder into a temporary
folder and runs the engines from that copy. A change to the color version code during
the hours the games take then cannot change a version halfway through its games.

Remus is pure Python, so it plays weaker when it shares a processor core. Each
game needs about one core, because only one engine of a game thinks at a time:
keep --workers at or below the number of physical cores.

Usage:
    uv run misc/scripts/version_elo.py --workers 20         all 12 versions, 576 games
    uv run misc/scripts/version_elo.py --niram-gold         Niram too, 48 more
    uv run misc/scripts/version_elo.py --colors WHITE GOLD  only some versions
    uv run misc/scripts/version_elo.py --levels 1800 2000   other Stockfish strengths
    uv run misc/scripts/version_elo.py --games 2            fewer games per strength
    uv run misc/scripts/version_elo.py --report-only        only the ratings, saved games

A game already in the games file is not played twice, so a run that stops
partway, such as when the computer restarts, picks up where it stopped.
This is a course designer tool: the engine itself never imports python-chess.
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

# version_match.py lives beside the Remus versions in engines/instructor
ENGINES = Path(__file__).parent.parent.parent / "engines"
sys.path.insert(0, str(ENGINES / "instructor"))

from version_match import Player, all_players

# The top Remus folder is the nearest folder above this one with pyproject.toml
REPOSITORY = Path(__file__).parent
for folder in Path(__file__).parents:
    if (folder / "pyproject.toml").exists():
        REPOSITORY = folder
        break
# Every game any script plays goes into one file
GAMES_PATH = REPOSITORY / "misc" / "games" / "remus_games.pgn"
# Niram's program, which cargo builds inside engines/Niram
NIRAM_GOLD = ENGINES / "Niram"
NIRAM_GOLD_PROGRAM = NIRAM_GOLD / "target" / "release" / "niram"
if sys.platform == "win32":
    NIRAM_GOLD_PROGRAM = NIRAM_GOLD_PROGRAM.with_suffix(".exe")
LUCAS_CHESS_ENGINES = (
    Path.home() / "AppData" / "Local" / "Programs" / "LucasChessR" / "bin" / "OS"
)  # Where Lucas Chess keeps the Stockfish it installs on Windows
EVENT = "Engine Elo test"  # The Event header of every game this script plays
# Stockfish strengths for each engine, close to where each engine scores half
LEVELS = {"Remus": [1650, 1800, 1950, 2100], "Niram": [2000, 2200, 2400, 2600]}
GAMES_PER_LEVEL = 12  # Half with the version as White, half as Black
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
                program,
                copy,
                ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "engines"),
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
        The interval comes from how far each game's real score landed from its
        expected score, so a version that draws often gets a narrower interval
        than one that only wins and loses.
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
    # A game tells us the most when its result was hard to predict (p near 0.5):
    # the expected total score then changes fastest as the rating changes
    slope = 0.0
    spread = 0.0
    for elo, score in results:
        chance = expected_score(rating, elo)
        slope += chance * (1 - chance) / ELO_SCALE
        spread += (score - chance) ** 2
    if slope == 0 or spread == 0:
        return rating, 0.0
    margin = 1.96 * math.sqrt(spread) / slope
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
    # Niram is one program file; a Remus version is a folder of Python
    if program.is_file():
        command, folder = [str(program)], program.parent
    else:
        command, folder = [sys.executable, str(program / "uci_engine.py")], program
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


def engine_of(name: str) -> str:
    """Return "Remus" or "Niram", the engine part of a name like "Niram-GOLD"."""
    return name.split("-")[0]


def play_all(
    players: list[Player], games_per_level: int, stockfish_path: str, workers: int
) -> None:
    """Play every game not yet in the games file, workers games at a time."""
    played = played_games()
    # Game 1 of every version and level first, then game 2, and so on, so the
    # results stay balanced if the run stops partway
    jobs: list[Job] = []
    total = 0
    for number in range(1, games_per_level + 1):
        for player in players:
            for elo in LEVELS[engine_of(player[0])]:
                total += 1
                if (player[0], game_round(elo, number)) not in played:
                    jobs.append((player, elo, number))
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
    levels = []
    for by_level in results.values():
        for elo in by_level:
            if elo not in levels:
                levels.append(elo)
    levels.sort()
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
    for elo in levels:
        head += f" SF {elo} |"
        rule += " :---: |"
    report = head + "\n" + rule + "\n"
    for rank, (rating, margin, name, by_level, games) in enumerate(rated, start=1):
        points = 0.0
        for _, score in games:
            points += score
        cells = ""
        for elo in levels:
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
    parser.add_argument("--niram-gold", action="store_true", help="play Niram too")
    parser.add_argument(
        "--levels", type=int, nargs="+", help="Stockfish strengths, like 1800 2000"
    )
    parser.add_argument(
        "--games", type=int, default=GAMES_PER_LEVEL, help="games per strength"
    )
    options = parser.parse_args()
    start = time.perf_counter()
    if options.levels:
        LEVELS["Remus"] = options.levels
        LEVELS["Niram"] = options.levels
    wanted = []
    for color in options.colors or []:
        wanted.append(color.upper())
    players = []
    for player in all_players():
        if not wanted or player[0].split("-")[1] in wanted:
            players.append(player)
    if options.niram_gold:
        if not options.report_only and not NIRAM_GOLD_PROGRAM.exists():
            sys.exit(f"No {NIRAM_GOLD_PROGRAM}: run 'cargo build --release' first")
        # The games file names Niram "Niram-GOLD", so its saved games still count
        players.append(("Niram-GOLD", NIRAM_GOLD_PROGRAM))
    if not options.report_only:
        stockfish_path = options.stockfish or find_stockfish()
        print(f"Stockfish: {stockfish_path}")
        play_all(players, options.games, stockfish_path, options.workers)
    for engine in ["Remus", "Niram"]:
        results = read_results(engine)
        if not results:
            continue
        print(f"{engine} versions against Stockfish")
        print(write_report(results))
        # Every game of the engine's versions, rated as if one player played them
        pooled = []
        for by_level in results.values():
            for elo in by_level:
                for points in by_level[elo]:
                    pooled.append((elo, points))
        rating, margin = estimate_rating(pooled)
        print(f"All {len(pooled)} {engine} games: {rating:.0f} +/- {margin:.0f}")
    print(f"Total run time (sec): {time.perf_counter() - start:.3f}")


if __name__ == "__main__":
    main()
