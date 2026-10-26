#!/usr/bin/env -S uv run
"""board.py

Hold the chessboard as an 8x8 list of lists and convert between square names, such
as "e2", and (row, col) tuples, such as (6, 4).

Row 0 is rank 8 and column 0 is file a, so the board prints in the same order a
player sees it from White's side: rank 8 at the top, rank 1 at the bottom.
"""

EMPTY = "."  # An empty square
FILES = "abcdefgh"  # File letters, indexed by column number
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


def new_board() -> list[list[str]]:
    """Return a fresh board set up in the starting position."""
    return [list(row) for row in START_ROWS]


def print_board(board: list[list[str]]) -> None:
    """
    Print the board with rank numbers on the left and file letters below.

    Parameters
    ----------
    board : list[list[str]]
        The board, row 0 first (rank 8).
    """
    for row in range(8):
        rank = 8 - row
        print(rank, " ".join(board[row]))
    print(" ", " ".join(FILES))


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
    return FILES[col] + str(8 - row)


def parse_square(name: str) -> tuple[int, int]:
    """
    Convert an algebraic square name to (row, col) coordinates.

    Parameters
    ----------
    name : str
        A square name such as "e2".

    Returns
    -------
    tuple[int, int]
        The (row, col) of the square, such as (6, 4) for "e2".

    Raises
    ------
    ValueError
        If the name is not a square on the board, such as "i9".
    """
    if len(name) != 2 or name[0] not in FILES or name[1] not in "12345678":
        raise ValueError(f"Not a square: {name!r}")
    col = FILES.index(name[0])
    row = 8 - int(name[1])
    return row, col


def piece_at(board: list[list[str]], square: tuple[int, int]) -> str:
    """Return the piece on a (row, col) square, or EMPTY."""
    row, col = square
    return board[row][col]


def main():
    board = new_board()
    print_board(board)
    print()
    print(f"e2 is {parse_square('e2')}, expected (6, 4)")
    print(f"(0, 0) is {square_name(0, 0)}, expected a8")
    print(f"b1 holds {piece_at(board, parse_square('b1'))}, expected N")


if __name__ == "__main__":
    main()
