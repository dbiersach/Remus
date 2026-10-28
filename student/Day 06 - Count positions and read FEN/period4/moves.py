#!/usr/bin/env -S uv run
"""moves.py

Describe a move as a small record, and convert it to and from UCI text such as
"e2e4" or "e7e8q", the format chess programs use to talk to each other.
"""

from dataclasses import dataclass

from board import Square, parse_square, square_name


@dataclass(frozen=True)
class Move:
    """
    One move: where the piece starts, where it lands, and any promotion.

    from_square and to_square are (row, col) tuples. promotion is the piece a pawn
    becomes on the last rank ("Q", "R", "B", "N" for White; lowercase for Black),
    or None for every other move.
    """

    from_square: Square
    to_square: Square
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
    text = square_name(*move.from_square) + square_name(*move.to_square)
    if move.promotion is not None:
        text += move.promotion.lower()
    return text


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
    from_square = parse_square(text[0:2])
    to_square = parse_square(text[2:4])
    promotion = None
    if len(text) == 5:
        promotion = text[4].upper() if white_to_move else text[4].lower()
    return Move(from_square, to_square, promotion)


def main():
    move = move_from_uci("g1f3")
    print(f"g1f3 is {move}")
    print(f"Back to text: {move_to_uci(move)}  (expected g1f3)")
    print(f"Promotion: {move_to_uci(move_from_uci('e7e8q'))}  (expected e7e8q)")


if __name__ == "__main__":
    main()
