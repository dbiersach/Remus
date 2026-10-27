#!/usr/bin/env -S uv run
"""make_period_folders.py

Build period1, period2, and period3 of every instructor Day folder from period4.

Each Day folder in instructor/ holds four period folders, and each period folder is
a complete, runnable copy of Remus as it stands at the end of that period. period4
is the finished code of the day, and the teacher edits only period4. This script
rebuilds the three earlier periods from it:

1. A file that arrives or grows during the day keeps its form from the end of the
   day before until the period named in ARRIVALS.
2. CHANGES lists what the earlier periods leave out of a file that grows: whole
   functions to drop, text to swap, or a smaller main().
3. When a function is left out, every import of it is removed, and every function
   or test that uses it is left out too, until each file uses only what exists.

Each period folder also gets a README.md that says what the period is about,
which files changed, and which functions the students write.

Run make_student_folders.py after this script.
"""

import ast
import shutil
import subprocess
import sys
from pathlib import Path

from make_student_folders import STUDENT_FUNCTIONS

ROOT = Path(__file__).parent
INSTRUCTOR = ROOT / "instructor"

# For each day, the period in which a file takes its period4 form. Before that
# period the file keeps its form from the day before, or is absent if it is new.
ARRIVALS = {
    1: {"board.py": 4, "test_board.py": 4, "show_board.py": 4},
    2: {
        "board.py": 3,
        "game_state.py": 3,
        "moves.py": 3,
        "test_make_move.py": 3,
        "make_move.py": 4,
    },
    3: {"move_generation.py": 2, "test_move_generation.py": 2, "show_board.py": 2},
    4: {"attacks.py": 2, "test_legal_moves.py": 2, "legal_moves.py": 3},
    5: {
        "make_move.py": 2,
        "legal_moves.py": 2,
        "test_special_moves.py": 2,
        "move_generation.py": 3,
        "uci_engine.py": 4,
        "remus.bat": 4,
    },
    6: {"perft.py": 2, "test_perft.py": 3},
    7: {
        "fen.py": 1,
        "test_game.py": 1,
        "test_perft.py": 1,
        "game_state.py": 2,
        "make_move.py": 2,
        "game_end.py": 2,
        "notation.py": 3,
        "console_game.py": 3,
        "search.py": 4,
        "uci_engine.py": 4,
        "play_match.py": 4,
    },
    8: {
        "evaluation.py": 1,
        "test_search.py": 1,
        "search.py": 3,
        "console_game.py": 4,
        "uci_engine.py": 4,
    },
    9: {
        "search.py": 1,
        "compare_search.py": 1,
        "test_search.py": 1,
        "move_ordering.py": 3,
        "console_game.py": 4,
        "uci_engine.py": 4,
    },
    10: {
        "evaluation.py": 1,
        "move_ordering.py": 1,
        "search.py": 1,
        "console_game.py": 1,
        "uci_engine.py": 1,
        "transposition_table.py": 1,
        "opening_book.py": 1,
        "opening_book.txt": 1,
        "mate_solver.py": 1,
        "test_upgrades.py": 1,
        "hidden_peak.py": 2,
        "tournament.py": 3,
        "remus.sh": 4,
    },
}

# Text that the en passant and promotion code adds to make_move.py on Day 5
MAKE_MOVE_EN_PASSANT = """    # En passant: a pawn moves diagonally onto the empty en passant target square
    is_pawn = piece.upper() == "P"
    if is_pawn and move.to_square == state["en_passant"]:
        victim = en_passant_victim_square(move)
        undo["en_passant_victim"] = victim
        undo["captured"] = piece_at(board, victim)
        set_piece(board, victim, EMPTY)

"""
MAKE_MOVE_PROMOTION = """    # Promotion: the pawn becomes the new piece on the last rank
    landing_piece = piece if move.promotion is None else move.promotion
    set_piece(board, move.to_square, landing_piece)
"""
MAKE_MOVE_DOUBLE_STEP = """    # A double step leaves an en passant target on the square the pawn skipped
    state["en_passant"] = None
    if is_pawn and abs(move.to_square[0] - move.from_square[0]) == 2:
        skipped_row = (move.from_square[0] + move.to_square[0]) // 2
        state["en_passant"] = (skipped_row, move.from_square[1])
"""
UNDO_MOVE_EN_PASSANT = """    if undo["en_passant_victim"] is None:
        set_piece(board, move.to_square, undo["captured"])
    else:
        set_piece(board, move.to_square, EMPTY)
        set_piece(board, undo["en_passant_victim"], undo["captured"])
"""
MAKE_MOVE_ABOUT = """Three moves change more than two squares: castling also moves a rook, en passant
removes a pawn that is not on the landing square, and promotion swaps the pawn for
a new piece."""
MAKE_MOVE_TEXTS = """        "e2e4",
        "g8f6",
        "e4e5",
        "d7d5",
        "e5d6",
        "c8g4",
        "f1e2",
        "b8c6",
        "g1f3",
        "d8d7",
        "e1g1",
        "e8c8",
        "d6c7",
        "a7a6",
        "c7d8n",
"""
MAKE_MOVE_REPORT = (
    "Fifteen moves (en passant, both castlings, a knight promotion) made and undone"
)

SEARCH_DAY_9_ABOUT = """Day 9 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result, quiescence keeps looking until the captures
stop, move ordering tries strong moves first, and iterative deepening searches
one move deeper at a time until the clock runs out."""
SEARCH_INFO_CLOCK = """    deadline: float | None = None  # time.perf_counter() value when the search must stop
    stop: threading.Event | None = None  # Set by the GUI's "stop" command
"""
SEARCH_THINK_DEMO = """    print("Thinking for 2 seconds from that position:")
    think(state, 2.0, report=print)
"""
SEARCH_DAY_9_LATER = ["format_info", "think", "think_move"]

# What the earlier periods leave out of a file that grows during the day:
# ("drop", [names]) drops top-level functions, classes, and constants;
# ("replace", old, new) swaps text that must appear exactly once;
# ("main", text) swaps the whole main() function.
CHANGES = {
    (3, 2, "move_generation.py"): [
        (
            "drop",
            [
                "ROOK_DIRECTIONS",
                "BISHOP_DIRECTIONS",
                "QUEEN_DIRECTIONS",
                "PROMOTION_PIECES",
                "slide",
                "slider_moves",
                "pawn_moves_to",
                "pawn_pushes",
                "pawn_captures",
                "piece_moves",
                "pseudo_legal_moves",
            ],
        ),
        (
            "main",
            """def main():
    empty = [["."] * 8 for _ in range(8)]
    print(f"Knight on a1: {len(knight_moves(empty, (7, 0), WHITE))} moves  (expected 2)")
    print(f"King on a1: {len(king_moves(empty, (7, 0), WHITE))} moves  (expected 3)")
""",
        ),
    ],
    (3, 3, "move_generation.py"): [
        (
            "drop",
            [
                "PROMOTION_PIECES",
                "pawn_moves_to",
                "pawn_pushes",
                "pawn_captures",
                "piece_moves",
                "pseudo_legal_moves",
            ],
        ),
        (
            "main",
            """def main():
    empty = [["."] * 8 for _ in range(8)]
    print(f"Knight on a1: {len(knight_moves(empty, (7, 0), WHITE))} moves  (expected 2)")
    print(
        f"Rook on d4: {len(slider_moves(empty, (4, 3), WHITE, ROOK_DIRECTIONS))} moves"
        "  (expected 14)"
    )
""",
        ),
    ],
    (4, 2, "attacks.py"): [
        ("drop", ["find_king", "in_check"]),
        (
            "replace",
            """    print(f"White in check at the start: {in_check(state, WHITE)}  (expected False)")
""",
            "",
        ),
    ],
    (4, 3, "test_legal_moves.py"): [
        (
            "drop",
            [
                "test_twenty_legal_moves_from_the_start",
                "test_king_in_check_has_only_escapes",
                "test_pinned_knight_has_no_moves",
            ],
        ),
    ],
    (5, 2, "make_move.py"): [
        ("drop", ["en_passant_victim_square"]),
        (
            "replace",
            MAKE_MOVE_ABOUT,
            "Castling changes more than two squares: the king and a rook both move.",
        ),
        (
            "replace",
            """    Make any move, including castling, en passant, and promotion, and return the
    record needed to undo it.""",
            "    Make a move, including castling, and return the record needed to undo it.",
        ),
        ("replace", '        "en_passant_victim": None,\n', ""),
        ("replace", MAKE_MOVE_EN_PASSANT, '    is_pawn = piece.upper() == "P"\n'),
        (
            "replace",
            MAKE_MOVE_PROMOTION,
            "    set_piece(board, move.to_square, piece)\n",
        ),
        ("replace", MAKE_MOVE_DOUBLE_STEP, '    state["en_passant"] = None\n'),
        (
            "replace",
            UNDO_MOVE_EN_PASSANT,
            '    set_piece(board, move.to_square, undo["captured"])\n',
        ),
        (
            "replace",
            MAKE_MOVE_TEXTS,
            """        "e2e4",
        "e7e5",
        "g1f3",
        "b8c6",
        "f1c4",
        "g8f6",
        "e1g1",
        "f8c5",
        "e8g8",
""",
        ),
        ("replace", MAKE_MOVE_REPORT, "Nine moves (both sides castle) made and undone"),
    ],
    (5, 3, "make_move.py"): [
        (
            "replace",
            MAKE_MOVE_ABOUT,
            """Two moves change more than two squares: castling also moves a rook, and en
passant removes a pawn that is not on the landing square.""",
        ),
        (
            "replace",
            """    Make any move, including castling, en passant, and promotion, and return the
    record needed to undo it.""",
            """    Make a move, including castling and en passant, and return the record
    needed to undo it.""",
        ),
        (
            "replace",
            MAKE_MOVE_PROMOTION,
            "    set_piece(board, move.to_square, piece)\n",
        ),
        ("replace", '        "d6c7",\n        "a7a6",\n        "c7d8n",\n', ""),
        (
            "replace",
            MAKE_MOVE_REPORT,
            "Twelve moves (en passant and both castlings) made and undone",
        ),
    ],
    (5, 2, "test_special_moves.py"): [
        (
            "drop",
            [
                "test_en_passant_only_on_the_very_next_move",
                "test_en_passant_removes_the_pawn_beside_and_undo_restores_it",
                "test_en_passant_that_exposes_the_king_is_illegal",
                "test_promotion_to_all_four_pieces",
                "test_knight_underpromotion_and_undo",
                "test_uci_engine_follows_a_game_with_castling",
            ],
        ),
    ],
    (5, 3, "test_special_moves.py"): [
        (
            "drop",
            [
                "test_promotion_to_all_four_pieces",
                "test_knight_underpromotion_and_undo",
                "test_uci_engine_follows_a_game_with_castling",
            ],
        ),
    ],
    (7, 1, "fen.py"): [
        ("replace", '    state["history"] = [position_key(state)]\n', ""),
    ],
    (7, 3, "console_game.py"): [
        (
            "replace",
            """Play chess in the terminal by typing moves in SAN, such as e4, Nf3, or O-O.
With "remus" as the first argument, Remus plays Black. Type "quit" to stop.""",
            """Two players take turns typing moves in SAN, such as e4, Nf3, or O-O.
Type "quit" to stop.""",
        ),
        (
            "main",
            """def main():
    state = state_from_fen(START_FEN)
    while True:
        print_board(state["board"])
        outcome = game_result(state)
        if outcome is not None:
            break  # The game is over
        text = input(f"{'White' if state['turn'] == 'w' else 'Black'} to move: ")
        if text.strip() == "quit":
            print("Game stopped.")
            return
        try:
            move = parse_san(state, text)
        except ValueError as error:
            print(error)
            continue
        make_move(state, move)
    result, reason = outcome
    print(f"Game over: {result} by {reason}")
""",
        ),
    ],
    (8, 1, "evaluation.py"): [
        (
            "replace",
            """A positive score is good for White. Two terms make up the score:

1. Material: the value of every piece on the board.
2. Placement: a bonus or penalty from a piece-square table, such as a knight
   in the center (it attacks eight squares) against a knight in the corner (two).

Each table is written from White's side, row 0 (rank 8) first. A Black piece reads
the table upside down, so its row 7 uses the table's row 0.""",
            """A positive score is good for White. The score is the material: the value of
every piece on the board.""",
        ),
        (
            "drop",
            [
                "PAWN_TABLE",
                "KNIGHT_TABLE",
                "BISHOP_TABLE",
                "ROOK_TABLE",
                "KING_TABLE",
                "QUEEN_TABLE",
                "PLACEMENT_TABLES",
                "placement",
            ],
        ),
        ("replace", "Material plus placement in centipawns", "Material in centipawns"),
        (
            "replace",
            'white_score = material(state["board"]) + placement(state["board"])',
            'white_score = material(state["board"])',
        ),
        (
            "replace",
            """    print(f"  Placement: {placement(board):+} centipawns for White")
""",
            "",
        ),
        (
            "main",
            """def main():
    print("Start position:")
    explain_evaluation(state_from_fen(START_FEN))
    print("  (expected 0 for every term: the position is symmetric)")
    print("White knight against a Black rook:")
    explain_evaluation(state_from_fen("r3k3/8/8/4N3/8/8/8/4K3 w - - 0 1"))
    print("  (expected material -200: the rook is worth 200 more than the knight)")
""",
        ),
    ],
    (8, 3, "search.py"): [
        (
            "replace",
            """Then Remus looks
ahead: minimax tries every move and every reply, and negamax does the same work
with one function instead of two mirror-image halves.""",
            """Then Remus looks
ahead: minimax tries every move and every reply.""",
        ),
        ("drop", ["negamax", "best_move", "negamax_move"]),
        (
            "main",
            """def main():
    state = state_from_fen("4k3/8/8/3q4/8/2N1p3/8/4K3 w - - 0 1")
    print(
        f"Greedy move: {move_to_uci(greedy_move(state))}  (expected c3d5, taking the queen)"
    )
    print(f"Random move: {move_to_uci(random_move(state))}  (any legal move)")
    state = state_from_fen("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1")
    before = state_snapshot(state)
    info = SearchInfo()
    score = minimax(state, 2, info)
    print(f"Back-rank mate: minimax scores {score}  (expected {MATE_SCORE}, White mates)")
    print(
        f"Positions visited: {info.nodes:,}; root unchanged: {state_snapshot(state) == before}"
    )
""",
        ),
    ],
    (9, 1, "search.py"): [
        (
            "replace",
            SEARCH_DAY_9_ABOUT,
            """Day 9 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result.""",
        ),
        ("replace", SEARCH_INFO_CLOCK, ""),
        (
            "drop",
            [
                "SearchTimeout",
                "check_time",
                "capture_moves",
                "quiescence",
                "alpha_beta_with_quiescence",
            ]
            + SEARCH_DAY_9_LATER,
        ),
        ("replace", SEARCH_THINK_DEMO, ""),
    ],
    (9, 2, "search.py"): [
        (
            "replace",
            SEARCH_DAY_9_ABOUT,
            """Day 9 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result, and quiescence keeps looking until the
captures stop.""",
        ),
        ("replace", SEARCH_INFO_CLOCK, ""),
        (
            "drop",
            ["SearchTimeout", "check_time", "alpha_beta_with_quiescence"]
            + SEARCH_DAY_9_LATER,
        ),
        (
            "replace",
            "    check_time(info)\n    stand_pat = evaluate(state)\n",
            "    stand_pat = evaluate(state)\n",
        ),
        (
            "replace",
            'for move in order_moves(capture_moves(state), state["board"]):',
            "for move in capture_moves(state):",
        ),
        (
            "replace",
            """    info : SearchInfo
        Counts positions and holds the deadline.

    Returns
    -------
    int
        The score for the side to move.""",
            """    info : SearchInfo
        Counts the positions visited.

    Returns
    -------
    int
        The score for the side to move.""",
        ),
        ("replace", SEARCH_THINK_DEMO, ""),
    ],
    (9, 3, "search.py"): [
        (
            "replace",
            SEARCH_DAY_9_ABOUT,
            """Day 9 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result, quiescence keeps looking until the captures
stop, and move ordering tries strong moves first.""",
        ),
        ("drop", SEARCH_DAY_9_LATER),
        ("replace", SEARCH_THINK_DEMO, ""),
    ],
    (9, 1, "test_search.py"): [("drop", ["test_uci_engine_answers_while_thinking"])],
    (9, 2, "test_search.py"): [("drop", ["test_uci_engine_answers_while_thinking"])],
    (9, 3, "test_search.py"): [("drop", ["test_uci_engine_answers_while_thinking"])],
}

# The title of every period, from docs/remus_course_plan.md
PERIOD_TITLES = {
    (1, 1): "Welcome and setup",
    (1, 2): "Python lab 1: scripts, strings, ord and chr, f-strings",
    (1, 3): "Python lab 2: lists and nested lists",
    (1, 4): "board.py: the board and its square names",
    (2, 1): "Python lab 3: functions, type hints, tuples, assert, pytest",
    (2, 2): "Python lab 4: dicts, dataclasses, aliasing, copying",
    (2, 3): "game_state.py and moves.py: a game state and a move record",
    (2, 4): "make_move.py: make and undo ordinary moves",
    (3, 1): "Python lab 5: while, break, direction tuples",
    (3, 2): "Jumping pieces: knights and kings",
    (3, 3): "Sliding pieces: rooks, bishops, and queens",
    (3, 4): "Pawns",
    (4, 1): "Python lab 6: modules, imports, __main__, git",
    (4, 2): "Attacks",
    (4, 3): "Check and the legal filter",
    (4, 4): "Practice positions",
    (5, 1): "Python lab 7: sets, in, string replacement",
    (5, 2): "Castling",
    (5, 3): "En passant and the double step",
    (5, 4): "Promotion, and Remus plays in En Croissant",
    (6, 1): "Python lab 8: recursion",
    (6, 2): "Perft",
    (6, 3): "Perft against python-chess, and bug hunt",
    (6, 4): "Week 1 review and catch-up",
    (7, 1): "Python lab 9 and FEN",
    (7, 2): "Ending the game",
    (7, 3): "SAN and the console game",
    (7, 4): "First brains and the GUI",
    (8, 1): "What makes a position good? Material",
    (8, 2): "Piece-square tables",
    (8, 3): "Minimax",
    (8, 4): "Negamax and mates",
    (9, 1): "Python lab 11 and alpha-beta",
    (9, 2): "The horizon effect and quiescence",
    (9, 3): "Move ordering",
    (9, 4): "Iterative deepening, the clock, and UCI info",
    (10, 1): "Upgrade stations",
    (10, 2): "Science AI: hidden_peak.py",
    (10, 3): "Tournament",
    (10, 4): "Presentations, take-home, and wrap-up",
}

# A few periods need a sentence more than the title and the file list give
PERIOD_NOTES = {
    (1, 1): "Watch the finished Remus play in En Croissant, form pairs, and check that "
    "every laptop runs `uv run pytest`.",
    (1, 4): "`uv run show_board.py` draws the board as a picture in the web browser.",
    (3, 2): "`uv run show_board.py` draws an arrow for every move a generator returns.",
    (5, 4): "Register `remus.bat` from this folder as an engine in En Croissant and "
    "play your own Remus. It plays random legal moves, and every special move works.",
    (7, 4): "Register `remus.bat` from this folder in En Croissant again: Remus now "
    "plays greedy moves. `uv run play_match.py` plays random Remus against greedy Remus.",
    (10, 3): "`uv run tournament.py` plays the class round robin and saves every game "
    "as PGN beside the script.",
}

# Every Python module name that appears in any Day folder
LOCAL_MODULES = {path.stem for path in INSTRUCTOR.glob("Day */period4/*.py")}


def day_folder(day: int) -> Path:
    """Return the instructor Day folder for a day number, such as Day 03."""
    return next(INSTRUCTOR.glob(f"Day {day:02} - *"))


def read_folder(folder: Path) -> dict[str, str]:
    """Return {file name: text} for every file in a folder."""
    files = {}
    for path in sorted(folder.iterdir()):
        if path.is_file():
            files[path.name] = path.read_text()
    return files


def top_level_names(node: ast.stmt) -> list[str]:
    """Return the names a top-level function, class, or constant defines."""
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return [node.name]
    if isinstance(node, ast.Assign):
        return [target.id for target in node.targets if isinstance(target, ast.Name)]
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return [node.target.id]
    return []


def defined_names(text: str) -> set[str]:
    """Return every name a module defines at the top level."""
    names = set()
    for node in ast.parse(text).body:
        names.update(top_level_names(node))
    return names


def node_lines(lines: list[str], node: ast.stmt) -> tuple[int, int]:
    """
    Return the (first, last) line index of a top-level node, counting from 0.

    The first line includes decorators and the comment lines right above.
    """
    first = node.lineno - 1
    decorators = getattr(node, "decorator_list", [])
    if decorators:
        first = decorators[0].lineno - 1
    while first > 0 and lines[first - 1].startswith("#"):
        first -= 1
    last = node.end_lineno or node.lineno
    return first, last - 1


def drop_names(text: str, names: set[str]) -> str:
    """Remove the top-level functions, classes, and constants with these names."""
    lines = text.split("\n")
    for node in reversed(ast.parse(text).body):
        if set(top_level_names(node)) & names:
            first, last = node_lines(lines, node)
            del lines[first : last + 1]
    return "\n".join(lines)


def replace_main(text: str, new_main: str) -> str:
    """Swap the whole main() function for new text."""
    lines = text.split("\n")
    for node in ast.parse(text).body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            first, last = node_lines(lines, node)
            lines[first : last + 1] = new_main.rstrip("\n").split("\n")
            return "\n".join(lines)
    raise ValueError("No main() to replace")


def apply_changes(text: str, changes: list[tuple], label: str) -> str:
    """Apply the CHANGES entries for one file of one period."""
    for change in changes:
        if change[0] == "drop":
            missing = set(change[1]) - defined_names(text)
            if missing:
                raise ValueError(f"{label}: nothing named {missing} to drop")
            text = drop_names(text, set(change[1]))
        elif change[0] == "replace":
            old, new = change[1], change[2]
            if text.count(old) != 1:
                raise ValueError(
                    f"{label}: {old[:50]!r} appears {text.count(old)} times"
                )
            text = text.replace(old, new)
        else:
            text = replace_main(text, change[1])
    return text


def remove_missing_imports(text: str, files: dict[str, str]) -> tuple[str, set[str]]:
    """
    Remove each imported name that its Remus module does not define.

    Returns
    -------
    tuple[str, set[str]]
        The new text and the names removed.
    """
    lines = text.split("\n")
    removed = set()
    for node in reversed(ast.parse(text).body):
        if not isinstance(node, ast.ImportFrom) or node.module not in LOCAL_MODULES:
            continue
        module_text = files.get(f"{node.module}.py")
        available = defined_names(module_text) if module_text is not None else set()
        kept = [alias.name for alias in node.names if alias.name in available]
        if len(kept) == len(node.names):
            continue
        removed.update(alias.name for alias in node.names if alias.name not in kept)
        first, last = node.lineno - 1, (node.end_lineno or node.lineno) - 1
        new_lines = [f"from {node.module} import {', '.join(kept)}"] if kept else []
        lines[first : last + 1] = new_lines
    return "\n".join(lines), removed


def used_names(node: ast.stmt) -> set[str]:
    """Return every plain name a top-level node reads."""
    return {item.id for item in ast.walk(node) if isinstance(item, ast.Name)}


def drop_users(text: str, missing: set[str]) -> tuple[str, set[str]]:
    """Drop top-level functions and constants that use a missing name."""
    users = set()
    for node in ast.parse(text).body:
        names = top_level_names(node)
        if names and used_names(node) & missing:
            users.update(names)
    if not users:
        return text, users
    return drop_names(text, users), users


def settle(files: dict[str, str], label: str) -> dict[str, str]:
    """
    Remove imports of names that do not exist, and everything that uses them,
    until every Python file uses only names that exist.
    """
    changed = True
    while changed:
        changed = False
        for name in sorted(files):
            if not name.endswith(".py"):
                continue
            text, missing = remove_missing_imports(files[name], files)
            while missing:
                text, users = drop_users(text, missing)
                if "main" in users:
                    raise ValueError(f"{label}/{name}: main() uses {missing}")
                if users:
                    print(f"  {label}/{name}: leaves out {', '.join(sorted(users))}")
                missing = users
            if text != files[name]:
                files[name] = text
                changed = True
    return files


def build_period(day: int, period: int, day_end: dict, day_before: dict) -> dict:
    """Return {file name: text} for one period of one day."""
    label = f"Day {day:02} period{period}"
    files = {}
    for name, text in day_end.items():
        arrival = ARRIVALS[day].get(name)
        if arrival is None:
            if day_before.get(name) != text:
                raise ValueError(f"{label}: {name} changed but has no ARRIVALS entry")
            files[name] = text
        elif period >= arrival:
            changes = CHANGES.get((day, period, name), [])
            files[name] = apply_changes(text, changes, f"{label}/{name}")
        elif name in day_before:
            files[name] = day_before[name]
    for change_day, change_period, name in CHANGES:
        if change_day == day and change_period == period and name not in files:
            raise ValueError(f"{label}: CHANGES for {name}, which is absent")
    return settle(files, label)


def readme_text(day: int, period: int, files: dict, files_before: dict) -> str:
    """Return the README.md that explains one period folder."""
    title = PERIOD_TITLES[(day, period)]
    sections = [f"# Day {day}, Period {period}: {title}"]
    if (day, period) in PERIOD_NOTES:
        sections.append(PERIOD_NOTES[(day, period)])
    new_files = [name for name in files if name not in files_before]
    grown_files = [
        name
        for name in files
        if name in files_before and files[name] != files_before[name]
    ]
    written = [
        f"- `{function}()` in `{file_name}`"
        for (row_day, row_period, file_name, function) in STUDENT_FUNCTIONS
        if (row_day, row_period) == (day, period)
    ]
    if title.startswith("Python lab"):
        sections.append(f"The lab files for this period live in `labs/day{day:02}/`.")
    if not files:
        sections.append(
            "This period comes before any Remus code, so the folder is empty."
        )
    elif not new_files and not grown_files:
        sections.append(
            "The Remus code here is the same as at the end of the period before."
        )
    if new_files:
        sections.append(
            "New files this period:\n\n"
            + "\n".join(f"- `{name}`" for name in new_files)
        )
    if grown_files:
        sections.append(
            "Files that grow this period:\n\n"
            + "\n".join(f"- `{name}`" for name in grown_files)
        )
    if written:
        sections.append(
            "Functions the pairs write this period:\n\n" + "\n".join(written)
        )
        sections.append(
            "In `student/` these functions raise `NotImplementedError` until a pair "
            "writes them. In `instructor/` they are finished."
        )
    if any(name.startswith("test_") for name in files):
        sections.append(
            "Check the work from inside this folder with `uv run pytest`, and run any "
            "file on its own, such as `uv run board.py`."
        )
    return "\n\n".join(sections) + "\n"


def write_folder(folder: Path, files: dict[str, str], day_end_folder: Path) -> None:
    """Write a period folder, copying file permissions from the period4 copy."""
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir()
    for name, text in files.items():
        file_path = folder / name
        file_path.write_text(text)
        source = day_end_folder / name
        if source.exists():
            shutil.copymode(source, file_path)


def tidy(folders: list[Path]) -> None:
    """Remove unused imports and format the code with ruff."""
    paths = [str(folder) for folder in folders]
    ruff = [sys.executable, "-m", "ruff"]
    subprocess.run(
        ruff + ["check", "--quiet", "--fix", "--select", "F401,I001", *paths],
        check=False,
    )
    subprocess.run(ruff + ["format", "--quiet", *paths], check=True)


def main():
    day_before = {}
    built = []
    for day in range(1, 11):
        end_folder = day_folder(day) / "period4"
        day_end = read_folder(end_folder)
        day_end.pop("README.md", None)
        files_before = day_before
        for period in range(1, 5):
            if period == 4:
                files = day_end
            else:
                files = build_period(day, period, day_end, day_before)
                folder = day_folder(day) / f"period{period}"
                write_folder(folder, files, end_folder)
                built.append(folder)
            readme = readme_text(day, period, files, files_before)
            (day_folder(day) / f"period{period}" / "README.md").write_text(readme)
            files_before = files
        day_before = day_end
    tidy(built)
    print(f"Built {len(built)} period folders  (expected 30)")


if __name__ == "__main__":
    main()
