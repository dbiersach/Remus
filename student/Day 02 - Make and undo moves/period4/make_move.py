#!/usr/bin/env -S uv run
"""make_move.py

Make a move on the game state, and undo it exactly. make_move returns an undo
record that holds everything the move changed, so undo_move can put it all back.
"""

from board import EMPTY, piece_at, print_board, set_piece
from game_state import BLACK, new_game, opponent
from moves import Move, move_from_uci


def make_move(state: dict, move: Move) -> dict:
    """
    Make a quiet move or a capture, and return the record needed to undo it.

    Parameters
    ----------
    state : dict
        The game state. It changes in place.
    move : Move
        The move to make. It must be a move the side to move may play.

    Returns
    -------
    dict
        The undo record: the move, the piece that moved, the piece it captured,
        and the old values of every state field the move changes.
    """
    # Day 2, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 2 P4: write make_move()")


def undo_move(state: dict, undo: dict) -> None:
    """
    Take back the move described by an undo record.

    Parameters
    ----------
    state : dict
        The game state, as make_move left it. It changes in place.
    undo : dict
        The record make_move returned for this move.
    """
    # Day 2, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 2 P4: write undo_move()")


def state_snapshot(state: dict) -> str:
    """Return the whole state as text, so two states can be compared with ==."""
    rows = ["".join(row) for row in state["board"]]
    fields = [
        state["turn"],
        state["castling"],
        str(state["en_passant"]),
        str(state["halfmove_clock"]),
        str(state["fullmove_number"]),
    ]
    return "/".join(rows) + " " + " ".join(fields)


def main():
    state = new_game()
    start = state_snapshot(state)
    texts = [
        "e2e4",
        "e7e5",
        "g1f3",
        "b8c6",
        "f1b5",
        "a7a6",
        "b5c6",
        "d7c6",
        "e1f1",
        "g8f6",
    ]
    undo_records = []
    for text in texts:
        undo_records.append(make_move(state, move_from_uci(text)))
    print_board(state["board"])
    for undo in reversed(undo_records):
        undo_move(state, undo)
    same = state_snapshot(state) == start
    print(f"Ten moves made and undone, back at the start: {same}  (expected True)")


if __name__ == "__main__":
    main()
