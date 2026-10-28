#!/usr/bin/env -S uv run
"""attacks.py

Decide whether a square is attacked, and whether a king is in check.

Version 1 loops over the enemy pieces and asks each one "do you attack this
square?", the way Turbo GameWorks Chess does. Version 2 stands on the square and
looks outward like a "super piece": along the lines for rooks, bishops, and queens,
and at the knight, pawn, and king squares nearby. Version 2 is the one Remus uses.
"""

from board import EMPTY, Board, Square, parse_square, piece_at
from game_state import BLACK, WHITE, color_of, new_game, opponent
from move_generation import (
    BISHOP_DIRECTIONS,
    KING_STEPS,
    KNIGHT_JUMPS,
    ROOK_DIRECTIONS,
    Direction,
    on_board,
    piece_moves,
)


def is_attacked_by_scanning(board: Board, square: Square, by_color: str) -> bool:
    """
    Version 1: ask every enemy piece whether it attacks the square.

    Parameters
    ----------
    board : Board
        The board.
    square : Square
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


def piece_at_offsets(
    board: Board, square: Square, piece: str, offsets: list[Direction]
) -> bool:
    """
    Return True if the piece stands one of the offsets away from the square.

    Parameters
    ----------
    board : Board
        The board.
    square : Square
        The (row, col) of the square to test.
    piece : str
        The piece to look for, such as "N" for a White knight.
    offsets : list[Direction]
        The steps from the square to look at, such as KNIGHT_JUMPS.

    Returns
    -------
    bool
        True if one of the squares the offsets reach holds the piece.
    """
    row, col = square
    for row_change, col_change in offsets:
        target = (row + row_change, col + col_change)
        if on_board(*target) and piece_at(board, target) == piece:
            return True
    return False


def attacked_by_knight(board: Board, square: Square, by_color: str) -> bool:
    """Return True if a knight of by_color is one knight jump away."""
    knight = "N" if by_color == WHITE else "n"
    return piece_at_offsets(board, square, knight, KNIGHT_JUMPS)


def attacked_by_king(board: Board, square: Square, by_color: str) -> bool:
    """Return True if the king of by_color is one step away."""
    king = "K" if by_color == WHITE else "k"
    return piece_at_offsets(board, square, king, KING_STEPS)


def attacked_by_pawn(board: Board, square: Square, by_color: str) -> bool:
    """
    Return True if a pawn of by_color attacks the square.

    White pawns capture toward row 0, so a White pawn that attacks (row, col)
    stands one row below it, at (row + 1, col - 1) or (row + 1, col + 1).
    """
    if by_color == WHITE:
        return piece_at_offsets(board, square, "P", [(1, -1), (1, 1)])
    return piece_at_offsets(board, square, "p", [(-1, -1), (-1, 1)])


def first_piece(board: Board, square: Square, direction: Direction) -> str:
    """Return the first piece met walking from the square in a direction, or EMPTY."""
    row, col = square
    row_change, col_change = direction
    row, col = row + row_change, col + col_change
    while on_board(row, col):
        if board[row][col] != EMPTY:
            return board[row][col]
        row, col = row + row_change, col + col_change
    return EMPTY


def attacked_along_lines(board: Board, square: Square, by_color: str) -> bool:
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


def is_square_attacked(board: Board, square: Square, by_color: str) -> bool:
    """
    Version 2: look outward from the square for any attacker of by_color.

    Parameters
    ----------
    board : Board
        The board.
    square : Square
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


def find_king(board: Board, color: str) -> Square:
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
