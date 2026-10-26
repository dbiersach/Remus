#!/usr/bin/env -S uv run
"""attacks.py

Decide whether a square is attacked, and whether a king is in check.

Version 1 loops over the enemy pieces and asks each one "do you attack this
square?", the way Turbo GameWorks Chess does. Version 2 stands on the square and
looks outward like a "super piece": along the lines for rooks, bishops, and queens,
and at the knight, pawn, and king squares nearby. Version 2 is the one Remus uses.
"""

from board import EMPTY, parse_square, piece_at
from game_state import BLACK, WHITE, color_of, new_game
from move_generation import (
    BISHOP_DIRECTIONS,
    KING_STEPS,
    KNIGHT_JUMPS,
    ROOK_DIRECTIONS,
    on_board,
    piece_moves,
)


def is_attacked_by_scanning(
    board: list[list[str]], square: tuple[int, int], by_color: str
) -> bool:
    """
    Version 1: ask every enemy piece whether it attacks the square.

    Parameters
    ----------
    board : list[list[str]]
        The board.
    square : tuple[int, int]
        The (row, col) of the square to test.
    by_color : str
        The color of the attacking side.

    Returns
    -------
    bool
        True if any piece of by_color attacks the square. Version 1 reuses the move
        generator, so it does not count a square that holds a piece of by_color
        (a defended piece). Check and castling never ask about such a square.
    """
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if color_of(piece) != by_color:
                continue
            if piece.upper() == "P":
                # A pawn attacks diagonally forward, even an empty square
                forward = -1 if by_color == WHITE else 1
                if square in [(row + forward, col - 1), (row + forward, col + 1)]:
                    return True
            else:
                for move in piece_moves(board, (row, col)):
                    if move.to_square == square:
                        return True
    return False


def attacked_by_knight(
    board: list[list[str]], square: tuple[int, int], by_color: str
) -> bool:
    """Return True if a knight of by_color is one knight jump away."""
    # Day 4, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 4 P2: write attacked_by_knight()")


def attacked_by_king(
    board: list[list[str]], square: tuple[int, int], by_color: str
) -> bool:
    """Return True if the king of by_color is one step away."""
    # Day 4, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 4 P2: write attacked_by_king()")


def attacked_by_pawn(
    board: list[list[str]], square: tuple[int, int], by_color: str
) -> bool:
    """
    Return True if a pawn of by_color attacks the square.

    White pawns capture toward row 0, so a White pawn that attacks (row, col)
    stands one row below it, at (row + 1, col - 1) or (row + 1, col + 1).
    """
    # Day 4, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 4 P2: write attacked_by_pawn()")


def first_piece(
    board: list[list[str]], square: tuple[int, int], direction: tuple[int, int]
) -> str:
    """Return the first piece met walking from the square in a direction, or EMPTY."""
    row, col = square
    row_change, col_change = direction
    row, col = row + row_change, col + col_change
    while on_board(row, col):
        if board[row][col] != EMPTY:
            return board[row][col]
        row, col = row + row_change, col + col_change
    return EMPTY


def attacked_along_lines(
    board: list[list[str]], square: tuple[int, int], by_color: str
) -> bool:
    """Return True if a rook, bishop, or queen of by_color attacks along a line."""
    for direction in ROOK_DIRECTIONS:
        piece = first_piece(board, square, direction)
        if color_of(piece) == by_color and piece.upper() in "RQ":
            return True
    for direction in BISHOP_DIRECTIONS:
        piece = first_piece(board, square, direction)
        if color_of(piece) == by_color and piece.upper() in "BQ":
            return True
    return False


def is_square_attacked(
    board: list[list[str]], square: tuple[int, int], by_color: str
) -> bool:
    """
    Version 2: look outward from the square for any attacker of by_color.

    Parameters
    ----------
    board : list[list[str]]
        The board.
    square : tuple[int, int]
        The (row, col) of the square to test.
    by_color : str
        The color of the attacking side.

    Returns
    -------
    bool
        True if any piece of by_color attacks the square.
    """
    return (
        attacked_by_knight(board, square, by_color)
        or attacked_by_pawn(board, square, by_color)
        or attacked_by_king(board, square, by_color)
        or attacked_along_lines(board, square, by_color)
    )


def find_king(board: list[list[str]], color: str) -> tuple[int, int]:
    """Return the (row, col) of the king of the given color."""
    king = "K" if color == WHITE else "k"
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                return row, col
    raise ValueError(f"No {king} on the board")


def in_check(state: dict, color: str) -> bool:
    """
    Return True if the king of the given color is attacked.

    Parameters
    ----------
    state : dict
        The game state.
    color : str
        The color of the king to test, "w" or "b".

    Returns
    -------
    bool
        True if that king stands on a square the other side attacks.
    """
    # Day 4, period 3: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 4 P3: write in_check()")


def main():
    state = new_game()
    board = state["board"]
    f3 = parse_square("f3")
    print(
        f"f3 attacked by White: {is_square_attacked(board, f3, WHITE)}  (expected True)"
    )
    print(
        f"f3 attacked by Black: {is_square_attacked(board, f3, BLACK)}  (expected False)"
    )
    tests = 0
    agree = 0
    for row in range(8):
        for col in range(8):
            for color in (WHITE, BLACK):
                if color_of(board[row][col]) == color:
                    continue  # Version 1 skips squares held by the attacker
                tests += 1
                version_1 = is_attacked_by_scanning(board, (row, col), color)
                agree += version_1 == is_square_attacked(board, (row, col), color)
    print(f"Versions 1 and 2 agree on {agree} of {tests} squares  (expected all)")
    print(f"White in check at the start: {in_check(state, WHITE)}  (expected False)")


if __name__ == "__main__":
    main()
