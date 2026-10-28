#!/usr/bin/env -S uv run
"""station_league.py

Rank every Remus version: Remus-WHITE, the ten color stations, and Remus-GOLD.

A league plays a round robin: every version plays every other version, a few games
each, from the OPENINGS of station_match.py. Then the script fits one Elo rating to
every player from all the station games in games/remus_games.pgn, including the
games station_match.py played. Remus-WHITE, with no enhancements, is pinned at 0,
so each rating is that version's gain over Remus-WHITE.

Usage:
    uv run station_league.py                 the round robin, then the ratings
    uv run station_league.py --games 4       4 games for each pair of players
    uv run station_league.py --rate-only     only the ratings, from the saved games
    uv run station_league.py --at-once 16    16 games at a time
    uv run station_league.py --event "Station league 2"
                                             a second league, kept and rated apart

League games last 10 minutes a side. Remus searches only a few thousand positions a
second, so a shorter clock stops every version after 2 to 4 plies, too shallow for
most enhancements to help. Games at one clock are rated apart from games at another
clock.

This is a teacher tool, like station_match.py: the engine never imports python-chess.
"""

import argparse
import itertools
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor

import chess.pgn
from station_match import (
    GAMES_PATH,
    OPENINGS,
    STATIONS,
    YARDSTICK,
    find_player,
    play_game,
    time_control,
)

ANCHOR = f"Remus-{YARDSTICK}"  # Remus-WHITE is rated 0
MINUTES = 10.0  # Each side's clock in a league game
INCREMENT = 0.0  # Seconds added after each move
EVENT_PREFIX = "Station"  # Events of station_match.py and of this league
LEAGUE_EVENT = "Station league"  # The Event header of every league game
PRIOR_DRAWS = 1  # Pretend draws against Remus-WHITE, so a perfect score stays finite
SCALE = 400 / math.log(10)  # Elo points per unit of the natural logarithm
# Only one engine of a game thinks at a time, so each game needs one processor core
GAMES_AT_ONCE = os.cpu_count() or 2

Result = tuple[str, str, float]  # (White, Black, White's points)


def all_colors() -> list[str]:
    """Return the color of every station folder, such as "RED"."""
    colors = []
    for folder in sorted(STATIONS.iterdir()):
        if folder.is_dir() and " - " in folder.name:
            colors.append(folder.name.split(" - ")[0])
    return colors


def read_results(clock: str, event: str = LEAGUE_EVENT) -> list[Result]:
    """
    Return (White, Black, White's points) for every station game at one clock.

    Only games that start from one of the OPENINGS count. Remus plays the same
    move in the same position, so games from the starting position replay one
    game again and again, and counting them would count one game many times.

    Parameters
    ----------
    clock : str
        The TimeControl of the games to count, such as "600+0" from time_control().
    event : str
        LEAGUE_EVENT counts every station game, station_match.py games included.
        Any other Event name, such as "Station league 2", counts only the games
        of that league.

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
            if not headers.get("Event", "").startswith(EVENT_PREFIX):
                continue
            if event != LEAGUE_EVENT and headers.get("Event") != event:
                continue
            if headers.get("Result") not in points or "StartMoves" not in headers:
                continue
            if headers.get("TimeControl") != clock:
                continue
            results.append(
                (headers["White"], headers["Black"], points[headers["Result"]])
            )
    return results


def expected_score(rating: float, opponent: float) -> float:
    """Return the points per game the Elo formula expects for the first player."""
    return 1 / (1 + 10 ** ((opponent - rating) / 400))


def fit_ratings(results: list[Result]) -> dict[str, tuple[float, float]]:
    """
    Find the Elo ratings that best explain every result.

    Parameters
    ----------
    results : list[Result]
        Every game as (White, Black, White's points).

    Returns
    -------
    dict[str, tuple[float, float]]
        For each player, the rating and its 95 percent margin. ANCHOR is 0.

    Each round moves every rating toward the one where the player's expected
    points equal its real points, the way estimate_elo.py finds a rating
    against Stockfish. The anchor stays at 0, so the ratings are gains over it.
    """
    players = []
    for white, black, _ in results:
        for name in (white, black):
            if name not in players:
                players.append(name)
    players.sort()
    games = list(results)
    for name in players:
        if name != ANCHOR:
            games += [(name, ANCHOR, 0.5)] * PRIOR_DRAWS
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
            if name != ANCHOR and weight[name] > 0:
                ratings[name] += SCALE * surplus[name] / weight[name]
    fitted = {}
    for name in players:
        margin = 1.96 * SCALE / math.sqrt(weight[name]) if name != ANCHOR else 0.0
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
) -> None:
    """
    Play every pair of players games_per_pair times, adding each game to the file.

    A league game already in the file is not played twice, so a league that
    stops partway, such as when the computer restarts, picks up where it stopped.
    """
    players = []
    for color in all_colors():
        players.append(find_player(color))
    jobs = []
    opening_number = 0
    opening = OPENINGS[0]
    for first, second in itertools.combinations(players, 2):
        for number in range(games_per_pair):
            if number % 2 == 0:
                opening = OPENINGS[opening_number % len(OPENINGS)]
                opening_number += 1
            white, black = (first, second) if number % 2 == 0 else (second, first)
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


def print_ratings(results: list[Result], clock: str) -> None:
    """Print every player's games, score, and rating, strongest first."""
    fitted = fit_ratings(results)
    played = dict.fromkeys(fitted, 0)
    scored = dict.fromkeys(fitted, 0.0)
    for white, black, points in results:
        played[white] += 1
        played[black] += 1
        scored[white] += points
        scored[black] += 1 - points
    print(
        f"Ratings from {len(results)} station games at {clock}, {ANCHOR} pinned at 0:"
    )
    print(f"  {'Rank':>4}  {'Player':13} {'Games':>5}  {'Score':>6}  Elo vs WHITE")
    standings = []
    for name in fitted:
        standings.append((-fitted[name][0], name))  # A minus sign puts the top first
    standings.sort()
    for rank, (_, name) in enumerate(standings, start=1):
        rating, margin = fitted[name]
        share = 100 * scored[name] / played[name]
        print(
            f"  {rank:>4}  {name:13} {played[name]:>5}  {share:5.1f}%  "
            f"{rating:+5.0f} +/- {margin:.0f}"
        )


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
    options = parser.parse_args()
    clock = time_control(options.minutes, options.increment)
    start = time.perf_counter()
    if not options.rate_only:
        play_league(
            options.games,
            options.minutes,
            options.increment,
            options.at_once,
            options.event,
        )
    print_ratings(read_results(clock, options.event), clock)
    print(f"Total run time (sec): {time.perf_counter() - start:.3f}")


if __name__ == "__main__":
    main()
