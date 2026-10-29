#!/usr/bin/env -S uv run
"""version_match.py

Measure how much one color version adds. A color version's Remus plays a match
against Remus-WHITE (the finished Day 9 Remus with no enhancements, in the period1
folder of Day 9, on the same instructor or student side as this file), or against another color version, with python-chess as the referee. Every game is added to the class
games file, misc/games/remus_games.pgn at the top of the Remus folder, and the script
turns the score into an Elo gap. This is a teacher tool: the engine itself never
imports python-chess.

Remus picks the same move every time it sees the same position, so two games from
the starting position would be the same game twice. Each pair of games therefore
starts from one of the OPENINGS, three moves deep, and each player takes White once.

Pairs never type a command: smoke_test.py and play_battle.py in each color folder
run this file with the Run button. The course designer may also run it by hand:
    uv run version_match.py RED            Remus-RED against Remus-WHITE, 2 games
    uv run version_match.py RED BLUE       Remus-RED against Remus-BLUE
    uv run version_match.py RED --games 1 --minutes 2
                                           one short game, to check the engine runs
    uv run version_match.py RED GOLD       Remus-RED against Remus-GOLD

Each side gets 10 minutes, because Remus searches only a few thousand positions a
second and a shorter clock stops every version too shallow for most enhancements
to help. The two games run at once, so the match takes about 20 minutes.

A color names a version folder, so "RED" finds "10 RED - Transposition table".
The number in front ranks the color versions by the teacher's league. "WHITE"
finds the period1 folder of Day 9, and "GOLD" finds the Remus-GOLD folder
beside this file.
"""

import argparse
import asyncio
import math
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import chess
import chess.engine
import chess.pgn

REMUS_FOLDER = Path(__file__).parent
# The top Remus folder is the nearest folder above this one with pyproject.toml
REPOSITORY = Path(__file__).parent
for folder in Path(__file__).parents:
    if (folder / "pyproject.toml").exists():
        REPOSITORY = folder
        break
# Every game any script plays
GAMES_PATH = REPOSITORY / "misc" / "games" / "remus_games.pgn"
YARDSTICK = "WHITE"  # Remus-WHITE, with no enhancements, measures every color version
MINUTES = 10.0  # Each side's clock
INCREMENT = 0.0  # Seconds added after each move
GAMES_AT_ONCE = 2  # Each game runs two engine processes
# What engines print to stderr
ERRORS_PATH = REPOSITORY / "misc" / "games" / "engine_errors.log"
SILENCE_GRACE = 10.0  # Seconds past its clock an engine may take before it forfeits
# Remus-WHITE, the Day 9 engine: period1/instructor or period1/student, the same side
WHITE_FOLDER = REMUS_FOLDER.parent.parent.parent / "period1" / REMUS_FOLDER.parent.name
GOLD_FOLDER = (
    REMUS_FOLDER / "Remus-GOLD"
)  # The finished Remus, with all ten enhancements
# Well-known openings, three moves for each side, in UCI notation
OPENINGS = [
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6",  # Ruy Lopez
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6",  # Queen's Gambit Declined
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4",  # Sicilian
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7",  # King's Indian
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4",  # French
    "c2c4 e7e5 b1c3 g8f6 g1f3 b8c6",  # English
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4",  # Caro-Kann
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4",  # Nimzo-Indian
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5",  # Italian
    "g1f3 d7d5 g2g3 g8f6 f1g2 e7e6",  # Reti
    "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4",  # Scotch
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6",  # Slav
    "e2e4 c7c5 g1f3 b8c6 d2d4 c5d4",  # Sicilian, with Nc6
    "d2d4 g8f6 c2c4 g7g6 b1c3 d7d5",  # Grunfeld
    "e2e4 d7d6 d2d4 g8f6 b1c3 g7g6",  # Pirc
    "d2d4 d7d5 c2c4 d5c4 g1f3 g8f6",  # Queen's Gambit Accepted
    "e2e4 e7e5 g1f3 g8f6 f3e5 d7d6",  # Petrov
    "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6",  # Queen's Indian
    "e2e4 g8f6 e4e5 f6d5 d2d4 d7d6",  # Alekhine
    "d2d4 f7f5 g2g3 g8f6 f1g2 g7g6",  # Dutch
    "e2e4 d7d5 e4d5 d8d5 b1c3 d5a5",  # Scandinavian
    "d2d4 d7d5 g1f3 g8f6 c1f4 e7e6",  # London
    "e2e4 c7c5 c2c3 g8f6 e4e5 f6d5",  # Sicilian, Alapin
    "c2c4 c7c5 g1f3 g8f6 b1c3 b8c6",  # Symmetrical English
    "e2e4 e7e5 b1c3 g8f6 f2f4 d7d5",  # Vienna
    "d2d4 g8f6 c2c4 c7c5 d4d5 e7e6",  # Benoni
    "e2e4 e7e6 d2d4 d7d5 e4e5 c7c5",  # French, advance
    "e2e4 c7c6 d2d4 d7d5 e4e5 c8f5",  # Caro-Kann, advance
    "e2e4 e7e5 f2f4 e5f4 g1f3 g7g5",  # King's Gambit
    "e2e4 c7c5 b1c3 b8c6 g2g3 g7g6",  # Closed Sicilian
    "g1f3 g8f6 c2c4 g7g6 b2b3 f8g7",  # Reti, double fianchetto
    "e2e4 e7e5 g1f3 b8c6 b1c3 g8f6",  # Four Knights
]

Player = tuple[str, Path]  # A version's name, such as "Remus-RED", and its program


def version_color(folder_name: str) -> str:
    """Return the color in a version folder's name: "RED" from "10 RED - Transposition table"."""
    words = folder_name.split(" - ")[0].split()
    return words[len(words) - 1].upper()


def all_players() -> list[Player]:
    """
    Return the name and folder of every Remus version, WHITE first and GOLD last.

    Returns
    -------
    list[Player]
        Each version's name, such as "Remus-RED", and its folder.
    """
    players = [(f"Remus-{YARDSTICK}", WHITE_FOLDER)]
    for folder in sorted(REMUS_FOLDER.iterdir()):
        if folder.is_dir() and " - " in folder.name:
            players.append((f"Remus-{version_color(folder.name)}", folder))
    if GOLD_FOLDER.is_dir():
        players.append(("Remus-GOLD", GOLD_FOLDER))
    return players


def find_player(color: str) -> Player:
    """Return one version's name, such as "Remus-RED", and its folder."""
    for player in all_players():
        if player[0] == f"Remus-{color.upper()}":
            return player
    sys.exit(f"No Remus version has the color {color!r}")


def engine_command(program: Path) -> tuple[list[str], Path]:
    """Return the command that starts a version, and the folder it runs in."""
    return [sys.executable, str(program / "uci_engine.py")], program


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


def time_control(minutes: float, increment: float) -> str:
    """Return the PGN TimeControl text, such as "600+0" for 10 minutes a side."""
    return f"{minutes * 60:.0f}+{increment:g}"


def ask_for_move(
    engine: chess.engine.SimpleEngine,
    board: chess.Board,
    limit: chess.engine.Limit,
    seconds: float,
) -> chess.Move | None:
    """
    Ask an engine for its move, and stop waiting after a number of seconds.

    Parameters
    ----------
    engine : chess.engine.SimpleEngine
        The engine to move.
    board : chess.Board
        The position.
    limit : chess.engine.Limit
        The clocks the engine sees.
    seconds : float
        How long to wait for the answer.

    Returns
    -------
    chess.Move | None
        The engine's move, or None if no "bestmove" arrived in time. A clock alone
        never ends python-chess's wait, so an engine that stops answering would
        otherwise hold up the whole match.
    """
    waiting = asyncio.wait_for(engine.protocol.play(board, limit), seconds)
    future = asyncio.run_coroutine_threadsafe(waiting, engine.protocol.loop)
    try:
        return future.result().move
    except TimeoutError:
        return None


def save_engine_errors(game: chess.pgn.Game, names: list[str], logs: list) -> None:
    """Copy anything the two engines printed to stderr into ERRORS_PATH."""
    for name, log in zip(names, logs, strict=True):
        log.seek(0)
        text = log.read().decode(errors="replace").strip()
        if not text:
            continue
        headers = game.headers
        with ERRORS_PATH.open("a") as file:
            print(
                f"{name} in {headers['White']} vs {headers['Black']}, "
                f"{headers['Event']}, {headers.get('StartMoves', '')}, "
                f"after {len(game.end().board().move_stack)} plies:\n{text}\n",
                file=file,
            )
        print(f"  {name} wrote to stderr; see {ERRORS_PATH}", flush=True)


def referee(
    white: Player,
    black: Player,
    opening: str,
    minutes: float,
    increment: float,
    logs: list,
) -> tuple[chess.Board, str | None, str]:
    """
    Start both engines, play the game on a chess clock, and stop the engines.

    Parameters
    ----------
    white, black, opening, minutes, increment
        The same as for play_game().
    logs : list
        Two open files that receive what the White and Black engines print to
        stderr.

    Returns
    -------
    tuple[chess.Board, str | None, str]
        The final board, the result if a side lost by forfeit (else None), and
        the reason for the forfeit (else "").
    """
    engines = []
    for side in range(2):  # 0 is White, 1 is Black
        command, folder = engine_command((white, black)[side][1])
        engines.append(
            chess.engine.SimpleEngine.popen_uci(command, cwd=folder, stderr=logs[side])
        )
    board = chess.Board()
    for text in opening.split():
        board.push_uci(text)
    clocks = [minutes * 60, minutes * 60]  # Seconds left for White, then Black
    result, reason = None, ""
    try:
        while not board.is_game_over(claim_draw=True):
            side = 0 if board.turn == chess.WHITE else 1
            limit = chess.engine.Limit(
                white_clock=clocks[0],
                black_clock=clocks[1],
                white_inc=increment,
                black_inc=increment,
            )
            start = time.perf_counter()
            try:
                move = ask_for_move(
                    engines[side], board, limit, clocks[side] + SILENCE_GRACE
                )
                if move is None:
                    reason = "engine sent no move"
            except chess.engine.EngineError as error:
                move, reason = None, f"engine error: {error}"
            clocks[side] -= time.perf_counter() - start
            if move is None or move not in board.legal_moves:
                reason = reason or f"illegal move {move}"
            elif clocks[side] < 0:
                reason = "lost on time"
            else:
                board.push(move)
                clocks[side] += increment
                continue
            result = "0-1" if side == 0 else "1-0"  # The side to move loses
            break
    finally:
        for engine in engines:
            try:
                engine.quit()
            except TimeoutError:
                engine.close()  # The engine ignored "quit", so end its process
    return board, result, reason


def play_game(
    white: Player,
    black: Player,
    event: str,
    opening: str = "",
    minutes: float = MINUTES,
    increment: float = INCREMENT,
) -> chess.pgn.Game:
    """
    Play one game on a chess clock and return it as PGN, with the result set.

    Parameters
    ----------
    white, black : Player
        Each player's name and program, from find_player().
    event : str
        The Event header of the game.
    opening : str
        Moves in UCI notation, such as "e2e4 e7e5", played before the engines
        start thinking.
    minutes : float
        Each side's clock at the start of the game.
    increment : float
        Seconds added to a side's clock after each of its moves.
    """
    # Each engine's stderr goes to a temporary file, kept only if it holds text
    with tempfile.TemporaryFile() as white_log, tempfile.TemporaryFile() as black_log:
        logs = [white_log, black_log]
        board, result, reason = referee(white, black, opening, minutes, increment, logs)
        game = chess.pgn.Game.from_board(board)
        game.headers["Event"] = event
        game.headers["Date"] = date.today().strftime("%Y.%m.%d")
        game.headers["White"], game.headers["Black"] = white[0], black[0]
        game.headers["TimeControl"] = time_control(minutes, increment)
        game.headers["Result"] = result or board.result(claim_draw=True)
        if reason:
            game.headers["Termination"] = reason
        if opening:
            game.headers["StartMoves"] = opening  # The opening the engines started from
        save_engine_errors(game, [white[0], black[0]], logs)
    return game


def main():
    parser = argparse.ArgumentParser(description="Measure a color version.")
    parser.add_argument("first", help='a color, such as "RED"')
    parser.add_argument("second", nargs="?", default=YARDSTICK)
    parser.add_argument("--games", type=int, default=2, help="games in the match")
    parser.add_argument("--minutes", type=float, default=MINUTES, help="each clock")
    parser.add_argument(
        "--increment", type=float, default=INCREMENT, help="seconds added per move"
    )
    options = parser.parse_args()
    clock = (options.minutes, options.increment)
    first = find_player(options.first)
    second = find_player(options.second)
    event = f"Station match {first[0]} vs {second[0]}"

    print(
        f"{event}: {options.games} games at {options.minutes:g} min + "
        f"{options.increment:g} s"
    )
    print(f"Adding every game to {GAMES_PATH}")
    GAMES_PATH.parent.mkdir(exist_ok=True)
    # Games 0 and 1 share an opening, and the first player takes White in game 0
    pairings = []
    for number in range(options.games):
        if number % 2 == 0:
            pairings.append((first, second))
        else:
            pairings.append((second, first))
    points = 0.0
    start = time.perf_counter()
    with ThreadPoolExecutor(GAMES_AT_ONCE) as pool:
        jobs = []
        for number in range(len(pairings)):
            white, black = pairings[number]
            opening = OPENINGS[number // 2 % len(OPENINGS)]
            jobs.append(pool.submit(play_game, white, black, event, opening, *clock))
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
    # A few games say little: one lucky win moves the gap by about 200 points
    if options.games >= 10:
        print(f"Elo gap: {elo_gap(points, options.games):+.0f} for {first[0]}")
    else:
        print("Too few games for an Elo gap: version_league.py rates every version")
    print(f"Total run time (sec): {time.perf_counter() - start:.3f}")


if __name__ == "__main__":
    main()
