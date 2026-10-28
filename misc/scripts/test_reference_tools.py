"""test_reference_tools.py

Check that the reference tools used to cross-check Remus are installed and
agree with the counts the workshop expects. These tests exercise python-chess
only; the native engine's own tests are written lesson by lesson.
"""

import chess


def test_python_chess_counts_twenty_moves_from_the_start() -> None:
    """The starting position has 16 pawn moves and 4 knight moves."""
    board = chess.Board()
    assert board.legal_moves.count() == 20


def test_python_chess_perft_depth_two_from_the_start() -> None:
    """Each of White's 20 moves leaves Black 20 replies: 400 positions."""
    board = chess.Board()
    count = 0
    for move in list(board.legal_moves):
        board.push(move)
        count += board.legal_moves.count()
        board.pop()
    assert count == 400
