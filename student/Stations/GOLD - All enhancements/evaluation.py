#!/usr/bin/env -S uv run
"""evaluation.py

Score a position in centipawns (hundredths of a pawn) without looking ahead.
A positive score is good for White. Two terms make up the score:

1. Material: the value of every piece on the board.
2. Placement: a bonus or penalty from a piece-square table, such as a knight
   in the center (it attacks eight squares) against a knight in the corner (two).

Each table is written from White's side, row 0 (rank 8) first. A Black piece reads
the table upside down, so its row 7 uses the table's row 0.

Day 10 adds two upgrade-station terms, both ideas from Turbo GameWorks Chess:

3. Pawn structure: penalties for doubled and isolated pawns, a bonus for passed pawns.
4. Mating: with a big material lead, drive the losing king to the edge and bring
   the winning king close, so Remus can finish off a won endgame.
5. King safety: while the enemy queen is on the board, a bonus for each pawn that
   shelters the king from in front.
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
QUEEN_TABLE = [[0] * 8 for _ in range(8)]  # The queen is strong anywhere
DOUBLED_PAWN = 8  # Penalty for each pawn that shares its file with another of its color
ISOLATED_PAWN = (
    20  # Penalty for a pawn with no friendly pawn on either neighboring file
)
PASSED_PAWN = [0, 10, 20, 40, 60, 70]  # Bonus for a passed pawn, by squares advanced
CENTER_DISTANCE = [3, 2, 1, 0, 0, 1, 2, 3]  # How far a row or column is from the center
MATING_MARGIN = 200  # A lead of at least a rook for a bishop starts the mating term
WEAK_SIDE_LIMIT = 600  # ... when the losing side has at most two bishops' worth left
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


def pawn_structure(board: list[list[str]]) -> int:
    """
    Score the pawn structure in centipawns, positive when it favors White.

    Parameters
    ----------
    board : list[list[str]]
        The board.

    Returns
    -------
    int
        For each side: a penalty for every doubled pawn and every isolated pawn,
        and a bonus for every passed pawn (no enemy pawn ahead of it on its own
        file or a neighboring file), bigger the further it has advanced.
    """
    score = 0
    for pawn, enemy, sign in (("P", "p", 1), ("p", "P", -1)):
        files = [0] * 8
        for row in range(8):
            for col in range(8):
                if board[row][col] == pawn:
                    files[col] += 1
        for row in range(8):
            for col in range(8):
                if board[row][col] != pawn:
                    continue
                if files[col] > 1:
                    score -= sign * DOUBLED_PAWN
                left = files[col - 1] if col > 0 else 0
                right = files[col + 1] if col < 7 else 0
                if left == 0 and right == 0:
                    score -= sign * ISOLATED_PAWN
                ahead = (
                    range(row) if pawn == "P" else range(row + 1, 8)
                )  # White moves to row 0
                blocked = any(
                    board[r][c] == enemy
                    for r in ahead
                    for c in (col - 1, col, col + 1)
                    if 0 <= c < 8
                )
                if not blocked:
                    advanced = 6 - row if pawn == "P" else row - 1
                    score += sign * PASSED_PAWN[advanced]
    return score


def mating_bonus(board: list[list[str]]) -> int:
    """
    Return a bonus for cornering the losing king, positive when it favors White.

    Parameters
    ----------
    board : list[list[str]]
        The board.

    Returns
    -------
    int
        0 unless one side leads by at least MATING_MARGIN and the other side has
        at most WEAK_SIDE_LIMIT of material left. Then 10 points for each step the
        losing king stands from the center, and 4 points for each step the
        winning king has closed toward it.
    """
    white_material = 0
    black_material = 0
    kings = {}
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in "Kk":
                kings[piece] = (row, col)
            elif piece != EMPTY:
                if piece.isupper():
                    white_material += PIECE_VALUES[piece]
                else:
                    black_material += PIECE_VALUES[piece.upper()]
    lead = white_material - black_material
    weaker = min(white_material, black_material)
    if abs(lead) < MATING_MARGIN or weaker > WEAK_SIDE_LIMIT:
        return 0
    winner, loser = ("K", "k") if lead > 0 else ("k", "K")
    loser_row, loser_col = kings[loser]
    winner_row, winner_col = kings[winner]
    edge = CENTER_DISTANCE[loser_row] + CENTER_DISTANCE[loser_col]
    kings_apart = max(abs(loser_row - winner_row), abs(loser_col - winner_col))
    bonus = 10 * edge + 4 * (7 - kings_apart)
    return bonus if lead > 0 else -bonus


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
    score = 0
    # White's pawns stand in front of its king at smaller rows, since row 0 is rank 8
    for king, pawn, enemy_queen, forward, sign in (
        ("K", "P", "q", -1, 1),
        ("k", "p", "Q", 1, -1),
    ):
        if not any(enemy_queen in row for row in board):
            continue
        for row in range(8):
            for col in range(8):
                if board[row][col] != king:
                    continue
                for file in (col - 1, col, col + 1):
                    if not 0 <= file < 8:
                        continue
                    for step in (1, 2):
                        ahead = row + forward * step
                        if 0 <= ahead < 8 and board[ahead][file] == pawn:
                            score += sign * SHIELD_PAWN
                            break
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
        Material, placement, pawn structure, the mating bonus, and king safety in
        centipawns, positive when the side to move stands better. Negamax search needs the
        score from the mover's side.
    """
    board = state["board"]
    white_score = (
        material(board)
        + placement(board)
        + pawn_structure(board)
        + mating_bonus(board)
        + king_safety(board)
    )
    return white_score if state["turn"] == "w" else -white_score


def explain_evaluation(state: dict) -> None:
    """Print each term of the evaluation, so Remus can say why it likes a position."""
    board = state["board"]
    print(f"  Material:  {material(board):+} centipawns for White")
    print(f"  Placement: {placement(board):+} centipawns for White")
    print(f"  Pawns:     {pawn_structure(board):+} centipawns for White")
    print(f"  Mating:    {mating_bonus(board):+} centipawns for White")
    print(f"  King:      {king_safety(board):+} centipawns for White")
    print(f"  Score for the side to move ({state['turn']}): {evaluate(state):+}")


def main():
    print("Start position:")
    explain_evaluation(state_from_fen(START_FEN))
    print("  (expected 0 for every term: the position is symmetric)")
    print("White knight on e5 against a Black knight on a8:")
    explain_evaluation(state_from_fen("n3k3/8/8/4N3/8/8/8/4K3 w - - 0 1"))
    print("  (expected material 0, placement in White's favor)")
    print("Rook endgame, Black king in the corner:")
    explain_evaluation(state_from_fen("k7/8/2K5/8/8/8/8/7R w - - 0 1"))
    print("  (expected a mating bonus for White)")
    print("White castled behind three pawns, Black king in the open:")
    explain_evaluation(state_from_fen("q3k3/8/8/8/8/8/5PPP/6K1 w - - 0 1"))
    print("  (expected king safety +45 for White)")


if __name__ == "__main__":
    main()
