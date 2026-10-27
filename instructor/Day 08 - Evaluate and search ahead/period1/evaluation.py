#!/usr/bin/env -S uv run
"""evaluation.py

Score a position in centipawns (hundredths of a pawn) without looking ahead.
A positive score is good for White. The score is the material: the value of
every piece on the board.
"""

from board import EMPTY
from fen import START_FEN, state_from_fen

PIECE_VALUES = {
    "P": 100,
    "N": 300,
    "B": 300,
    "R": 500,
    "Q": 900,
    "K": 0,
}  # In centipawns


def material(board: list[list[str]]) -> int:
    """
    Return the material balance in centipawns, positive when White is ahead.

    Parameters
    ----------
    board : list[list[str]]
        The board.

    Returns
    -------
    int
        White's piece values minus Black's.
    """
    score = 0
    for row in board:
        for piece in row:
            if piece == EMPTY:
                continue
            if piece.isupper():
                score += PIECE_VALUES[piece]
            else:
                score -= PIECE_VALUES[piece.upper()]
    return score


def evaluate(state: dict) -> int:
    """
    Score the position for the side to move.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    int
        Material in centipawns, positive when the side to move
        stands better. Negamax search needs the score from the mover's side.
    """
    white_score = material(state["board"])
    return white_score if state["turn"] == "w" else -white_score


def explain_evaluation(state: dict) -> None:
    """Print each term of the evaluation, so Remus can say why it likes a position."""
    board = state["board"]
    print(f"  Material:  {material(board):+} centipawns for White")
    print(f"  Score for the side to move ({state['turn']}): {evaluate(state):+}")


def main():
    print("Start position:")
    explain_evaluation(state_from_fen(START_FEN))
    print("  (expected 0 for every term: the position is symmetric)")
    print("White knight against a Black rook:")
    explain_evaluation(state_from_fen("r3k3/8/8/4N3/8/8/8/4K3 w - - 0 1"))
    print("  (expected material -200: the rook is worth 200 more than the knight)")


if __name__ == "__main__":
    main()
