#!/usr/bin/env -S uv run
"""fen.py

Read and write FEN (Forsyth-Edwards Notation), the one-line text that describes a
whole chess position. The start position is:

    rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

The six fields are the pieces (rank 8 first), the side to move, the castling rights,
the en passant square, the halfmove clock, and the fullmove number.
"""

from board import EMPTY, Board, parse_square, print_board, square_name

# The start position
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# The position after 1. e4, with Black to move
AFTER_E4_FEN = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"


def fen_placement(board: Board) -> str:
    """
    Return the piece-placement field of FEN for a board.

    Parameters
    ----------
    board : Board
        The board, row 0 (rank 8) first.

    Returns
    -------
    str
        One group per rank, rank 8 first, separated by "/". A digit counts the
        empty squares in a row, so an empty rank is "8".
    """
    # Day 6, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 6 P4: write fen_placement()")


def board_from_placement(text: str) -> Board:
    """
    Build a board from the piece-placement field of FEN.

    Parameters
    ----------
    text : str
        The placement field, such as "8/8/8/4k3/8/8/8/4K3".

    Returns
    -------
    Board
        The board, row 0 (rank 8) first.
    """
    # Day 6, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 6 P4: write board_from_placement()")


def state_from_fen(fen: str) -> dict:
    """Build a game state from a full FEN string."""
    fields = fen.split()
    state = {
        "board": board_from_placement(fields[0]),
        "turn": fields[1],
        "castling": "" if fields[2] == "-" else fields[2],
        "en_passant": None if fields[3] == "-" else parse_square(fields[3]),
        "halfmove_clock": int(fields[4]) if len(fields) > 4 else 0,
        "fullmove_number": int(fields[5]) if len(fields) > 5 else 1,
    }
    return state


def state_to_fen(state: dict) -> str:
    """Write a game state as a full FEN string."""
    en_passant = (
        "-" if state["en_passant"] is None else square_name(*state["en_passant"])
    )
    castling = state["castling"] or "-"  # FEN writes "-" when no one can castle
    fen = f"{fen_placement(state['board'])} {state['turn']} {castling} {en_passant}"
    return fen + f" {state['halfmove_clock']} {state['fullmove_number']}"


def print_state(state: dict) -> None:
    """
    Print a game state the way a person reads it: the board, then each FEN field
    with its meaning, then the whole FEN string.

    Parameters
    ----------
    state : dict
        The game state, such as one from state_from_fen().
    """
    print_board(state["board"])
    turn = "White" if state["turn"] == "w" else "Black"
    castling = state["castling"] or "nobody"  # An empty string means no rights left
    en_passant = "none"
    if state["en_passant"] is not None:
        en_passant = square_name(*state["en_passant"])
    print(f"Side to move:      {turn}")
    print(f"Castling rights:   {castling}  (K and Q for White, k and q for Black)")
    print(f"En passant square: {en_passant}")
    print(
        f"Halfmove clock:    {state['halfmove_clock']}  "
        "(moves since the last capture or pawn move)"
    )
    print(f"Fullmove number:   {state['fullmove_number']}")
    print(f"FEN: {state_to_fen(state)}")


def main():
    # The position after 1. e4: Black to move, and e3 is the en passant square
    print_state(state_from_fen(AFTER_E4_FEN))
    print("  (expected: Black to move, en passant square e3)")
    state = state_from_fen(START_FEN)
    same = state_to_fen(state) == START_FEN
    print(f"Start FEN read and written back unchanged: {same}  (expected True)")


if __name__ == "__main__":
    main()
