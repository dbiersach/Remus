#!/usr/bin/env -S uv run
"""version_league.py

Rank every Remus version: Remus-WHITE, the ten color versions, and Remus-GOLD.

A league plays a round robin: every version plays every other version, a few games
each, from the OPENINGS of version_match.py. Then the script fits one Elo rating to
every player from all the version games in games/remus_games.pgn, including the
games version_match.py played. Remus-WHITE, with no enhancements, is pinned at 0,
so each rating is that version's gain over Remus-WHITE.

Usage:
    uv run scripts/version_league.py             the round robin, then the ratings
    uv run scripts/version_league.py --games 4   4 games for each pair of players
    uv run scripts/version_league.py --rate-only only the ratings, from saved games
    uv run scripts/version_league.py --rate-only --player GOLD
                                                 also Remus-GOLD's score against each
    uv run scripts/version_league.py --at-once 16
                                                 16 games at a time
    uv run scripts/version_league.py --event "Station league 2"
                                                 a second league, rated apart
    uv run scripts/version_league.py --niram --rate-only --event "Niram league 1"
                                                 the saved Niram league, rated
    uv run scripts/version_league.py --book-start
                                                 GREEN's and GOLD's games from move 1

League games last 10 minutes a side. Remus searches only a few thousand positions a
second, so a shorter clock stops every version after 2 to 4 plies, too shallow for
most enhancements to help. Games at one clock are rated apart from games at another
clock.

The teacher's league ran on Niram, Rust copies of the same 12 versions that chose
the same moves as Remus about 50 times faster, so a 10 minute Niram game searched
as deep as a Remus game of many hours. Only Niram-GOLD is kept, in the Niram-GOLD
folder, but the Niram games stay in the games file: --niram with --rate-only rates
them apart from Remus games, with Niram-WHITE pinned at 0.

Every game starts from one of the OPENINGS of version_match.py, three moves for each
side, because a version with no book plays the same game again from the starting
position. Those six moves also hand every version a short opening book, which hides
most of what the book of Remus-GREEN and Remus-GOLD is worth. With --book-start, every
game with GREEN or GOLD starts from the starting position instead: their book picks
among its moves at random, so their games still differ. The other pairs keep the
OPENINGS. Rate such a league with --book-start too.

This is a teacher tool, like version_match.py: the engine never imports python-chess.
"""

import argparse
import itertools
import math
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import chess.pgn

# version_match.py lives beside the color versions in Day 9, period2/engines
INSTRUCTOR = Path(__file__).parent.parent / "instructor"
sys.path.insert(0, str(next(INSTRUCTOR.glob("Day 09 - *")) / "period2" / "engines"))

from version_match import (
    GAMES_PATH,
    OPENINGS,
    YARDSTICK,
    all_players,
    play_game,
    time_control,
)

MINUTES = 10.0  # Each side's clock in a league game
INCREMENT = 0.0  # Seconds added after each move
EVENT_PREFIX = "Station"  # Events of version_match.py and of this league
LEAGUE_EVENT = "Station league"  # The Event header of every league game
PRIOR_DRAWS = 1  # Pretend draws against Remus-WHITE, so a perfect score stays finite
SCALE = 400 / math.log(10)  # Elo points per unit of the natural logarithm
# Only one engine of a game thinks at a time, so each game needs one processor core
GAMES_AT_ONCE = os.cpu_count() or 2
BOOK_COLORS = ["GREEN", "GOLD"]  # The versions that play from the opening book

Result = tuple[str, str, float]  # (White, Black, White's points)


def uses_book(name: str) -> bool:
    """Return True if the player, such as "Niram-GREEN", plays from the book."""
    return name.split("-")[-1] in BOOK_COLORS


def read_results(
    clock: str,
    event: str = LEAGUE_EVENT,
    engine: str = "Remus",
    book_start: bool = False,
) -> list[Result]:
    """
    Return (White, Black, White's points) for every version game at one clock.

    Only games that start from one of the OPENINGS count. Remus plays the same
    move in the same position, so games from the starting position replay one
    game again and again, and counting them would count one game many times.
    With book_start, a game with Remus-GREEN or Remus-GOLD counts only when it
    starts from the starting position: their book picks among its moves at
    random, so those games differ from each other.

    Parameters
    ----------
    clock : str
        The TimeControl of the games to count, such as "600+0" from time_control().
    event : str
        LEAGUE_EVENT counts every version game, version_match.py games included.
        Any other Event name, such as "Niram league 1", counts only the games
        of that league, whatever its name starts with.
    engine : str
        "Remus" or "Niram": only games between two versions of that engine count,
        so Remus and Niram get separate ratings.
    book_start : bool
        True to rate the games of GREEN and GOLD from the starting position.

    Returns
    -------
    list[Result]
        One (White, Black, White's points) for each game.
    """
    results = []
    if not GAMES_PATH.exists():
        return results
    points = {"1-0": 1.0, "0-1": 0.0, "1/2-1/2": 0.5}
    with GAMES_PATH.open() as file:
        while (game := chess.pgn.read_game(file)) is not None:
            headers = game.headers
            if event == LEAGUE_EVENT:
                if not headers.get("Event", "").startswith(EVENT_PREFIX):
                    continue
            elif headers.get("Event") != event:
                continue
            if headers.get("Result") not in points:
                continue
            from_start = "StartMoves" not in headers
            book_game = uses_book(headers["White"]) or uses_book(headers["Black"])
            if from_start != (book_start and book_game):
                continue
            if headers.get("TimeControl") != clock:
                continue
            if not headers["White"].startswith(engine + "-"):
                continue
            if not headers["Black"].startswith(engine + "-"):
                continue
            results.append(
                (headers["White"], headers["Black"], points[headers["Result"]])
            )
    return results


def expected_score(rating: float, opponent: float) -> float:
    """Return the points per game the Elo formula expects for the first player."""
    return 1 / (1 + 10 ** ((opponent - rating) / 400))


def fit_ratings(results: list[Result], anchor: str) -> dict[str, tuple[float, float]]:
    """
    Find the Elo ratings that best explain every result.

    Parameters
    ----------
    results : list[Result]
        Every game as (White, Black, White's points).
    anchor : str
        The player pinned at 0, such as "Remus-WHITE".

    Returns
    -------
    dict[str, tuple[float, float]]
        For each player, the rating and its 95 percent margin. The anchor is 0.

    Each round moves every rating toward the one where the player's expected
    points equal its real points, the way estimate_elo.py finds a rating
    against Stockfish. The anchor stays at 0, so the ratings are gains over it.
    """
    players = []
    for white, black, _ in results:
        for name in (white, black):
            if name not in players:
                players.append(name)
    # The anchor takes part in the pretend draws even if it played no real game
    if results and anchor not in players:
        players.append(anchor)
    players.sort()
    games = list(results)
    for name in players:
        if name != anchor:
            games += [(name, anchor, 0.5)] * PRIOR_DRAWS
    ratings = dict.fromkeys(players, 0.0)
    weight = dict.fromkeys(players, 0.0)
    for _ in range(500):
        surplus = dict.fromkeys(players, 0.0)  # Real points minus expected points
        weight = dict.fromkeys(players, 0.0)  # How much one point of rating moves it
        for white, black, points in games:
            expected = expected_score(ratings[white], ratings[black])
            surplus[white] += points - expected
            surplus[black] -= points - expected
            weight[white] += expected * (1 - expected)
            weight[black] += expected * (1 - expected)
        for name in players:
            if name != anchor and weight[name] > 0:
                ratings[name] += SCALE * surplus[name] / weight[name]
    fitted = {}
    for name in players:
        margin = 1.96 * SCALE / math.sqrt(weight[name]) if name != anchor else 0.0
        fitted[name] = (ratings[name], margin)
    return fitted


def played_league_games(clock: str, event: str) -> list[tuple[str, str, str]]:
    """Return (White, Black, StartMoves) for every game of one league at one clock."""
    played = []
    if not GAMES_PATH.exists():
        return played
    with GAMES_PATH.open() as file:
        while (headers := chess.pgn.read_headers(file)) is not None:
            if headers.get("Event") == event and headers.get("TimeControl") == clock:
                played.append(
                    (headers["White"], headers["Black"], headers.get("StartMoves", ""))
                )
    return played


def play_league(
    games_per_pair: int,
    minutes: float,
    increment: float,
    games_at_once: int,
    event: str,
    book_start: bool = False,
) -> None:
    """
    Play every pair of players games_per_pair times, adding each game to the file.

    A league game already in the file is not played twice, so a league that
    stops partway, such as when the computer restarts, picks up where it stopped.
    With book_start, every game with GREEN or GOLD starts from the starting
    position, so their opening book plays from the first move.
    """
    players = all_players()
    jobs = []
    opening_number = 0
    opening = OPENINGS[0]
    for first, second in itertools.combinations(players, 2):
        for number in range(games_per_pair):
            if number % 2 == 0:
                opening = OPENINGS[opening_number % len(OPENINGS)]
                opening_number += 1
            white, black = (first, second) if number % 2 == 0 else (second, first)
            if book_start and (uses_book(first[0]) or uses_book(second[0])):
                jobs.append((white, black, ""))
            else:
                jobs.append((white, black, opening))
    played = played_league_games(time_control(minutes, increment), event)
    waiting = []
    for white, black, opening in jobs:
        if (white[0], black[0], opening) in played:
            played.remove((white[0], black[0], opening))
        else:
            waiting.append((white, black, opening))
    print(
        f"League: {len(players)} players, {len(jobs)} games at {minutes:g} min + "
        f"{increment:g} s, {len(jobs) - len(waiting)} already played, "
        f"{games_at_once} at a time"
    )
    print(f"Adding every game to {GAMES_PATH}")
    GAMES_PATH.parent.mkdir(exist_ok=True)
    with ThreadPoolExecutor(games_at_once) as pool:
        futures = []
        for white, black, opening in waiting:
            futures.append(
                pool.submit(play_game, white, black, event, opening, minutes, increment)
            )
        for number, future in enumerate(futures, start=len(jobs) - len(waiting) + 1):
            game = future.result()
            with GAMES_PATH.open("a") as file:
                print(game, end="\n\n", file=file)
            print(
                f"  Game {number}: {game.headers['White']} vs "
                f"{game.headers['Black']}: {game.headers['Result']}",
                flush=True,
            )


def print_ratings(results: list[Result], clock: str, anchor: str) -> None:
    """Print every player's games, score, and rating, strongest first."""
    fitted = fit_ratings(results, anchor)
    played = dict.fromkeys(fitted, 0)
    scored = dict.fromkeys(fitted, 0.0)
    for white, black, points in results:
        played[white] += 1
        played[black] += 1
        scored[white] += points
        scored[black] += 1 - points
    print(
        f"Ratings from {len(results)} version games at {clock}, {anchor} pinned at 0:"
    )
    print(f"  {'Rank':>4}  {'Player':13} {'Games':>5}  {'Score':>6}  Elo vs WHITE")
    standings = []
    for name in fitted:
        standings.append((-fitted[name][0], name))  # A minus sign puts the top first
    standings.sort()
    for rank, (_, name) in enumerate(standings, start=1):
        rating, margin = fitted[name]
        share = 0.0  # The anchor may have no games of its own
        if played[name] > 0:
            share = 100 * scored[name] / played[name]
        print(
            f"  {rank:>4}  {name:13} {played[name]:>5}  {share:5.1f}%  "
            f"{rating:+5.0f} +/- {margin:.0f}"
        )


def print_head_to_head(results: list[Result], player: str) -> None:
    """
    Print one player's score against each opponent, such as Remus-GOLD's.

    Parameters
    ----------
    results : list[Result]
        Every game as (White, Black, White's points).
    player : str
        The player to report, such as "Remus-GOLD".
    """
    played = {}
    scored = {}
    for white, black, points in results:
        if player == white:
            opponent, gained = black, points
        elif player == black:
            opponent, gained = white, 1 - points
        else:
            continue
        played[opponent] = played.get(opponent, 0) + 1
        scored[opponent] = scored.get(opponent, 0.0) + gained
    print(f"{player} against each opponent:")
    print(f"  {'Opponent':13} {'Games':>5}  {'Points':>6}")
    for opponent in sorted(played):
        print(f"  {opponent:13} {played[opponent]:>5}  {scored[opponent]:6g}")


def main():
    parser = argparse.ArgumentParser(description="Rank every Remus version.")
    parser.add_argument("--games", type=int, default=6, help="games for each pair")
    parser.add_argument("--rate-only", action="store_true", help="skip the games")
    parser.add_argument("--minutes", type=float, default=MINUTES, help="each clock")
    parser.add_argument(
        "--increment", type=float, default=INCREMENT, help="seconds added per move"
    )
    parser.add_argument(
        "--at-once", type=int, default=GAMES_AT_ONCE, help="games played at once"
    )
    parser.add_argument(
        "--event", default=LEAGUE_EVENT, help="the Event name of this league's games"
    )
    parser.add_argument("--player", help='also show one color\'s games, such as "GOLD"')
    parser.add_argument(
        "--niram", action="store_true", help="rate the saved Niram games"
    )
    parser.add_argument(
        "--book-start",
        action="store_true",
        help="start GREEN's and GOLD's games from the starting position",
    )
    options = parser.parse_args()
    engine = "Niram" if options.niram else "Remus"
    anchor = f"{engine}-{YARDSTICK}"
    clock = time_control(options.minutes, options.increment)
    start = time.perf_counter()
    if options.niram and not options.rate_only:
        sys.exit("Only Niram-GOLD is kept, so --niram works only with --rate-only")
    if not options.rate_only:
        play_league(
            options.games,
            options.minutes,
            options.increment,
            options.at_once,
            options.event,
            options.book_start,
        )
    results = read_results(clock, options.event, engine, options.book_start)
    print_ratings(results, clock, anchor)
    if options.player:
        print_head_to_head(results, f"{engine}-{options.player.upper()}")
    print(f"Total run time (sec): {time.perf_counter() - start:.3f}")


if __name__ == "__main__":
    main()
