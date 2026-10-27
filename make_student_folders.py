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

from make_station_folders import STATIONS_TABLE

ROOT = Path(__file__).parent
INSTRUCTOR = ROOT / "instructor"
STUDENT = ROOT / "student"
MAX_TYPED_LINES = 40  # Most lines of code a pair types in one period

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
    (6, 4, "fen.py", "fen_placement"),
    (6, 4, "fen.py", "board_from_placement"),
    (7, 1, "game_end.py", "insufficient_material"),
    (7, 1, "game_end.py", "game_result"),
    (7, 2, "notation.py", "parse_san"),
    (7, 3, "search.py", "random_move"),
    (7, 3, "search.py", "greedy_move"),
    (7, 4, "evaluation.py", "material"),
    (8, 3, "search.py", "capture_moves"),
    (8, 4, "move_ordering.py", "mvv_lva_score"),
    (9, 1, "search.py", "format_info"),
    (9, 4, "mate_solver.py", "mating_move"),
    (10, 1, "hidden_peak.py", "candidate_squares"),
    (10, 1, "hidden_peak.py", "score_candidate"),
    (10, 1, "hidden_peak.py", "choose_next_measurement"),
    (10, 2, "beam_time.py", "estimate"),
    (10, 2, "beam_time.py", "expected_wrong_calls"),
    (10, 3, "beam_time.py", "gain"),
    (10, 3, "beam_time.py", "choose_next_sample"),
]


def typed_lines(source: str, name: str) -> int:
    """Return how many lines of code (not blank, not comments) a function's body has."""
    tree = ast.parse(source)
    node = next(
        n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name
    )
    lines = source.splitlines()[node.body[0].end_lineno : node.end_lineno]
    return sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))


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
    typed: dict[tuple[int, int], int] = {}  # (day, period) -> lines the pairs type
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
            typed[(day, period)] = typed.get((day, period), 0) + typed_lines(
                text, function
            )
            file_path.write_text(stub_function(text, function, stub_day, stub_period))
            stubbed += 1
    # Each station folder stubs the functions its pair writes during the station
    (STUDENT / "Stations").mkdir(exist_ok=True)
    shutil.copy2(
        INSTRUCTOR / "Stations" / "station_match.py",
        STUDENT / "Stations" / "station_match.py",
    )
    for station in STATIONS_TABLE:
        folder = INSTRUCTOR / "Stations" / station["folder"]
        target = STUDENT / "Stations" / station["folder"]
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(
            folder,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "*.svg"),
        )
        color = station["folder"].split(" - ")[0]
        count = 0
        for file_name, function in station["students"]:
            file_path = target / file_name
            text = file_path.read_text()
            count += typed_lines(text, function)
            file_path.write_text(stub_function(text, function, 9, 2))
            stubbed += 1
        print(f"{color} station: {count} lines to type")
        if count > MAX_TYPED_LINES:
            print(f"  Too long: the {color} station asks for {count} lines")
    print(f"Wrote {STUDENT}")
    print(
        f"Functions turned into stubs: {stubbed}  (expected "
        f"{len(STUDENT_FUNCTIONS) + sum(len(st['students']) for st in STATIONS_TABLE)})"
    )
    longest = max(typed, key=lambda day_period: typed[day_period])
    print(
        f"Most lines typed in one period: {typed[longest]} on Day {longest[0]}, "
        f"period {longest[1]}  (expected at most {MAX_TYPED_LINES})"
    )
    for (day, period), count in sorted(typed.items()):
        if count > MAX_TYPED_LINES:
            print(f"  Too long: Day {day}, period {period} asks for {count} lines")


if __name__ == "__main__":
    main()
