#!/usr/bin/env -S uv run
"""fen.py

Read and write FEN (Forsyth-Edwards Notation), the one-line text that describes a
whole chess position. The start position is:

    rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

The six fields are the pieces (rank 8 first), the side to move, the castling rights,
the en passant square, the halfmove clock, and the fullmove number.
"""

from board import EMPTY, Board, parse_square, print_board, square_name
from game_state import position_key

# The start position
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


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
    placement = ""
    for row in board:
        text = ""
        empty_count = 0
        for piece in row:
            if piece == EMPTY:
                empty_count += 1
            else:
                if empty_count > 0:
                    text += str(empty_count)
                    empty_count = 0
                text += piece
        if empty_count > 0:
            text += str(empty_count)
        if placement != "":
            placement += "/"  # A slash separates one rank from the next
        placement += text
    return placement


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
    board = []
    for rank_text in text.split("/"):
        row = []
        for character in rank_text:
            if character.isdigit():
                row += [EMPTY] * int(character)
            else:
                row.append(character)
        if len(row) != 8:
            raise ValueError(f"A FEN rank must describe 8 squares: {rank_text!r}")
        board.append(row)
    if len(board) != 8:
        raise ValueError(f"FEN must describe 8 ranks: {text!r}")
    return board


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
    state["history"] = [position_key(state)]
    return state


def state_to_fen(state: dict) -> str:
    """Write a game state as a full FEN string."""
    en_passant = (
        "-" if state["en_passant"] is None else square_name(*state["en_passant"])
    )
    castling = state["castling"] or "-"  # FEN writes "-" when no one can castle
    fen = f"{fen_placement(state['board'])} {state['turn']} {castling} {en_passant}"
    return fen + f" {state['halfmove_clock']} {state['fullmove_number']}"


def main():
    state = state_from_fen(START_FEN)
    print_board(state["board"])
    same = state_to_fen(state) == START_FEN
    print(f"Start FEN read and written back unchanged: {same}  (expected True)")


if __name__ == "__main__":
    main()
