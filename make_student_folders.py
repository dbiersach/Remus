#!/usr/bin/env -S uv run
"""make_student_folders.py

Build the student/ folder from the finished code in instructor/.

student/ mirrors instructor/ day by day and period by period. Each student period
folder holds the same files as the instructor period folder, except that the
functions the students write in that period are stubs: the signature and docstring
stay, and the body raises NotImplementedError. The tests stay complete, so they
fail until the pair writes each function. Functions from earlier periods are
complete, so every period folder starts from working code.

Run this script again whenever the instructor code changes, after
make_period_folders.py.
"""

import ast
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
INSTRUCTOR = ROOT / "instructor"
STUDENT = ROOT / "student"

# (day, period, file, function) for every function the students write
STUDENT_FUNCTIONS = [
    (1, 4, "board.py", "print_board"),
    (1, 4, "board.py", "square_name"),
    (1, 4, "board.py", "parse_square"),
    (1, 4, "board.py", "piece_at"),
    (2, 3, "game_state.py", "is_white"),
    (2, 3, "game_state.py", "color_of"),
    (2, 3, "moves.py", "move_to_uci"),
    (2, 3, "moves.py", "move_from_uci"),
    (2, 4, "make_move.py", "undo_move"),
    (2, 4, "make_move.py", "state_snapshot"),
    (3, 2, "move_generation.py", "king_moves"),
    (3, 3, "move_generation.py", "slide"),
    (3, 4, "move_generation.py", "pawn_pushes"),
    (4, 2, "attacks.py", "attacked_by_knight"),
    (4, 2, "attacks.py", "attacked_by_pawn"),
    (4, 2, "attacks.py", "attacked_by_king"),
    (4, 3, "attacks.py", "in_check"),
    (4, 3, "legal_moves.py", "legal_moves"),
    (5, 2, "make_move.py", "update_castling_rights"),
    (5, 3, "make_move.py", "en_passant_victim_square"),
    (6, 2, "perft.py", "perft"),
    (7, 1, "fen.py", "fen_placement"),
    (7, 1, "fen.py", "board_from_placement"),
    (7, 2, "game_end.py", "insufficient_material"),
    (7, 2, "game_end.py", "game_result"),
    (7, 3, "notation.py", "parse_san"),
    (7, 4, "search.py", "random_move"),
    (7, 4, "search.py", "greedy_move"),
    (8, 1, "evaluation.py", "material"),
    (9, 2, "search.py", "capture_moves"),
    (9, 3, "move_ordering.py", "mvv_lva_score"),
    (9, 4, "search.py", "format_info"),
    (10, 1, "mate_solver.py", "mating_move"),
    (10, 2, "hidden_peak.py", "candidate_squares"),
    (10, 2, "hidden_peak.py", "score_candidate"),
    (10, 2, "hidden_peak.py", "choose_next_measurement"),
]


def stub_function(source: str, name: str, day: int, period: int) -> str:
    """
    Replace the body of one function with a NotImplementedError stub.

    Parameters
    ----------
    source : str
        The text of a Python file.
    name : str
        The name of a top-level function in that file.
    day, period : int
        The day and period when the students write the function.

    Returns
    -------
    str
        The file text with the function's body after its docstring replaced.
    """
    tree = ast.parse(source)
    node = next(
        n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name
    )
    lines = source.splitlines(keepends=True)
    docstring = node.body[0]
    body_start = docstring.end_lineno  # Line numbers count from 1
    body_end = node.end_lineno
    indent = " " * (node.col_offset + 4)
    stub = [
        f"{indent}# Day {day}, period {period}: write this function.\n",
        f"{indent}# The docstring above says what it must do; the tests check it.\n",
        f'{indent}raise NotImplementedError("Day {day} P{period}: write {name}()")\n',
    ]
    return "".join(lines[:body_start] + stub + lines[body_end:])


def main():
    stubbed = 0
    for folder in sorted(INSTRUCTOR.glob("Day */period*")):
        day = int(folder.parent.name[4:6])
        period = int(folder.name.removeprefix("period"))
        target = STUDENT / folder.parent.name / folder.name
        if target.exists():
            shutil.rmtree(target)  # Rebuild each student period folder from scratch
        shutil.copytree(
            folder,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "*.svg"),
        )
        for stub_day, stub_period, file_name, function in STUDENT_FUNCTIONS:
            if (stub_day, stub_period) != (day, period):
                continue
            file_path = target / file_name
            text = file_path.read_text()
            file_path.write_text(stub_function(text, function, stub_day, stub_period))
            stubbed += 1
    print(f"Wrote {STUDENT}")
    print(
        f"Functions turned into stubs: {stubbed}  (expected {len(STUDENT_FUNCTIONS)})"
    )


if __name__ == "__main__":
    main()
