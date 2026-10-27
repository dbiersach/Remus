#!/usr/bin/env -S uv run
"""opening_book.py

Play the first few moves from a list of well-known openings instead of searching.
Each line of opening_book.txt is one opening written in SAN. Remus replays every
line from the starting position and records, for each position along the way, the
moves the book suggests there. The book is a dict:

    position_key -> list of book moves

Every book move is read with parse_san, which accepts only legal moves, so a typo
in the file is reported and skipped. A missing file is reported and gives an empty
book, and an empty book never stops play: Remus simply searches instead. Reports go
to standard error, because standard output carries the UCI conversation with the
GUI.
"""

import random
import sys
from pathlib import Path

from fen import START_FEN, state_from_fen
from game_state import position_key
from make_move import make_move
from moves import Move, move_to_uci
from notation import parse_san

BOOK_PATH = Path(__file__).parent / "opening_book.txt"


def load_book(file_path: Path = BOOK_PATH) -> dict[str, list[Move]]:
    """
    Read an opening book file into a dict from position key to book moves.

    Parameters
    ----------
    file_path : Path
        The book file: one opening per line in SAN, "#" for comments.

    Returns
    -------
    dict[str, list[Move]]
        For each position reached in the book, the moves the book plays there.
        The dict is empty if the file does not exist.
    """
    # Day 9, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 9 P2: write load_book()")


def book_move(book: dict[str, list[Move]], state: dict) -> Move | None:
    """Return a random book move for this position, or None when out of book."""
    choices = book.get(position_key(state))
    return random.choice(choices) if choices else None


def main():
    print(f"Reading {BOOK_PATH}")
    book = load_book()
    print(f"Book positions: {len(book)}")
    state = state_from_fen(START_FEN)
    first_moves = sorted(move_to_uci(move) for move in book[position_key(state)])
    print(
        f"First moves in the book: {' '.join(first_moves)}  (expected c2c4 d2d4 e2e4 g1f3)"
    )
    make_move(state, parse_san(state, "e4"))
    reply = book_move(book, state)
    reply_text = move_to_uci(reply) if reply is not None else "none"
    print(f"A book reply to 1. e4: {reply_text}  (e7e5, c7c5, e7e6, or c7c6)")
    missing = load_book(Path(__file__).parent / "no_such_book.txt")
    print(f"Missing book file gives {len(missing)} positions  (expected 0)")


if __name__ == "__main__":
    main()
