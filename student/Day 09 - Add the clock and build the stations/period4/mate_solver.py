#!/usr/bin/env -S uv run
"""mate_solver.py

Solve "White to play and mate in n moves" puzzles, like the MATE.001 to MATE.010
problems that came with Turbo GameWorks Chess. A mate solver asks a yes-or-no
question instead of computing a score:

    Does the attacker have a move such that every defender reply still allows
    mate in one move fewer?

The attacker's last move must give check, because only a check can be mate. The
solver skips every quiet move on that last move, which makes it much faster than
a general search of the same depth.
"""

import time
from pathlib import Path

from attacks import in_check
from fen import state_from_fen
from legal_moves import legal_moves
from make_move import make_move, state_snapshot, undo_move
from moves import Move
from notation import move_to_san

PUZZLE_PATH = Path(__file__).parent.parent.parent.parent / "tests" / "mate_puzzles.epd"


def mating_move(state: dict, moves_left: int) -> Move | None:
    """
    Find a move that forces checkmate within moves_left of the attacker's moves.

    Parameters
    ----------
    state : dict
        The game state, with the attacker to move. It is unchanged when the
        function returns.
    moves_left : int
        How many attacker moves are allowed, counting this one.

    Returns
    -------
    Move | None
        A move that forces mate, or None if there is no forced mate in time.
    """
    # Day 9, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 9 P4: write mating_move()")


def defense_fails(state: dict, reply: Move, moves_left: int) -> bool:
    """Return True if the attacker still mates in moves_left after this reply."""
    undo = make_move(state, reply)
    try:
        return mating_move(state, moves_left) is not None
    finally:
        undo_move(state, undo)


def read_puzzles(file_path: Path = PUZZLE_PATH) -> list[tuple[str, str, int, str]]:
    """
    Read mate puzzles from an EPD file.

    Parameters
    ----------
    file_path : Path
        A file with lines such as
        '... w - - bm Be4; dm 2; id "MATE.001";'.

    Returns
    -------
    list[tuple[str, str, int, str]]
        For each puzzle: the FEN, the best move in SAN, the mate length in
        moves, and the puzzle's name.
    """
    puzzles = []
    for line in file_path.read_text().splitlines():
        if not line.strip():
            continue
        fields = line.split()
        # EPD gives four FEN fields, then operations such as bm Qg6; dm 2;
        fen = fields[0] + " " + fields[1] + " " + fields[2] + " " + fields[3] + " 0 1"
        rest = ""
        for word in fields[4:]:
            rest += word + " "
        operations = {}
        for part in rest.split(";"):
            part = part.strip()
            if part != "":
                name, value = part.split(" ", 1)
                operations[name] = value
        puzzles.append(
            (fen, operations["bm"], int(operations["dm"]), operations["id"].strip('"'))
        )
    return puzzles


def main():
    print(f"Reading {PUZZLE_PATH}")
    for fen, best, length, name in read_puzzles():
        state = state_from_fen(fen)
        before = state_snapshot(state)
        start = time.perf_counter()
        move = mating_move(state, length)
        seconds = time.perf_counter() - start
        found = move_to_san(state, move) if move else "none"
        unchanged = state_snapshot(state) == before
        print(
            f"{name}: mate in {length} with {found:6} (expected {best:5})"
            f"  {seconds:5.1f} s  root unchanged: {unchanged}"
        )


if __name__ == "__main__":
    main()
