#!/usr/bin/env -S uv run
"""notation.py

Write and read moves in Standard Algebraic Notation (SAN), the notation people use:
"e4", "Nf3", "Bxh8", "O-O", "e8=Q+", "Nbd2".

Reading SAN uses a simple idea: write the SAN of every legal move, and pick the one
that matches what the player typed.
"""

from attacks import in_check
from board import EMPTY, FILES, piece_at, square_name
from fen import state_from_fen
from legal_moves import legal_moves
from make_move import make_move, undo_move
from moves import Move


def move_to_san(state: dict, move: Move) -> str:
    """
    Return the SAN text of a legal move in the current position.

    Parameters
    ----------
    state : dict
        The game state before the move. It is unchanged when the function returns.
    move : Move
        A legal move.

    Returns
    -------
    str
        The SAN text, with "+" for check and "#" for checkmate.
    """
    board = state["board"]
    piece = piece_at(board, move.from_square)
    kind = piece.upper()
    target = square_name(*move.to_square)
    is_capture = piece_at(board, move.to_square) != EMPTY or (
        kind == "P" and move.to_square == state["en_passant"]
    )

    if kind == "K" and abs(move.to_square[1] - move.from_square[1]) == 2:
        text = "O-O" if move.to_square[1] == 6 else "O-O-O"
    elif kind == "P":
        text = FILES[move.from_square[1]] + "x" + target if is_capture else target
        if move.promotion is not None:
            text += "=" + move.promotion.upper()
    else:
        text = (
            kind
            + disambiguation(state, move, piece)
            + ("x" if is_capture else "")
            + target
        )

    undo = make_move(state, move)
    if in_check(state, state["turn"]):
        text += "#" if not legal_moves(state) else "+"
    undo_move(state, undo)
    return text


def disambiguation(state: dict, move: Move, piece: str) -> str:
    """
    Return the file, rank, or square that tells this move apart from another
    legal move by the same kind of piece to the same square, such as "b" in "Nbd2".
    """
    rivals = [
        other.from_square
        for other in legal_moves(state)
        if other.to_square == move.to_square
        and other.from_square != move.from_square
        and piece_at(state["board"], other.from_square) == piece
    ]
    if not rivals:
        return ""
    row, col = move.from_square
    if all(rival[1] != col for rival in rivals):
        return FILES[col]
    if all(rival[0] != row for rival in rivals):
        return str(8 - row)
    return square_name(row, col)


def parse_san(state: dict, text: str) -> Move:
    """
    Find the legal move that a SAN text describes.

    Parameters
    ----------
    state : dict
        The game state.
    text : str
        SAN typed by a player, such as "Nf3", "exd5", or "O-O". A trailing "+",
        "#", "!", or "?" is ignored, and "0-0" is accepted for "O-O".

    Returns
    -------
    Move
        The matching legal move.

    Raises
    ------
    ValueError
        If no legal move matches.
    """
    wanted = text.strip().rstrip("+#!?").replace("0", "O")
    for move in legal_moves(state):
        if move_to_san(state, move).rstrip("+#") == wanted:
            return move
    raise ValueError(f"Not a legal move here: {text!r}")


def main():
    state = state_from_fen("r3k2r/8/8/8/8/8/8/R3K1NR w KQkq - 0 1")
    sans = sorted(move_to_san(state, move) for move in legal_moves(state))
    print(" ".join(sans))
    print(f"parse_san('O-O-O') gives {parse_san(state, 'O-O-O')}")
    print("  (expected Move(from_square=(7, 4), to_square=(7, 2), promotion=None))")


if __name__ == "__main__":
    main()
