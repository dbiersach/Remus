#!/usr/bin/env -S uv run
"""moves.py

Describe a move as a small record, and convert it to and from UCI text such as
"e2e4" or "e7e8q", the format chess programs use to talk to each other.
"""

from dataclasses import dataclass

from board import parse_square, square_name


@dataclass(frozen=True)
class Move:
    """
    One move: where the piece starts, where it lands, and any promotion.

    from_square and to_square are (row, col) tuples. promotion is the piece a pawn
    becomes on the last rank ("Q", "R", "B", "N" for White; lowercase for Black),
    or None for every other move.
    """

    from_square: tuple[int, int]
    to_square: tuple[int, int]
    promotion: str | None = None


def move_to_uci(move: Move) -> str:
    """
    Convert a move to UCI text.

    Parameters
    ----------
    move : Move
        The move to convert.

    Returns
    -------
    str
        Text such as "e2e4", or "e7e8q" for a promotion (always lowercase).
    """
    # Day 2, period 3: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 2 P3: write move_to_uci()")


def move_from_uci(text: str, white_to_move: bool = True) -> Move:
    """
    Convert UCI text to a move.

    Parameters
    ----------
    text : str
        Text such as "g1f3" or "e7e8q".
    white_to_move : bool
        True if White makes the move, so a promotion piece is uppercase.

    Returns
    -------
    Move
        The move the text describes.
    """
    # Day 2, period 3: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 2 P3: write move_from_uci()")


def main():
    move = move_from_uci("g1f3")
    print(f"g1f3 is {move}")
    print(f"Back to text: {move_to_uci(move)}  (expected g1f3)")
    print(f"Promotion: {move_to_uci(move_from_uci('e7e8q'))}  (expected e7e8q)")


if __name__ == "__main__":
    main()
