#!/usr/bin/env -S uv run
"""game_state.py

Hold everything about a game that the board alone does not show: whose turn it is,
which castling moves are still allowed, the en passant target, and the move clocks.
"""

from board import EMPTY, new_board, print_board

WHITE = "w"  # White's color, as FEN writes it
BLACK = "b"  # Black's color


def new_game() -> dict:
    """
    Return the state of a new game.

    Returns
    -------
    dict
        board : the 8x8 board, row 0 is rank 8.
        turn : "w" or "b", the side to move.
        castling : the castling moves still allowed, "KQkq" at the start.
        en_passant : the square a pawn just skipped over, or None.
        halfmove_clock : moves since the last capture or pawn move.
        fullmove_number : starts at 1 and grows after each Black move.
    """
    return {
        "board": new_board(),
        "turn": WHITE,
        "castling": "KQkq",
        "en_passant": None,
        "halfmove_clock": 0,
        "fullmove_number": 1,
    }


def is_white(piece: str) -> bool:
    """Return True if the piece is White (an uppercase letter)."""
    return piece.isupper()


def color_of(piece: str) -> str | None:
    """Return "w" or "b" for a piece, or None for an empty square."""
    if piece == EMPTY:
        return None
    if is_white(piece):
        return WHITE
    return BLACK


def opponent(color: str) -> str:
    """Return the other side's color."""
    if color == WHITE:
        return BLACK
    return WHITE


def main():
    state = new_game()
    print_board(state["board"])
    print(f"Side to move: {state['turn']}  (expected w)")
    print(
        f"Color of N: {color_of('N')}, of p: {color_of('p')}, of .: {color_of(EMPTY)}"
    )
    print("  (expected w, b, None)")


if __name__ == "__main__":
    main()
