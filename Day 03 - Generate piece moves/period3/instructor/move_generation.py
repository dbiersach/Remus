#!/usr/bin/env -S uv run
"""move_generation.py

Generate pseudo-legal moves: every move the pieces can make by their movement rules,
before checking whether the move leaves the mover's own king in check.

Directions are (row change, col change) pairs. Row 0 is rank 8, so White pawns move
toward row 0 (a row change of -1) and Black pawns move toward row 7 (+1).
"""

from board import EMPTY, Board, Square, piece_at
from game_state import WHITE, color_of
from moves import Move

Direction = tuple[int, int]  # A (row change, col change) step, such as (-1, 0)
KNIGHT_JUMPS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
KING_STEPS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
ROOK_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Along ranks and files
BISHOP_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Along diagonals
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS


def on_board(row: int, col: int) -> bool:
    """Return True if (row, col) is one of the 64 squares."""
    return 0 <= row < 8 and 0 <= col < 8


def jump_moves(
    board: Board, square: Square, color: str, offsets: list[Direction]
) -> list[Move]:
    """
    Return the moves of a piece that jumps by fixed offsets (a knight or a king).

    Parameters
    ----------
    board : Board
        The board.
    square : Square
        The (row, col) of the jumping piece.
    color : str
        The color of the jumping piece, "w" or "b".
    offsets : list[Direction]
        The jumps the piece can make, such as KNIGHT_JUMPS.

    Returns
    -------
    list[Move]
        A move to every target square that is on the board and does not hold a
        piece of the same color.
    """
    row, col = square
    moves = []
    for row_change, col_change in offsets:
        target = (row + row_change, col + col_change)
        if on_board(*target) and color_of(piece_at(board, target)) != color:
            moves.append(Move(square, target))
    return moves


def knight_moves(board: Board, square: Square, color: str) -> list[Move]:
    """Return the moves of a knight on the square."""
    return jump_moves(board, square, color, KNIGHT_JUMPS)


def king_moves(board: Board, square: Square, color: str) -> list[Move]:
    """Return the one-step moves of a king on the square (castling comes later)."""
    return jump_moves(board, square, color, KING_STEPS)


def slide(board: Board, square: Square, direction: Direction, color: str) -> list[Move]:
    """
    Walk from a square in one direction and return the moves along the way.

    Parameters
    ----------
    board : Board
        The board.
    square : Square
        The (row, col) of the sliding piece.
    direction : Direction
        The (row change, col change) of one step.
    color : str
        The color of the sliding piece.

    Returns
    -------
    list[Move]
        A move to each empty square until the walk reaches the edge or a piece. If
        that piece is an enemy, the capture is the last move in the list.
    """
    row, col = square
    row_change, col_change = direction
    moves = []
    row, col = row + row_change, col + col_change
    while on_board(row, col):
        target_piece = piece_at(board, (row, col))
        if target_piece == EMPTY:
            moves.append(Move(square, (row, col)))
        else:
            if color_of(target_piece) != color:
                moves.append(Move(square, (row, col)))
            break
        row, col = row + row_change, col + col_change
    return moves


def slider_moves(
    board: Board, square: Square, color: str, directions: list[Direction]
) -> list[Move]:
    """Return the moves of a rook, bishop, or queen, one direction at a time."""
    moves = []
    for direction in directions:
        moves += slide(board, square, direction, color)
    return moves


def main():
    empty = [["."] * 8 for _ in range(8)]
    print(
        f"Knight on a1: {len(knight_moves(empty, (7, 0), WHITE))} moves  (expected 2)"
    )
    print(
        f"Rook on d4: {len(slider_moves(empty, (4, 3), WHITE, ROOK_DIRECTIONS))} moves"
        "  (expected 14)"
    )


if __name__ == "__main__":
    main()
