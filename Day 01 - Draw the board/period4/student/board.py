#!/usr/bin/env -S uv run
"""board.py

Hold the chessboard as an 8x8 list of lists and convert between square names, such
as "e2", and (row, col) tuples, such as (6, 4).

Row 0 is rank 8 and column 0 is file a, so the board prints in the same order a
player sees it from White's side: rank 8 at the top, rank 1 at the bottom.
"""

EMPTY = "."  # An empty square
BOARD_FILES = "abcdefgh"  # File letters, indexed by column: column 0 is file a
BOARD_RANKS = "87654321"  # Rank digits, indexed by row: row 0 is rank 8
START_ROWS = [  # The starting position, row 0 (rank 8) first
    "rnbqkbnr",
    "pppppppp",
    "........",
    "........",
    "........",
    "........",
    "PPPPPPPP",
    "RNBQKBNR",
]

Square = tuple[int, int]  # A (row, col) pair, such as (6, 4) for e2
Board = list[list[str]]  # Eight rows of eight squares, row 0 (rank 8) first


def new_board() -> Board:
    """Return a fresh board set up in the starting position."""
    board = []
    for row in START_ROWS:
        board.append(list(row))  # list("rnbqkbnr") gives one letter per square
    return board


def print_board(board: Board) -> None:
    """
    Print the board with rank numbers on the left and file letters below.

    Parameters
    ----------
    board : Board
        The board, row 0 first (rank 8).
    """
    # Day 1, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 1 P4: write print_board()")


def square_name(row: int, col: int) -> str:
    """
    Convert board coordinates to an algebraic square name.

    Parameters
    ----------
    row : int
        Board row, where row 0 is rank 8.
    col : int
        Board column, where column 0 is file a.

    Returns
    -------
    str
        The square name, such as "e2" for (6, 4).
    """
    # Day 1, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 1 P4: write square_name()")


def parse_square(name: str) -> Square:
    """
    Convert an algebraic square name to (row, col) coordinates.

    Parameters
    ----------
    name : str
        A square name such as "e2".

    Returns
    -------
    Square
        The (row, col) of the square, such as (6, 4) for "e2".

    Raises
    ------
    ValueError
        If the name is not a square on the board, such as "i9".
    """
    # Day 1, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 1 P4: write parse_square()")


def piece_at(board: Board, square: Square) -> str:
    """Return the piece on a (row, col) square, or EMPTY."""
    # Day 1, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 1 P4: write piece_at()")


def main():
    board = new_board()
    print_board(board)
    print()
    print(f"e2 is {parse_square('e2')}, expected (6, 4)")
    print(f"(0, 0) is {square_name(0, 0)}, expected a8")
    print(f"b1 holds {piece_at(board, parse_square('b1'))}, expected N")


if __name__ == "__main__":
    main()
