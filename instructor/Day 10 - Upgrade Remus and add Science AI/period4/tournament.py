#!/usr/bin/env -S uv run
"""tournament.py

Run a round robin: every engine plays every other engine once, with colors
balanced, at 2 minutes plus 1 second a move per side. python-chess is the referee,
so an illegal move, a crash, or a lost connection loses the game. Every game is
added to the class games file, games/remus_games.pgn at the top of the Remus folder.
This is a teacher tool: the engine itself never imports python-chess.

Usage: uv run tournament.py "C:/Tournament/Knights" "C:/Tournament/Rooks" ...

Each argument is a pair's Remus folder; the folder name is the team name. With no
arguments, the four brains of this folder's Remus play each other as a demo, at
10 seconds plus 0.1 seconds a move.
"""

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
GAMES_AT_ONCE = 4  # Each game runs two engine processes


def round_robin(count: int) -> list[list[tuple[int, int]]]:
    """
    Pair entrants for every round with the circle method.

    Parameters
    ----------
    count : int
        The number of entrants. With an odd count, one entrant rests each round.

    Returns
    -------
    list[list[tuple[int, int]]]
        For each round, the games as (white index, black index).
    """
    players = list(range(count)) + ([None] if count % 2 else [])
    rounds = []
    for number in range(len(players) - 1):
        games = []
        for board in range(len(players) // 2):
            first, second = players[board], players[-1 - board]
            if first is None or second is None:
                continue
            if board == 0 and number % 2:  # The fixed first entrant alternates colors
                first, second = second, first
            games.append((first, second))
        rounds.append(games)
        players = [players[0], players[-1]] + players[
            1:-1
        ]  # Keep the first, rotate the rest
    return rounds


def play_game(
    white: tuple[str, list[str]],
    black: tuple[str, list[str]],
    minutes: float,
    increment: float,
) -> chess.pgn.Game:
    """Play one game on a chess clock and return it as PGN, with the result set."""
    engines = [
        chess.engine.SimpleEngine.popen_uci(command) for _, command in (white, black)
    ]
    board = chess.Board()
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
                clocks[side] += increment
                continue
            result = "0-1" if side == 0 else "1-0"  # The side to move loses
            break
    finally:
        for engine in engines:
            engine.quit()
    game = chess.pgn.Game.from_board(board)
    game.headers["Event"] = "Remus round robin"
    game.headers["Date"] = date.today().strftime("%Y.%m.%d")
    game.headers["White"], game.headers["Black"] = white[0], black[0]
    game.headers["Result"] = result or board.result(claim_draw=True)
    if reason:
        game.headers["Termination"] = reason
    return game


def main():
    if len(sys.argv) > 1:
        folders = [Path(name) for name in sys.argv[1:]]
        entrants = [
            (folder.name, [sys.executable, str(folder / "uci_engine.py")])
            for folder in folders
        ]
        minutes, increment = 2.0, 1.0
    else:
        entrants = [
            (brain, [sys.executable, str(ENGINE_FILE), brain])
            for brain in ("random", "greedy", "negamax", "think")
        ]
        minutes, increment = 10 / 60, 0.1
    points = {name: 0.0 for name, _ in entrants}
    print(f"Adding every game to {GAMES_PATH}")
    GAMES_PATH.parent.mkdir(exist_ok=True)
    for number, games in enumerate(round_robin(len(entrants)), start=1):
        with ThreadPoolExecutor(GAMES_AT_ONCE) as pool:
            finished = list(
                pool.map(
                    lambda pair: play_game(
                        entrants[pair[0]], entrants[pair[1]], minutes, increment
                    ),
                    games,
                )
            )
        for game in finished:
            white, black, result = (
                game.headers[key] for key in ("White", "Black", "Result")
            )
            points[white] += {"1-0": 1, "0-1": 0}.get(result, 0.5)
            points[black] += {"1-0": 0, "0-1": 1}.get(result, 0.5)
            print(f"Round {number}: {white} vs {black}: {result}")
            with GAMES_PATH.open("a") as file:
                print(game, end="\n\n", file=file)
        print(f"Standings after round {number}:")
        for name, score in sorted(points.items(), key=lambda item: -item[1]):
            print(f"  {score:4.1f}  {name}")
    print(
        f"Games played: {sum(points.values()):.0f}  (expected {len(entrants) * (len(entrants) - 1) // 2})"
    )


if __name__ == "__main__":
    main()
