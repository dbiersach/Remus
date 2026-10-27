#!/usr/bin/env -S uv run
"""evaluation.py

Score a position in centipawns (hundredths of a pawn) without looking ahead.
A positive score is good for White. Two terms make up the score:

1. Material: the value of every piece on the board.
2. Placement: a bonus or penalty from a piece-square table, such as a knight
   in the center (it attacks eight squares) against a knight in the corner (two).

Each table is written from White's side, row 0 (rank 8) first. A Black piece reads
the table upside down, so its row 7 uses the table's row 0.

The GRAY station adds a third term, king_safety.
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

PAWN_TABLE = [  # Pawns gain as they advance, most in the center
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
KNIGHT_TABLE = [  # Knights belong in the center, where they reach eight squares
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
]
BISHOP_TABLE = [  # Bishops like long open diagonals, not corners
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20],
]
ROOK_TABLE = [  # Rooks like the seventh rank and the center files
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0],
]
KING_TABLE = [  # The king hides behind its pawns until the endgame
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20],
]
QUEEN_TABLE = [  # The queen is strong anywhere
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
SHIELD_PAWN = (
    15  # Bonus for each pawn on the king's file or a neighbor, 1 or 2 rows ahead
)
PLACEMENT_TABLES = {
    "P": PAWN_TABLE,
    "N": KNIGHT_TABLE,
    "B": BISHOP_TABLE,
    "R": ROOK_TABLE,
    "Q": QUEEN_TABLE,
    "K": KING_TABLE,
}


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


def placement(board: list[list[str]]) -> int:
    """Return the piece-square bonus in centipawns, positive when it favors White."""
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == EMPTY:
                continue
            table = PLACEMENT_TABLES[piece.upper()]
            if piece.isupper():
                score += table[row][col]
            else:
                score -= table[7 - row][col]  # Black reads the table upside down
    return score


def king_safety(board: list[list[str]]) -> int:
    """
    Score the pawn shields in front of both kings, positive when it favors White.

    Parameters
    ----------
    board : list[list[str]]
        The board.

    Returns
    -------
    int
        For each king facing an enemy queen: SHIELD_PAWN for every file (the king's
        own and its two neighbors) with a friendly pawn one or two rows in front of
        the king. A White king on g1 behind pawns on f2, g2, and h2 earns 45. Once the
        queens are gone the king is safe enough to walk forward, so the term is 0.
    """
    # Day 9, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 9 P2: write king_safety()")


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
        Material, placement, and king safety in centipawns, positive when the side
        to move
        stands better. Negamax search needs the score from the mover's side.
    """
    board = state["board"]
    white_score = material(board) + placement(board) + king_safety(board)
    return white_score if state["turn"] == "w" else -white_score


def explain_evaluation(state: dict) -> None:
    """Print each term of the evaluation, so Remus can say why it likes a position."""
    board = state["board"]
    print(f"  Material:  {material(board):+} centipawns for White")
    print(f"  Placement: {placement(board):+} centipawns for White")
    print(f"  King:      {king_safety(board):+} centipawns for White")
    print(f"  Score for the side to move ({state['turn']}): {evaluate(state):+}")


def main():
    print("Start position:")
    explain_evaluation(state_from_fen(START_FEN))
    print("  (expected 0 for every term: the position is symmetric)")
    print("White knight on e5 against a Black knight on a8:")
    explain_evaluation(state_from_fen("n3k3/8/8/4N3/8/8/8/4K3 w - - 0 1"))
    print("  (expected material 0, placement in White's favor)")


if __name__ == "__main__":
    main()
