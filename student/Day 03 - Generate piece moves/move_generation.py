#!/usr/bin/env -S uv run
"""move_generation.py

Generate pseudo-legal moves: every move the pieces can make by their movement rules,
before checking whether the move leaves the mover's own king in check.

Directions are (row change, col change) pairs. Row 0 is rank 8, so White pawns move
toward row 0 (a row change of -1) and Black pawns move toward row 7 (+1).
"""

from board import EMPTY, piece_at
from game_state import BLACK, WHITE, color_of, new_game
from moves import Move

KNIGHT_JUMPS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
KING_STEPS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
ROOK_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Along ranks and files
BISHOP_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Along diagonals
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS
PROMOTION_PIECES = "QRBN"  # A pawn on the last rank may become any of these


def on_board(row: int, col: int) -> bool:
    """Return True if (row, col) is one of the 64 squares."""
    return 0 <= row < 8 and 0 <= col < 8


def jump_moves(
    board: list[list[str]],
    square: tuple[int, int],
    color: str,
    offsets: list[tuple[int, int]],
) -> list[Move]:
    """
    Return the moves of a piece that jumps by fixed offsets (a knight or a king).

    Parameters
    ----------
    board : list[list[str]]
        The board.
    square : tuple[int, int]
        The (row, col) of the jumping piece.
    color : str
        The color of the jumping piece, "w" or "b".
    offsets : list[tuple[int, int]]
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


def knight_moves(
    board: list[list[str]], square: tuple[int, int], color: str
) -> list[Move]:
    """Return the moves of a knight on the square."""
    return jump_moves(board, square, color, KNIGHT_JUMPS)


def king_moves(
    board: list[list[str]], square: tuple[int, int], color: str
) -> list[Move]:
    """Return the one-step moves of a king on the square (castling comes later)."""
    # Day 3, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 3 P2: write king_moves()")


def slide(
    board: list[list[str]],
    square: tuple[int, int],
    direction: tuple[int, int],
    color: str,
) -> list[Move]:
    """
    Walk from a square in one direction and return the moves along the way.

    Parameters
    ----------
    board : list[list[str]]
        The board.
    square : tuple[int, int]
        The (row, col) of the sliding piece.
    direction : tuple[int, int]
        The (row change, col change) of one step.
    color : str
        The color of the sliding piece.

    Returns
    -------
    list[Move]
        A move to each empty square until the walk reaches the edge or a piece. If
        that piece is an enemy, the capture is the last move in the list.
    """
    # Day 3, period 3: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 3 P3: write slide()")


def slider_moves(
    board: list[list[str]],
    square: tuple[int, int],
    color: str,
    directions: list[tuple[int, int]],
) -> list[Move]:
    """Return the moves of a rook, bishop, or queen, one direction at a time."""
    moves = []
    for direction in directions:
        moves += slide(board, square, direction, color)
    return moves


def pawn_moves_to(
    square: tuple[int, int], target: tuple[int, int], color: str
) -> list[Move]:
    """Return a pawn move, or the four promotion moves if it reaches the last rank."""
    last_row = 0 if color == WHITE else 7
    if target[0] != last_row:
        return [Move(square, target)]
    moves = []
    for piece in PROMOTION_PIECES:
        promotion = piece if color == WHITE else piece.lower()
        moves.append(Move(square, target, promotion))
    return moves


def pawn_pushes(
    board: list[list[str]], square: tuple[int, int], color: str
) -> list[Move]:
    """
    Return a pawn's forward moves: one step, or two steps from its starting rank.

    Parameters
    ----------
    board : list[list[str]]
        The board.
    square : tuple[int, int]
        The (row, col) of the pawn.
    color : str
        The color of the pawn.

    Returns
    -------
    list[Move]
        The pushes onto empty squares. A pawn never captures straight ahead.
    """
    # Day 3, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 3 P4: write pawn_pushes()")


def pawn_captures(
    board: list[list[str]], square: tuple[int, int], color: str
) -> list[Move]:
    """Return a pawn's diagonal captures of enemy pieces."""
    row, col = square
    forward = -1 if color == WHITE else 1
    moves = []
    for col_change in (-1, 1):
        target = (row + forward, col + col_change)
        if on_board(*target):
            target_color = color_of(piece_at(board, target))
            if target_color is not None and target_color != color:
                moves += pawn_moves_to(square, target, color)
    return moves


def piece_moves(board: list[list[str]], square: tuple[int, int]) -> list[Move]:
    """Return the pseudo-legal moves of whatever piece stands on the square."""
    piece = piece_at(board, square)
    color = WHITE if piece.isupper() else BLACK  # The square holds a piece, never EMPTY
    kind = piece.upper()
    if kind == "N":
        return knight_moves(board, square, color)
    if kind == "K":
        return king_moves(board, square, color)
    if kind == "R":
        return slider_moves(board, square, color, ROOK_DIRECTIONS)
    if kind == "B":
        return slider_moves(board, square, color, BISHOP_DIRECTIONS)
    if kind == "Q":
        return slider_moves(board, square, color, QUEEN_DIRECTIONS)
    if kind == "P":
        return pawn_pushes(board, square, color) + pawn_captures(board, square, color)
    return []


def pseudo_legal_moves(state: dict) -> list[Move]:
    """
    Return every pseudo-legal move for the side to move.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    list[Move]
        The moves of every piece of the side to move, by movement rules alone.
    """
    board = state["board"]
    moves = []
    for row in range(8):
        for col in range(8):
            if color_of(board[row][col]) == state["turn"]:
                moves += piece_moves(board, (row, col))
    return moves


def main():
    state = new_game()
    print(
        f"Pseudo-legal moves from the start: {len(pseudo_legal_moves(state))}  (expected 20)"
    )
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
