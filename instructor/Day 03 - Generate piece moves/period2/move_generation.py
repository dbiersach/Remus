#!/usr/bin/env -S uv run
"""move_generation.py

Generate pseudo-legal moves: every move the pieces can make by their movement rules,
before checking whether the move leaves the mover's own king in check.

Directions are (row change, col change) pairs. Row 0 is rank 8, so White pawns move
toward row 0 (a row change of -1) and Black pawns move toward row 7 (+1).
"""

from board import Board, Square, piece_at
from game_state import WHITE, color_of
from moves import Move

Direction = tuple[int, int]  # A (row change, col change) step, such as (-1, 0)
KNIGHT_JUMPS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
KING_STEPS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


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


def main():
    empty = [["."] * 8 for _ in range(8)]
    print(
        f"Knight on a1: {len(knight_moves(empty, (7, 0), WHITE))} moves  (expected 2)"
    )
    print(f"King on a1: {len(king_moves(empty, (7, 0), WHITE))} moves  (expected 3)")


if __name__ == "__main__":
    main()
