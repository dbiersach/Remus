#!/usr/bin/env -S uv run
"""make_version_folders.py

Build one folder per color version in instructor/Day 09 .../period2/engines.

Remus-WHITE is the Day 9 Remus at the end of period 1, with none of the ten
enhancements: the period1 and period2 folders of Day 9 hold its engine. Its engine is
complete before the pairs start their color versions in period 2. Each color version
folder is Remus-WHITE plus one enhancement,
named by a color so that no color version sounds better than another. A pair builds its
color version, then its Remus plays Remus-WHITE to measure how much Elo the one
enhancement adds. Remus-GOLD, the finished Remus of Day 10, holds every
enhancement at once. Its folder, engines/Remus-GOLD, is written by hand, and this
script only rewrites its README.md. engines/Niram-GOLD holds the same engine in Rust.

The script copies the Day 9 files, adds the color version's files from the GOLD folder,
and applies the color version's edits. Each search enhancement gets a new search function
built from alpha_beta_with_quiescence, so the one idea it adds stands out. Run it
after any change to the Day 9 or GOLD code, then run make_student_folders.py.
"""

import ast
import shutil
import subprocess
import sys
from pathlib import Path

from period_guides import (
    CHANGE_NOTES,
    VERSION_GUIDES,
    VERSION_MEASURES,
    VERSION_OBJECTIVES,
)

ROOT = Path(__file__).parent.parent  # The top Remus folder, above scripts/
INSTRUCTOR = ROOT / "instructor"
BASE = next(INSTRUCTOR.glob("Day 09 - *")) / "period1"  # Remus-WHITE
REMUS_FOLDER = BASE.parent / "period2" / "engines"  # The color versions and GOLD
FINAL = REMUS_FOLDER / "Remus-GOLD"  # Written by hand


def function_text(file_path: Path, name: str) -> str:
    """Return the source of one top-level function or constant, with its comments."""
    source = file_path.read_text()
    lines = source.splitlines(keepends=True)
    for node in ast.parse(source).body:
        names = []
        if isinstance(node, ast.FunctionDef):
            names = [node.name]
        elif isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if name in names:
            return "".join(lines[node.lineno - 1 : node.end_lineno])
    raise ValueError(f"{name} not found in {file_path.name}")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    """Replace text that must appear exactly once."""
    count = text.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected one match, found {count}: {old[:60]!r}")
    return text.replace(old, new)


BASE_SEARCH = function_text(BASE / "search.py", "alpha_beta_with_quiescence")
BASE_SUMMARY = """    The full Day 8 search: alpha-beta with quiescence at the leaves, ordered
    moves, a check extension, a clock, and the line of best play."""
THINK_CALL = """            score, pv = alpha_beta_with_quiescence(
                state, depth, 0, -MATE_SCORE - 1, MATE_SCORE + 1, info, best
            )"""
EVALUATE_SUM = 'white_score = material(state["board"]) + placement(state["board"])'
EVALUATE_DOC = (
    "        Material plus placement in centipawns, positive when the side to move"
)
EXPLAIN_LAST = '    print(f"  Score for the side to move'


def version_search(name: str, summary: str, edits: list[tuple[str, str]]) -> str:
    """Return alpha_beta_with_quiescence renamed to `name`, with the color version's edits."""
    text = BASE_SEARCH.replace("alpha_beta_with_quiescence(", f"{name}(")
    text = replace_once(text, BASE_SUMMARY, summary, name)
    for old, new in edits:
        text = replace_once(text, old, new, name)
    return text


# Lines of alpha_beta_with_quiescence that the search enhancements change
AFTER_QUIESCENCE = """    if depth <= 0:
        return quiescence(state, alpha, beta, info), []
"""
ORDER_LOOP = """    for move in order_moves(moves, state["board"], first):
"""
CUTOFF = """        if score >= beta:
            return score, [move] + line  # Cutoff: the opponent will not allow this
"""
FINAL_RETURN = """    return alpha, best_line
"""
CHILD_SEARCH = """            score, line = {name}(
                state, depth - 1, ply + 1, -beta, -alpha, info
            )
            score = -score
"""

RED_SEARCH = version_search(
    "table_search",
    """    The Remus-RED search: the Day 9 search plus a transposition table. A
    position already searched deeply enough is not searched again, and its stored
    best move is tried first.""",
    [
        (
            AFTER_QUIESCENCE,
            AFTER_QUIESCENCE
            + """    key = state["history"][-1]
    stored = probe(info.table, key, depth, alpha, beta)
    if ply > 0 and stored is not None:
        return stored, []
""",
        ),
        (
            ORDER_LOOP,
            """    original_alpha = alpha
    first = first or best_stored_move(info.table, key)
"""
            + ORDER_LOOP,
        ),
        (
            CUTOFF,
            """        if score >= beta:
            if abs(score) < MATE_SCORE - 1000:
                store(info.table, key, depth, score, LOWER, move)
            return score, [move] + line  # Cutoff: the opponent will not allow this
""",
        ),
        (
            FINAL_RETURN,
            """    # Mate scores depend on ply, so they are not stored
    if abs(alpha) < MATE_SCORE - 1000:
        bound = EXACT if alpha > original_alpha else UPPER
        store(info.table, key, depth, alpha, bound, best_line[0] if best_line else None)
"""
            + FINAL_RETURN,
        ),
    ],
)

BLUE_SEARCH = version_search(
    "killer_search",
    """    The Remus-BLUE search: the Day 9 search plus killer moves. A quiet move
    that caused a cutoff at this ply is tried right after the captures in the
    next position at the same ply.""",
    [
        (
            ORDER_LOOP,
            """    killers = info.killers.get(ply)
    for move in order_moves(moves, state["board"], first, killers):
""",
        ),
        (
            CUTOFF,
            """        if score >= beta:
            remember_killer(info, ply, move, state["board"])
            return score, [move] + line  # Cutoff: the opponent will not allow this
""",
        ),
    ],
)

PINK_LATER_MOVE = '''def search_later_move(
    state: dict, depth: int, ply: int, alpha: int, beta: int, info: SearchInfo
) -> tuple[int, list[Move]]:
    """
    Search a move after the first one, which is made already, the PVS way.

    Parameters
    ----------
    state : dict
        The game state after the move.
    depth : int
        How many more plies to look ahead from here.
    ply : int
        How many moves from the root this position is.
    alpha, beta : int
        The window of the position before the move, for the side that moved.
    info : SearchInfo
        Counts positions and holds the deadline.

    Returns
    -------
    tuple[int, list[Move]]
        The move's score for the side that moved, and its line. First a null
        window (alpha, alpha + 1) asks only "is this move better than alpha?".
        Only a surprise, a score between alpha and beta, gets a second search with
        the full window to find the exact score.
    """
    score, line = pvs_search(state, depth, ply, -alpha - 1, -alpha, info)
    score = -score
    if alpha < score < beta:  # A surprise: search it again with the full window
        score, line = pvs_search(state, depth, ply, -beta, -alpha, info)
        score = -score
    return score, line


'''

PINK_SEARCH = version_search(
    "pvs_search",
    """    The Remus-PINK search: the Day 9 search plus principal variation search.
    The first move, the best one by the move ordering, gets the full window, and
    every later move first gets a cheap null window.""",
    [
        (
            ORDER_LOOP,
            """    ordered = order_moves(moves, state["board"], first)
    for index, move in enumerate(ordered):
""",
        ),
        (
            CHILD_SEARCH.format(name="pvs_search"),
            """            if index == 0:
                score, line = pvs_search(
                    state, depth - 1, ply + 1, -beta, -alpha, info
                )
                score = -score
            else:
                score, line = search_later_move(
                    state, depth - 1, ply + 1, alpha, beta, info
                )
""",
        ),
    ],
)

YELLOW_DRAW = '''def is_draw_in_search(state: dict) -> bool:
    """
    Return True if the search should score this position as a draw.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    bool
        True if the position already appeared earlier in the game or the search
        (its key is in the history at least twice), or if the halfmove clock has
        reached 100, the fifty-move limit. Repeating a position gains nothing, so
        the search scores it 0 instead of chasing a win that cannot happen.
    """
    key = state["history"][-1]
    return state["history"].count(key) >= 2 or state["halfmove_clock"] >= 100


'''

YELLOW_SEARCH = version_search(
    "draw_sense_search",
    """    The Remus-YELLOW search: the Day 9 search plus draw sense. A position
    that repeats, or that reaches the fifty-move limit, scores 0.""",
    [
        (
            """    check_time(info)
""",
            """    check_time(info)
    if ply > 0 and is_draw_in_search(state):
        return 0, []  # Draw sense: a repeated position is a draw, not a gain
""",
        ),
    ],
)

ORANGE_HELPERS = (
    function_text(FINAL / "search.py", "make_null_move")
    + "\n\n"
    + function_text(FINAL / "search.py", "undo_null_move")
    + "\n\n"
    + function_text(FINAL / "search.py", "has_pieces")
    + "\n\n"
)

ORANGE_SEARCH = version_search(
    "null_move_search",
    """    The Remus-ORANGE search: the Day 9 search plus null-move pruning. The side
    to move passes, so the opponent moves twice, and runs a shallower search. If
    the side to move still scores at least beta, the opponent would never allow
    this position, because a real move almost always beats a pass, so the
    position is cut off early.""",
    [
        (
            """    first: Move | None = None,
) -> tuple[int, list[Move]]:""",
            """    first: Move | None = None,
    allow_null: bool = True,
) -> tuple[int, list[Move]]:""",
        ),
        (
            """    first : Move | None
        A move to try first, such as the best move of the last iteration.
""",
            """    first : Move | None
        A move to try first, such as the best move of the last iteration.
    allow_null : bool
        False right after a null move, so that two passes never follow each other.
""",
        ),
        (
            AFTER_QUIESCENCE,
            AFTER_QUIESCENCE
            + """    # Never pass in check (passing would be illegal) or with only pawns left,
    # where passing can be better than any move (zugzwang)
    can_pass = allow_null and ply > 0 and not in_check_now and depth >= 3
    if can_pass and abs(beta) < MATE_SCORE - 1000 and has_pieces(
        state["board"], state["turn"]
    ):
        en_passant = make_null_move(state)
        try:
            score, _ = null_move_search(
                state,
                depth - 1 - NULL_MOVE_REDUCTION,
                ply + 1,
                -beta,
                -beta + 1,
                info,
                allow_null=False,
            )
            score = -score
        finally:
            undo_null_move(state, en_passant)
        if score >= beta:
            return beta, []
""",
        ),
    ],
)

BROWN_SEARCH = version_search(
    "reduced_search",
    """    The Remus-BROWN search: the Day 9 search plus late move reductions. Late,
    quiet moves get a search one ply shallower, and a full-depth search only if
    they turn out better than alpha.""",
    [
        (
            ORDER_LOOP,
            """    ordered = order_moves(moves, state["board"], first)
    for index, move in enumerate(ordered):
""",
        ),
        (
            CHILD_SEARCH.format(name="reduced_search"),
            """            gives_check = in_check(state, state["turn"])
            cut = reduction(depth, index, move, undo["captured"], gives_check)
            score, line = reduced_search(
                state, depth - 1 - cut, ply + 1, -beta, -alpha, info
            )
            score = -score
            if cut and score > alpha:  # A late move surprised: search full depth
                score, line = reduced_search(
                    state, depth - 1, ply + 1, -beta, -alpha, info
                )
                score = -score
""",
        ),
    ],
)


def search_version(
    color: str,
    function: str,
    helpers: str,
    search: str,
    imports: list[tuple[str, str]],
    extra: list[tuple[str, str, str]],
) -> list[tuple[str, str, str]]:
    """Return the edits that add a version search to the Day 9 search.py."""
    edits = [
        (
            "search.py",
            "def format_info(",
            helpers + search + "\n\ndef format_info(",
        ),
        (
            "search.py",
            THINK_CALL,
            THINK_CALL.replace("alpha_beta_with_quiescence", function),
        ),
        (
            "search.py",
            "one move deeper at a time until the clock runs out.\n",
            (
                "one move deeper at a time until the clock runs out.\n\n"
                f"The {color} color version adds {function}, and think uses it.\n"
            ),
        ),
    ]
    edits += [("search.py", old, new) for old, new in imports]
    return edits + extra


TABLE_FIELD = (
    "    deadline: float | None = None  # time.perf_counter() value when the search "
    "must stop\n"
)


def evaluation_version(color: str, term: str, constants: list[str], label: str):
    """Return the edits that add one evaluation term to the Day 9 evaluation.py."""
    constant_text = "".join(
        function_text(FINAL / "evaluation.py", name) for name in constants
    )
    return [
        (
            "evaluation.py",
            "PLACEMENT_TABLES = {",
            constant_text + "PLACEMENT_TABLES = {",
        ),
        (
            "evaluation.py",
            "def evaluate(",
            function_text(FINAL / "evaluation.py", term) + "\n\ndef evaluate(",
        ),
        (
            "evaluation.py",
            EVALUATE_SUM,
            (
                f'board = state["board"]\n    white_score = material(board) + placement(board)'
                f" + {term}(board)"
            ),
        ),
        (
            "evaluation.py",
            EVALUATE_DOC,
            (
                f"        Material, placement, and {term.replace('_', ' ')} in centipawns, "
                "positive when the side\n        to move"
            ),
        ),
        (
            "evaluation.py",
            EXPLAIN_LAST,
            f'    print(f"  {label:<10} {{{term}(board):+}} centipawns for White")\n'
            + EXPLAIN_LAST,
        ),
        (
            "evaluation.py",
            "the table upside down, so its row 7 uses the table's row 0.\n",
            (
                "the table upside down, so its row 7 uses the table's row 0.\n\n"
                f"The {color} color version adds a third term, {term}.\n"
            ),
        ),
    ]


def test_text(header: str, imports: str, tests: list[str], extra: str = "") -> str:
    """Return a color version's test_upgrades.py: its own tests plus tests from GOLD."""
    final_tests = FINAL / "test_upgrades.py"
    bodies = "".join(function_text(final_tests, name) + "\n\n" for name in tests)
    return (
        f'"""test_upgrades.py\n\n{header}\n"""\n\n{imports}\n'
        'ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"\n'
        "WIDE = (-MATE_SCORE - 1, MATE_SCORE + 1)  # A window that every score fits inside\n"
        f"\n\n{bodies}{extra}"
    )


def agreement_test(function: str) -> str:
    """Return a test that a version search finds the plain search's score."""
    return f'''def test_{function}_agrees_with_alpha_beta() -> None:
    """The color version saves work but finds the same score at the same depth."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, SearchInfo())
    score, pv = {function}(state, 3, 0, *WIDE, SearchInfo())
    assert score == plain_score
    assert pv
    assert state_snapshot(state) == before


'''


PINK_NULL_WINDOW_TEST = '''def test_a_null_window_answers_only_better_or_not() -> None:
    """A null window (alpha, alpha + 1) says only whether the exact score beats alpha."""
    state = state_from_fen(ITALIAN)
    exact, _ = pvs_search(state, 3, 0, *WIDE, SearchInfo())
    for alpha in (exact - 50, exact + 50):
        score, _ = pvs_search(state, 3, 0, alpha, alpha + 1, SearchInfo())
        assert (score > alpha) == (exact > alpha)


'''


def saving_test(function: str) -> str:
    """Return a test that a pruning version search visits fewer positions."""
    return f'''def test_{function}_saves_work_and_keeps_the_state() -> None:
    """The upgraded search visits fewer positions than plain alpha-beta at depth 4."""
    state = state_from_fen(ITALIAN)
    before = state_snapshot(state)
    plain = SearchInfo()
    upgraded = SearchInfo()
    alpha_beta_with_quiescence(state, 4, 0, *WIDE, plain)
    _, pv = {function}(state, 4, 0, *WIDE, upgraded)
    assert upgraded.nodes < plain.nodes
    assert pv
    assert state_snapshot(state) == before


'''


SEARCH_TEST_IMPORTS = """from fen import state_from_fen
from make_move import state_snapshot
from search import MATE_SCORE, SearchInfo, alpha_beta_with_quiescence, {names}
"""

# For each color version: the folder name, the idea in one line, the files it copies
# from the GOLD folder, its edits as (file, old text, new text), its test file,
# and the functions the pair writes
VERSIONS_TABLE = [
    {
        "folder": "Remus-GOLD",
        "idea": "Remus-GOLD is the finished Remus of Day 10, with all ten "
        "enhancements at once. It lives only in the teacher's folders; "
        "estimate_elo.py measures its rating against Stockfish, and Niram-GOLD, "
        "beside it, is the same engine in Rust.",
        "source": FINAL,
        "copies": [],
        "edits": [],
        "tests": "",
        "students": [],
    },
    {
        "folder": "10 RED - Transposition table",
        "idea": "Remember positions already searched, so the same position reached "
        "in two move orders is scored once.",
        "copies": ["transposition_table.py"],
        "edits": search_version(
            "RED",
            "table_search",
            "",
            RED_SEARCH,
            [
                (
                    "from dataclasses import dataclass\n",
                    "from dataclasses import dataclass, field\n",
                ),
                (
                    "from moves import Move, move_to_uci\n",
                    (
                        "from moves import Move, move_to_uci\nfrom transposition_table "
                        "import EXACT, LOWER, UPPER, best_stored_move, probe, store\n"
                    ),
                ),
                (
                    TABLE_FIELD,
                    TABLE_FIELD
                    + "    table: dict = field(default_factory=dict)  # position_key "
                    "-> entry\n",
                ),
            ],
            [],
        ),
        "tests": test_text(
            "Tests for the RED color version: the transposition table and table_search.",
            SEARCH_TEST_IMPORTS.format(names="table_search")
            + "from fen import START_FEN\nfrom game_state import position_key\n"
            "from make_move import make_move\nfrom moves import Move, move_from_uci\n"
            "from transposition_table import EXACT, LOWER, UPPER, best_stored_move, "
            "probe, store\n",
            [
                "test_transposition_table_bounds",
                "test_two_move_orders_reach_one_position_key",
            ],
            agreement_test("table_search"),
        ),
        "students": [
            ("transposition_table.py", "store"),
            ("transposition_table.py", "probe"),
            ("test_upgrades.py", "test_transposition_table_bounds"),
        ],
    },
    {
        "folder": "08 GREEN - Opening book",
        "idea": "Play the first moves of well-known openings from a book instead of "
        "searching.",
        "copies": ["opening_book.py", "opening_book.txt"],
        "edits": [
            (
                "uci_engine.py",
                '"bestmove" before Remus listens again.\n',
                (
                    '"bestmove" before Remus listens again. The "think" brain plays a '
                    "move from the\nopening book first, while the position is in the "
                    "book.\n"
                ),
            ),
            (
                "uci_engine.py",
                "from search import",
                "from opening_book import book_move, load_book\nfrom search import",
            ),
            (
                "uci_engine.py",
                "    state = state_from_fen(START_FEN)\n    for line",
                "    state = state_from_fen(START_FEN)\n    book = load_book()\n    for line",
            ),
            (
                "uci_engine.py",
                '        elif command == "go":\n',
                (
                    '        elif command == "go":\n            opening = book_move(book, '
                    "state)  # None once the game leaves the book\n"
                ),
            ),
            (
                "uci_engine.py",
                "            else:\n                seconds = thinking_time(",
                (
                    '            elif opening is not None:\n                send(f"bestmove '
                    '{move_to_uci(opening)}")\n            else:\n                seconds = thinking_time('
                ),
            ),
            (
                "console_game.py",
                "from search import think_move\n",
                (
                    "from opening_book import book_move, load_book\nfrom search import "
                    "think_move\n"
                ),
            ),
            (
                "console_game.py",
                "    state = state_from_fen(START_FEN)\n",
                "    book = load_book()\n    state = state_from_fen(START_FEN)\n",
            ),
            (
                "console_game.py",
                "            move = think_move(state)\n",
                (
                    "            move = book_move(book, state) or think_move(state)  "
                    "# Book first\n"
                ),
            ),
        ],
        "tests": test_text(
            "Tests for the GREEN color version: the opening book.",
            "from fen import START_FEN, state_from_fen\nfrom make_move import "
            "make_move\nfrom moves import move_to_uci\nfrom notation import parse_san\n"
            "from opening_book import BOOK_PATH, book_move, load_book\n"
            "from search import MATE_SCORE\n",
            [
                "test_opening_book_is_legal_and_answers_e4",
                "test_book_typo_is_skipped_without_touching_stdout",
                "test_trap_line_stores_only_the_defenders_moves",
                "test_book_answers_scholars_mate_but_never_tries_it",
                "test_missing_book_never_stops_play",
            ],
        ),
        "students": [
            ("opening_book.py", "load_book"),
            ("opening_book.py", "book_move"),
        ],
    },
    {
        "folder": "09 BLUE - Killer moves",
        "idea": "Try quiet moves that caused a cutoff at the same depth right after "
        "the captures.",
        "copies": ["move_ordering.py"],
        "edits": search_version(
            "BLUE",
            "killer_search",
            function_text(FINAL / "search.py", "remember_killer") + "\n\n",
            BLUE_SEARCH,
            [
                (
                    "from dataclasses import dataclass\n",
                    "from dataclasses import dataclass, field\n",
                ),
                (
                    "from board import EMPTY, piece_at\n",
                    "from board import EMPTY, Board, piece_at\n",
                ),
                (
                    TABLE_FIELD,
                    TABLE_FIELD
                    + "    killers: dict = field(default_factory=dict)  # Ply -> up "
                    "to two killer moves\n",
                ),
            ],
            [],
        ),
        "tests": test_text(
            "Tests for the BLUE color version: killer moves and killer_search.",
            SEARCH_TEST_IMPORTS.format(names="killer_search, remember_killer")
            + "from fen import START_FEN\nfrom moves import move_from_uci, "
            "move_to_uci\n",
            ["test_killers_keep_two_quiet_moves"],
            agreement_test("killer_search"),
        ),
        "students": [
            ("search.py", "remember_killer"),
            ("move_ordering.py", "order_moves"),
            ("test_upgrades.py", "test_killers_keep_two_quiet_moves"),
        ],
    },
    {
        "folder": "04 PINK - Principal variation search",
        "idea": "Search the first move with the full window and every other move "
        "with a cheap null window first.",
        "copies": [],
        "edits": search_version(
            "PINK", "pvs_search", PINK_LATER_MOVE, PINK_SEARCH, [], []
        ),
        "tests": test_text(
            "Tests for the PINK color version: principal variation search.",
            SEARCH_TEST_IMPORTS.format(names="pvs_search"),
            [],
            agreement_test("pvs_search") + PINK_NULL_WINDOW_TEST,
        ),
        "students": [
            ("search.py", "search_later_move"),
            ("test_upgrades.py", "test_pvs_search_agrees_with_alpha_beta"),
            ("test_upgrades.py", "test_a_null_window_answers_only_better_or_not"),
        ],
    },
    {
        "folder": "02 YELLOW - Draw sense",
        "idea": "Score a repeated position, or one at the fifty-move limit, as a "
        "draw inside the search.",
        "copies": [],
        "edits": search_version(
            "YELLOW", "draw_sense_search", YELLOW_DRAW, YELLOW_SEARCH, [], []
        ),
        "tests": test_text(
            "Tests for the YELLOW color version: draw sense.",
            SEARCH_TEST_IMPORTS.format(names="draw_sense_search, is_draw_in_search")
            + "from fen import START_FEN\nfrom make_move import make_move\n"
            "from moves import move_from_uci\n",
            [],
            agreement_test("draw_sense_search")
            + '''def test_a_repeated_position_is_a_draw() -> None:
    """After Nf3 Nf6 Ng1 Ng8 the starting position appears for the second time."""
    state = state_from_fen(START_FEN)
    assert not is_draw_in_search(state)
    for text in ("g1f3", "g8f6", "f3g1", "f6g8"):
        make_move(state, move_from_uci(text))
    assert is_draw_in_search(state)


def test_the_fifty_move_limit_is_a_draw() -> None:
    """A halfmove clock of 100 is 50 moves by each side with no capture or pawn move."""
    state = state_from_fen("4k3/8/8/8/8/8/8/R3K3 w - - 100 80")
    assert is_draw_in_search(state)


''',
        ),
        "students": [
            ("search.py", "is_draw_in_search"),
            ("test_upgrades.py", "test_draw_sense_search_agrees_with_alpha_beta"),
            ("test_upgrades.py", "test_a_repeated_position_is_a_draw"),
            ("test_upgrades.py", "test_the_fifty_move_limit_is_a_draw"),
        ],
    },
    {
        "folder": "07 PURPLE - Pawn structure",
        "idea": "Penalize doubled and isolated pawns and reward passed pawns.",
        "copies": [],
        "edits": evaluation_version(
            "PURPLE",
            "pawn_structure",
            ["DOUBLED_PAWN", "ISOLATED_PAWN", "PASSED_PAWN"],
            "Pawns:",
        ),
        "tests": test_text(
            "Tests for the PURPLE color version: pawn structure.",
            "from evaluation import pawn_structure\nfrom fen import START_FEN, "
            "state_from_fen\nfrom search import MATE_SCORE\n",
            [
                "test_pawn_structure_is_level_at_the_start",
                "test_doubled_isolated_pawns_cost_points",
                "test_a_passed_pawn_earns_a_bonus",
            ],
        ),
        "students": [("evaluation.py", "pawn_structure")],
    },
    {
        "folder": "03 CYAN - Mating bonus",
        "idea": "With a big material lead, drive the losing king to the edge and "
        "bring the winning king close.",
        "copies": [],
        "edits": evaluation_version(
            "CYAN",
            "mating_bonus",
            ["CENTER_DISTANCE", "MATING_MARGIN", "WEAK_SIDE_LIMIT"],
            "Mating:",
        ),
        "tests": test_text(
            "Tests for the CYAN color version: the mating bonus.",
            "from evaluation import mating_bonus\nfrom fen import state_from_fen\n"
            "from search import MATE_SCORE\n",
            ["test_mating_bonus_prefers_the_losing_king_in_the_corner"],
        ),
        "students": [("evaluation.py", "mating_bonus")],
    },
    {
        "folder": "05 ORANGE - Null-move pruning",
        "idea": "Let the opponent move twice in a shallow search. If Remus is still "
        "too far ahead, the opponent would never allow this position, so stop "
        "searching it.",
        "copies": [],
        "edits": search_version(
            "ORANGE",
            "null_move_search",
            ORANGE_HELPERS,
            ORANGE_SEARCH,
            [
                (
                    "from board import EMPTY, piece_at\n",
                    "from board import EMPTY, Board, Square, piece_at\n",
                ),
                (
                    "from fen import state_from_fen\n",
                    (
                        "from fen import state_from_fen\nfrom game_state import "
                        "opponent, position_key\n"
                    ),
                ),
                (
                    "# Larger than any material count",
                    (
                        "NULL_MOVE_REDUCTION = 2  # How many plies shallower the "
                        "null-move search looks\n# Larger than any material count"
                    ),
                ),
            ],
            [],
        ),
        "tests": test_text(
            "Tests for the ORANGE color version: null-move pruning.",
            SEARCH_TEST_IMPORTS.format(
                names="make_null_move, null_move_search, undo_null_move"
            ),
            ["test_null_move_and_undo_restore_the_state"],
            saving_test("null_move_search"),
        ),
        "students": [
            ("search.py", "make_null_move"),
            ("search.py", "undo_null_move"),
            ("test_upgrades.py", "test_null_move_and_undo_restore_the_state"),
            (
                "test_upgrades.py",
                "test_null_move_search_saves_work_and_keeps_the_state",
            ),
        ],
    },
    {
        "folder": "06 BROWN - Late move reductions",
        "idea": "Search late, quiet moves one ply shallower, and in full only if "
        "they surprise.",
        "copies": [],
        "edits": search_version(
            "BROWN",
            "reduced_search",
            function_text(FINAL / "search.py", "reduction") + "\n\n",
            BROWN_SEARCH,
            [
                (
                    "# Larger than any material count",
                    (
                        "LATE_MOVE_INDEX = 3  # Moves after the first three in the "
                        "ordered list count as late\n# Larger than any material count"
                    ),
                ),
            ],
            [],
        ),
        "tests": test_text(
            "Tests for the BROWN color version: late move reductions.",
            SEARCH_TEST_IMPORTS.format(names="reduced_search, reduction")
            + "from board import EMPTY\nfrom moves import Move\n",
            ["test_only_late_quiet_moves_are_reduced"],
            saving_test("reduced_search"),
        ),
        "students": [
            ("search.py", "reduction"),
            ("test_upgrades.py", "test_only_late_quiet_moves_are_reduced"),
            ("test_upgrades.py", "test_reduced_search_saves_work_and_keeps_the_state"),
        ],
    },
    {
        "folder": "01 GRAY - King safety",
        "idea": "While the enemy queen is on the board, reward pawns that shelter "
        "the king.",
        "copies": [],
        "edits": evaluation_version("GRAY", "king_safety", ["SHIELD_PAWN"], "King:"),
        "tests": test_text(
            "Tests for the GRAY color version: king safety.",
            "from evaluation import king_safety\nfrom fen import START_FEN, "
            "state_from_fen\nfrom search import MATE_SCORE\n",
            ["test_king_safety_rewards_the_pawn_shield"],
        ),
        "students": [("evaluation.py", "king_safety")],
    },
]


def measured_table(color: str) -> str:
    """Return the Markdown table that compares a version's search with Remus-WHITE."""
    rows = ["WHITE"] if color == "WHITE" else ["WHITE", color]
    white = VERSION_MEASURES["WHITE"]
    lines = [
        (
            "| Version | Positions to finish depth 4 | Share of Remus-WHITE's | "
            "Positions per second | Average depth in 5 seconds |"
        ),
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name in rows:
        measure = VERSION_MEASURES[name]
        share = 100 * measure["nodes"] / white["nodes"]
        speed = measure["nodes"] / measure["seconds"]
        lines.append(
            f"| Remus-{name} | {measure['nodes']:,} | {share:.0f}% | {speed:,.0f} | "
            f"{measure['depth']:.1f} |"
        )
    return (
        "Each version searched the ten positions of `compare_search.py`, one depth at "
        "a time up to depth 4, on one computer. Fewer positions for the same depth "
        "means a smaller search tree. Positions per second shows what each position "
        "costs. The last column gave each position 5 seconds, the way a game does, "
        "and averages the deepest search that finished.\n\n" + "\n".join(lines)
    )


def readme_text(version: dict) -> str:
    """Return the README.md that explains one version folder."""
    if version["folder"] == FINAL.name:
        color, name = "GOLD", "All enhancements"
    else:
        number_and_color, name = version["folder"].split(" - ")
        color = number_and_color.split(" ")[1]  # "10 RED" gives "RED"
    guide = VERSION_GUIDES[color]
    sections = [
        f"# Remus-{color}: {name}\n\n{version['idea']}",
    ]
    if version["students"]:
        objectives = "\n".join(
            f"- {objective} **Measured by:** {measure}"
            for objective, measure in VERSION_OBJECTIVES
        )
        sections.append(
            "## Learning objectives\n\n"
            f"By the end of Day 9, each pair can:\n\n{objectives}"
        )
    sections += [
        f"## The idea, with an example\n\n{guide['example']}",
        f"## {guide.get('why_title', 'Why it makes Remus stronger')}\n\n{guide['why']}",
        f"## What it costs\n\n{guide['cost']}",
        f"## Measured against Remus-WHITE\n\n{measured_table(color)}",
        f"## What to expect\n\n{guide['expect']}",
    ]
    if color == "GOLD":
        sections.append(
            "## Check it\n\nCheck it from inside this folder with `uv run pytest`, "
            "and rate it against Stockfish by opening `estimate_elo.py` and clicking "
            "Run Python File. From the "
            "top Remus folder, "
            '`uv run scripts/version_league.py --niram --rate-only --event "Niram league 1" --book-start --player GOLD` '
            "shows its score against every other version in the teacher's league."
        )
    else:
        written = ", ".join(
            f"`{function}()` in `{file}`" for file, function in version["students"]
        )
        changes = "\n\n".join(
            f"### `{function}()` in `{file}`\n\n{CHANGE_NOTES[(file, function)]}"
            for file, function in version["students"]
        )
        sections += [
            f"## Where your code fits\n\n{guide['fits']}",
            (
                "## The files\n\nThis folder is Remus-WHITE, the finished Day 9 Remus in "
                "`period1`, "
                f"plus this one enhancement. The pair writes {written}."
            ),
            f"## The changes and why\n\n{changes}",
            (
                "## Check it\n\nCheck the work from inside this folder with "
                "`uv run pytest`. Then open `smoke_test.py` in VS Code and press Run: "
                f"Remus-{color} plays one 2-minute game against Remus-WHITE, which "
                "shows that the engine plays legal moves to the end of a game. In the "
                "Day 9 battles, copy the visiting pair's color folder into the `engines` "
                "folder, open `play_battle.py`, press Run, and type the visitor's "
                f"color: Remus-{color} plays it twice at 10 minutes a side, once with "
                "each color, and both games go into games/remus_games.pgn. Each "
                "script runs `version_match.py` from the `engines` folder above this one."
            ),
        ]
    return "\n\n".join(sections) + "\n"


def tidy(folders: list[Path]) -> None:
    """Remove unused imports and format the code with ruff."""
    paths = [str(folder) for folder in folders]
    ruff = [sys.executable, "-m", "ruff"]
    subprocess.run(
        ruff + ["check", "--quiet", "--fix", "--select", "F401,I001", *paths],
        check=False,
    )
    subprocess.run(ruff + ["format", "--quiet", *paths], check=True)


RUN_SCRIPTS = {
    "play_battle.py": (
        (
            "The Day 9 battle for this color version. Copy the visiting pair's color "
            "folder into\nthe engines folder on this laptop, press Run in VS Code, and "
            "type the visitor's\ncolor. Remus-{color} plays two 10-minute games "
            "against it from the same opening,\nWhite in game 1 and Black in game 2. "
            "The two games take about 20 minutes."
        ),
        ["OPPONENT"],
    ),
    "smoke_test.py": (
        (
            "The Day 9 smoke test for this color version. Press Run in VS Code: Remus-{color} "
            "plays\none 2-minute game against Remus-WHITE, which shows that the engine "
            "plays legal\nmoves to the end of a game. Nobody reads the result."
        ),
        ["--games", "1", "--minutes", "2"],
    ),
}  # File name -> (what it does, the extra arguments for version_match.py)


def run_script_text(name: str, color: str) -> str:
    """Return a script that runs version_match.py for one color from the Run button."""
    about, extra = RUN_SCRIPTS[name]
    arguments = ""
    ask = ""
    for word in [color, *extra]:
        if word == "OPPONENT":
            arguments += ", opponent"
            # The visitor types its color, such as RED, in the VS Code terminal
            ask = (
                '    opponent = input("The visiting color, such as RED: ")'
                ".strip().upper()\n"
            )
        else:
            arguments += f', "{word}"'
    return (
        f'#!/usr/bin/env -S uv run\n"""{name}\n\n{about.format(color=color)}\n'
        "version_match.py, in the Remus folder above this one, plays the games and "
        'adds\nthem to games/remus_games.pgn.\n"""\n\n'
        "import subprocess\nimport sys\nfrom pathlib import Path\n\n\n"
        "def main():\n"
        + ask
        + '    match_path = Path(__file__).parent.parent / "version_match.py"\n'
        '    print(f"Running {match_path}")\n'
        "    # sys.executable is the Python that VS Code runs, with python-chess\n"
        f"    subprocess.run([sys.executable, str(match_path){arguments}], check=True)\n"
        '\n\nif __name__ == "__main__":\n    main()\n'
    )


def main():
    REMUS_FOLDER.mkdir(parents=True, exist_ok=True)
    built = []
    for version in VERSIONS_TABLE:
        folder = REMUS_FOLDER / version["folder"]
        if folder == FINAL:
            # GOLD is written by hand: only its README is rebuilt
            (folder / "README.md").write_text(readme_text(version))
            continue
        if folder.exists():
            shutil.rmtree(folder)
        shutil.copytree(
            version.get("source", BASE),
            folder,
            ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "*.svg", "README.md"),
        )
        for name in version["copies"]:
            shutil.copy2(FINAL / name, folder / name)
        for file_name, old, new in version["edits"]:
            file_path = folder / file_name
            text = replace_once(file_path.read_text(), old, new, version["folder"])
            file_path.write_text(text)
        if version["tests"]:
            (folder / "test_upgrades.py").write_text(version["tests"])
        (folder / "README.md").write_text(readme_text(version))
        if version["students"]:
            color = version["folder"].split(" - ")[0].split()[-1]
            for name in RUN_SCRIPTS:
                (folder / name).write_text(run_script_text(name, color))
                (folder / name).chmod(0o755)  # The shebang runs it on Mac and Linux
        built.append(folder)
    tidy(built)
    print(f"Built {len(built)} color version folders in {REMUS_FOLDER}  (expected 10)")
    print(f"Kept the hand-written {FINAL.name} and rewrote its README.md")


if __name__ == "__main__":
    main()
