#!/usr/bin/env -S uv run
"""legal_moves.py

Keep only the legal moves: a move is legal if, after it is made, the mover's own
king is not attacked. Testing after the move catches pins, discovered checks, and
a king stepping into check, all with one rule. Castling has extra conditions,
so castling_moves checks them before the move joins the list.
"""

from attacks import in_check, is_square_attacked
from board import EMPTY, piece_at
from game_state import WHITE, new_game, opponent
from make_move import make_move, undo_move
from move_generation import pseudo_legal_moves
from moves import Move

CASTLES = [  # (right, king from, king to, squares that must be empty, square the king crosses)
    ("K", (7, 4), (7, 6), [(7, 5), (7, 6)], (7, 5)),
    ("Q", (7, 4), (7, 2), [(7, 3), (7, 2), (7, 1)], (7, 3)),
    ("k", (0, 4), (0, 6), [(0, 5), (0, 6)], (0, 5)),
    ("q", (0, 4), (0, 2), [(0, 3), (0, 2), (0, 1)], (0, 3)),
]


def castling_moves(state: dict) -> list[Move]:
    """
    Return the castling moves the side to move may make.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    list[Move]
        The king's two-square moves whose castling right remains, with empty
        squares between king and rook, the king not in check, and the square the
        king crosses not attacked. The legal filter checks the landing square.
    """
    color = state["turn"]
    board = state["board"]
    enemy = opponent(color)
    moves = []
    for right, king_from, king_to, must_be_empty, crossed in CASTLES:
        if right not in state["castling"] or right.isupper() != (color == WHITE):
            continue
        if any(piece_at(board, square) != EMPTY for square in must_be_empty):
            continue
        if in_check(state, color) or is_square_attacked(board, king_to, enemy):
            continue
        moves.append(Move(king_from, king_to))
    return moves


def legal_moves(state: dict) -> list[Move]:
    """
    Return every legal move for the side to move.

    Parameters
    ----------
    state : dict
        The game state. Each move is made and undone, so the state ends unchanged.

    Returns
    -------
    list[Move]
        The pseudo-legal moves that do not leave the mover's king in check.
    """
    mover = state["turn"]
    moves = []
    for move in pseudo_legal_moves(state) + castling_moves(state):
        undo = make_move(state, move)
        if not in_check(state, mover):
            moves.append(move)
        undo_move(state, undo)
    return moves


def main():
    state = new_game()
    print(f"Legal moves from the start: {len(legal_moves(state))}  (expected 20)")


if __name__ == "__main__":
    main()
