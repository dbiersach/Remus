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

Each period folder also gets a README.md that says what the period is about, its
learning objectives and how each one is measured, which files changed, and one
paragraph on every change the students make, all from period_guides.py. A Python
lab or demo period keeps its answer file, <name>_instructor.py, which lives in
that period folder and survives each rebuild, and Day 6, period 3 gets the bug_hunt
folder: a copy of the period's code with three planted
bugs for the pairs to find with divide().

Run make_student_folders.py after this script.
"""

import ast
import shutil
import subprocess
import sys
from pathlib import Path

from make_student_folders import STUDENT_FUNCTIONS
from period_guides import CHANGE_NOTES, LAB_NOTES, LABS, OBJECTIVES, PERIOD_GUIDES

ROOT = Path(__file__).parent.parent  # The top Remus folder, above scripts/
INSTRUCTOR = ROOT / "instructor"
SAVED_OUTPUT_SUFFIXES = {".pgn", ".svg"}  # Games and board pictures that scripts save
BUG_HUNT_PERIOD = (6, 3)  # The period whose folder holds bug_hunt/
BUG_HUNT_FILES = [  # The Remus files that bug_hunt/ copies, so that perft runs there
    "attacks.py",
    "board.py",
    "game_state.py",
    "legal_moves.py",
    "make_move.py",
    "move_generation.py",
    "moves.py",
    "perft.py",
]
# (file, correct text, planted text, what goes wrong, root moves that show it)
PLANTED_BUGS = [
    (
        "make_move.py",
        "        set_piece(board, victim, EMPTY)\n",
        "",
        "An en passant capture leaves the captured pawn on the board.",
        (
            "g2g4 and e2e4 in position 3: the White pawn left on rank 4 hides the "
            "Black king on h4 from the rook on b4"
        ),
    ),
    (
        "legal_moves.py",
        "if in_check(state, color) or is_square_attacked(board, crossed, enemy):",
        "if in_check(state, color) or is_square_attacked(board, king_to, enemy):",
        "Castling checks the landing square instead of the square the king crosses.",
        "e5f7, e5d7, e5g6, and e5c6 in kiwipete: the knight attacks d8 or f8",
    ),
    (
        "move_generation.py",
        'PROMOTION_PIECES = "QRBN"',
        'PROMOTION_PIECES = "QRB"',
        "A pawn cannot promote to a knight.",
        "d7c8n in position 5, missing from Remus's list, and six moves in position 4",
    ),
]

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
    6: {"perft.py": 2, "test_perft.py": 3, "fen.py": 4, "test_game.py": 4},
    7: {
        "fen.py": 1,
        "test_game.py": 1,
        "game_state.py": 1,
        "make_move.py": 1,
        "game_end.py": 1,
        "notation.py": 2,
        "console_game.py": 2,
        "search.py": 3,
        "uci_engine.py": 3,
        "play_match.py": 3,
        "evaluation.py": 4,
        "test_search.py": 4,
    },
    8: {
        "search.py": 1,
        "test_search.py": 1,
        "console_game.py": 1,
        "uci_engine.py": 1,
        "compare_search.py": 2,
        "mate_puzzles.epd": 2,
        "move_ordering.py": 4,
    },
    9: {
        "search.py": 1,
        "test_search.py": 1,
        "console_game.py": 1,
        "uci_engine.py": 1,
        "test_game.py": 1,
        "mate_solver.py": 4,
    },
    # Day 10 holds only the science files; its engine is Remus-GOLD in instructor/Remus
    10: {
        "hidden_peak.py": 1,
        "test_hidden_peak.py": 1,
        "phase_hunt.py": 2,
        "test_phase_hunt.py": 2,
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
MAKE_MOVE_TEXTS = """    texts = ["e2e4", "g8f6", "e4e5", "d7d5", "e5d6", "c8g4", "f1e2", "b8c6"]
    texts += ["g1f3", "d8d7", "e1g1", "e8c8", "d6c7", "a7a6", "c7d8n"]
"""
MAKE_MOVE_REPORT = (
    "Fifteen moves (en passant, both castlings, a knight promotion) made and undone"
)

SEARCH_DAY_8_ABOUT = """Day 8 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result, quiescence keeps looking until the captures
stop, and move ordering tries strong moves first."""
SEARCH_INFO_CLOCK = """    deadline: float | None = None  # time.perf_counter() value when the search must stop
"""
SEARCH_ALPHA_BETA_DEMO = """
    state = state_from_fen(
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    )
    plain = SearchInfo()
    plain_score = negamax(state, 3, 0, plain)
    pruned = SearchInfo()
    pruned_score = alpha_beta(state, 3, 0, -MATE_SCORE - 1, MATE_SCORE + 1, pruned)
    print(f"Negamax depth 3: score {plain_score}, {plain.nodes:,} positions")
    print(
        f"Alpha-beta depth 3: score {pruned_score}, {pruned.nodes:,} positions"
        "  (expected the same score, fewer positions)"
    )
"""

# Text that test_perft.py swaps on Day 6, before Remus reads FEN in period 4
TEST_PERFT_FEN_ABOUT = (
    "the standard test positions. From Day 6, period 4 on, Remus reads each FEN itself."
)
TEST_PERFT_HELPER = '''def state_from_python_chess(board: chess.Board) -> dict:
    """Build a Remus state from a python-chess board (test helper only)."""
    state = new_game()
    state["board"] = [[EMPTY] * 8 for _ in range(8)]
    for square, piece in board.piece_map().items():
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)
        state["board"][row][col] = piece.symbol()
    state["turn"] = WHITE if board.turn == chess.WHITE else BLACK
    state["castling"] = board.castling_xfen().replace("-", "")
    state["en_passant"] = None
    if board.ep_square is not None:
        state["en_passant"] = (
            7 - chess.square_rank(board.ep_square),
            chess.square_file(board.ep_square),
        )
    state["halfmove_clock"] = board.halfmove_clock
    state["fullmove_number"] = board.fullmove_number
    return state


def python_chess_perft('''

# The main() of phase_hunt.py before the pairs write the tree search in period 3
PHASE_HUNT_MAIN = """def main():
    measured, truth = make_pattern(SILVER_POWDER)
    print(f"Powder {SILVER_POWDER} shows {len(measured)} peaks: {measured}")
    print(f"  True phases:  {truth}")
    print(f"  Greedy says:  {greedy_phases(measured)}")
    print("  (expected: greedy names gold, but the powder holds silver)")
    print(f"Benchmark: {TRIALS} powders of 1 to {MAX_PHASES} phases")
    show_benchmark("Greedy", benchmark(greedy_answer))
    print("  (expected: greedy names most powders right and about 1 in 6 wrong)")
"""

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
            """    texts = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6", "e1g1", "f8c5", "e8g8"]
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
        ("replace", ', "d6c7", "a7a6", "c7d8n"]', "]"),
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
    (6, 3, "test_perft.py"): [
        (
            "replace",
            TEST_PERFT_FEN_ABOUT,
            """the standard test positions. python-chess also converts each FEN into a Remus state,
because Remus learns to read FEN in period 4.""",
        ),
        (
            "replace",
            "from fen import state_from_fen\nfrom game_state import new_game\n",
            "from board import EMPTY\nfrom game_state import BLACK, WHITE, new_game\n",
        ),
        ("replace", "def python_chess_perft(", TEST_PERFT_HELPER),
        (
            "replace",
            "perft(state_from_fen(fen), depth)",
            "perft(state_from_python_chess(board), depth)",
        ),
        (
            "replace",
            "divide(state_from_fen(POSITIONS[1][1]), 2)",
            "divide(state_from_python_chess(board), 2)",
        ),
    ],
    (7, 2, "console_game.py"): [
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
    (8, 1, "search.py"): [
        ("replace", "\n\n" + SEARCH_DAY_8_ABOUT, ""),
        ("replace", SEARCH_INFO_CLOCK, ""),
        (
            "drop",
            [
                "SearchTimeout",
                "check_time",
                "alpha_beta",
                "capture_moves",
                "quiescence",
                "alpha_beta_with_quiescence",
            ],
        ),
        ("replace", SEARCH_ALPHA_BETA_DEMO, ""),
    ],
    (8, 1, "test_search.py"): [("drop", ["MATE_PUZZLES"])],
    (8, 2, "search.py"): [
        (
            "replace",
            SEARCH_DAY_8_ABOUT,
            """Day 8 makes the search smarter without changing its answer: alpha-beta skips
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
            ],
        ),
    ],
    (8, 3, "search.py"): [
        (
            "replace",
            SEARCH_DAY_8_ABOUT,
            """Day 8 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result, and quiescence keeps looking until the
captures stop.""",
        ),
        ("replace", SEARCH_INFO_CLOCK, ""),
        ("drop", ["SearchTimeout", "check_time", "alpha_beta_with_quiescence"]),
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
    ],
    (10, 2, "phase_hunt.py"): [
        (
            "replace",
            "import random\nfrom dataclasses import dataclass, field\n",
            "import random\n",
        ),
        (
            "drop",
            ["Hunt", "search", "run_search", "search_answer", "sets_every_order"],
        ),
        ("main", PHASE_HUNT_MAIN),
    ],
    (10, 2, "test_phase_hunt.py"): [
        (
            "replace",
            (
                "the evaluation, the greedy agent, the tree search, and the\n"
                "benchmark against known powders."
            ),
            "the evaluation and the greedy agent.",
        ),
        (
            "replace",
            (
                "from phase_hunt import (\n"
                "    LIBRARY,\n"
                "    MAX_PHASES,\n"
                "    SILVER_POWDER,\n"
                "    Hunt,\n"
                "    benchmark,\n"
                "    greedy_answer,\n"
                "    greedy_phases,\n"
                "    make_pattern,\n"
                "    matches,\n"
                "    run_search,\n"
                "    score,\n"
                "    search,\n"
                "    search_answer,\n"
                ")\n"
            ),
            (
                "from phase_hunt import (\n"
                "    LIBRARY,\n"
                "    SILVER_POWDER,\n"
                "    greedy_phases,\n"
                "    make_pattern,\n"
                "    matches,\n"
                "    score,\n"
                ")\n"
            ),
        ),
        (
            "drop",
            [
                "test_search_leaves_the_phases_as_it_found_them",
                "test_search_scores_each_set_once",
                "test_search_finds_both_look_alikes",
                "test_search_makes_fewer_wrong_calls_than_greedy",
            ],
        ),
    ],
}

# The title of every period, from docs/course/remus_course_plan.md
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
    (5, 4): "Promotion, and Remus plays in Lucas Chess",
    (6, 1): "Python lab 8: recursion",
    (6, 2): "Perft",
    (6, 3): "Perft against python-chess, and bug hunt",
    (6, 4): "Python lab 9 and FEN",
    (7, 1): "Ending the game",
    (7, 2): "SAN and the console game",
    (7, 3): "First brains and the GUI",
    (7, 4): "What makes a position good? Material and piece-square tables",
    (8, 1): "Minimax, negamax, and mates",
    (8, 2): "Python lab 11 and alpha-beta",
    (8, 3): "The horizon effect and quiescence",
    (8, 4): "Move ordering",
    (9, 1): "Iterative deepening, the clock, and UCI info",
    (9, 2): "Python lab 12 and the color versions",
    (9, 3): "Color versions: test and measure",
    (9, 4): "The mate solver",
    (10, 1): "Science AI: hidden_peak.py",
    (10, 2): "The phase hunt: score a guess, and the greedy agent",
    (10, 3): "The phase hunt: search every set, and verify",
    (10, 4): "Results, tournament, take-home, and wrap-up",
}

# A few periods need a sentence more than the title and the file list give
PERIOD_NOTES = {
    (1, 1): "Watch the finished Remus play in Lucas Chess, form pairs, and check that "
    "every laptop runs `uv run pytest`.",
    (1, 4): "Running `show_board.py` draws the board as a picture in the web browser.",
    (3, 2): "Running `show_board.py` draws an arrow for every move a generator "
    "returns.",
    (5, 4): "Register `remus.bat` from this folder as an engine in Lucas Chess and "
    "play your own Remus. It plays random legal moves, and every special move works.",
    (6, 3): "The `bug_hunt` folder holds a copy of this period's Remus with three "
    "planted bugs. Running `hunt.py` inside it shows where the counts go wrong.",
    (7, 3): "Register `remus.bat` from this folder in Lucas Chess again: Remus now "
    "plays greedy moves. Running `play_match.py` plays random Remus against greedy Remus.",
    (9, 2): "Each pair builds one color version in the `Remus` folder next to the "
    "Day folders, such as `10 RED - Transposition table`. The code in this Day "
    "folder is Remus-WHITE, the starting point of every color version.",
    (10, 2): "Running `phase_hunt.py` names the crystal phases in an X-ray powder "
    "pattern and counts the right and wrong calls over 200 powders.",
    (10, 4): "The tournament: each pair opens `play_tournament.py` in its version "
    "folder under `Remus` and presses Run in VS Code: two 10-minute games of its color "
    "against Remus-WHITE, one with each color, all pairs at once. Running "
    "`estimate_elo.py` in the GOLD folder measures the Elo rating of Remus-GOLD "
    "against Stockfish. Both add every game to games/remus_games.pgn "
    "at the top of the repository.",
}

# Every Python module name that appears in any Day folder
LOCAL_MODULES = {path.stem for path in INSTRUCTOR.glob("Day */period4/*.py")}


def day_folder(day: int) -> Path:
    """Return the instructor Day folder for a day number, such as Day 03."""
    return next(INSTRUCTOR.glob(f"Day {day:02} - *"))


def read_folder(folder: Path) -> dict[str, str]:
    """Return {file name: text} for every code and data file in a folder."""
    files = {}
    for path in sorted(folder.iterdir()):
        # Games and pictures that scripts save beside themselves are not course code
        if path.is_file() and path.suffix not in SAVED_OUTPUT_SUFFIXES:
            # newline="" keeps the CRLF line endings that remus.bat has on Windows
            files[path.name] = path.read_text(newline="")
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


def objectives_section(day: int, period: int) -> str:
    """Return the learning objectives of a period, each with how it is measured."""
    lines = [
        "## Learning objectives",
        "",
        "By the end of this period, each pair can:",
        "",
    ]
    for objective, measure in OBJECTIVES[(day, period)]:
        lines.append(f"- {objective} **Measured by:** {measure}")
    return "\n".join(lines)


def changes_section(day: int, period: int) -> str:
    """Return one paragraph for every change the pairs make this period."""
    lines = ["## The changes and why"]
    if (day, period) in LABS:
        name = LABS[(day, period)]
        lines += [
            "",
            (
                f"The pairs fill in the blanks of `{name}.py`. Each `#` line in the "
                "student file stands for one line to type, and the answer sits on the "
                f"same line of `{name}_instructor.py`."
            ),
        ]
        for paragraph in LAB_NOTES[(day, period)]:
            lines += ["", paragraph]
    for row_day, row_period, file_name, function in STUDENT_FUNCTIONS:
        if (row_day, row_period) == (day, period):
            lines += [
                "",
                f"### `{function}()` in `{file_name}`",
                "",
                CHANGE_NOTES[(file_name, function)],
            ]
    if len(lines) == 1:
        return ""
    return "\n".join(lines)


def readme_text(day: int, period: int, files: dict, files_before: dict) -> str:
    """Return the README.md that explains one period folder."""
    title = PERIOD_TITLES[(day, period)]
    sections = [f"# Day {day}, Period {period}: {title}"]
    if (day, period) in PERIOD_NOTES:
        sections.append(PERIOD_NOTES[(day, period)])
    sections.append(objectives_section(day, period))
    if (day, period) in PERIOD_GUIDES:
        sections.append(PERIOD_GUIDES[(day, period)])
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
    sections.append("## The files")
    if day == 10:
        sections.append(
            "The engine for Day 10 is Remus-GOLD, the finished Remus with all ten "
            "enhancements, in the `Remus/11 GOLD - All enhancements` folder beside "
            "the Day folders. Lucas Chess runs its `remus.bat`, and its "
            "`estimate_elo.py` rates it against Stockfish. This folder holds only "
            "the science files, which never import the engine."
        )
    if (day, period) in LABS:
        name = LABS[(day, period)]
        kind = "demo" if name.startswith("demo_") else "lab"
        before = "This period comes before any Remus code. " if not files else ""
        sections.append(
            f"{before}The {kind} is `{name}.py` in `student/`, with the answers in "
            f"`{name}_instructor.py` in `instructor/`. Open `{name}.py` in VS Code "
            "and run it with the Run Python File button (the triangle at the top "
            "right of the editor)."
        )
    if not files:
        if (day, period) not in LABS:
            sections.append(
                "This period comes before any Remus code, so the folder is empty."
            )
    elif not new_files and not grown_files:
        sections.append("The code here is the same as at the end of the period before.")
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
    changes = changes_section(day, period)
    if changes:
        sections.append(changes)
    if any(name.startswith("test_") for name in files):
        example = "board.py"
        if example not in files:
            scripts = [n for n in files if n.endswith(".py") and "test_" not in n]
            example = min(scripts)
        sections.append(
            "Check the work with the tests: open a terminal in VS Code inside this "
            "folder and type `uv run pytest`. To run one file on its own, such as "
            f"`{example}`, open it in VS Code and click the Run Python File button "
            "(the triangle at the top right of the editor)."
        )
    return "\n\n".join(sections) + "\n"


def lab_answer_files(day: int) -> list[str]:
    """Return the names of the lab and demo answer files of one day."""
    names = []
    for (lab_day, _), name in LABS.items():
        if lab_day == day:
            names.append(f"{name}_instructor.py")
    return names


def bug_hunt_readme(with_answers: bool) -> str:
    """Return the README.md of the bug_hunt folder, with or without the answers."""
    lines = [
        "# Bug hunt",
        "",
        (
            "The Remus files in this folder are a copy of the Day 6, period 3 code, "
            "with three bugs planted in them. Each bug breaks one chess rule. Run "
            "`hunt.py` from inside this folder in VS Code: it uses `divide()` to count "
            "the positions under every root move of four standard positions, and "
            "prints each root move where Remus and python-chess disagree."
        ),
        "",
        (
            "A root move that disagrees points at a rule that its position needs. "
            "Ask what is special about that move or about the replies to it, find "
            "the rule in the code, fix the line, and run the hunt again. The hunt "
            "is over when it prints 0 root moves that disagree."
        ),
    ]
    if with_answers:
        lines += ["", "## Answers", "", "| File | The bug | Root moves that show it |"]
        lines += ["| --- | --- | --- |"]
        for file_name, correct, _, problem, shown_by in PLANTED_BUGS:
            fix = correct.strip()
            lines.append(f"| `{file_name}` | {problem} The fix: `{fix}` | {shown_by} |")
    return "\n".join(lines) + "\n"


def write_bug_hunt(folder: Path) -> None:
    """Write folder/bug_hunt: the period's Remus files with three planted bugs."""
    hunt = folder / "bug_hunt"
    hunt.mkdir()
    for name in BUG_HUNT_FILES:
        text = (folder / name).read_text()
        for file_name, correct, planted, _, _ in PLANTED_BUGS:
            if file_name == name:
                if text.count(correct) != 1:
                    raise ValueError(f"bug_hunt/{name}: cannot plant the bug")
                text = text.replace(correct, planted)
        (hunt / name).write_text(text)
        shutil.copymode(folder / name, hunt / name)
    (hunt / "README.md").write_text(bug_hunt_readme(with_answers=True))


def keep_hand_written(day: int, period: int, folder: Path) -> dict[str, str]:
    """
    Read the hand-written files of a period folder before the rebuild deletes it.

    A lab's answer file and the bug hunt's hunt.py are written by hand inside their
    period folder, so the rebuild reads them first and writes them back after.
    """
    names = []
    if (day, period) in LABS:
        names.append(f"{LABS[(day, period)]}_instructor.py")
    if (day, period) == BUG_HUNT_PERIOD:
        names.append("bug_hunt/hunt.py")
    kept = {}
    for name in names:
        if not (folder / name).exists():
            raise FileNotFoundError(f"{folder / name} is hand-written; restore it")
        kept[name] = (folder / name).read_text()
    return kept


def write_folder(folder: Path, files: dict[str, str], day_end_folder: Path) -> None:
    """Write a period folder, copying file permissions from the period4 copy."""
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir()
    for name, text in files.items():
        file_path = folder / name
        file_path.write_text(text, newline="")
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
        for name in lab_answer_files(day):
            day_end.pop(name, None)  # A lab's answer file belongs to its own period
        files_before = day_before
        for period in range(1, 5):
            if period == 4:
                files = day_end
            else:
                files = build_period(day, period, day_end, day_before)
                folder = day_folder(day) / f"period{period}"
                kept = keep_hand_written(day, period, folder)
                write_folder(folder, files, end_folder)
                if (day, period) == BUG_HUNT_PERIOD:
                    write_bug_hunt(folder)
                for name, text in kept.items():
                    (folder / name).write_text(text, newline="")
                    (folder / name).chmod(0o755)  # Each script runs on its own
                built.append(folder)
            readme = readme_text(day, period, files, files_before)
            (day_folder(day) / f"period{period}" / "README.md").write_text(readme)
            files_before = files
        day_before = day_end
    tidy(built)
    print(f"Built {len(built)} period folders  (expected 30)")


if __name__ == "__main__":
    main()
