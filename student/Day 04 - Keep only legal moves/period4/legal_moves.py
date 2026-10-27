#!/usr/bin/env -S uv run
"""legal_moves.py

Keep only the legal moves: a move is legal if, after it is made, the mover's own
king is not attacked. Testing after the move catches pins, discovered checks, and
a king stepping into check, all with one rule.
"""

from attacks import in_check
from game_state import new_game
from make_move import make_move, undo_move
from move_generation import pseudo_legal_moves
from moves import Move


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
    for move in pseudo_legal_moves(state):
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
