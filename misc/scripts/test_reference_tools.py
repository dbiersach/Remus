"""test_reference_tools.py

Check that the reference tools used to cross-check Remus are installed and
agree with the counts the workshop expects. These tests exercise python-chess
only; the native engine's own tests are written lesson by lesson. The last test
checks that every run_tests.py names only files that sit in its own folder.
"""

import ast
from pathlib import Path

import chess

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder


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


def test_every_run_tests_names_files_in_its_own_folder() -> None:
    """A file name in run_tests.py must name a file beside it, or the tests skip it."""
    missing = []
    for run_tests in ROOT.glob("Day */**/run_tests.py"):
        tree = ast.parse(run_tests.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                name = node.value
                is_file_name = name.endswith(".py") and " " not in name
                if is_file_name and not (run_tests.parent / name).exists():
                    missing.append(f"{run_tests}: {name}")
    assert missing == []
