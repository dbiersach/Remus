#!/usr/bin/env -S uv run
"""exchange.py

Static exchange evaluation (SEE): add up a capture and every recapture on the same
square, each side always taking with its least valuable piece, without searching.
Quiescence search skips a capture whose exchange loses material, such as a queen
taking a pawn that a knight defends.

Coordinates: row 0 is rank 8, and column 0 is file a.
"""

from board import EMPTY, Board, Square, piece_at
from evaluation import PIECE_VALUES
from fen import state_from_fen
from moves import Move

KING_VALUE = 10_000  # The king can take last, but no exchange may win the king
KNIGHT_JUMPS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]


def exchange_value(piece: str) -> int:
    """Return a piece's value in an exchange: its centipawns, or KING_VALUE."""
    if piece.upper() == "K":
        return KING_VALUE
    return PIECE_VALUES[piece.upper()]


def step_toward(gap: int) -> int:
    """Return 1, -1, or 0: one step in the direction of the gap."""
    if gap > 0:
        return 1
    if gap < 0:
        return -1
    return 0


def attacks_square(board: Board, start: Square, target: Square) -> bool:
    """
    Return True if the piece on start attacks the target square.

    Parameters
    ----------
    board : Board
        The board.
    start : Square
        The (row, col) of the attacking piece.
    target : Square
        The (row, col) of the square.

    Returns
    -------
    bool
        True if the piece could capture on target. A rook, bishop, or queen needs
        every square between the two to be empty.
    """
    piece = piece_at(board, start)
    kind = piece.upper()
    row_gap = target[0] - start[0]
    col_gap = target[1] - start[1]
    if kind == "P":
        forward = -1 if piece == "P" else 1  # White pawns move toward row 0
        return row_gap == forward and abs(col_gap) == 1
    if kind == "N":
        return (row_gap, col_gap) in KNIGHT_JUMPS
    if kind == "K":
        return max(abs(row_gap), abs(col_gap)) == 1
    straight = row_gap == 0 or col_gap == 0
    diagonal = abs(row_gap) == abs(col_gap)
    if (row_gap, col_gap) == (0, 0):
        return False
    if kind == "R" and not straight:
        return False
    if kind == "B" and not diagonal:
        return False
    if kind == "Q" and not (straight or diagonal):
        return False
    row_step = step_toward(row_gap)
    col_step = step_toward(col_gap)
    row = start[0] + row_step
    col = start[1] + col_step
    while (row, col) != target:
        if board[row][col] != EMPTY:
            return False  # A piece in between blocks the line
        row += row_step
        col += col_step
    return True


def least_valuable_attacker(board: Board, target: Square, white: bool) -> Square | None:
    """Return the square of the cheapest piece of one side attacking target, or None."""
    best = None
    best_value = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == EMPTY or piece.isupper() != white:
                continue
            value = exchange_value(piece)
            if best is not None and value >= best_value:
                continue
            if attacks_square(board, (row, col), target):
                best = (row, col)
                best_value = value
    return best


def static_exchange(board: Board, move: Move) -> int:
    """
    Return the material a capture wins or loses once every recapture is made.

    Parameters
    ----------
    board : Board
        The board before the capture. It is unchanged when the function returns.
    move : Move
        A capture of a piece on move.to_square.

    Returns
    -------
    int
        The centipawns the moving side gains, if each side keeps recapturing with
        its cheapest piece and stops when one more recapture would lose. A queen
        taking a pawn defended by a knight returns 100 - 900 = -800.
    """
    work = []  # A copy, so pieces can leave and x-rays open
    for row in board:
        work.append(row[:])
    target = move.to_square
    gains = [exchange_value(piece_at(work, target))]
    mover = piece_at(work, move.from_square)
    on_square = exchange_value(mover)  # The value of the piece standing on target
    work[move.from_square[0]][move.from_square[1]] = EMPTY
    work[target[0]][target[1]] = mover
    white = not mover.isupper()  # The side that recaptures next
    while True:
        attacker = least_valuable_attacker(work, target, white)
        if attacker is None:
            break
        # The recapturing side wins the piece on target but gives back what it won
        gains.append(on_square - gains[-1])
        piece = piece_at(work, attacker)
        on_square = exchange_value(piece)
        work[attacker[0]][attacker[1]] = EMPTY
        work[target[0]][target[1]] = piece
        white = not white
    # Each side may stop recapturing: walk back from the last capture
    index = len(gains) - 1
    while index > 0:
        gains[index - 1] = -max(-gains[index - 1], gains[index])
        index -= 1
    return gains[0]


def main():
    state = state_from_fen("4k3/8/5n2/3p4/8/8/8/3QK3 w - - 0 1")
    queen_takes = Move((7, 3), (3, 3))
    print(f"Qxd5, defended by a knight: {static_exchange(state['board'], queen_takes)}")
    print("  (expected -800: the queen wins a pawn and is taken)")
    state = state_from_fen("4k3/8/8/3p4/4P3/8/8/4K3 w - - 0 1")
    pawn_takes = Move((4, 4), (3, 3))
    print(f"exd5, undefended: {static_exchange(state['board'], pawn_takes)}")
    print("  (expected 100)")


if __name__ == "__main__":
    main()
