#!/usr/bin/env -S uv run
"""period_guides.py

The teaching text of every period goals file: the learning objectives, each with a way
to measure it, and one paragraph for every change the student pairs make to the code. It
also holds the overview of every day, which goes into the syllabus at the top of
each Day folder ("Day NN Syllabus.md").

make_period_folders.py writes this text into each period goals file, such as
"Day 03 Period 02 Goals.md", and make_student_folders.py adds the period's timed
steps and tasks to it and writes the version READMEs. Keep
the language at a middle school reading level: short sentences, one idea each.
"""

# The Python skills lab files, by (day, period). Each name has a student file
# <name>.py in the student period folder and an answer file <name>_instructor.py in
# the instructor period folder; both are written by hand and kept by the builders
LABS = {
    (1, 1): "python_setup",
    (1, 2): "python_strings",
    (1, 3): "python_lists",
    (2, 1): "python_functions",
    (2, 2): "python_dicts",
    (3, 1): "python_loops",
    (4, 1): "python_modules",
    (4, 4): "demo_practice_positions",
    (5, 1): "python_sets",
    (5, 4): "demo_promotion",
    (6, 1): "python_recursion",
    (6, 4): "python_fen_fields",
    (7, 2): "python_input_output",
    (8, 2): "python_sorting",
    (9, 2): "python_caches",
    (9, 4): "demo_results",
}

# (day, period) -> [(objective, how the teacher measures it)]
OBJECTIVES = {
    (1, 1): [
        (
            "Start VS Code, open a Python file, and run it with the Run Python File button (the triangle at the top right of the editor).",
            (
                "Running `python_setup.py` prints Python 3.14 or later and "
                "`python-chess installed: True` on the student pair's laptop."
            ),
        ),
        (
            "Store text in a variable and print it inside an f-string.",
            (
                "Part #2 of `python_setup.py` greets the student pair's own team name and counts "
                "its characters correctly."
            ),
        ),
        (
            (
                "Name the parts of a chess engine that Remus will grow: board, moves, "
                "rules, search, and evaluation."
            ),
            "Exit ticket: each student lists three of the five parts and one job of each.",
        ),
    ],
    (1, 2): [
        (
            "Pick single characters out of a string by index, counting from 0.",
            (
                "Part #1 of `python_strings.py` prints file letter e and rank digit 2 "
                'for `"e2"`.'
            ),
        ),
        (
            "Turn letters into numbers and back with `ord()` and `chr()`.",
            (
                'Part #2 prints file number 4 for e2, and Part #3 builds `"g7"` from '
                "file number 6 and rank 7."
            ),
        ),
        (
            "Tell White and Black pieces apart by uppercase and lowercase.",
            'Part #4 prints `RNBQKBNR` from `rnbqkbnr` and `True` for `"N".isupper()`.',
        ),
        (
            "Explain why file a is number 0.",
            (
                "Without running code, the student pair says the file number of h4 (7) and of "
                "a1 (0), and why."
            ),
        ),
    ],
    (1, 3): [
        (
            "Make a list, read one item by index, and count the items with `len()`.",
            "Part #1 of `python_lists.py` prints 8 pieces and `q` on the d-file.",
        ),
        (
            "Visit every item with `for` and `range()`.",
            "Part #2 prints the back rank `r n b q k b n r` on one line.",
        ),
        (
            "Build an 8x8 board as a list of rows and read `board[row][col]`.",
            (
                "Part #3 prints the starting position, and the student pair names the square "
                "`board[4][4]` (e4) without running code."
            ),
        ),
        (
            "Say where each rank lives: row 0 is rank 8.",
            (
                'Unplugged warm-up "Call the square": each student converts four squares '
                "on the printed board, such as e2 to (6, 4), with no mistakes."
            ),
        ),
    ],
    (1, 4): [
        (
            "Print the board with rank numbers and file letters.",
            (
                "Running `board.py` prints the start board with 8 at the top and a to h "
                "below it."
            ),
        ),
        (
            "Convert between square names and (row, col) in both directions.",
            "`test_board.py` passes, including e2 to (6, 4) and back.",
        ),
        (
            "Reject text that is not a square.",
            (
                '`parse_square("i9")` raises `ValueError`, and the student pair explains which '
                "check catches it."
            ),
        ),
    ],
    (2, 1): [
        (
            (
                "Write a function with parameters, a return value, type hints, and a "
                "docstring."
            ),
            (
                "The lab's `is_white()` and `on_board()` return the right answers for "
                "every example on the worksheet."
            ),
        ),
        (
            "Check a function with `assert` and with pytest.",
            (
                "`run_tests.py` shows the lab's tests passing, and one deliberately "
                "wrong `assert` fails with a clear report."
            ),
        ),
        (
            "Pack two numbers into a tuple and unpack them.",
            "The student pair writes `row, col = square` and explains what each name holds.",
        ),
    ],
    (2, 2): [
        (
            "Store named facts in a dict and read them back.",
            "The lab's state dict answers whose turn it is and the castling rights.",
        ),
        (
            "Explain aliasing: two names for one list.",
            (
                "The student pair predicts, then shows, that `b2 = board` changes both boards, "
                "and that a copy does not."
            ),
        ),
        (
            "Describe a record with a `dataclass`.",
            "The student pair makes a small `dataclass` and prints one of its fields.",
        ),
    ],
    (2, 3): [
        (
            "Tell the piece color of a piece, and handle an empty square.",
            (
                "The `is_white` and `color_of` tests in `test_make_move.py` pass, "
                "including `None` for `.`."
            ),
        ),
        (
            "Write a move as UCI text and read it back.",
            "`move_to_uci` and `move_from_uci` round-trip `e2e4` and `e7e8q`.",
        ),
        (
            "Name the fields of a game state.",
            "Exit ticket: list the six fields of the state dict and what each holds.",
        ),
    ],
    (2, 4): [
        (
            "Make a move and take it back exactly.",
            (
                "The make and undo tests pass, and ten moves made and undone leave the "
                "same state as the start, clocks and rights included."
            ),
        ),
        (
            "Explain why undo needs a record of what the move changed.",
            (
                "The student pair names what a capture destroys (the captured piece) and where "
                "the undo record keeps it."
            ),
        ),
    ],
    (3, 1): [
        (
            "Repeat steps with `while` and stop early with `break`.",
            "The lab's walk from d4 toward the edge stops at the first piece in its way.",
        ),
        (
            "Describe a direction as a (row change, col change) tuple.",
            (
                'The student pair writes the tuple for "up and to the right" (-1, 1) and '
                "explains the minus sign."
            ),
        ),
    ],
    (3, 2): [
        (
            "Generate knight and king moves from a list of jumps.",
            (
                "The jumping-piece tests pass: a knight on a1 has 2 moves and a king on "
                "a1 has 3."
            ),
        ),
        (
            "See the moves a generator returns.",
            (
                "Running `show_board.py` draws one arrow per king move, and the student pair "
                "counts the arrows."
            ),
        ),
    ],
    (3, 3): [
        (
            "Slide a rook, bishop, or queen until a piece or the edge stops it.",
            "The slider tests pass: a rook on d4 of an empty board has 14 moves.",
        ),
        (
            "Explain why a slider may land on an enemy piece but not on a friend.",
            "The student pair traces `slide()` by hand on a board with one friend and one enemy.",
        ),
    ],
    (3, 4): [
        (
            "Generate pawn pushes, including the two-step first move.",
            "The pawn tests pass, and the start position gives 20 pseudo-legal moves.",
        ),
        (
            "Explain why White pawns move toward row 0.",
            'Exit ticket: "Row 0 is rank 8, so a White pawn on row 6 moves to row ..."',
        ),
    ],
    (4, 1): [
        (
            "Split code into modules and import one from another.",
            (
                "The lab's two files run together, and running the imported file "
                "alone with the Run button prints its own self-check only through "
                "`main()`."
            ),
        ),
        (
            "Draw which Remus files import which, and name the file that runs.",
            (
                "The student pair's paper import map draws arrows from `move_generation.py` "
                "to `board.py`, `game_state.py`, and `moves.py`, and marks the lab "
                "as the file named `__main__`."
            ),
        ),
    ],
    (4, 2): [
        (
            "Decide whether a knight, pawn, or king attacks a square.",
            "The attack tests in `test_legal_moves.py` pass for all three pieces.",
        ),
        (
            "Explain that a pawn attacks diagonally but moves straight.",
            (
                "The student pair marks the two squares a White pawn on e4 attacks (d5, f5) on "
                "the printed board."
            ),
        ),
    ],
    (4, 3): [
        (
            "Tell whether a king is in check.",
            "The `in_check` tests pass in check and out of check.",
        ),
        (
            (
                "Keep only legal moves by making each move, testing the king, and "
                "undoing it."
            ),
            (
                "The legal-move tests pass: 20 moves from the start, only escapes in "
                "check, and no moves for a pinned knight."
            ),
        ),
    ],
    (4, 4): [
        (
            "Check the move generator on practice positions.",
            "Every practice-position test in `test_legal_moves.py` passes.",
        ),
        (
            "Predict a legal-move count before running the code.",
            (
                "In `demo_practice_positions.py` the student pair types its prediction for "
                "each position first, then runs the file and compares."
            ),
        ),
    ],
    (5, 1): [
        (
            "Use sets and `in` to test membership, and change strings with `replace()`.",
            'The lab removes `"K"` from `"KQkq"` when the h1 rook moves.',
        ),
    ],
    (5, 2): [
        (
            (
                "State the castling rules: no earlier king or rook move, empty squares "
                "between, and no check on the king's path."
            ),
            "Six-position quiz on castling: each student pair gets at least five right.",
        ),
        (
            "Update the castling rights after any move.",
            (
                "The castling tests in `test_special_moves.py` pass, including a "
                "captured rook."
            ),
        ),
    ],
    (5, 3): [
        (
            "Capture en passant on the very next move only.",
            (
                "The en passant tests pass, including the capture that is legal only "
                "once."
            ),
        ),
        (
            "Find the square of the pawn an en passant capture removes.",
            "The student pair names the removed pawn's square for exd6 (d5) on the printed board.",
        ),
    ],
    (5, 4): [
        (
            "Promote a pawn to any of four pieces.",
            "The promotion tests pass for queen, rook, bishop, and knight.",
        ),
        (
            "Explain why a player sometimes promotes to a knight.",
            (
                "Running `demo_promotion.py` prints stalemate for b8=Q, b8=R, and b8=B "
                "and checkmate for b8=N, and the student pair says why the queen only draws."
            ),
        ),
        (
            "Play Remus in Lucas Chess.",
            (
                "The student pair registers `remus.bat`, plays one game, and sees a random legal "
                "reply to every move, special moves included."
            ),
        ),
    ],
    (6, 1): [
        (
            "Write a recursive function with a base case.",
            "The lab's countdown and leaf count give the worksheet's numbers.",
        ),
        (
            "Trace a call stack by hand.",
            "The student pair draws the calls of a depth-2 count and the value each one returns.",
        ),
    ],
    (6, 2): [
        (
            "Count the positions of the move tree with `perft()`.",
            "Running `perft.py` prints 20, 400, and 8,902 for depths 1 to 3.",
        ),
        (
            "Explain why perft proves the rules right.",
            "Exit ticket: one sentence on what a wrong count tells you.",
        ),
    ],
    (6, 3): [
        (
            "Compare Remus with python-chess on standard positions.",
            "`test_perft.py` passes on all five positions.",
        ),
        (
            "Find a planted bug with `divide()`.",
            (
                "Running `hunt.py` in `bug_hunt/` points at three bugs; the student pair fixes at "
                "least two of them and names the root move that showed each one."
            ),
        ),
    ],
    (6, 4): [
        (
            "Read and write the piece placement of FEN.",
            (
                "`test_game.py` FEN tests pass: the start FEN goes in and comes back "
                "out the same."
            ),
        ),
        (
            "Name the six fields of a FEN string.",
            (
                "`python_fen_fields.py` prints the six fields of the start FEN with "
                "their names, and the student pair labels them on the worksheet."
            ),
        ),
    ],
    (7, 1): [
        (
            (
                "Name every way a game ends: checkmate, stalemate, insufficient "
                "material, repetition, and the fifty-move rule."
            ),
            "Six-position quiz: each student pair gets at least five right.",
        ),
        (
            "Detect the end of a game in code.",
            "The game-end tests in `test_game.py` pass for all five endings.",
        ),
    ],
    (7, 2): [
        (
            "Read a move typed in SAN, such as Nf3 or O-O.",
            "The `parse_san` tests pass, and a typo raises `ValueError`.",
        ),
        (
            "Write every legal move of a position in SAN.",
            (
                "Running `notation.py` lists every legal move in SAN, and "
                "`parse_san()` reads `O-O-O` back as the queenside castling move."
            ),
        ),
        (
            "Read commands from `sys.stdin` and answer on stdout.",
            (
                "`python_input_output.py` answers `isready` with `readyok` and stops "
                "at `quit`."
            ),
        ),
    ],
    (7, 3): [
        (
            "Choose a random move and a greedy move.",
            "The brain tests pass: greedy Remus takes a hanging queen.",
        ),
        (
            "Explain what the UCI commands do.",
            (
                "The student pair explains `position`, `go`, and `bestmove` from a printed "
                "conversation."
            ),
        ),
        (
            "Measure one brain against another.",
            "Running `play_match.py` shows greedy Remus scoring more than random Remus.",
        ),
    ],
    (7, 4): [
        (
            "Count material in centipawns.",
            (
                "The evaluation tests pass, and running `evaluation.py` prints -200 for "
                "a knight against a rook."
            ),
        ),
        (
            "Explain a piece-square table.",
            (
                "The student pair says why a knight scores more on d4 than on a1, using the "
                "number of squares it attacks (8 and 2)."
            ),
        ),
    ],
    (8, 1): [
        (
            "Back up scores through a tree with minimax.",
            "Paper minimax: the student pair's best move matches `minimax()` on the same tree.",
        ),
        (
            "Score checkmate so that a faster mate wins.",
            (
                "The negamax tests pass: `negamax()` finds every mate in 1, and the root "
                "state is unchanged after each search."
            ),
        ),
    ],
    (8, 2): [
        (
            "Explain an alpha-beta cutoff.",
            (
                '"Fewest flips": the student pair reaches the right move while turning fewer '
                "cards than the whole tree."
            ),
        ),
        (
            "Show that alpha-beta keeps the answer and saves work.",
            (
                "The `alpha_beta` tests pass, and running `compare_search.py` prints the "
                "same scores as negamax with fewer nodes."
            ),
        ),
        (
            (
                "Keep a list in order with `insert()`, start a best value at minus "
                "infinity, and time code."
            ),
            (
                "`python_sorting.py` puts the queen first, finds the best victim, and "
                "prints the run time of `perft(3)`."
            ),
        ),
    ],
    (8, 3): [
        (
            "Explain the horizon effect.",
            "The student pair explains why depth 2 takes a defended pawn with the queen.",
        ),
        (
            "List the moves quiescence searches.",
            (
                'The `quiescence` tests pass, and the student pair explains what "stand pat" '
                "means with the defended-pawn position."
            ),
        ),
    ],
    (8, 4): [
        (
            "Order moves so the best ones come first.",
            (
                "The `mvv_lva_score` test passes: pawn takes queen scores above queen "
                "takes rook."
            ),
        ),
        (
            "Measure what ordering saves.",
            "The student pair records node counts before and after ordering for one position.",
        ),
    ],
    (9, 1): [
        (
            "Search deeper one step at a time until the clock runs out.",
            (
                "`test_think_respects_its_time` passes, and Remus never loses on time "
                "in Lucas Chess."
            ),
        ),
        (
            "Report the search to the GUI with `info` lines.",
            (
                "Lucas Chess shows Remus's depth, score, and best line for each depth "
                "that `think()` finishes."
            ),
        ),
    ],
    (9, 2): [
        (
            "Use a dict as a cache with tuples as keys.",
            "The lab remembers perft counts already computed and prints the time saved.",
        ),
        (
            "Add one enhancement to Remus-WHITE.",
            "The enhanced engine's own tests pass in its folder.",
        ),
    ],
    (9, 3): [
        (
            "Test an enhancement before trusting it.",
            (
                "The enhanced engine passes `run_tests.py` and a one-game basic test against "
                "Remus-WHITE with no illegal moves."
            ),
        ),
        (
            "Predict what the enhancement changes.",
            (
                "Each student pair writes one sentence on the board: what should change, and how "
                "the class will see it in the match results."
            ),
        ),
    ],
    (9, 4): [
        (
            "Run a fair match between two enhanced engines.",
            (
                "The student pair copies its engine folder to another student pair's laptop, plays two "
                "games against that student pair's engine, one with each piece color, and "
                "writes the "
                "result on the board."
            ),
        ),
        (
            "Read a match result with its margin of error.",
            (
                "`demo_results.py` turns the student pair's two battle games, and then its "
                "engine's league games, into an Elo gap and margin, and the student pair says "
                "which gap is larger than its margin and why two games cannot show "
                "which enhancement is stronger."
            ),
        ),
    ],
    (10, 1): [
        (
            "Map the chess engine's loop onto a measurement problem.",
            (
                "The student pair fills in the chess-to-science table: legal moves, evaluation, "
                "and greedy move each have a science partner."
            ),
        ),
        (
            "Balance exploring and exploiting.",
            (
                "The student pair's `choose_next_measurement()` beats random guessing on the "
                "100-grid benchmark, and the student pair names the explore weight it chose."
            ),
        ),
    ],
    (10, 2): [
        (
            "Score a guess about what a powder holds.",
            (
                "The `score` test passes, and the student pair explains why an extra phase "
                "costs a point even when every peak is explained."
            ),
        ),
        (
            "Build an answer greedily, one best step at a time.",
            (
                "The `greedy_phases` tests pass, and the student pair explains why greedy "
                "names gold for a powder that holds silver."
            ),
        ),
    ],
    (10, 3): [
        (
            "Search every set of phases with make and undo, as Remus searches moves.",
            (
                "The `search` tests pass: the phases list comes back unchanged, and "
                "the search scores 176 sets, one for each set of up to three phases."
            ),
        ),
        (
            (
                "Verify a method against known answers, and say when the data "
                "cannot decide."
            ),
            (
                "Running `phase_hunt.py` shows the search making fewer wrong calls "
                "than greedy, and the student pair names the extra measurement that would "
                "tell gold from silver."
            ),
        ),
    ],
    (10, 4): [
        (
            "Report a science result the way a scientist does.",
            (
                "The student pair's results table gives the hidden-peak benchmark against "
                "random guessing and the phase hunt's right, wrong, and can't-tell "
                "counts for greedy and for search, from the student pair's own runs."
            ),
        ),
        (
            "Explain one decision the science AI made.",
            (
                "Each student pair presents one powder its search named and one it answered "
                "with can't tell, and says which measurement would settle the second."
            ),
        ),
        (
            "Take the code home.",
            (
                "Each student's USB drive holds the student pair's Remus folder, every Day "
                "folder included, and the copy opens in VS Code."
            ),
        ),
    ],
}

# Objectives for the version READMEs, the same for every color
VERSION_OBJECTIVES = [
    (
        "Explain the idea of this enhancement in two sentences.",
        "The student pair explains the idea to another student pair, who can restate it.",
    ),
    (
        "Add the enhancement without breaking the rules.",
        "`run_tests.py` passes in the version folder.",
    ),
    (
        "Run a fair experiment: same opening, both piece colors.",
        (
            "In the Day 9 battles, `play_battle.py` in the version folder plays both "
            "10-minute games with no illegal moves or crashes when the student pair presses "
            "Run in VS Code, and the student pair says why two games cannot show which "
            "enhancement is stronger."
        ),
    ),
]

# Where the board diagrams live, seen from a version README in
# engines/instructor/<engine folder>/ or engines/student/<engine folder>/.
# make_board_diagrams.py draws them.
BOARD_IMAGES = "../../../misc/students/images/boards"
# The same folder seen from a period goals file in Day NN - .../periodK/
GOALS_BOARD_IMAGES = "../../misc/students/images/boards"


def board_image(name: str, words: str, folder: str = BOARD_IMAGES) -> str:
    """Return the Markdown that shows one board diagram, with words for a screen reader."""
    return f"![{words}]({folder}/{name}.svg)"


def goals_board_image(name: str, words: str) -> str:
    """Return the Markdown that shows one board diagram in a period goals file."""
    return board_image(name, words, GOALS_BOARD_IMAGES)


# The long explanation in each version README, by color. Each section is Markdown:
# "example" walks through one concrete case, "why" says how the idea makes Remus
# stronger, "cost" says what it spends (positions per second, memory, re-searches),
# "expect" says what the student pair should see in the numbers and in games, and "fits"
# traces where the student pair's code is called from.
VERSION_GUIDES = {
    "WHITE": {
        "why_title": "Why it matters",
        "example": (
            "Remus-WHITE thinks the way the class built it through Day 9. `think()` "
            "searches 1 ply deep, then 2, then 3, until its time for the move runs out, "
            "and plays the best move of the deepest search that finished. Each search "
            "is alpha-beta: once one reply shows a move is worse than a move already "
            "found, Remus stops looking at that move. At the end of every line, "
            "quiescence keeps playing captures until the position is quiet, so Remus "
            "never stops counting in the middle of a trade. Captures are tried first, "
            "most valuable victim and least valuable attacker first (MVV-LVA), and the "
            "best move of the last depth is tried before everything else."
        ),
        "why": (
            "Every enhanced engine is Remus-WHITE plus exactly one change. Playing each "
            "enhanced engine against Remus-WHITE is a fair experiment: same openings, both "
            "piece colors, and only one thing different."
        ),
        "cost": (
            "Remus-WHITE is pure Python, so it searches only a few thousand positions "
            "a second. Most of them are quiescence positions at the ends of lines. "
            "With 10 minutes for a game, Remus thinks about 20 seconds a move and "
            "usually finishes depth 4 or 5 in the middlegame."
        ),
        "expect": (
            "Remus-WHITE is pinned at 0 in every league table, so every other "
            "version's rating is its gain or loss against Remus-WHITE."
        ),
    },
    "GOLD": {
        "why_title": "Why it is stronger",
        "example": (
            "Remus-GOLD is the finished Day 10 Remus: Remus-WHITE plus all ten "
            "enhancements working together in one search, `upgraded_search()`. It "
            "probes the transposition table (RED), tries a null move (ORANGE), orders "
            "the moves with the stored best move and killers first (RED, BLUE), "
            "searches later moves with a null window (PINK) and late quiet moves one "
            "ply shallower (BROWN), scores repeated positions as draws (YELLOW), plays "
            "from the opening book (GREEN), and adds pawn structure, the mating bonus, "
            "and king safety to its evaluation (PURPLE, CYAN, GRAY)."
        ),
        "why": (
            "The search tricks multiply. The table and the killers put the best move "
            "first, a good first move makes PVS's null windows cheap, and null moves "
            "and late move reductions remove whole subtrees. Together they reach a "
            "ply or two deeper in the same time than Remus-WHITE, and the better "
            "evaluation chooses better among the moves it sees."
        ),
        "cost": (
            "Its evaluation does three more scans of the board for every position, so "
            "Remus-GOLD evaluates fewer positions a second than Remus-WHITE. It wins "
            "that time back by visiting far fewer positions for each depth."
        ),
        "expect": (
            "In the designer's league, where every version searched about as deep "
            "as Remus does in a game of several hours, Remus-GOLD scored 85 "
            "percent and rated +339 plus or minus 91 over Remus-WHITE, far ahead "
            "of every engine with one enhancement. It gains more the longer the clock, "
            "because null moves and late move reductions save work only at depth 3 "
            "and deeper."
        ),
    },
    "RED": {
        "example": (
            "1. Nf3 Nf6 2. d4 and 1. d4 Nf6 2. Nf3 reach the same position by two "
            "different move orders. Chess players call that a transposition.\n\n"
            + board_image(
                "red_transposition",
                "The position after 1. Nf3 Nf6 2. d4, Black to move",
            )
            + "\n\n"
            "*The green arrows are White's two moves, Nf3 and d4, and the blue arrow is "
            "Black's Nf6. Play them in either order and the board ends up the same.*"
            "\n\n"
            "A "
            "search meets transpositions all the time: Remus playing Nf3 then d4 "
            "against ...Nf6 and ...e6 reaches one position four ways. Remus-WHITE "
            "searches that position four times. Remus-RED searches it once, writes "
            "the result in a dict (the transposition table), and looks it up the "
            "other three times.\n\n"
            "Each entry, keyed by `position_key`, holds the depth searched, the "
            "score, the move that was best, and a bound that says how much the score "
            "can be trusted. Alpha-beta often stops early, so a score is not always "
            "exact:\n\n"
            "- `EXACT`: the search found the true score.\n"
            "- `LOWER`: a move caused a cutoff, so the true score is at least this "
            "much.\n"
            "- `UPPER`: no move beat alpha, so the true score is at most this much.\n\n"
            "`probe()` answers from the table only when the stored search went at "
            "least as deep as the one needed and the bound settles the question. A "
            'lower bound of +120 settles a search that only asks "is it at least '
            '+100?" (beta = 100), but not one that asks for the exact score.'
        ),
        "why": (
            "A lookup replaces a whole subtree. Even when the stored score cannot "
            "be used, because it is too shallow or its bound does not settle the "
            "question, the stored best move is tried first. Iterative deepening "
            "makes this pay twice: the depth 3 search fills the table with best "
            "moves that put the depth 4 search's best move first almost everywhere, "
            "and alpha-beta prunes most when the best move comes first."
        ),
        "cost": (
            "One dict lookup and one dict write per position. The key is already in "
            "the game history, so it costs nothing to build. The table starts empty "
            "for every move and holds one entry per position searched, a few hundred "
            "thousand at most, which a laptop's memory holds easily. Mate scores are "
            "not stored, because a mate score counts plies from the root, so the "
            "same position gets a different mate score at a different ply."
        ),
        "expect": (
            "Remus-RED is the only engine with one enhancement that rated clearly above "
            "Remus-WHITE in the designer's league: +101 plus or minus 67. "
            "Fewer positions for the same depth, and the biggest savings in endgames, "
            "where a few pieces shuffle between the same squares and nearly every "
            "position is reached many ways. Positions per second stay close to "
            "Remus-WHITE's."
        ),
        "fits": (
            "`table_search()` in `search.py` replaces Remus-WHITE's search. At the "
            "top of every position it calls `probe()`, and if the answer is a score, "
            "it returns at once. After a cutoff it calls `store()` with `LOWER`; "
            "after searching every move it calls `store()` with `EXACT` if a move "
            "beat alpha and `UPPER` if none did. `store()` keeps the deeper of two "
            "results for the same position."
        ),
    },
    "GREEN": {
        "example": (
            "`opening_book.txt` holds 43 well-known openings, five moves for each "
            "side, written in SAN: `e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7` is the Ruy "
            "Lopez. `load_book()` plays every line on a board from the starting "
            "position and records, for each position it passes, which moves the "
            "book plays there. After 1. e4 the book holds seven replies: ...e5, "
            "...c5, ...e6, ...c6, ...d5, ...d6, and ...Nf6.\n\n"
            + board_image(
                "green_book_replies",
                "The position after 1. e4, with the book's seven replies marked",
            )
            + "\n\n"
            "*After 1. e4 (the green arrow), the yellow squares show where Black's "
            "seven book replies go: e5, c5, e6, c6, d5, d6, and the knight to f6.*\n\n"
            "`book_move()` picks one of them at random, so Remus-GREEN does "
            "not play the same opening every game. Once the game leaves the book, "
            "Remus searches as usual."
        ),
        "why": (
            "Searching the opening is slow and not very good: at depth 4 Remus "
            "cannot see why 1. e4 e5 2. Nf3 Nc6 3. Bb5 works. A book move costs no "
            "thinking time and comes from a century of human play. Every book move "
            "also passes through `parse_san()` and Remus's own legal move generator, "
            "so a typo in the book file is reported and skipped, never played."
        ),
        "cost": (
            "Nothing during the search: the book is read once when the engine "
            "starts, and asking it is one dict lookup. Positions per second and "
            "positions per depth are the same as Remus-WHITE's, because the search "
            "itself does not change."
        ),
        "expect": (
            "The time saved goes to later moves. Remus thinks about one thirtieth of "
            "its remaining clock per move, so five instant book moves leave roughly "
            "a minute and a half more for the middlegame. Every version match game "
            "starts from one of 32 openings three moves deep, and 24 of those "
            "positions are in the book, so Remus-GREEN usually gets two more instant "
            "moves before it searches. The book saves the most time in games that "
            "start from the first move. In the designer's league, Remus-GREEN rated "
            "+7 over Remus-WHITE when its games started three moves deep, and +58 "
            "when they started from the first move. The benchmark below never asks "
            "the book, so its numbers match Remus-WHITE's exactly."
        ),
        "fits": (
            "`uci_engine.py` asks `book_move()` before it searches. `None` means "
            "the position is not in the book, and the engine calls `think()` as "
            "Remus-WHITE does."
        ),
    },
    "BLUE": {
        "example": (
            "Black has just made a weak move, and White's quiet move Qh5 threatens "
            "mate on f7.\n\n"
            + board_image(
                "blue_killer_qh5",
                "After 1. e4 e5 2. Bc4 Nc6 3. Qh5, White threatens Qxf7 mate",
            )
            + "\n\n"
            "*After 1. e4 e5 2. Bc4 Nc6 3. Qh5, the queen and the bishop both aim at "
            "f7 (the red arrows). Only Black's king guards f7, so Qxf7 would be mate.*"
            "\n\n"
            "Deep in the search, the same Qh5 refutes many different "
            "Black moves at the same ply: almost any Black move that does not defend "
            "f7 loses to it. Remus-WHITE tries the captures first, then the quiet "
            "moves in the order the generator found them, so it may try 20 quiet "
            "moves before Qh5 each time. Remus-BLUE remembers Qh5 as a killer move "
            "for that ply, because it caused a cutoff there, and tries it right "
            "after the captures in every other position at the same ply."
        ),
        "why": (
            "Alpha-beta cuts off a position as soon as one move is good enough to "
            "refute it. The sooner that move comes, the fewer moves are searched. "
            "Captures are easy to rank by value, but quiet moves have no such order. "
            "Killers give the quiet moves an order learned from the search itself."
        ),
        "cost": (
            "Very little: two moves stored per ply, and a check whether each quiet "
            "move is one of them while ordering. Positions per second stay close to "
            "Remus-WHITE's."
        ),
        "expect": (
            "Fewer positions for the same depth, most of all in quiet middlegame "
            "positions with many moves. A killer that is a capture or a promotion is "
            "not stored, because captures and promotions are already ordered first."
        ),
        "fits": (
            "`killer_search()` in `search.py` calls `remember_killer()` whenever a "
            "quiet move causes a cutoff, and passes the killers of the next ply to "
            "`order_moves()` in `move_ordering.py`. `order_moves()` scores captures "
            "by MVV-LVA, gives a killer `KILLER_SCORE` (50, below every capture and "
            "above every other quiet move), and puts the best move of the last "
            "depth in front of them all."
        ),
    },
    "PINK": {
        "example": (
            "After Remus has searched its first move and found it scores +30, the "
            'only question about each other move is "is it better than +30?" '
            "Remus-WHITE searches every move with the full window, alpha to beta, "
            "to find its exact score. Remus-PINK searches the later moves with a "
            "null window from +30 to +31. A null window has no room between alpha "
            "and beta, so every reply either fails low (worse than +30) or fails "
            "high (better), and cutoffs come at once. Only a move that fails high "
            "gets a second search with the full window to find how much better it "
            "is."
        ),
        "why": (
            "With good move ordering the first move is usually the best one, so "
            "most later moves fail low on the cheap null-window search and never "
            "need a full one. This is principal variation search, PVS: the first "
            "move is searched as the principal variation, and the rest only have to "
            "prove that they are worse."
        ),
        "cost": (
            "A move that turns out better than the first one is searched twice. PVS "
            "saves work only when the move ordering is good; with poor ordering the "
            "re-searches can cost more than the null windows save."
        ),
        "expect": (
            "Fewer positions for the same depth, and the same move in "
            "almost every position, because PVS changes how much Remus searches, "
            "not what it finds. PVS gains much more in Remus-GOLD, where the table "
            "and the killers make the first move the best one far more often."
        ),
        "fits": (
            "`pvs_search()` in `search.py` searches the first move with the full "
            "window and calls `search_later_move()` for every other move. The move "
            "is already made when `search_later_move()` runs, and the score comes "
            "back from the opponent's point of view, so the code flips its sign "
            "and the window, as negamax does."
        ),
    },
    "YELLOW": {
        "example": (
            "Remus-WHITE is a rook behind, and the opponent's king can be checked "
            "forever.\n\n"
            + board_image(
                "yellow_perpetual",
                "White is a rook behind and checks forever with Qg5 and Qf6",
            )
            + "\n\n"
            "*White, to move, is a rook behind. Qg5+ (the red arrow) drives the king to "
            "h8, Qf6+ drives it back to g8, and Qg5+ starts again. The red squares are "
            "the queen's two checking squares and the blue squares are the king's only "
            "two squares.*\n\n"
            "Inside its search,Remus-WHITE scores the position after the "
            "third repetition as a rook behind, because nothing in its search knows "
            "that the game ends there as a draw. So it avoids the checks and loses "
            "slowly. Remus-YELLOW scores any position that already appeared in the "
            "game or in the search line as 0, a draw, and so does a position after "
            "100 half moves with no capture or pawn move (the fifty-move rule). It "
            "sees that the checks save half a point and plays them."
        ),
        "why": (
            "The same knowledge works the other way. A side that is ahead stops "
            "repeating positions, because a repetition scores 0 instead of its +300 "
            "lead. A repetition can only be claimed after the third time, but the "
            "search treats the second time as a draw: if repeating once is the best "
            "either side can do, it can repeat again."
        ),
        "cost": (
            "`is_draw_in_search()` counts the position key in the game history at "
            "every position, a short list scan. Positions per second stay close to "
            "Remus-WHITE's, and the search saves work when it meets a repetition, "
            "because a draw ends that line at once."
        ),
        "expect": (
            "More draws in lost positions and fewer accidental draws in won ones. "
            "The benchmark positions below start with no game history, so they hold "
            "almost no repetitions and the numbers match Remus-WHITE's; the "
            "difference shows up in games."
        ),
        "fits": (
            "`draw_sense_search()` in `search.py` calls `is_draw_in_search()` at the "
            "top of every position below the root, before any move is generated. "
            "The root is skipped, because Remus must still choose a move there."
        ),
    },
    "PURPLE": {
        "example": (
            "White pawns on c2, c3, and e4, Black pawns on d6 and e5: White's c-pawns "
            "are doubled (two on one file), and the e4 pawn is isolated (no White "
            "pawn on the d- or f-file beside it).\n\n"
            + board_image(
                "purple_pawns",
                "White pawns on c2, c3, and e4 against Black pawns on d6 and e5",
            )
            + "\n\n"
            "*The yellow squares are White's doubled pawns on the c-file. The red square "
            "is the isolated pawn on e4: no White pawn stands anywhere on the d-file or "
            "the f-file to protect it.*\n\n"
            "Remus-PURPLE scores each doubled "
            "pawn -8 and each isolated pawn -20. A passed pawn, with no enemy pawn in "
            "front of it on its own file or a neighboring file, earns a bonus that "
            "grows as it advances: 0, 10, 20, 40, 60, and then 70 one step from "
            "promotion. Remus-WHITE counts every pawn as 100 plus its square's "
            "placement value and sees none of this."
        ),
        "why": (
            "Pawns cannot move backward, so a weak pawn stays weak for the whole "
            "game, and a passed pawn becomes a queen threat that ties down enemy "
            "pieces. A search at depth 4 cannot see those long-term effects, but an "
            "evaluation term can score them in every position."
        ),
        "cost": (
            "`pawn_structure()` scans the board for pawns, then looks ahead of each "
            "pawn for enemy pawns, in every evaluated position. Evaluation is most "
            "of Remus's work at the ends of lines, so Remus-PURPLE evaluates fewer "
            "positions a second than Remus-WHITE. The number of positions per depth "
            "changes a little either way, because different scores lead alpha-beta "
            "to different cutoffs."
        ),
        "expect": (
            "Better pawn moves: Remus-PURPLE avoids doubling its own pawns, attacks "
            "isolated enemy pawns, and pushes passed pawns in the endgame. The cost "
            "in speed can cancel the gain at a short clock."
        ),
        "fits": (
            "`white_score()` in `evaluation.py` adds `pawn_structure(board)` to "
            "material and placement, and `explain_evaluation()` prints it as its own "
            "line, so a student pair can see the term in any position."
        ),
    },
    "CYAN": {
        "example": (
            "White has king and rook, Black has only a king. Mate needs the Black "
            "king on the edge, and it takes far more than 4 plies of good moves to "
            "drive it there. Remus-WHITE sees no mate within its depth and scores "
            "every rook move the same, +500, so it shuffles. Remus-CYAN adds a bonus "
            "once one side leads by at least 200 and the losing side has at most 600 "
            "left: 10 points for each step the losing king stands from the center, "
            "and 4 points for each step the winning king has closed in.\n\n"
            + board_image("cyan_king_center", "The Black king on e5, in the center")
            + " "
            + board_image(
                "cyan_king_edge", "The Black king on e8, with the White king on e6"
            )
            + "\n\n"
            "*The yellow squares are the center. Left: the Black king stands on e5, 0 "
            "steps from the center, and the White king on c2 is 3 steps away, so the "
            "bonus is 4 x (7 - 3) = 16. Right: the Black king on e8 is 3 steps from "
            "the center and the White king on e6 is 2 steps away, so the bonus is "
            "10 x 3 + 4 x (7 - 2) = 50.*\n\n"
            "Now every "
            "move that squeezes the king toward the edge scores higher, and the "
            "search walks it into a mating net."
        ),
        "why": (
            "An evaluation term can stand in for a search that is too deep to run. "
            'The bonus turns a long plan, "push the king to the edge, then mate", '
            "into small steps that a shallow search can see."
        ),
        "cost": (
            "One scan of the board to count material and find the kings, in every "
            "evaluated position. In most positions the margins are not met and the "
            "bonus is 0, so the cost is the scan only."
        ),
        "expect": (
            "Faster wins in won endgames, and no change before that. Many games are "
            "decided or drawn before such an endgame appears, so the league rating "
            "moves little."
        ),
        "fits": (
            "`white_score()` in `evaluation.py` adds `mating_bonus(board)` to "
            "material and placement. `CENTER_DISTANCE` gives each row and column's "
            "distance from the center: 3 on the edge, 0 in the middle."
        ),
    },
    "ORANGE": {
        "example": (
            "Somewhere in the search, Remus is a knight ahead in a line it is "
            "checking. Earlier in the tree, the opponent already found a different "
            "move that keeps the game even. That earlier choice is beta: any line "
            "better for Remus than beta, the opponent will simply avoid. Before "
            "searching its 35 real moves here, Remus-ORANGE tries a cheap test. It "
            "passes, so the opponent gets two moves in a row, and searches 2 plies "
            "shallower than usual. If Remus still scores at least beta after "
            "giving away a whole move, then a real move would do even better, because "
            "moving is almost always better than passing. The opponent will never "
            "allow this position, so Remus stops searching it without trying one "
            "real move."
        ),
        "why": (
            "Most positions deep in a search are lopsided, and the null move "
            "removes them with one shallow search instead of a full one. The "
            "positions saved go into searching the close lines one ply deeper."
        ),
        "cost": (
            "An extra shallow search at every position 3 or more plies from the "
            "leaves, which is wasted when the test fails. The test can also be "
            "wrong. In zugzwang, every legal move makes the position worse, and "
            "passing would be the best move if it were allowed; this happens "
            "mostly in pawn endings. So Remus never passes when it is in check, "
            "when it has only king and pawns, right after a pass, or at the root."
        ),
        "expect": (
            "Far fewer positions for the same depth once the search reaches depth "
            "3 and deeper, and the same moves in most positions. The saving grows "
            "with depth, so null moves help most at longer clocks."
        ),
        "fits": (
            "`null_move_search()` in `search.py` calls `make_null_move()`, searches "
            "the pass with the window (-beta, -beta + 1) at `depth - 1 - "
            "NULL_MOVE_REDUCTION`, and calls `undo_null_move()` in a `finally` "
            "block. A pass changes the side to move, clears the en passant target, "
            "and adds a history entry, and `undo_null_move()` must restore all "
            "three exactly, like every undo in Remus."
        ),
    },
    "BROWN": {
        "example": (
            "Remus orders its moves: the best move from the last depth first, then "
            "captures, then quiet moves. In a position with 35 moves, the best one "
            "is almost always among the first three. Remus-BROWN searches the first "
            "three moves at full depth and every later quiet move one ply "
            "shallower. A late move that still beats alpha at the shallower depth is "
            "a surprise, and Remus searches it again at full depth before trusting "
            "it."
        ),
        "why": (
            "Most of a search's work goes into proving that bad moves are bad. Late "
            "move reductions prove it more cheaply, and the re-search keeps the "
            "rare good late move from being missed. Captures, promotions, and "
            "checks are never reduced, because they change the position too much "
            "to judge from a shallow search."
        ),
        "cost": (
            "Each surprise costs a second search. The reduction only starts with 3 "
            "or more plies to go, so it does nothing in a depth 2 search."
        ),
        "expect": (
            "Fewer positions for the same depth, growing with depth, and now and "
            "then a different move, because a reduced search can miss a quiet move "
            "that only works deep down."
        ),
        "fits": (
            "`reduced_search()` in `search.py` makes each move, asks `reduction()` "
            "how many plies to cut (1 or 0), and searches at `depth - 1 - cut`. If "
            "a cut search scores above alpha, it searches the move again at full "
            "depth. `LATE_MOVE_INDEX` (3) says where the late moves begin."
        ),
    },
    "GRAY": {
        "example": (
            "White has castled kingside: king on g1, pawns on f2, g2, and h2. Each of "
            "the king's three files has a White pawn one or two squares in front, so "
            "Remus-GRAY adds 3 x 15 = 45 points. Push the h-pawn to h4, and the h-file "
            "no longer shelters the king: 30 points.\n\n"
            + board_image(
                "gray_shield_full", "White king on g1 behind pawns on f2, g2, and h2"
            )
            + " "
            + board_image(
                "gray_shield_broken", "The same position after the h-pawn moves to h4"
            )
            + "\n\n"
            "*Left: the three green pawns on f2, g2, and h2 shield the king on g1, "
            "45 points. Right: after h2 to h4, no White pawn stands on h2 or h3 (the "
            "red squares), so only f2 and g2 count, 30 points. Black's queen is still "
            "on d8, so the bonus counts in both.*\n\n"
            "The bonus counts only while "
            "the enemy queen is on the board, because the queen is the piece that "
            "makes an open king dangerous. Once the queens come off, the king should "
            "walk toward the center, and the term is 0."
        ),
        "why": (
            "A king attack takes many moves to build, too many for a depth 4 search "
            "to see. The shield bonus teaches Remus to castle and to keep the pawns "
            "in front of its king, before an attack is in range of the search."
        ),
        "cost": (
            "A scan of the board for the enemy queen and the king, and up to six "
            "squares checked in front of the king, in every evaluated position. "
            "Remus-GRAY evaluates a few positions a second fewer than Remus-WHITE."
        ),
        "expect": (
            "Earlier castling, fewer pawn pushes in front of its own king, and a "
            "reason to trade queens when its own shield is broken."
        ),
        "fits": (
            "`white_score()` in `evaluation.py` adds `king_safety(board)` to "
            "material and placement. White's pawns stand in front of its king at "
            "smaller rows, because row 0 is rank 8, so the code steps the other way "
            "for Black."
        ),
    },
}

# Each version's search on the ten positions of remus_benchmark.py, measured with
# think() on one computer: positions to finish depth 4, the seconds that took, and
# the average deepest depth finished in 5 seconds a position
VERSION_MEASURES = {
    "WHITE": {"nodes": 431_212, "seconds": 83.2, "depth": 3.1},
    "GOLD": {"nodes": 84_812, "seconds": 18.8, "depth": 4.9},
    "RED": {"nodes": 243_223, "seconds": 48.7, "depth": 3.7},
    "GREEN": {"nodes": 431_212, "seconds": 85.4, "depth": 3.2},
    "BLUE": {"nodes": 328_889, "seconds": 65.8, "depth": 3.4},
    "PINK": {"nodes": 289_419, "seconds": 50.2, "depth": 3.3},
    "YELLOW": {"nodes": 431_138, "seconds": 85.4, "depth": 3.1},
    "PURPLE": {"nodes": 452_398, "seconds": 99.5, "depth": 3.1},
    "CYAN": {"nodes": 425_602, "seconds": 87.5, "depth": 3.1},
    "ORANGE": {"nodes": 273_470, "seconds": 47.9, "depth": 3.5},
    "BROWN": {"nodes": 162_998, "seconds": 31.5, "depth": 3.7},
    "GRAY": {"nodes": 459_732, "seconds": 93.3, "depth": 3.1},
}

# Picture folder, as a path from a period goals file at the top of Day NN/periodK
PHASE_HUNT_IMAGES = "../../misc/students/images/phase_hunt"

# A longer illustrated guide for a period that needs more than the objectives and
# change notes, written into the README right after the objectives.
# make_phase_hunt_figures.py draws the pictures.
PERIOD_GUIDES = {
    (10, 2): f"""## The experiment: what is in this powder?

Scientists at Brookhaven National Laboratory mix chemicals, heat them, and get a
gray powder. Did they make the new material they wanted, or something else? The
powder looks the same either way. To find out, they take it to a beamline at the
National Synchrotron Light Source II (NSLS-II), one of the brightest X-ray sources
in the world, and shine its X-ray beam through the powder.

![The experiment: X-rays go through a powder and make rings on a detector, and the
rings turn into a pattern of peaks]({PHASE_HUNT_IMAGES}/experiment.png)

A powder is millions of tiny crystals. In a crystal, the atoms sit in rows, as
neatly as the squares of a chessboard. The rows bounce the X-rays off at a few
special angles, so the detector shows bright rings. Each ring becomes a **peak**
in the pattern on the right. The angle of a peak is called **2θ** ("two theta"),
measured in degrees.

## Every crystal has a fingerprint

Each kind of crystal, called a **phase**, has its own spacing between its rows of
atoms. So each phase makes peaks at its own angles: a fingerprint. Bragg's law, a
rule from 1913, turns the spacing into the angles. `phase_hunt.py` holds the
fingerprints of ten real phases, with their four strongest peaks each, in the
dictionary `LIBRARY`.

![The fingerprints of the ten phases in the library, each a row of four colored
peaks, with where you meet each one]({PHASE_HUNT_IMAGES}/fingerprints.png)

Look closely: gold and silver have almost the same fingerprint. That will matter
later.

## The mystery powder

A powder can hold two or three phases at once. Then the pattern shows **all** their
peaks together, and the job is to work out which fingerprints were mixed. Here is
powder 23 from the benchmark. `make_pattern(23)` makes it.

![A pattern with eight peaks. Which crystals made them?]({PHASE_HUNT_IMAGES}/mystery_powder.png)

Real patterns are messy, and `make_pattern()` makes them messy on purpose. A real
peak lands a little away from its library angle (up to 0.15 degrees here), and a
weak peak can hide in the noise (each peak shows up 85 times out of 100). So two
peaks count as the same peak when they are within `TOLERANCE`, 0.3 degrees.

## What Remus is searching

In chess, Remus tries moves, looks at each position, and keeps the best. In the
phase hunt, the program tries **guesses**. A guess is a set of phases, such as
silicon + halite. Adding a phase to the guess is like making a move, and taking it
back out is like undoing it. The program scores every guess and keeps the best one.

| Chess engine | Phase hunt |
| --- | --- |
| A position | A guess: the set of phases chosen so far |
| Legal moves | The phases in the library that are not in the guess yet |
| `make_move()` and `undo_move()` | `phases.append(name)` and `phases.pop()` |
| `material()`, the evaluation | `score()`: how well the guess explains the peaks |
| `greedy_move()` | `greedy_phases()`: add the phase that helps most, again and again |

## Your first function: `score()`

`score(phases, measured)` grades a guess, the way a teacher grades a test. It looks
at every peak twice:

1. For each **measured** peak (a dot in the picture): +1 if a phase in the guess
   explains it (green ✓), -1 if no phase does (orange ?).
2. For each **predicted** peak (a stick): -1 if the pattern does not show it
   (red ✗). A real phase would have made that peak.
3. Then -1 for each phase in the guess, so that a simpler explanation wins a tie.

![Three guesses for powder 23, each peak marked explained, left over, or missing,
with the points for each]({PHASE_HUNT_IMAGES}/scoring.png)

Silicon alone explains 4 peaks and leaves 4 over: 4 - 4 - 0 - 1 = -1 point.
Silicon + halite explains all 8: 8 - 0 - 0 - 2 = 6 points. Adding zincite explains
nothing new, and two of its peaks are missing: 8 - 0 - 2 - 3 = 3 points. The best
guess is the one with the most points.

The helpers `predicted_peaks(phases)` (every peak of every phase in the guess, in one
list) and `matches(peak, peaks)` (is some peak within `TOLERANCE`?) are finished, so
`score()` needs only two loops and a few `+=` and `-=` lines.

## Your second function: `greedy_phases()`

`greedy_phases(measured)` builds a guess one phase at a time. At each step it tries
adding every phase that is not in the guess yet (`append`), scores the guess, takes
the phase back out (`pop`), and remembers the phase with the best score. If that
phase raises the score, it stays. If no phase helps, the guess is finished.

![Greedy on powder 23: step 1 picks silicon, step 2 picks halite, step 3 finds
nothing that helps and stops]({PHASE_HUNT_IMAGES}/greedy_steps.png)

In step 1, silicon and halite tie at -1. Greedy keeps the first one it found,
silicon, and picks up halite in step 2. On powder 23 greedy gets the right answer.

## Where greedy goes wrong

Greedy never looks back, and it never doubts. Powder 12 holds anatase and silver.
Silver's peaks sit less than 0.3 degrees from gold's, so the peaks fit gold exactly
as well. Gold comes first in the library, so greedy says "anatase and gold" and
sounds just as sure as when it is right.

![Gold's and silver's four peaks side by side, each student pair inside the 0.3 degree
tolerance]({PHASE_HUNT_IMAGES}/gold_and_silver.png)

Run `phase_hunt.py` in VS Code when both functions pass their tests. Greedy names 166 of
the 200 benchmark powders right and 34 wrong. In period 3 you write `search()`, which
scores every guess of up to three phases, 176 of them, and keeps every guess that
ties for the best score. When gold and silver tie, the search can answer "can't
tell", and a scientist knows to take a second measurement.

## Real scientists do this

Naming the phases in a powder pattern is called **phase identification**, and
beamline scientists do it every day. At the NSLS-II Student pair Distribution Function (PDF)
beamline, Brookhaven's Crystallography Companion Agent names phases while the data
comes in. The CrystalShift program (Cornell, 2025) and the Dara program (Berkeley Lab,
2025) search a tree of phase sets the way your code will in period 3, on real
patterns from the synchrotrons SSRL and CHESS and from a self-driving lab.
`misc/designer/science_tree_search_survey.md` lists the papers.

## Words to know

- **phase:** one kind of crystal, such as quartz. A powder can mix several phases.
- **peak:** a bright spot in the X-ray pattern, at an angle called 2θ.
- **fingerprint:** the list of a phase's peaks, in `LIBRARY`.
- **tolerance:** how close two peaks must be, 0.3 degrees, to count as one peak.
- **guess:** a set of phases that might explain the pattern.
- **greedy:** always take the step that looks best right now, and never go back.""",
    (10, 3): f"""## The tree you search

In period 2, `greedy_phases()` built one guess, one phase at a time. In this period,
`search()` scores **every** guess of up to three phases. The guesses form a tree,
like Remus's game tree: the empty guess at the top, one more phase on each level
down. Going down a branch adds a phase (`append`, like making a move), and coming
back up takes it out (`pop`, like undoing it). The period 2 goals file explains the
experiment and the score.

![The tree of guesses for powder 23, using 4 of the 10 phases and 2 levels, with
the score of each guess; silicon + halite scores best]({PHASE_HUNT_IMAGES}/search_tree.png)

Silicon + halite is the same guess as halite + silicon, just as two move orders can
reach the same chess position. So `search()` adds phases only in library order,
from `PHASE_NAMES[start]` on. With 10 phases and 3 levels, that scores 176 guesses
instead of 821.

`search()` keeps every guess that ties for the best score in `hunt.sets`, not just
the first. When the answer is one guess, the search is sure. When gold and silver tie,
the answer holds both, and the verdict is "can't tell".

![Over 200 powders, greedy is right 166 times and wrong 34 times; the search is
right 139 times, says can't tell 52 times, and is wrong 9
times]({PHASE_HUNT_IMAGES}/verdicts.png)

Greedy names more powders right, because it guesses gold every time and gold is
right half the time. The search is wrong far less often, and it says so when the
pattern cannot decide. A scientist then takes a second measurement, such as X-ray
fluorescence, which tells gold from silver at once.""",
}

# (file, function) -> one paragraph: what the change does, why, and the big picture
# (file, function), or (lab name, "Part #N") and (lab name, function), -> how the
# code a student pair types works, line by line. make_student_folders.py writes each
# note under the code in the "The code you type" section.
CODE_NOTES: dict[tuple[str, str], str] = {
    ("evaluation.py", "king_safety"): (
        "The loop runs twice, once for each side. The first pass looks at White's "
        "king `K`, its pawns `P`, and Black's queen `q`. White's pawns stand in "
        "front of its king at smaller row numbers (row 0 is rank 8), so `forward` "
        "is -1, and `sign` is +1 because points for White are positive. The second "
        "pass swaps all four for Black. The first small loop sets `queen_on_board` "
        "to True if the enemy queen is anywhere on the board; with no enemy queen, "
        "`continue` skips that side, since a king is safe enough without a shield. "
        "Next the two loops over `row` and `col` find the king. For the king's own "
        "file and the files on each side (`col - 1` to `col + 1`), the code looks "
        "one and then two squares ahead. The first friendly pawn it finds adds "
        "`SHIELD_PAWN` (15) and `break` stops, so each file counts at most once. "
        "Example: a White king on g1 with pawns on f2, g2, and h2 earns 3 x 15 = "
        "45."
    ),
    ("search.py", "is_draw_in_search"): (
        '`state["history"]` holds the key of every position of the game so far, '
        "with the current position last, so `key` is the position on the board "
        "right now. `count(key) >= 2` is True when that same position appeared "
        "before, the first step toward a threefold repetition. The search treats "
        "the first repeat as a draw: if the line can repeat once, the side that "
        "wants a draw can repeat it again. `halfmove_clock >= 100` catches the "
        "fifty-move rule: 100 half-moves, 50 by each side, with no capture and no "
        "pawn move. `or` makes the function return True when either rule applies."
    ),
    ("test_upgrades.py", "test_draw_sense_search_agrees_with_alpha_beta"): (
        "The test sets up the Italian opening from its FEN and takes a snapshot of "
        "the whole state. It runs the plain search, `alpha_beta_with_quiescence`, "
        "to depth 3 with the wide window, then the enhanced engine's "
        "`draw_sense_search` on the same position. The three asserts check that "
        "both searches give the same score, that the new search returns a line of "
        "moves (a non-empty principal variation), and that the snapshot is "
        "unchanged, which proves every `make_move` was undone. `*WIDE` unpacks the "
        "pair of numbers into the two arguments `alpha` and `beta`."
    ),
    ("test_upgrades.py", "test_a_repeated_position_is_a_draw"): (
        "The game starts from the normal starting position, where nothing has "
        "repeated, so the first assert expects False. The loop plays four moves "
        "from their UCI text: the knights jump out (g1f3, g8f6) and back (f3g1, "
        "f6g8). The board then looks exactly like the start, with White to move, so "
        "its key is in the history twice and `is_draw_in_search` must say True."
    ),
    ("test_upgrades.py", "test_the_fifty_move_limit_is_a_draw"): (
        "The FEN puts a king and rook against a lone king and sets the halfmove "
        "clock, the fifth field, to 100. Nothing has repeated, so only the "
        "fifty-move rule can make the assert pass."
    ),
    ("evaluation.py", "mating_bonus"): (
        "The first loops walk the board once. They remember where each king stands "
        "in the dict `kings` and add up the material of each side with "
        "`PIECE_VALUES`, using the uppercase letter for a Black piece. `lead` is "
        "White's material minus Black's, and `weaker` is the smaller of the two "
        "totals. If the lead is under `MATING_MARGIN` (200) or the weaker side "
        "still has more than `WEAK_SIDE_LIMIT` (600), the endgame is not yet a "
        "mating race and the function returns 0. Otherwise the code picks the "
        "winning and losing kings. `CENTER_DISTANCE` gives 3 for an edge row or "
        "column and 0 for the middle, so `edge` grows as the losing king is pushed "
        "toward the edge or a corner. `kings_apart` counts the king steps between "
        "the two kings, and `7 - kings_apart` grows as the winning king closes in. "
        "The bonus is positive when White is winning and negative when Black is."
    ),
    ("search.py", "search_later_move"): (
        "This is the heart of principal variation search. The first call to "
        "`pvs_search` uses a null window, `-alpha - 1` to `-alpha`, a window one "
        "point wide. It costs little and answers one question: is this move better "
        "than the best move so far? The minus signs flip the window and the score, "
        "as in every negamax call. If the score lands strictly between `alpha` and "
        "`beta`, the move surprised us by being better, so the code searches it "
        "again with the full window, `-beta` to `-alpha`, to learn its exact score. "
        "Most moves are not better, so most moves need only the cheap search."
    ),
    ("test_upgrades.py", "test_pvs_search_agrees_with_alpha_beta"): (
        "The test runs the plain search, `alpha_beta_with_quiescence`, and the "
        "enhanced engine's `pvs_search` on the Italian opening at depth 3. The "
        "asserts check that both find the same score, that PVS returns a line of "
        "moves, and that the state snapshot is unchanged, which proves the search "
        "undid every move it made. `*WIDE` unpacks the pair of numbers into `alpha` "
        "and `beta`."
    ),
    ("test_upgrades.py", "test_a_null_window_answers_only_better_or_not"): (
        "First the test finds the exact score with the wide window. Then it tries "
        "two null windows, one 50 points below the exact score and one 50 points "
        "above. A null-window search does not promise the exact score, only the "
        "right side of `alpha`: the assert checks that `score > alpha` agrees with "
        "`exact > alpha` both times."
    ),
    ("search.py", "make_null_move"): (
        "A null move is a pass: the side to move gives the turn away without moving "
        "a piece. The function saves the en passant target first, because the undo "
        'needs it back. `opponent` flips the turn from "w" to "b" or back. A pass '
        "cancels any en passant capture, so the target becomes None. The new "
        "position's key goes onto the history, so the repetition rules still see "
        "every position the search visits, and the saved target is returned for "
        "`undo_null_move`."
    ),
    ("search.py", "undo_null_move"): (
        "The undo takes the three steps of `make_null_move` back in reverse order: "
        "it removes the last history key, flips the turn back, and puts back the en "
        "passant target that `make_null_move` returned."
    ),
    ("test_upgrades.py", "test_null_move_and_undo_restore_the_state"): (
        "The test takes a snapshot of the Italian opening, makes a null move, and "
        "checks that Black now has the turn. After `undo_null_move` the snapshot "
        "must match exactly: same board, turn, en passant target, clocks, and "
        "history."
    ),
    ("test_upgrades.py", "test_null_move_search_saves_work_and_keeps_the_state"): (
        "Two `SearchInfo` records count positions: `plain` for ordinary alpha-beta "
        "and `upgraded` for the null-move search, both at depth 4 on the Italian "
        "opening. The asserts check that the upgraded search visits fewer "
        "positions, that it returns a line of moves, and that the state snapshot is "
        "unchanged afterward."
    ),
    ("search.py", "reduction"): (
        "`index` is the move's place in the ordered list, counting from 0, so "
        "`index >= LATE_MOVE_INDEX` (3) means the fourth move or later. `depth >= "
        "3` keeps the reduction away from the last plies, where one ply matters "
        "most. `quiet` is True for a move that captures nothing (`captured == "
        "EMPTY`) and does not promote. The last line returns 1, meaning search this "
        "move one ply shallower, only for a late, quiet move that does not give "
        "check. Every other move returns 0 and gets the full depth."
    ),
    ("test_upgrades.py", "test_only_late_quiet_moves_are_reduced"): (
        "The test builds one quiet pawn move, a2a3, and asks `reduction` about it "
        "five times, changing one thing each time. At depth 4 and index 5 with no "
        "capture and no check the answer is 1. Each other line breaks one "
        "condition, an early index, a depth of 2, a captured pawn, or a check, and "
        "expects 0."
    ),
    ("test_upgrades.py", "test_reduced_search_saves_work_and_keeps_the_state"): (
        "Two `SearchInfo` records count positions: `plain` for ordinary alpha-beta "
        "and `upgraded` for `reduced_search`, both at depth 4 on the Italian "
        "opening. The asserts check that the reduced search visits fewer positions, "
        "that it returns a line of moves, and that the state snapshot is unchanged "
        "afterward."
    ),
    ("evaluation.py", "pawn_structure"): (
        "The outer loop runs once for White (`P`, enemy `p`, sign +1) and once for "
        "Black. First it counts the side's pawns on each file in the list `files`, "
        "so `files[4]` is the number of pawns on the e-file. The second pass visits "
        "each pawn. A file with more than one pawn means doubled pawns, and each "
        "costs `DOUBLED_PAWN` (8). If both neighboring files hold no friendly pawn, "
        "the pawn is isolated and costs `ISOLATED_PAWN` (20); a pawn on the a-file "
        "or h-file has only one neighbor, so the missing side counts as 0. Then "
        "`ahead` lists the rows in front of the pawn: smaller rows for White, "
        "because row 0 is rank 8. If no enemy pawn stands on those rows on the "
        "pawn's own file or a neighboring file, nothing can stop it, so it is "
        "passed. `advanced` counts how far it has come from its starting row, and "
        "`PASSED_PAWN[advanced]` gives a bigger bonus the closer it is to "
        "promoting."
    ),
    ("opening_book.py", "load_book"): (
        "The book is a dict from a position key to a list of moves. If the file is "
        "missing, the function prints a note to stderr (not stdout, which belongs "
        "to the UCI conversation) and returns the empty book, so Remus still plays. "
        "Otherwise it reads the file line by line and skips blank lines and "
        'comments. `read_defender` splits a line such as "Black: e4 e5 Bc4 Nc6" '
        "into the side it teaches and its moves. Each line replays from the "
        "starting position: `parse_san` turns text such as Nc6 into a Move, and a "
        "move that is not legal skips the rest of the line. Before making each "
        "move, the code stores it under the current position's key, but in a trap "
        "line only for the defending side. `setdefault` makes a new empty list the "
        "first time a position appears, and `if move not in moves_here` keeps a "
        "move from appearing twice when two openings share it."
    ),
    ("opening_book.py", "book_move"): (
        "`book.get` looks up the current position's key and returns its list of "
        "moves, or None if the position is not in the book. `random.choice` picks "
        "one of the moves, so Remus does not play the same opening every game. When "
        "the list is missing, the function returns None and the search chooses the "
        "move instead."
    ),
    ("search.py", "remember_killer"): (
        "A killer is a quiet move that caused a cutoff, so the first line returns "
        "at once for a capture or a promotion, which move ordering already puts "
        "first. `info.killers` maps each ply to its list of killers; `setdefault` "
        "makes an empty list the first time a ply appears. A new killer goes to the "
        "front of the list with `insert(0, move)`, and `del killers[2:]` cuts the "
        "list back to the two newest moves."
    ),
    ("move_ordering.py", "order_moves"): (
        "Each move gets a score: `mvv_lva_score` gives a capture a high score and a "
        "quiet move 0, and a quiet move that is one of this ply's killers gets "
        "`KILLER_SCORE` (50) instead, which ranks it above the other quiet moves "
        "but below every capture. The `while` loop finds where the move belongs in "
        "the list kept sorted from the highest score down, stepping past every move "
        "that scores at least as high so that ties keep the order the generator "
        "gave them. `insert` puts the move and its score at that place. At the end, "
        "the move named `first`, such as the best move of the last iteration, moves "
        "to the very front."
    ),
    ("test_upgrades.py", "test_killers_keep_two_quiet_moves"): (
        "The test takes the board of the starting position and records three quiet "
        "moves as killers at ply 2: e2e4, then d2d4, then g1f3. Only two fit, the "
        "newest first, so the list must read g1f3, d2d4. `move_to_uci` turns each "
        "Move into text for the comparison."
    ),
    ("transposition_table.py", "store"): (
        "`table.get(key)` returns what the table already holds for this position, "
        "or None. The new result is saved when there is no old one, or when the new "
        'search went at least as deep (`depth >= old["depth"]`), because a deeper '
        "search is worth more. The entry is a small dict with the depth, the score, "
        "the bound (EXACT, LOWER, or UPPER), and the best move."
    ),
    ("transposition_table.py", "probe"): (
        "The function returns a score only when the stored result answers the "
        "question this search asks. A missing entry, or one searched less deeply "
        "than `depth`, returns None. An EXACT score always answers. A LOWER bound "
        "means the true score is at least the stored score, so it answers only when "
        "it reaches `beta`: that is already a cutoff. An UPPER bound means the true "
        "score is at most the stored score, so it answers only when it is at or "
        "below `alpha`: the move cannot improve on the best so far. Anything else "
        "returns None, and the position is searched."
    ),
    ("test_upgrades.py", "test_transposition_table_bounds"): (
        'The test fills an empty table by hand with three made-up positions, "a", '
        '"b", and "c", one for each kind of bound. Each assert then asks one '
        "question. Position a's exact 50 answers at depth 3 but not at depth 4, "
        "which was never searched. Position b is at least 80: that settles a window "
        "whose beta is 70 (a cutoff), but not one whose beta is 100. Position c is "
        "at most -20, which cannot beat alpha 0. The last line checks that the best "
        "move of position a was kept."
    ),
    ("python_caches", "remembered_perft"): (
        "`(square, depth)` packs two values into one tuple, such as `((7, 6), 8)` "
        "for 8 moves from g1. A tuple never changes, so Python accepts it as a dict "
        "key, and one key holds both facts. `if key not in cache` asks whether this "
        "question has been answered before. Only when it has not does the slow "
        "`knight_perft` run, and its answer goes into `cache[key]`. The last line "
        "returns the stored answer either way, so the second call with the same "
        "square and depth skips the counting and returns at once."
    ),
    ("python_caches", "Part #2"): (
        "`math.dist` measures the straight-line distance between two points. d4 is "
        "(row 4, col 3) and g7 is (row 1, col 6): 3 rows and 3 columns apart, so "
        "the distance is the square root of 3 x 3 + 3 x 3 = 18, about 4.243. The "
        "f-string's `:.3f` prints three digits after the decimal point."
    ),
    ("python_caches", "Part #3"): (
        "`random.seed(2016)` sets the starting point of Python's random numbers. "
        "The code below rolls a die, seeds again with the same number, and rolls "
        "again, so both rolls are the same and the comparison prints True. Without "
        "the first seed the two rolls would match only about one time in six."
    ),
    ("python_setup", "Part #2"): (
        "The first line stores text in a variable named `team_name`; the quotes "
        "mark where the text starts and stops. An f-string, the `f` before the "
        "quotes, fills each `{...}` with the value inside, so the greeting prints "
        "your team name. `len()` counts the characters of a string, and spaces "
        "count too."
    ),
    ("python_setup", "Part #3"): (
        "`back_rank` holds White's eight back-rank pieces as one string, from the "
        "a-file to the h-file. `back_rank[4]` reads the character at index 4. "
        "Python counts from 0, so index 4 is the fifth letter, the king on the "
        "e-file."
    ),
    ("python_strings", "Part #1"): (
        "A string is a row of characters, and `[ ]` reads one of them by its index. "
        "`square[0]` is the first character, the file letter e, and `square[1]` is "
        "the second, the rank digit 2. The f-string prints both."
    ),
    ("python_strings", "Part #2"): (
        "`ord()` turns a letter into its number in the computer's character table, "
        'and the letters a to h have numbers in a row. Subtracting `ord("a")` gives '
        '0 for a, 1 for b, and 4 for e: a file number. `int()` turns the text "2" '
        "into the number 2, so Python can do arithmetic with it."
    ),
    ("python_strings", "Part #3"): (
        "`chr()` goes the other way, from a number back to a letter. Adding 6 to "
        'the number of "a" lands on "g". The f-string then glues the letter and the '
        "rank 7 into the square name g7."
    ),
    ("python_strings", "Part #4"): (
        "`upper()` returns a new string with every letter in uppercase, which turns "
        "Black's back rank into White's. Remus uses the same rule as FEN: uppercase "
        'is White and lowercase is Black. `"N".isupper()` asks whether a letter is '
        "uppercase and gives True or False."
    ),
    ("python_lists", "Part #1"): (
        "`len()` counts the items in a list: 8 pieces. `back_rank[3]` reads the "
        "item at index 3. Counting from 0, a is index 0 and d is index 3, so the "
        "d-file holds the queen."
    ),
    ("python_lists", "Part #2"): (
        "`for col in range(8)` runs the indented line once for each number from 0 "
        'to 7. `end=" "` prints a space instead of starting a new line, so the '
        "eight pieces appear on one line. The empty `print()` after the loop ends "
        "that line."
    ),
    ("python_lists", "Part #3"): (
        "The board starts as an empty list, and the first loop appends 8 rows of 8 "
        'dots. Each `["."] * 8` builds a new list, so changing one row never '
        "changes another. The next four lines put the pieces on rows 0, 1, 6, and "
        "7; row 0 is rank 8, Black's back rank. The last two loops build one line "
        "of text per row with `+=` and print it, so the board appears with Black at "
        "the top."
    ),
    ("python_lists", "Part #4"): (
        "`board[6][4]` is row 6 (rank 2), column 4 (the e-file), the square e2. "
        "Setting it to a dot and `board[4][4]` to `P` plays 1. e4. The loop then "
        "visits each square of row 6 and adds 1 to `pawns` for every White pawn it "
        "finds: 7 are left."
    ),
    ("python_functions", "is_white"): (
        "`isupper()` returns True when a letter is uppercase. In Remus uppercase "
        "letters are White pieces, so this one line answers the question in the "
        "function's name."
    ),
    ("python_functions", "on_board"): (
        "`0 <= row <= 7` is True only when the row is 0, 1, ..., or 7, and the same "
        "test checks the column. `and` makes the whole answer True only when both "
        "are inside the board."
    ),
    ("python_functions", "is_black"): (
        "This function you write from nothing: the `def` line names it and lists "
        "its input with a type hint, the docstring says what it does, and the body "
        "returns the answer. `islower()` is True for a lowercase letter, a Black "
        "piece."
    ),
    ("python_functions", "test_is_white"): (
        "A test is a function whose name starts with `test_`. Each `assert` checks "
        "one fact: a White knight `N` is White, and a Black knight `n` is not. If a "
        "fact is False, the assert stops the program and names the line."
    ),
    ("python_functions", "test_on_board"): (
        "The first assert checks a square in the corner, a1 (row 7, col 0). The "
        "second checks row 8, which is one row past the edge, so `on_board` must "
        "answer False."
    ),
    ("python_functions", "Part #2"): (
        "Each line calls your `is_black` inside an f-string and prints the answer "
        "next to the expected one. The single quotes around the f-string let the "
        "code use double quotes inside it."
    ),
    ("python_functions", "Part #3"): (
        "A square is a tuple of two numbers. `row, col = square` unpacks it, giving "
        "the first number the name `row` and the second the name `col`. The last "
        "line passes both names to `on_board`."
    ),
    ("python_functions", "Part #4"): (
        "Calling the two test functions runs their asserts. If every assert is "
        "True, nothing happens and the program goes on to print its success line."
    ),
    ("python_dicts", "Move"): (
        "`@dataclass` turns a short class into a record type. Each line inside "
        "names one field and its type. Python then writes the code that builds a "
        "Move from two values and prints it neatly."
    ),
    ("python_dicts", "Part #1"): (
        "A dict stores values under keys. `state['turn']` reads the value stored "
        'under the key "turn". Inside an f-string that already uses double quotes, '
        'the key needs single quotes. `state["turn"] = "b"` replaces the value: '
        "Black is to move."
    ),
    ("python_dicts", "Part #2"): (
        "`b2 = board` makes no copy. It gives the same board a second name, so "
        "writing a pawn through `b2` changes `board` too. `is` asks whether two "
        "names point to the very same object, and here the answer is True."
    ),
    ("python_dicts", "Part #3"): (
        "`deepcopy` builds a new board, a new outer list holding new copies of "
        "every row. Changing `b3` leaves `board` alone. `is` is now False, because "
        "these are two objects, and `==` compares their contents, which differ on "
        "a8."
    ),
    ("python_dicts", "Part #4"): (
        '`Move("e2", "e4")` builds a record, filling the fields in the order the '
        "class lists them. `move.to_square` reads one field by name, and "
        "`print(move)` shows all of them."
    ),
    ("game_state.py", "is_white"): (
        "`isupper()` is True for an uppercase letter. FEN writes White pieces in "
        'uppercase, so `"N".isupper()` is True and `"n".isupper()` is False.'
    ),
    ("game_state.py", "color_of"): (
        "An empty square, the dot `EMPTY`, has no color, so the function returns "
        "None first. Every other square holds a piece: `is_white` sends White "
        'pieces to `WHITE` ("w"), and every piece left is Black.'
    ),
    ("moves.py", "move_to_uci"): (
        "`move.from_square` is a tuple such as (6, 4), and the `*` unpacks it into "
        'the two arguments `square_name` needs, giving "e2". The two names glue '
        'together into "e2e4". A promotion adds the new piece\'s letter in '
        "lowercase, as UCI always writes it: e7e8q."
    ),
    ("moves.py", "move_from_uci"): (
        '`text[0:2]` is the first two characters, such as "e7", and `parse_square` '
        "turns them into a (row, col) tuple; `text[2:4]` is the landing square. A "
        "five-character move ends in a promotion letter. That letter becomes "
        "uppercase when White moves and lowercase when Black moves, so the new "
        "piece has the right piece color."
    ),
    ("make_move.py", "make_move"): (
        "First the function reads the moving piece and whatever stands on the "
        "landing square. Before anything changes, it records the old values in the "
        "`undo` dict: the move, both pieces, the castling rights, the en passant "
        "target, and both clocks. Next `set_piece` puts the piece on its new square "
        "and empties the old one. A capture or a pawn move resets the halfmove "
        "clock to 0, and any other move adds 1. The fullmove number grows after "
        "Black moves. Finally the turn passes to the opponent, and the function "
        "returns the undo record."
    ),
    ("make_move.py", "undo_move"): (
        "The undo record holds everything the move changed. The piece goes back to "
        "its starting square, and the landing square gets back what stood there "
        "before: the captured piece, or `EMPTY` for a quiet move. The turn flips "
        "back, and the castling rights, en passant target, and both clocks are "
        "copied from the record."
    ),
    ("python_loops", "Part #1"): (
        "A `while` loop repeats its indented lines as long as its test is True. "
        "`count` starts at 0 and grows by 1 each time, so the loop prints steps 0, "
        "1, and 2 and stops when `count` reaches 3."
    ),
    ("python_loops", "Part #2"): (
        "A direction is a tuple of two steps. Unpacking gives each step a name: "
        "`row_step` is -1, one row toward rank 8, and `col_step` is 1, one column "
        "to the right."
    ),
    ("python_loops", "Part #3"): (
        "`while True` repeats until a `break` stops it. Each pass takes one step in "
        "the direction. If the step leaves the board, the walk ends. Otherwise the "
        "square's name is added to the text, and if a piece stands there the walk "
        "ends too, after counting that square. This is the walk a bishop, rook, or "
        "queen makes."
    ),
    ("move_generation.py", "king_moves"): (
        "A king jumps one step in any of eight directions, and `KING_STEPS` lists "
        "them. `jump_moves` already does the work for the knight: it tries each "
        "step, skips a square off the board or one with a friendly piece, and "
        "returns the rest. The king needs only its own list of steps."
    ),
    ("move_generation.py", "slide"): (
        "The function unpacks the start square and the direction, then takes its "
        "first step. The `while` loop runs while the square is on the board. An "
        "empty square is a move, and the walk goes on. A square with a piece ends "
        "the walk: an enemy piece is one last move, a capture, and a friendly piece "
        "is not a move at all. The last line of the loop takes the next step."
    ),
    ("move_generation.py", "pawn_pushes"): (
        "White pawns move toward row 0 (rank 8), so `forward` is -1 for White and 1 "
        "for Black, and each side's pawns start on their own row. A pawn may step "
        "one square ahead only onto an empty square. `pawn_moves_to` turns a step "
        "onto the last rank into four promotions. Only when the first square is "
        "empty, and the pawn still stands on its starting row, may it also step two "
        "squares to another empty square."
    ),
    ("python_modules", "imports"): (
        "`import board` loads `board.py` and keeps its names behind `board.`, as in "
        "`board.__name__`. `from board import new_board, parse_square` copies those "
        "two names into this file, so they can be called without the prefix. Python "
        "finds each file by its name, without `.py`, in the same folder."
    ),
    ("python_modules", "Part #1"): (
        'Every file has a `__name__`. The file you run is called "__main__", and a '
        'file you import keeps its own name, "board". The `if __name__ == '
        '"__main__"` guard at the bottom of `board.py` is false when the file is '
        "imported, so its `main()` does not run."
    ),
    ("python_modules", "Part #2"): (
        "These lines use functions from three other files. They build the starting "
        'board, turn "g1" into a square, and ask `knight_moves` for the knight\'s '
        "moves. The loop adds each move's UCI text to `names`."
    ),
    ("attacks.py", "piece_at_offsets"): (
        "The function adds each offset, such as (2, 1), to the square to reach a "
        "target square. If the target is on the board and holds the exact piece "
        "asked for, such as a White knight `N`, the square is attacked and the "
        "function returns True at once. After trying every offset with no match it "
        "returns False."
    ),
    ("attacks.py", "attacked_by_pawn"): (
        "A pawn attacks one step diagonally forward. To ask whether a White pawn "
        "attacks a square, look one row toward rank 1 from that square, at (row + "
        "1, col - 1) and (row + 1, col + 1), because White pawns move toward row 0. "
        "For a Black pawn, look the other way, at row - 1. `piece_at_offsets` does "
        "the looking."
    ),
    ("attacks.py", "attacked_by_king"): (
        "The function picks the king letter of the attacking side, `K` for White "
        "and `k` for Black, and asks `piece_at_offsets` whether that king stands on "
        "any of the eight squares around the target."
    ),
    ("attacks.py", "in_check"): (
        "`find_king` finds the king of `color` on the board, and `opponent` gives "
        "the other side. A king is in check when the other side attacks its square, "
        "so one call to `is_square_attacked` answers the question."
    ),
    ("legal_moves.py", "legal_moves"): (
        "The function remembers whose move it is in `mover`, because `make_move` "
        "passes the turn. For each pseudo-legal move it makes the move, asks "
        "whether the mover's own king is now in check, and keeps the move only if "
        "it is not. `undo_move` puts the position back before the next move is "
        "tried. This one test catches pins, moves into check, and en passant "
        "captures that expose the king."
    ),
    ("demo_practice_positions", "Part #1"): (
        "Before you run the file, change `prediction` to the number of legal moves "
        "you expect, then compare it with the count Remus prints. From the starting "
        "position it is 20: 16 pawn moves and 4 knight moves."
    ),
    ("demo_practice_positions", "Part #2"): (
        "`position` builds a board holding only the pieces in the dict. The Black "
        "rook on e8 checks the White king on e1 along the e-file, so `in_check` "
        "prints True. Count the king's legal moves yourself, put the number in "
        "`prediction`, and run the file."
    ),
    ("demo_practice_positions", "Part #3"): (
        "The White knight on e2 stands between its king and the Black rook, so it "
        "is pinned: any knight move would expose the king. The loop counts the "
        "legal moves that start on e2, using the first two characters of each "
        "move's UCI text, and finds none."
    ),
    ("python_sets", "Part #1"): (
        "`set()` makes an empty set, and `add` puts an item in. A set holds each "
        "item only once, so adding h1 a second time changes nothing and `len` "
        "counts 2."
    ),
    ("python_sets", "Part #2"): (
        "`in` asks whether an item is in the set and answers True or False. The "
        "question works on lists and dicts too, but a set answers it fastest."
    ),
    ("python_sets", "Part #3"): (
        "The dict maps each home square to the castling rights a move from it "
        "removes. `rights_lost['h1']` reads the rights of h1. `in` on a dict asks "
        "about its keys, and d1 is not one of them."
    ),
    ("python_sets", "Part #4"): (
        'Strings never change, so `replace("K", "")` returns a new string without '
        "the K, and the code stores it back in `rights`. The loop removes each "
        "letter that e8 guards, k and then q, which is what a Black king move does."
    ),
    ("make_move.py", "update_castling_rights"): (
        "A move can touch two home squares, the one it leaves and the one it lands "
        'on, so the loop checks both. `CASTLING_SQUARES.get(square, "")` gives the '
        "rights that square guards, or an empty string for any other square. Each "
        "guarded letter is removed with `replace`. Moving the h1 rook removes K, "
        "and capturing the rook on h1 removes K too."
    ),
    ("make_move.py", "en_passant_victim_square"): (
        "An en passant capture lands behind the pawn it takes. The captured pawn "
        "stands on the row the capturing pawn starts from, `move.from_square[0]`, "
        "and in the column it lands in, `move.to_square[1]`. Example: a White pawn "
        "on e5 captures on d6, and the Black pawn it takes stands on d5."
    ),
    ("demo_promotion", "Part #1"): (
        "The loop tries all four promotions on b8, one after the other. For each "
        "one it makes the move, counts Black's legal replies, and decides the "
        "result. With no reply, a king in check is checkmated and a king not in "
        "check is stalemated. `undo_move` restores the position before the next "
        "promotion is tried."
    ),
    ("python_recursion", "countdown"): (
        "A recursive function calls itself on a smaller problem. The base case "
        "comes first: at 0 the function prints Go! and returns, so the calls stop. "
        "Otherwise it prints its number and calls `countdown(number - 1)`, which "
        "does the rest."
    ),
    ("python_recursion", "count_leaves"): (
        "A leaf is a string, and it counts as 1. Any other tree is a list of "
        "branches, so the function adds up `count_leaves` of each branch. Each "
        "branch is a smaller tree, so every call gets closer to the leaves."
    ),
    ("perft.py", "perft"): (
        "At depth 0 the position itself is one leaf. Otherwise the function makes "
        "each legal move, counts the leaves below it with `perft(state, depth - "
        "1)`, and undoes the move before trying the next one. The total is the "
        "number of positions at the given depth. From the start position perft(3) "
        "is 8,902."
    ),
    ("fen.py", "fen_placement"): (
        "FEN writes each rank from the a-file to the h-file, and a run of empty "
        "squares becomes one digit. For each row the code counts empty squares in "
        "`empty_count`. When a piece appears, the count, if any, is written first, "
        "then the piece letter. At the end of the row a final count is written. A "
        'slash goes between ranks, so the starting row 0 gives "rnbqkbnr" and an '
        'empty rank gives "8".'
    ),
    ("fen.py", "board_from_placement"): (
        '`split("/")` cuts the placement into eight ranks, rank 8 first. In each '
        "rank a digit adds that many empty squares and a letter adds one piece. A "
        "rank that does not add up to 8 squares, or a placement without 8 ranks, "
        "raises `ValueError`, so a typing mistake in a FEN stops at once."
    ),
    ("python_fen_fields", "Part #1"): (
        "`split()` with no argument cuts text at every run of spaces and returns a "
        "list of the pieces. A FEN has six fields, so the list holds 6 items."
    ),
    ("python_fen_fields", "Part #2"): (
        "The loop counts i from 0 to 5 and prints the name of field i next to its "
        "value, so each field is labeled."
    ),
    ("python_fen_fields", "Part #3"): (
        '`try` runs a line that may fail. `int("x")` cannot make a number from x, '
        "so Python raises `ValueError`, and the `except ValueError` lines run "
        'instead of stopping the program. Change `text` to "12" to see the other '
        "path."
    ),
    ("game_end.py", "insufficient_material"): (
        "The loops collect every piece except the kings in `pieces`, in uppercase. "
        "For each bishop they add the color of its square: `(row + col) % 2` is 0 "
        "on one color and 1 on the other. Kings alone, or a king with one bishop or "
        "one knight, cannot mate, so the answer is True. Any other piece besides "
        "bishops can mate, so the answer is False. When only bishops are left, mate "
        "is impossible only if they all stand on squares of one color."
    ),
    ("game_end.py", "game_result"): (
        "The checks run in order. With no legal move, the game is over: checkmate "
        "if the side to move is in check, and the other side wins; stalemate if "
        "not. Next come the three draws: too little material to mate, the same "
        "position three times, and 100 half-moves with no capture or pawn move. If "
        "none applies, the game goes on and the function returns None."
    ),
    ("notation.py", "parse_san"): (
        '`strip()` removes spaces, `rstrip("+#!?")` removes check, mate, and '
        'comment marks from the end, and `replace("0", "O")` accepts castling typed '
        "with zeros. Then the function writes every legal move in SAN with "
        "`move_to_san` and returns the one whose text matches. Nothing matching "
        "means the text is not a legal move here, so it raises `ValueError`."
    ),
    ("python_input_output", "Part #1"): (
        "`random.choice` picks one item from a list. The seed above it makes the "
        "pick the same on every run."
    ),
    ("python_input_output", "Part #2"): (
        "The loop remembers the best item so far. It starts with the first victim, "
        "and every piece worth more takes its place. After the loop, `best` holds "
        "the most valuable piece, the queen."
    ),
    ("python_input_output", "Part #3"): (
        "`file=sys.stderr` sends the text to the error stream instead of the normal "
        "output. Lucas Chess reads only the normal output, so notes for people go "
        "to stderr and never confuse the GUI."
    ),
    ("python_input_output", "Part #4"): (
        "`for line in sys.stdin` reads one line each time you press Enter. "
        '`strip()` removes the newline. "quit" ends the loop; "isready" gets '
        '"readyok", the answer a UCI engine gives; anything else is echoed back. '
        "`flush=True` sends each answer at once, as the UCI conversation needs."
    ),
    ("search.py", "random_move"): (
        "`legal_moves` lists every legal move, and `random.choice` picks one. This "
        "is the simplest brain: it plays legal chess with no plan."
    ),
    ("search.py", "greedy_move"): (
        "The function shuffles the legal moves, so equal captures are picked at "
        "random. It starts with the first move as the best and checks every move "
        "with `capture_value`. A move that captures more becomes the new best. A "
        "greedy brain grabs the biggest piece it can, without looking at the reply."
    ),
    ("evaluation.py", "material"): (
        "The loops visit every square. An empty square adds nothing. A White piece "
        "adds its value from `PIECE_VALUES`, and a Black piece subtracts the value "
        "of its uppercase letter. The result is positive when White has more "
        "material, as in the starting position minus one Black knight: +300."
    ),
    ("search.py", "negamax"): (
        "Each call counts one node. At depth 0 the function stops looking ahead and "
        "returns `evaluate`. With no legal moves the game is over: a checkmated "
        "side gets a large negative score, worse the sooner the mate (`ply` counts "
        "how deep the search is), and stalemate is 0. Otherwise every move is made, "
        "searched one ply less deep, and undone; `try` and `finally` undo the move "
        "even if the search stops early. The minus sign turns the opponent's score "
        "into ours, and `best` keeps the highest."
    ),
    ("search.py", "alpha_beta"): (
        "The body is negamax with a window. `alpha` is the best score this side is "
        "already sure of, and `beta` is the most the opponent will allow. Each "
        "child is searched with the window flipped, `-beta` and `-alpha`. A score "
        "at or above `beta` is a cutoff: the opponent will never let the game reach "
        "this position, so the remaining moves are skipped. Otherwise a better "
        "score raises `alpha`, and the function returns `alpha`."
    ),
    ("python_sorting", "Part #1"): (
        "The list `ordered` starts empty. For each victim the `while` loop steps "
        "past every piece worth at least as much, and `insert(place, piece)` puts "
        "the new piece there. The list stays sorted from the most valuable down "
        "after each insert."
    ),
    ("python_sorting", "Part #2"): (
        '`-float("inf")` is minus infinity, a number smaller than any real value. '
        "Starting the best there means the first victim always replaces it, so no "
        "special case is needed."
    ),
    ("python_sorting", "Part #3"): (
        "`time.perf_counter()` reads a precise clock. Reading it before and after "
        "`perft` and subtracting gives the seconds the count took."
    ),
    ("search.py", "quiescence"): (
        "Quiescence keeps searching captures after the main search ends, so Remus "
        "never stops in the middle of a trade. The side to move may stand pat, "
        "keeping the score it has without capturing. If that score already reaches "
        "`beta`, the opponent avoids this position, so the function returns at "
        "once. Otherwise each capture is made, searched with the window flipped, "
        "and undone, with the same cutoff as alpha-beta."
    ),
    ("move_ordering.py", "mvv_lva_score"): (
        "MVV-LVA means most valuable victim, least valuable attacker. A capture "
        "scores 10 times the victim's value minus the attacker's value, so pawn "
        "takes queen (9,000 - 100) comes before queen takes queen (9,000 - 900). A "
        "quiet move scores 0. A promotion adds 10 times the new piece's value, as "
        "if it captured that piece."
    ),
    ("search.py", "think"): (
        "`SearchInfo` holds the node count and the deadline, now plus the seconds "
        "allowed. Before searching, `best` is the first move of the ordered list, "
        "so Remus always has an answer. The loop searches depth 1, then 2, then 3: "
        "iterative deepening. Each search starts with the best move of the last "
        "one. When time runs out, the search raises `SearchTimeout`, and `break` "
        "keeps the move from the last depth that finished. A forced mate or a "
        "single legal move ends the loop early."
    ),
    ("demo_results", "Part #1"): (
        "A win is 1 point and a draw half a point, so 9 wins and 4 draws make 11. "
        "The score is points per game, 11 / 20 = 0.55. `elo_gap` turns that score "
        "into the rating difference the Elo formula expects, about +35."
    ),
    ("demo_results", "Part #2"): (
        "20 games cannot measure a score exactly. `1.96 * sqrt(score * (1 - score) "
        "/ games)` is the margin that covers the true score 95 times in 100. "
        "Turning the low and high scores into Elo gives a range. If the whole range "
        "is above 0 or below 0, the enhancement really changed the strength; if it "
        "reaches past 0, more games are needed."
    ),
    ("hidden_peak.py", "candidate_squares"): (
        "The two loops visit every square of the grid, row by row, and keep each "
        "one that has no reading yet. Like `legal_moves` in Remus, this lists the "
        "choices at the current step."
    ),
    ("hidden_peak.py", "score_candidate"): (
        "`nearest` starts at infinity, and the loop lowers it to the distance from "
        "the square to the closest square already measured. The score adds two "
        "parts: `predicted_value`, how hot the square looks from the readings "
        "nearby (exploit), and `explore_weight` times that distance, a reward for "
        "trying somewhere new (explore)."
    ),
    ("hidden_peak.py", "choose_next_measurement"): (
        "This is `greedy_move` again, aimed at a science problem. The function "
        "lists the unmeasured squares, scores each one, and keeps the best so far "
        "in a loop. The square with the highest score is the next one to measure."
    ),
    ("phase_hunt.py", "score"): (
        "`predicted_peaks` lists every peak the chosen phases would make. The score "
        "starts with a cost for each phase, so a simpler answer wins a tie. Each "
        "measured peak that a predicted peak matches adds a point, and each one "
        "nothing explains costs a point. Each predicted peak that the measurement "
        "does not show also costs a point."
    ),
    ("phase_hunt.py", "greedy_phases"): (
        "The loop adds one phase at a time, up to `MAX_PHASES`. In each round it "
        "tries every phase not chosen yet: append it, score the set, and pop it "
        "back off, like making and undoing a move. The phase with the best score "
        "that beats the current set is kept. When no phase helps, `break` ends the "
        "search."
    ),
    ("phase_hunt.py", "search"): (
        "Each call scores the current set of phases. A new best score starts a "
        "fresh list of best sets, and a tie joins the list; `list(phases)` saves a "
        "copy, because `phases` keeps changing. At depth 0 the search stops. "
        "Otherwise it tries each phase from `start` on: append it (make), search "
        "one level deeper with the next index, and pop it (undo). Starting at "
        "`index + 1` means each set is tried once, never in two orders."
    ),
    ("board.py", "print_board"): (
        "The loop prints one line per row, row 0 (rank 8) first. Each line starts "
        "with the rank number from `BOARD_RANKS`, and the inner loop adds a space "
        "and each square's letter with `+`. After the eight rows, the last line "
        "prints the file letters, with two spaces in front so each letter sits "
        "under its column."
    ),
    ("board.py", "square_name"): (
        '`BOARD_FILES` is "abcdefgh", so `BOARD_FILES[col]` is the file letter, and '
        "`BOARD_RANKS` lists the rank digits from row 0, so `BOARD_RANKS[row]` is "
        'the rank. Glued together, (6, 4) gives "e" + "2" = "e2".'
    ),
    ("board.py", "parse_square"): (
        "A square name has exactly two characters, a file letter and a rank digit. "
        'Anything else, such as "i9" or "e10", raises `ValueError` with a message '
        "that shows the bad text. `index` finds where a character sits in a string, "
        'which turns the letter into a column and the digit into a row: "e4" '
        "becomes (4, 4)."
    ),
    ("board.py", "piece_at"): (
        "A square is a (row, col) tuple, so unpacking gives the two numbers their "
        "names. `board[row][col]` picks the row from the list of rows and then the "
        "square from that row."
    ),
}

CHANGE_NOTES = {
    ("board.py", "print_board"): "Prints the board one row at a time, with the rank "
    "number at the left of each row and the file letters along the bottom. Row 0 is "
    "rank 8, so the first line printed is Black's back rank, the way a board looks "
    "from White's side. Every later day prints positions this way, so this is the "
    "window you look through to check your own code.",
    ("board.py", "square_name"): "Turns (row, col) into a name such as e4 by looking "
    "up the file letter and the rank digit. The engine thinks in rows and columns, "
    "but people read square names, so every move Remus shows you goes through this "
    "one line.",
    ("board.py", "parse_square"): "Does the reverse: turns e4 into (4, 4), and "
    "raises `ValueError` for text that is not a square, such as i9. Checking the "
    "input here means a typo stops at the door instead of causing a strange bug "
    "deep in the engine.",
    ("board.py", "piece_at"): "Unpacks a square into its row and column and returns "
    'the piece there. Almost every rule in Remus asks "what is on this square?", '
    "so this tiny function is the one they all call.",
    ("game_state.py", "is_white"): "Returns True for an uppercase letter. Remus "
    "follows FEN, where uppercase is White and lowercase is Black, so one call to "
    "`isupper()` tells the piece colors apart.",
    ("game_state.py", "color_of"): 'Returns "w", "b", or None for an empty '
    "square. Move generation asks this about every square a piece might land on: a "
    "friend blocks the move, an enemy can be captured, and None means the square is "
    "free.",
    ("moves.py", "move_to_uci"): "Writes a move as text such as e2e4, adding a "
    "lowercase piece letter for a promotion (e7e8q). UCI is the language Lucas "
    "Chess speaks, so this is how Remus tells the GUI which move it chose.",
    ("moves.py", "move_from_uci"): "Reads text such as e7e8q back into a Move. The "
    "promotion letter becomes uppercase for White and lowercase for Black, so the "
    "new piece gets the right piece color on the board.",
    ("make_move.py", "undo_move"): "Puts back everything a move changed, using the "
    "undo record that `make_move()` saved: the moved piece, the captured piece, the "
    "side to move, and the clocks and rights. The search will make and undo millions "
    "of moves, so undo must restore the position exactly, or Remus slowly corrupts "
    "its own board.",
    ("make_move.py", "make_move"): "Moves a piece and empties the square it left, "
    "then updates the clocks and gives the turn to the other side. Before changing "
    "anything, it writes down every value the move will destroy, such as the "
    "captured piece and the old clocks, in an undo record. That record is the only "
    "way to take the move back, and a search in Remus makes and undoes thousands "
    "of moves for every move it plays.",
    ("move_generation.py", "king_moves"): "Hands the king's eight one-step jumps to "
    "`jump_moves()`, which the knight uses too. Two pieces share one helper because "
    "both jump to fixed squares; only their list of jumps differs.\n\n"
    + goals_board_image("jump_knight_d4", "A knight on d4 and its 8 squares")
    + " "
    + goals_board_image("jump_knight_a1", "A knight on a1 and its 2 squares")
    + " "
    + goals_board_image("jump_king_a1", "A king on a1 and its 3 squares")
    + "\n\n*Each green square is a jump that stays on the board. A knight on d4 has "
    "all 8. On a1 the knight keeps 2 of its 8 jumps and the king keeps 3 of its 8 "
    "steps, because the others land off the edge.*",
    ("move_generation.py", "slide"): "Walks one direction from a square, adding a "
    "move for each empty square, and stops at the edge or at the first piece. An "
    "enemy piece can be captured, so its square is added before the walk stops; a "
    "friendly piece is not. Rooks, bishops, and queens all use this walk with "
    "different directions.\n\n"
    + goals_board_image(
        "slide_rook", "A rook on d4 with a White pawn on d6 and a Black knight on f4"
    )
    + "\n\n*The rook on d4 walks four ways. Up, it stops on d5, because its own pawn "
    "stands on d6. Down and left, it walks to the edge. Right, it stops on f4 and "
    "may capture the Black knight there (the red arrow).*",
    ("move_generation.py", "pawn_pushes"): "Moves a pawn one square forward if it is "
    "empty, and two squares from its starting row if both are empty. White pawns "
    "move toward row 0, because row 0 is rank 8. Pawns are the only pieces that "
    "move one way and capture another, which is why pushes get their own function.",
    ("attacks.py", "piece_at_offsets"): "Stands on the square and looks at each "
    "offset for one piece, such as an enemy knight. Attacks work backward: instead "
    "of asking where every enemy piece can go, the test looks out from the square. "
    "A knight attacks e5 from exactly the squares a knight on e5 could jump to, so "
    "the knight, the king, and the pawn all share this one loop, the way "
    "`jump_moves()` serves both the knight and the king.\n\n"
    + goals_board_image("attack_knight_e5", "Is e5 attacked by a Black knight?")
    + "\n\n*To test e5 (yellow), the code looks at the eight knight squares around it "
    "(gray). It finds a Black knight on f3, so e5 is attacked (the red arrow).*",
    ("attacks.py", "attacked_by_pawn"): "Looks diagonally for an enemy pawn on the "
    "row behind the square, from the attacker's point of view. A pawn captures "
    "diagonally even though it moves straight, so its two offsets differ from its "
    "push, and they depend on its piece color.\n\n"
    + goals_board_image(
        "attack_pawn", "A White pawn on e4 moves to e5 but attacks d5 and f5"
    )
    + "\n\n*The White pawn on e4 moves straight to e5 (green) but attacks d5 and f5 "
    "(red). So the test for d5 looks one row down and one column to each side for a "
    "White pawn.*",
    ("attacks.py", "attacked_by_king"): "Looks one step away in all eight directions "
    "for the enemy king, with the same `KING_STEPS` the king moves by. Kings can "
    "never stand next to each other, and this check is what stops a king from "
    "walking up to the other king.",
    ("attacks.py", "in_check"): "Finds the king of one piece color and asks whether "
    "the other piece color attacks its square. Check decides which moves are legal, whether "
    "a game is over, and later how deep the search looks.",
    ("legal_moves.py", "legal_moves"): "Tries every pseudo-legal move: makes it, "
    "keeps it if the mover's king is not in check, and undoes it. Testing after the "
    "move catches pins and discovered checks without any special rules, which is why "
    "the code is so short.",
    ("make_move.py", "update_castling_rights"): "Removes castling rights when a king "
    "or rook leaves its square, or when a rook is captured on its square. Rights only "
    'ever disappear, so `replace()` deletes letters from a string such as "KQkq".\n\n'
    + goals_board_image(
        "castling_rights", "The six home squares of the kings and rooks"
    )
    + "\n\n*The six home squares hold the castling rights: e1 holds K and Q, h1 holds K, "
    "a1 holds Q, and for Black e8 holds k and q, h8 holds k, and a8 holds q. When the rook "
    'leaves h1 (the green arrow), White loses K, and "KQkq" becomes "Qkq".*',
    ("make_move.py", "en_passant_victim_square"): "Returns the square of the pawn that "
    "an en passant capture removes: the capturer's starting row and the landing "
    "column. It is the only capture where the victim is not on the landing square.\n\n"
    + goals_board_image(
        "en_passant", "White captures en passant from e5 to d6, removing the pawn on d5"
    )
    + "\n\n*Black has just pushed d7 to d5. The White pawn on e5 captures en passant: it "
    "lands on d6 (yellow), and the Black pawn it removes stands on d5 (red), on the "
    "capturer's starting row, rank 5, in the landing column, d.*",
    ("perft.py", "perft"): "Counts every position reached after exactly `depth` "
    "moves, by making each legal move, counting below it, and undoing it. The counts "
    "from the start (20, 400, 8,902) are published, so a match proves the rules right "
    "and a mismatch points to a bug.",
    ("fen.py", "fen_placement"): "Writes the board as the first field of FEN: one "
    "rank at a time, with a digit for each run of empty squares and a slash between "
    "ranks. FEN lets you save any position in one line and share it with other chess "
    "programs.",
    ("fen.py", "board_from_placement"): "Reads that field back into an 8x8 board, "
    "turning each digit into that many empty squares, and refuses a rank that does "
    "not describe exactly 8 squares. From now on every test position starts as FEN.",
    ("game_end.py", "insufficient_material"): "Returns True when neither side can "
    "ever checkmate: kings alone, a king with one bishop or knight, or bishops that "
    "all stand on light squares, or all on dark squares. A square is light or "
    "dark by "
    "(row + col) % 2.",
    ("game_end.py", "game_result"): "Checks every way a game ends, in order: no legal "
    "moves (checkmate or stalemate), insufficient material, threefold repetition, and "
    "the fifty-move rule. It returns the result and the reason, so a test can "
    "check why a game is over.",
    ("notation.py", "parse_san"): "Finds the legal move that matches typed SAN, such "
    "as Nf3, by writing the SAN of every legal move and comparing. Matching against "
    "real moves means any text Remus accepts is a legal move.",
    ("search.py", "random_move"): "Picks any legal move at random. It is Remus's "
    "first brain: weak, but it proves the engine can play a whole game legally.",
    ("search.py", "greedy_move"): "Picks the move that captures the most valuable "
    "piece, after shuffling so ties are broken at random. Greedy Remus beats random "
    "Remus, yet falls for any trap one move deep, which is why searching ahead comes "
    "next.",
    ("evaluation.py", "material"): "Adds up the pieces in centipawns (pawn 100, knight "
    "300, bishop 300, rook 500, queen 900), plus for White and minus for Black. It is "
    "the first evaluation term, and the search uses it to tell good positions from "
    "bad ones.",
    ("search.py", "negamax"): "Looks `depth` moves ahead. At depth 0 it returns the "
    "evaluation; with no legal moves it returns a mate score or 0 for stalemate. "
    "Otherwise it makes each move, asks for the opponent's score of the position, "
    "and flips its sign, because a position good for the opponent is bad for the "
    "mover. The best of those flipped scores is the score of the position. This "
    "one idea, calling itself on every reply, is the heart of every chess engine.",
    ("search.py", "alpha_beta"): "Does the same work as negamax, but carries two "
    "numbers: alpha, the score the mover is already sure of, and beta, the score "
    "the opponent will not allow. As soon as one move scores beta or more, the "
    "opponent would never let this position happen, so the other moves are skipped. "
    "The answer is the same as negamax, and far fewer positions are visited, so "
    "Remus can look deeper in the same time.",
    ("search.py", "quiescence"): "Keeps searching captures after the depth runs "
    "out, so Remus never judges a position in the middle of a trade. The mover may "
    '"stand pat" and take the evaluation as it is, or try a capture that does '
    "better. Without it, a search that stops after queen takes pawn misses the pawn "
    "that takes the queen back.",
    ("move_ordering.py", "mvv_lva_score"): "Scores a capture: most valuable victim, "
    "least valuable attacker, so pawn takes queen comes first. Alpha-beta cuts off "
    "more of the tree when strong moves come first, so the same search finishes "
    "faster.",
    ("search.py", "think"): "Searches depth 1, then depth 2, then depth 3, and keeps "
    "the best move of the deepest search that finished. When the clock runs out in "
    "the middle of a search, the unfinished search is thrown away. Each finished "
    "depth also puts its best move first for the next depth, so alpha-beta cuts off "
    "more. This is iterative deepening, and it lets Remus play on any clock.",
    ("hidden_peak.py", "candidate_squares"): "Lists every square not measured yet. "
    'These are the "legal moves" of the science problem: the places the AI could '
    "measure next.",
    ("hidden_peak.py", "score_candidate"): "Scores a square by its predicted value "
    "plus a bonus for being far from earlier readings. The first part exploits what "
    "the AI knows, and the second explores where it knows little.",
    ("hidden_peak.py", "choose_next_measurement"): "Returns the candidate with the "
    "highest score, just as `greedy_move()` returns the best capture. The same "
    "generate, score, and choose loop now runs on a science problem.",
    ("phase_hunt.py", "score"): "Scores a guess about which phases are in the "
    "powder: a point for each measured peak the phases explain, and a point lost for "
    "each peak left over, each predicted peak that is missing, and each phase used. "
    "It is the evaluation of the science problem, like `material()` for a chess "
    "position, and the cost per phase makes the simpler explanation win a tie.",
    ("phase_hunt.py", "greedy_phases"): "Adds the phase that raises the score most, "
    "then the next, and stops when no phase helps, the way `greedy_move()` takes the "
    "biggest capture. Each phase is tried with append and taken back with pop, like "
    "make and undo. Greedy gives one answer and never doubts it, so it names gold "
    "for a powder of silver.",
    ("phase_hunt.py", "search"): "Scores the set of phases it is given, keeps every "
    "set that ties for the best score, and calls itself on each set one phase "
    "larger, adding a phase with append and taking it back with pop. Phases go in "
    "library order only, so each set is scored once instead of once for every "
    "order, 176 sets instead of 821. Keeping every tied set lets the search say "
    "gold or silver when the pattern cannot tell them apart, as CrystalShift and "
    "Dara report every likely answer.",
    ("transposition_table.py", "probe"): "Looks up a position in the table and "
    "returns a stored score only when it answers this search: it was searched deep "
    "enough, and its bound fits the window. One position reached by two move orders "
    "is then searched once.",
    ("opening_book.py", "load_book"): "Reads the book file line by line, checks every "
    "SAN move with Remus's own rules, and stores the moves by position. A missing "
    "file or a typo only prints a note, so a bad book never stops Remus from playing.",
    ("search.py", "remember_killer"): "Keeps up to two quiet moves per ply that "
    "caused a cutoff. A move that refuted one position often refutes its neighbors, "
    "so trying it early saves work.",
    ("search.py", "search_later_move"): "Searches a later move with a null window "
    'first, which only answers "better or not?", and searches again with the full '
    "window only on a surprise. Most later moves are worse, so the cheap question "
    "is usually enough.",
    ("search.py", "is_draw_in_search"): "Says a position is a draw when it already "
    "appeared earlier in the game or the search, or when the fifty-move limit is "
    "reached. Then Remus aims for a repetition when losing and avoids one when "
    "winning.",
    ("evaluation.py", "pawn_structure"): "Counts doubled and isolated pawns as "
    "weaknesses and passed pawns as strengths, more the further they have gone. "
    "Pawns cannot move back, so their shape lasts the whole game.",
    ("evaluation.py", "mating_bonus"): "With a big lead and a weak opponent, rewards "
    "pushing the losing king to the edge and bringing the winning king close. "
    "Without it, Remus can be a queen up and still wander without mating.",
    ("search.py", "make_null_move"): "Passes the turn without moving a piece, and "
    "returns the en passant target so it can be put back. The opponent then moves "
    "twice in a row, and if Remus still scores at least beta, the opponent would "
    "never allow the position, so the search can stop early.",
    ("search.py", "undo_null_move"): "Takes the pass back: removes its history entry, "
    "gives the turn back, and restores the en passant target. Like every undo in "
    "Remus, it must restore the state exactly.",
    ("search.py", "reduction"): "Returns 1 for a late, quiet move that gives no "
    "check at depth 3 or more, and 0 otherwise. Late moves in a well-ordered list "
    "are rarely best, so a shallower look saves time, and a surprise earns a full "
    "search.",
    ("evaluation.py", "king_safety"): "Rewards each pawn that shelters the king on "
    "its own file or a neighbor, one or two squares ahead, while the enemy queen is "
    "on the board. A king without pawn cover is easy to attack.",
    ("transposition_table.py", "store"): (
        "Saves what one search learned about a position under its key: the depth, "
        "the score, whether that score is exact or only a bound, and the best move. "
        "A dict holds the table, so looking a position up again costs one step."
    ),
    ("test_upgrades.py", "test_transposition_table_bounds"): (
        "Proves the rules of `probe()` with three made-up entries before any real "
        'search uses them. A bound is the tricky part: "at least 80" settles a '
        "window whose beta is 70, but says nothing useful when beta is 100."
    ),
    ("opening_book.py", "book_move"): (
        "Looks the position up in the book and picks one of its moves at random, or "
        "returns None when the game has left the book. The random pick keeps Remus "
        "from playing the same opening every game."
    ),
    ("move_ordering.py", "order_moves"): (
        "Sorts the moves so captures come first by MVV-LVA, then this ply's killer "
        "moves, then every other move. The earlier a good move comes, the sooner "
        "alpha-beta cuts off the rest."
    ),
    ("test_upgrades.py", "test_killers_keep_two_quiet_moves"): (
        "Feeds three cutoff moves to `remember_killer()` and checks that only the "
        "two newest stay, newest first. Writing the expected list before running the "
        "test is how a student pair shows it understands the two slots."
    ),
    ("test_upgrades.py", "test_pvs_search_agrees_with_alpha_beta"): (
        "PVS must be a faster way to the same answer, never a different answer. The "
        "test searches one position with the Day 9 search and with PVS and compares "
        "the scores, and checks that the position is unchanged afterward."
    ),
    ("test_upgrades.py", "test_a_null_window_answers_only_better_or_not"): (
        "Shows what a null window really returns. With a window one point wide, the "
        "score only says whether the exact score is above alpha or not, so the test "
        "tries an alpha 50 below the exact score and one 50 above it. That yes-or-no "
        "answer is why PVS must search again when a move surprises it."
    ),
    ("test_upgrades.py", "test_draw_sense_search_agrees_with_alpha_beta"): (
        "In a position with no repetition, draw sense must change nothing, so the "
        "version search and the Day 9 search must find the same score."
    ),
    ("test_upgrades.py", "test_a_repeated_position_is_a_draw"): (
        "Plays Nf3 Nf6 Ng1 Ng8, which brings back the starting position, and checks "
        "that `is_draw_in_search()` says draw only after the knights come home."
    ),
    ("test_upgrades.py", "test_the_fifty_move_limit_is_a_draw"): (
        "Loads a FEN whose halfmove clock is 100 and checks that it counts as a "
        "draw. The FEN carries the clock, so no game needs to be played."
    ),
    ("test_upgrades.py", "test_null_move_and_undo_restore_the_state"): (
        "Makes a pass and takes it back, then compares the whole state with the "
        "start. A null move that leaves one thing changed, such as the en passant "
        "target, would corrupt every search after it."
    ),
    ("test_upgrades.py", "test_null_move_search_saves_work_and_keeps_the_state"): (
        "Counts positions: the null-move search must visit fewer than the Day 9 "
        "search at the same depth and leave the position unchanged. The count is "
        "the evidence that the pass saves work."
    ),
    ("test_upgrades.py", "test_only_late_quiet_moves_are_reduced"): (
        "Checks `reduction()` one condition at a time: a late quiet move is cut, "
        "and an early move, a move near the leaves, a capture, and a check are not."
    ),
    ("test_upgrades.py", "test_reduced_search_saves_work_and_keeps_the_state"): (
        "Counts positions: the reduced search must visit fewer than the Day 9 search "
        "at the same depth and leave the position unchanged."
    ),
}

# (day, period) -> paragraphs about the lab file, one per part the student pairs type
LAB_NOTES = {
    (1, 1): [
        (
            "Part #1 is already written. It prints the Python version and whether "
            "python-chess is installed, so the teacher can see at a glance that the "
            "laptop is ready."
        ),
        (
            "Part #2: you store your team name in a variable and print it inside an "
            "f-string. A variable is a name for a value, and an f-string puts values "
            "into text. Remus prints every result this way."
        ),
        (
            "Part #3: you store White's back rank as one string and print the letter at "
            "index 4, the king. Remus writes pieces as letters too, uppercase for White."
        ),
    ],
    (1, 2): [
        (
            'Part #1: you pick the file letter and the rank digit out of "e2" by index. '
            "Index 0 is the first character, the same counting Remus uses for rows and "
            "columns."
        ),
        (
            "Part #2: `ord()` turns a letter into its code number. Subtracting "
            '`ord("a")` makes file a number 0 and file e number 4, which is exactly how '
            "`parse_square()` finds a column on Day 1, period 4."
        ),
        (
            'Part #3: `chr()` goes the other way, so file number 6 becomes "g". Joining '
            'it with the rank gives "g7", the job of `square_name()`.'
        ),
        (
            "Part #4: `upper()` turns Black's pieces into White's, and `isupper()` tells "
            "the piece colors apart. Remus's `is_white()` on Day 2 is this one call."
        ),
    ],
    (1, 3): [
        (
            "Part #1: you count the pieces in a list with `len()` and read one by index. "
            "Index 3 is the d-file, where the queen starts."
        ),
        (
            "Part #2: a `for` loop with `range(8)` visits the eight files in order. Remus "
            "walks the board with loops like this everywhere."
        ),
        (
            "Part #3: you build the board as a list of eight rows, each a new list of "
            "eight dots, then put the pieces in. Row 0 is rank 8, so Black's pieces go in "
            "rows 0 and 1. This is the board `board.py` holds."
        ),
        (
            "Part #4: you play 1. e4 by changing two squares, then count the White pawns "
            "left on rank 2. `board[row][col]` is how every rule in Remus reads and "
            "changes the board."
        ),
    ],
    (2, 1): [
        (
            "Part #1 calls the finished `is_white()` and `on_board()`. You type the one "
            "line under each docstring: `is_white()` asks `isupper()`, and `on_board()` "
            "checks that the row and the column both lie between 0 and 7. Remus asks "
            "these two questions in nearly every function from Day 2 on."
        ),
        (
            "Part #2: you write `is_black()` from nothing: the `def` line with its type "
            "hints, the docstring, and the `return`. The type hints say what goes in "
            "and what comes out, so a reader knows how to call the function without "
            "reading its body."
        ),
        (
            "Part #3 packs e4 into the tuple `(4, 4)` and unpacks it with "
            "`row, col = square`. Every Remus square is a tuple like this one."
        ),
        (
            "Part #4 runs the two test functions, whose `assert` lines stop the program "
            "when a check fails. Running `run_tests.py` runs the same tests with pytest "
            "and prints a report, and breaking one test on purpose shows what a failure "
            "looks like before a real one happens."
        ),
    ],
    (2, 2): [
        (
            "Part #1 keeps the facts of a game in a dict and reads them by key, the way "
            "`new_game()` in `game_state.py` holds the board, the side to move, and the "
            "castling rights."
        ),
        (
            "Part #2 shows aliasing: `b2 = board` makes a second name for the same "
            "board, so a pawn put on e4 through `b2` shows up in `board` too. This is "
            "the most common surprise in a chess program that changes its board in place."
        ),
        (
            "Part #3 makes a real copy with `deepcopy()`, which copies every row. The "
            "copy changes alone, and `==` compares the two boards square by square."
        ),
        (
            "Part #4: you write a `dataclass` with two fields and print one of them. "
            "Remus's `Move` in `moves.py` is the same record with a third field for the "
            "promotion piece."
        ),
    ],
    (3, 1): [
        (
            "Part #1 counts to 3 with `while`, the loop that repeats as long as its test "
            "is true."
        ),
        (
            "Part #2 writes the direction up and to the right as the tuple `(-1, 1)`. "
            "The row step is -1 because row 0 is rank 8: moving toward Black's side "
            "makes the row smaller."
        ),
        (
            "Part #3 walks from d4 one square at a time with `while True` and leaves the "
            "loop with `break` at the edge of the board or at the first piece. The walk "
            "reaches e5, f6, and g7, where a Black pawn stops it. `slide()` on Day 3, "
            "period 3 is this same loop, and it returns moves instead of square names."
        ),
    ],
    (4, 1): [
        (
            "The lab imports `board.py`, `game_state.py`, `move_generation.py`, and "
            "`moves.py` from the same folder. An import runs the other file once and "
            "hands over its functions, so no code is copied."
        ),
        (
            "Part #1 prints `__name__`: the file that VS Code runs is `__main__`, and "
            "an imported file keeps its own name. That is why `board.py` prints its "
            "board when VS Code runs `board.py` and stays silent when the lab imports it, and "
            "why every Remus print sits inside `main()`."
        ),
        (
            "Part #2 calls `new_board()` and `knight_moves()` from the imported files "
            "and lists the two knight moves from g1. Part #3 runs "
            "`board.py` on its own in VS Code and shows its board, because there "
            "`board.py` is the file named `__main__`."
        ),
    ],
    (4, 4): [
        (
            "`demo_practice_positions.py` builds three positions from a dict of "
            "{square: piece} and prints each board with Remus's legal-move count. The "
            "student pair types each position and its prediction before running the file, so "
            "every count is a test of the student pair's own reasoning as well as of the code."
        ),
        (
            "Part #2 puts a rook check on the White king, and Part #3 adds a knight "
            "on e2 that blocks the check but cannot move: it is pinned. The loop at the "
            "end counts only the moves that start on e2, the same check as "
            "`test_pinned_knight_has_no_moves()`."
        ),
        (
            goals_board_image(
                "pin_check", "A Black rook on e8 checks the White king on e1"
            )
            + " "
            + goals_board_image(
                "pin_knight", "A White knight on e2 blocks the check and is pinned"
            )
            + "\n\n*Left, Part #2: the rook on e8 checks the king on e1 down the e-file. "
            "Right, Part #3: the knight on e2 blocks the check, so it is pinned to its "
            "king.*"
        ),
    ],
    (5, 1): [
        (
            "Part #1 adds squares to a set. A set holds each item once, so adding h1 a "
            "second time changes nothing."
        ),
        (
            "Parts #2 and #3 ask questions with `in`, of a set and of a dict. The dict "
            "`rights_lost` names the castling rights each home square guards: a piece "
            "leaving e1 removes K and Q, and a piece leaving h1 removes K."
        ),
        (
            "Part #4 removes rights with `replace()`, one letter at a time, starting from "
            '`"KQkq"`. `update_castling_rights()` in `make_move.py` does exactly this in '
            "period 2."
        ),
    ],
    (5, 4): [
        (
            "`demo_promotion.py` sets up a puzzle: White's pawn on b7 promotes on b8 next "
            "to the Black king on a6. The student pair writes the loop that tries all four "
            "promotion pieces, counts Black's legal replies, and names the result."
        ),
        (
            goals_board_image(
                "promotion_puzzle",
                "White king c6, bishop b6, and pawn b7 against the Black king on a6",
            )
            + "\n\n*The puzzle: White's king on c6, bishop on b6, and pawn on b7 against "
            "Black's king on a6. The pawn promotes on b8 (the green arrow).*"
        ),
        (
            "With no legal reply, `in_check()` decides between checkmate and stalemate. "
            "A queen, a rook, or a bishop takes away every square without giving check, "
            "so the game is a draw; only the knight on b8 gives check, and the king "
            "has nowhere to go. Every promotion is undone, and the snapshot at the end "
            "proves that the puzzle position comes back exactly."
        ),
    ],
    (6, 1): [
        (
            "Part #1: `countdown()` calls itself with a smaller number until it reaches "
            "the base case, 0. Without the base case the calls would never stop."
        ),
        (
            "Part #2: `count_leaves()` counts the moves at the bottom of a small tree "
            "made of lists. A move name is a leaf and counts 1, and a list adds up the "
            "counts of its branches."
        ),
        (
            "Part #3 is finished code to read and trace: `knight_paths()` counts the "
            "ways a knight can jump from a1. It has the same shape as `perft()` in "
            "period 2: at depth 0 return 1, otherwise add up the count under every move."
        ),
    ],
    (6, 4): [
        (
            "The lab cuts the start FEN into its six fields with `split()` and prints "
            "each with its name, the map the student pair needs before writing `fen.py`. Then "
            "`try` and `except ValueError` catch the error that `int()` raises on text "
            "that is not a number, which is how a FEN reader can reject a broken "
            "string instead of crashing."
        ),
    ],
    (7, 2): [
        (
            "Parts #1 and #2 pick moves the way the first brains in period 3 do: "
            "`random.choice()` takes any item, and a loop that keeps the best piece "
            "so far takes the item with the largest value."
        ),
        (
            "Parts #3 and #4 talk the way a UCI engine does. The program reads one "
            "command per line from `sys.stdin`, answers `isready` with `readyok`, and "
            "sends each answer at once with `flush=True`. Notes for people go to "
            "`sys.stderr`, where the GUI does not read them."
        ),
    ],
    (8, 2): [
        (
            "Part #1 sorts captures by the value of the piece they take: each new "
            "piece steps past every piece worth at least as much and is inserted "
            "there. `order_moves()` in period 4 sorts moves the same way."
        ),
        (
            "Part #2 starts the best value at minus infinity, so the first real value "
            "always replaces it. `alpha_beta()` starts its alpha the same way, below "
            "any score a move can get."
        ),
        (
            "Part #3 times `perft(3)` with `time.perf_counter()`, the clock that "
            "`compare_search.py` uses to show how much time alpha-beta saves."
        ),
    ],
    (9, 2): [
        (
            "Part #1: `remembered_perft()` stores each knight path count in a dict under "
            "the tuple key `(square, depth)`. The second call finds the answer and "
            "returns at once. "
            "Remus-RED's transposition table remembers search results the same way."
        ),
        (
            "Parts #2 and #3 use `math.dist()` for the straight-line distance from d4 "
            "to g7, which Remus-CYAN needs, and `random.seed()`, which makes a "
            "random choice repeat on every run."
        ),
    ],
    (9, 4): [
        (
            "Parts #1 and #2 of `demo_results.py` turn a match result into a score and "
            "an Elo gap, then into a range that holds the true gap 95 times out of "
            "100. When the range includes 0, the match has not shown that the "
            "enhancement helped, and more games are needed. Each student pair puts in its own "
            "two battle games, then its engine's league games from the designer's "
            "table, and compares the two ranges."
        ),
    ],
}

# The syllabus at the top of each Day folder ("Day NN Syllabus.md"): what the day is about, its
# objectives, the timed steps of each period, and the checkpoint at 4:30.
# Each step is (minutes after the period starts, what happens), and a step lasts
# until the next one starts.
DAY_GUIDES = {
    1: {
        "theme": "Setup and the board",
        "summary": (
            "Day 1 forms the student pairs, sets up the laptops, and teaches the first Python: "
            "strings and lists. In the last period each student pair writes its first Remus "
            "code. By 4:30 Remus prints its own board, converts a square name such as "
            "e2 into a (row, col) pair and back, and draws the board as a picture."
        ),
        "objectives": [
            (
                "Open a Python file in VS Code, run it with the Run Python File "
                "button, and read what it prints."
            ),
            (
                "Turn a square name such as e2 into numbers with indexing, `ord()`, "
                "and `chr()`, and print the answer in an f-string."
            ),
            (
                "Build an 8x8 board as a list of rows and read one square with "
                "`board[row][col]`."
            ),
            "Say where each rank lives: row 0 is rank 8, and column 0 is file a.",
            "Write the first four Remus functions in `board.py`.",
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Welcome. The finished Remus plays a game in Lucas Chess on "
                        "the projector."
                    ),
                ),
                (
                    10,
                    (
                        "The story of the name: Sargon, the 1978 chess program, and "
                        "Rimush, the first son of Sargon of Akkad. Remus is a son of "
                        "Sargon."
                    ),
                ),
                (
                    20,
                    (
                        "Form the ten student pairs. The driver types and the navigator reads "
                        "and checks; the two swap roles every period. Each student pair picks "
                        "a team name for `CONTRIBUTORS.md`."
                    ),
                ),
                (
                    30,
                    (
                        "Setup, the only git and uv commands of the workshop. The "
                        "teacher walks each student through installing git and uv, "
                        "cloning the Remus repository, and running `uv sync` once to build "
                        "the `.venv` folder. From here on every step runs from VS "
                        "Code's Run button."
                    ),
                ),
                (
                    50,
                    (
                        "Notation on the demonstration board: square names, SAN for "
                        "people (`Nf3`, `Bxh8`, `e8=Q`), and UCI for programs "
                        "(`g1f3`)."
                    ),
                ),
                (
                    60,
                    (
                        "Student pairs type the 6 lines of `python_setup.py` and run it. It "
                        "checks the laptop, greets the team, and prints a first chess "
                        "line. The teacher and the assistant check that every laptop "
                        "runs a file with the Run button and opens Lucas Chess."
                    ),
                ),
                (
                    80,
                    (
                        "Exit ticket: each student lists three of the five parts of a "
                        "chess engine (board, moves, rules, search, evaluation) and "
                        "one job of each."
                    ),
                ),
            ],
            2: [
                (
                    0,
                    (
                        "Slides: a script, `print()`, variables, and strings indexed "
                        "from 0."
                    ),
                ),
                (
                    15,
                    (
                        "The teacher shows `ord()` and `chr()` on the projector: the "
                        "letter e is file number 4 because a is 0."
                    ),
                ),
                (
                    25,
                    (
                        "Student pairs work through the four parts of `python_strings.py`, "
                        "running the file after each part."
                    ),
                ),
                (
                    70,
                    (
                        "Check together without running code: what is the file number "
                        "of h4, and of a1? Why does file a count as 0?"
                    ),
                ),
                (
                    80,
                    "Student pairs compare their printouts with the student pair next to them.",
                ),
            ],
            3: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Call the square": the teacher calls (6,'
                        " 4), the navigator puts a token on the printed board, and the"
                        " driver names the square, e2. Then the partners swap."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: lists, `for` and `range()`, `len()`, and a list of "
                        "lists."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs work through the four parts of `python_lists.py`: a "
                        "list of pieces, a loop over every square, the board as a list"
                        " of rows, and the pawns in a row."
                    ),
                ),
                (
                    75,
                    (
                        "Without running code, each student pair names `board[4][4]` (e4) and "
                        "says why row 0 is rank 8."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Slides: the Remus board is an 8x8 list of one-character "
                        "strings. Uppercase is White, lowercase is Black, and `.` is "
                        "empty. The teacher walks through `new_board()`."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `print_board()`, `square_name()`, "
                        "`parse_square()`, and `piece_at()` in `board.py` and run "
                        "`run_tests.py` after each one."
                    ),
                ),
                (
                    60,
                    (
                        "Student pairs run `show_board.py`, which draws their board as a "
                        "picture in the web browser."
                    ),
                ),
                (
                    70,
                    (
                        "Show and choose: two or three student pairs show their "
                        "`parse_square()` on the projector, the class picks one for "
                        "clarity, and the teacher adds the student pair's team name to "
                        "`CONTRIBUTORS.md`."
                    ),
                ),
                (
                    85,
                    (
                        "Checkpoint: running `board.py` prints the start board and "
                        '"b1 holds N, expected N".'
                    ),
                ),
            ],
        },
        "checkpoint": (
            'Running `board.py` prints the start board and "b1 holds N, expected N",'
            " and `test_board.py` passes."
        ),
    },
    2: {
        "theme": "Functions and records",
        "summary": (
            "Day 2 teaches functions, tests, dicts, and dataclasses, then uses them "
            "for the heart of every chess engine: making a move and taking it back "
            "exactly. By 4:30 Remus holds a whole game state, and ten moves made and "
            "undone return the exact start state."
        ),
        "objectives": [
            (
                "Write a function with type hints and a docstring, and check it with "
                "`assert` and pytest."
            ),
            (
                "Store named facts in a dict and a dataclass, and show why `b2 = "
                "board` gives one board two names instead of making a copy."
            ),
            (
                "Name the parts of a game state: the board, the side to move, castling"
                " rights, the en passant square, the two clocks, and the history."
            ),
            "Turn a move into UCI text such as `e2e4` and back.",
            "Make a move, record everything it destroys, and undo it exactly.",
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Slides: functions, parameters, `return`, type hints, and "
                        "docstrings."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs work through Parts #1 to #3 of `python_functions.py`: "
                        "call a function, write their own, and unpack a square tuple "
                        "such as `row, col = (6, 4)`."
                    ),
                ),
                (
                    55,
                    (
                        "Slides: `assert` and pytest. A slide shows a function with a "
                        "mistake in it, and the class reads the failing test together."
                    ),
                ),
                (
                    65,
                    (
                        "Student pairs finish Part #4, which checks their functions with "
                        "`assert`."
                    ),
                ),
                (
                    80,
                    (
                        "Wrap-up: each student pair says what a failing test tells them and "
                        "where to look first."
                    ),
                ),
            ],
            2: [
                (
                    0,
                    (
                        "Slides: a dict holds named facts, and a dataclass describes a"
                        " record with fixed fields."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs work through Parts #1 and #2 of `python_dicts.py` and "
                        "watch `b2 = board` change both boards."
                    ),
                ),
                (
                    45,
                    (
                        "The teacher explains aliasing on the whiteboard: two names, "
                        "one list. Then student pairs write Parts #3 and #4: a real copy, and "
                        "a dataclass that describes a move."
                    ),
                ),
                (
                    80,
                    (
                        "Wrap-up: why would a chess engine break if it changed a board"
                        " it meant to copy?"
                    ),
                ),
            ],
            3: [
                (
                    0,
                    (
                        "Slides: the game state dict in `new_game()` and the `Move` "
                        "dataclass with `from_square`, `to_square`, and `promotion`."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `is_white()` and `color_of()` in `game_state.py`,"
                        " then `move_to_uci()` and `move_from_uci()` in `moves.py`, "
                        "running `run_tests.py` after each."
                    ),
                ),
                (
                    65,
                    (
                        "Student pairs run `game_state.py` and `moves.py` and compare the "
                        "printouts with the expected answers."
                    ),
                ),
                (
                    75,
                    (
                        "Show and choose: the class picks one `move_from_uci()`, and the "
                        "teacher adds its student pair's team name to `CONTRIBUTORS.md`."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Undo from the card": one partner makes '
                        "three moves with sticky-note pieces and writes an undo card "
                        "for each. The other partner restores the start position from "
                        "the cards alone."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: what a move destroys (the captured piece, the clocks,"
                        " the side to move) and the undo record that saves it. The "
                        'teacher shows `state_snapshot()` and the "make ten, undo '
                        'ten, compare" test.'
                    ),
                ),
                (
                    25,
                    (
                        "Student pairs write `make_move()` and `undo_move()` in `make_move.py`"
                        " until the tests pass."
                    ),
                ),
                (
                    75,
                    (
                        "Show and choose for `make_move()`, then the checkpoint: ten "
                        "moves made and undone give back the exact start state."
                    ),
                ),
            ],
        },
        "checkpoint": (
            "Ten moves made and undone return the exact start state, and "
            "`test_make_move.py` passes."
        ),
    },
    3: {
        "theme": "Loops that walk the board",
        "summary": (
            "Day 3 teaches loops that walk across the board, then uses them to "
            "generate the moves of every piece. By 4:30 Remus finds the 20 moves of "
            "the start position, and `show_board.py` draws an arrow for every move the"
            " student pairs' code finds."
        ),
        "objectives": [
            "Repeat steps with `while`, and stop early with `break`.",
            (
                "Store a direction as a (row step, column step) tuple and walk it to "
                "the edge of the board or to the first piece."
            ),
            "Generate knight and king moves from a list of jumps.",
            "Generate rook, bishop, and queen moves by sliding in each direction.",
            "Generate pawn pushes, including the double step from the start rank.",
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Slides: `while`, `break`, `continue`, and a list of direction"
                        " tuples."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs work through the four parts of `python_loops.py`: "
                        "repeat with `while`, store a direction, walk from d4 until "
                        "the edge or a piece, and try another direction."
                    ),
                ),
                (
                    65,
                    (
                        "The teacher runs the walk on the projector with a piece in "
                        "the way and the class predicts where it stops."
                    ),
                ),
                (
                    80,
                    (
                        "Wrap-up: which loop stops at the edge, and which line stops "
                        "it at a piece?"
                    ),
                ),
            ],
            2: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Shade the reach": student pairs shade every '
                        "square a knight on d4, a knight on a1, and a bishop on c1 can"
                        " reach, and compare counts with the next student pair (8, 2, and 7)."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: an offset list for the knight. The teacher shows the "
                        "given `knight_moves()` on the projector."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs write `king_moves()` the same way and "
                        "pass the jumping-piece tests: a knight on a1 has 2 moves and "
                        "a king on a1 has 3."
                    ),
                ),
                (
                    50,
                    (
                        "Student pairs run `show_board.py`, which draws an arrow for every "
                        "move their generator returns, and count the arrows."
                    ),
                ),
                (
                    70,
                    (
                        "Student pairs try their own squares, such as a king in a corner, and "
                        "predict the arrows before they run the file."
                    ),
                ),
            ],
            3: [
                (
                    0,
                    (
                        "Slides: a sliding piece walks one direction until the edge or"
                        " the first piece, and captures that piece only if it is an "
                        "enemy."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `slide()` in `move_generation.py`. The given "
                        "`slider_moves()` calls it with the rook, bishop, and queen "
                        "directions."
                    ),
                ),
                (
                    60,
                    (
                        "Exercise: a rook on an empty board has 14 moves. Student pairs check "
                        "it with the tests and the arrow picture."
                    ),
                ),
                (
                    75,
                    "Show and choose for `slide()`.",
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Slides: pawns move forward toward row 0 for White, push one "
                        "or two squares, and capture diagonally. The given code holds "
                        "the captures and the four promotion choices."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `pawn_pushes()`: the single step and the double "
                        "step from the start rank."
                    ),
                ),
                (
                    55,
                    (
                        "Student pairs run the tests and the arrow picture on the start "
                        "position."
                    ),
                ),
                (
                    75,
                    (
                        "Checkpoint: `pseudo_legal_moves()` finds 20 moves from the "
                        "start."
                    ),
                ),
            ],
        },
        "checkpoint": (
            "`pseudo_legal_moves()` returns 20 moves from the start position."
        ),
    },
    4: {
        "theme": "Legal moves",
        "summary": (
            "Day 4 teaches modules and imports, then the rule that makes a move legal: the"
            " mover's own king must be safe after it. By 4:30 Remus finds attacks and "
            "check, and keeps only the legal moves, so a pinned knight has no moves "
            "and a king in check has only escapes."
        ),
        "objectives": [
            (
                "Import functions from another file, and explain why every Remus file "
                "keeps its prints inside `main()`."
            ),
            (
                "Draw a map of which Remus files import which, and name the file "
                "that runs."
            ),
            ("Decide whether a square is attacked by looking outward from the square."),
            "Keep only legal moves: make each move, test the king, and undo it.",
            (
                "Predict the legal moves of a position, then check the prediction with"
                " Remus."
            ),
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Slides: a module is a file, `import` reads it, and `if "
                        '__name__ == "__main__"` keeps a file quiet when another '
                        "file imports it."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs work through Parts #1 to #3 of `python_modules.py`: "
                        "every file has a `__name__`, use yesterday's `board.py` and "
                        "`move_generation.py`, and list the knight moves from g1."
                    ),
                ),
                (
                    50,
                    (
                        "Unplugged: the import map. On paper, each student pair writes the "
                        "name of every `.py` file in the folder and draws an arrow "
                        "from each file to every file it imports, then circles the "
                        "file that runs as `__main__`."
                    ),
                ),
                (
                    65,
                    (
                        "Two student pairs show their maps on the projector. The teacher "
                        "shows that every arrow stays inside the folder: each period "
                        "folder holds a complete Remus, so its files import only "
                        "each other."
                    ),
                ),
                (
                    80,
                    (
                        "Every student pair shows its map to the teacher or the assistant."
                    ),
                ),
            ],
            2: [
                (
                    0,
                    (
                        "Chess refresher on the demonstration board: check, pins, and "
                        "discovered check."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: a square is attacked if a piece could capture there. "
                        'Stand on the square and look outward like a "super piece". '
                        "The given code holds `attacked_by_knight()` and the "
                        "sliding-line part."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs write `piece_at_offsets()`, then `attacked_by_pawn()` "
                        "and `attacked_by_king()` on top of it."
                    ),
                ),
                (
                    70,
                    "Student pairs run the attack tests and the file's self-check.",
                ),
                (
                    80,
                    "Show and choose for `piece_at_offsets()`.",
                ),
            ],
            3: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Pin hunt": on four printed positions, '
                        "student pairs cross out every move that leaves the mover's king "
                        "attacked."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: a move is legal only if the mover's king is safe "
                        "after the move. Make it, test the king, undo it."
                    ),
                ),
                (
                    25,
                    (
                        "Student pairs write `in_check()` and `legal_moves()` until the tests "
                        "pass."
                    ),
                ),
                (
                    65,
                    "Student pairs compare Remus's answers with their pin hunt worksheets.",
                ),
                (
                    75,
                    "Show and choose for `legal_moves()`.",
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Slides: the workshop's first three verification positions: "
                        "the start, a king in check, and a pinned knight."
                    ),
                ),
                (
                    10,
                    (
                        "In `demo_practice_positions.py` student pairs type each position and "
                        "write their prediction of its legal move count before Remus "
                        "counts."
                    ),
                ),
                (
                    50,
                    (
                        "Part #4: each student pair builds a position of its own and trades it"
                        " with the next student pair, who predict before they run it."
                    ),
                ),
                (
                    75,
                    (
                        "Checkpoint: a pinned knight has zero legal moves, and a king "
                        "in check has only escapes."
                    ),
                ),
            ],
        },
        "checkpoint": (
            "A pinned knight has zero legal moves, a king in check has only escapes, "
            "and `test_legal_moves.py` passes."
        ),
    },
    5: {
        "theme": "Special moves",
        "summary": (
            "Day 5 adds the rare rules: castling, en passant, the double step, and "
            "promotion and underpromotion, each with an exact undo. It closes the "
            "first week with a payoff: by 4:30 every student pair plays its own Remus in Lucas"
            " Chess, where Remus answers with random legal moves."
        ),
        "objectives": [
            (
                "Use a set, `in`, a dict lookup, and `replace()` on the castling "
                'rights string `"KQkq"`.'
            ),
            (
                "State the five conditions for castling, and say which moves take away"
                " each castling right."
            ),
            (
                "Explain why the pawn an en passant capture removes is not on the "
                "square the capturing pawn lands on."
            ),
            (
                "Show that a knight promotion can win where a queen promotion "
                "stalemates."
            ),
            "Register Remus in Lucas Chess and play a game against it.",
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Slides: a set holds each item once, `in` asks a yes-or-no "
                        "question, and a dict looks up a value by its key."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs work through the four parts of `python_sets.py`, ending"
                        ' with `replace()` removing "K" from "KQkq" when the h1 '
                        "rook moves."
                    ),
                ),
                (
                    65,
                    (
                        "The class lists, on the board, every move that removes a "
                        "castling right."
                    ),
                ),
                (
                    80,
                    "Wrap-up and a preview of castling.",
                ),
            ],
            2: [
                (
                    0,
                    (
                        "Chess refresher on the demonstration board: the five castling"
                        " conditions. The rook may cross an attacked square (b1), and "
                        "a rook captured on its home square removes that right."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: the given castling generation and the "
                        "attacked-square checks."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs write `update_castling_rights()`, the table of which "
                        "moves remove K, Q, k, or q."
                    ),
                ),
                (
                    50,
                    (
                        "Student pairs run the castling tests and build one castling position "
                        "of their own to test."
                    ),
                ),
                (
                    80,
                    "Show and choose for `update_castling_rights()`.",
                ),
            ],
            3: [
                (
                    0,
                    (
                        "Chess refresher: en passant is allowed only on the very next "
                        "move after a two-square push, and the captured pawn is not on"
                        " the destination square."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: the double step sets the en passant target. The "
                        "teacher walks through the en passant make and undo."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs write `en_passant_victim_square()`, "
                        "then trace a capture and its undo on the printed board."
                    ),
                ),
                (
                    55,
                    (
                        "Student pairs run the en passant tests, including the rare capture "
                        "that exposes the king along the rank."
                    ),
                ),
                (
                    80,
                    (
                        "Wrap-up: which square does the undo put the captured pawn "
                        "back on?"
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Puzzle on the demonstration board: promoting to a knight "
                        "wins, and promoting to a queen stalemates. The teacher shows "
                        "promotion in `make_move()` and `undo_move()`."
                    ),
                ),
                (
                    15,
                    (
                        "In `demo_promotion.py` student pairs write the loop that tries all "
                        "four promotions and prints stalemate or checkmate for each."
                    ),
                ),
                (
                    45,
                    (
                        "The teacher hands out `uci_engine.py` and `remus.bat`. Student pairs "
                        "register `remus.bat` from the period's `student` folder in Lucas Chess, "
                        "following the [Lucas Chess guide](../misc/students/lucas_chess_guide.md)."
                    ),
                ),
                (
                    60,
                    (
                        "Student pairs play their own Remus, which answers with random legal "
                        "moves. Every special move works on a real board."
                    ),
                ),
                (
                    85,
                    "Checkpoint: every special-move test passes.",
                ),
            ],
        },
        "checkpoint": (
            "Every special-move test passes, every special move undoes exactly, and "
            "Remus plays random legal moves in Lucas Chess."
        ),
    },
    6: {
        "theme": "Counting the tree, and FEN",
        "summary": (
            "Day 6 teaches recursion and uses it to count every position the rules "
            "allow, a check called perft. Matching the counts of trusted chess "
            "programs proves the rules are right. By 4:30 perft matches the reference "
            "counts and Remus reads and writes positions as FEN text."
        ),
        "objectives": [
            "Write a recursive function with a base case and a recursive case.",
            (
                "Count the positions of the move tree to a fixed depth with `perft()`:"
                " 20, 400, and 8,902 from the start."
            ),
            (
                "Find a broken rule by comparing counts under each root move with "
                "python-chess."
            ),
            (
                "Read a FEN string with `split()` and `int()`, and catch a bad field "
                "with `try` and `ValueError`."
            ),
            "Turn a board into the placement part of FEN and back.",
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Slides: a function that calls itself, its base case, and the "
                        "call stack."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs work through the three parts of `python_recursion.py`: "
                        "count down, count the leaves of a small tree, and count the "
                        "paths of a knight."
                    ),
                ),
                (
                    65,
                    (
                        "The teacher draws the call stack of a short count on the "
                        "whiteboard while the class traces it."
                    ),
                ),
                (
                    80,
                    "Wrap-up: what stops a recursion?",
                ),
            ],
            2: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Count by hand": in a king and pawn '
                        "against king position, student pairs list every move two plies deep "
                        "on index cards and count the leaves."
                    ),
                ),
                (
                    15,
                    "Slides: perft counts the leaves of the legal move tree.",
                ),
                (
                    25,
                    (
                        "Student pairs write `perft()` and run it on the warm-up position to "
                        "check their cards."
                    ),
                ),
                (
                    55,
                    (
                        "Student pairs run `perft.py` from the start: 20, 400, and 8,902. The "
                        "teacher shows `divide()`, which prints the count under each "
                        "root move."
                    ),
                ),
                (
                    80,
                    "Show and choose for `perft()`.",
                ),
            ],
            3: [
                (
                    0,
                    (
                        "Slides: `test_perft.py` compares Remus with python-chess on "
                        "the standard positions."
                    ),
                ),
                (
                    15,
                    (
                        "Bug hunt: the `bug_hunt` folder holds a copy of Remus with "
                        "three planted bugs. Student pairs run `hunt.py` there and race to "
                        "find each bug from the root moves whose counts disagree."
                    ),
                ),
                (
                    70,
                    "Student pairs explain each bug they found and the rule it broke.",
                ),
                (
                    85,
                    (
                        "Wrap-up: the hunt is over when `hunt.py` prints 0 root moves "
                        "that disagree."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Slides: the six fields of FEN, `split()`, `int()`, and "
                        "`ValueError`."
                    ),
                ),
                (
                    10,
                    "Student pairs work through `python_fen_fields.py`.",
                ),
                (
                    30,
                    (
                        "Student pairs write `fen_placement()` and `board_from_placement()` in"
                        " `fen.py`. The given code holds the other five fields."
                    ),
                ),
                (
                    80,
                    (
                        "Checkpoint: every test position loads from FEN and perft "
                        "matches the reference."
                    ),
                ),
            ],
        },
        "checkpoint": (
            "Perft matches the reference at depth 3 for the start and the standard "
            "positions, and every test position loads from FEN. The rules are "
            "verified, so the search can begin."
        ),
    },
    7: {
        "theme": "A whole game, and judging a position",
        "summary": (
            "Day 7 turns the rules into a whole game. Remus learns when a game ends, "
            "reads moves in standard notation, plays its first moves with a plan, and "
            "scores a position. By 4:30 a full game in Lucas Chess ends with the right"
            ' result and reason. This is the "legal moves" milestone: from here on, '
            "the work is about good moves."
        ),
        "objectives": [
            (
                "Name every way a game ends: checkmate, stalemate, threefold "
                "repetition, the fifty-move rule, and insufficient material."
            ),
            (
                "Read a move a player types in SAN by matching it against the legal "
                "moves."
            ),
            (
                "Pick a random move, and pick the biggest capture with a loop that "
                "keeps the best so far."
            ),
            "Explain how Remus and Lucas Chess talk over UCI.",
            (
                "Score a position by its material in centipawns, and read the "
                "piece-square tables."
            ),
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Chess refresher: stalemate, repetition, the fifty and 75-move"
                        " rules, and insufficient material, with a six-position quiz."
                    ),
                ),
                (
                    20,
                    (
                        "Slides: the halfmove clock and `position_key()`, both in the "
                        "given code."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs write `insufficient_material()` and `game_result()` in "
                        "`game_end.py`."
                    ),
                ),
                (
                    75,
                    (
                        "Student pairs check their answers on the quiz positions, then show "
                        "and choose."
                    ),
                ),
            ],
            2: [
                (
                    0,
                    (
                        "Slides: SAN. The teacher walks through `move_to_san()`, "
                        "including `Nbd2` and the `+` and `#` endings."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `parse_san()`: build the SAN of every legal move "
                        "and return the one that matches."
                    ),
                ),
                (
                    35,
                    (
                        "Student pairs run `notation.py`, then change its position and "
                        "check that `parse_san()` reads each SAN move it prints."
                    ),
                ),
                (
                    50,
                    (
                        "Student pairs work through `python_input_output.py`: "
                        "`random.choice()`, a loop that keeps the best so far, stderr,"
                        " and a tiny program that answers `isready` with `readyok`."
                    ),
                ),
            ],
            3: [
                (
                    0,
                    (
                        "Slides: a brain is a function that picks a move. Random picks"
                        " any legal move, and greedy takes the most valuable capture."
                    ),
                ),
                (
                    10,
                    "Student pairs write `random_move()` and `greedy_move()`.",
                ),
                (
                    40,
                    (
                        "The class reads the Day 5 `uci_engine.py` line by line, then the "
                        "given version in this folder, which adds FEN positions and a "
                        "choice of brains."
                    ),
                ),
                (
                    60,
                    (
                        "Student pairs register `remus.bat` from the `student` folder in Lucas Chess "
                        "again and play greedy Remus."
                    ),
                ),
                (
                    75,
                    (
                        "Student pairs run `play_match.py`: random Remus against greedy Remus "
                        "for 20 games, with the score at the end."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Student pairs rank three printed positions and write one reason for "
                        "each. The reasons become the evaluation terms."
                    ),
                ),
                (
                    15,
                    (
                        "Chess refresher: piece values (pawn 1, knight 3, bishop 3, "
                        "rook 5, queen 9) and the fork, pin, and skewer."
                    ),
                ),
                (
                    25,
                    "Student pairs write `material()` in centipawns, scored for White.",
                ),
                (
                    50,
                    (
                        "The teacher shows the piece-square tables and "
                        "`explain_evaluation()`, which prints every term. A knight on "
                        "d4 attacks eight squares; on a1 it attacks two."
                    ),
                ),
                (
                    65,
                    (
                        "Each student pair proposes one change to one table, and the class "
                        "votes."
                    ),
                ),
                (
                    85,
                    "Checkpoint: `explain_evaluation()` gives 0 for the start.",
                ),
            ],
        },
        "checkpoint": (
            "A full game in Lucas Chess ends with the correct result and reason, and "
            "`explain_evaluation()` gives 0 for the start position."
        ),
    },
    8: {
        "theme": "Searching ahead, then smarter",
        "summary": (
            "Day 8 teaches Remus to look ahead. It starts with minimax, folds it into "
            "negamax, prunes it with alpha-beta, keeps capturing past the horizon with"
            " quiescence, and tries the best captures first. By 4:30 Remus finds every"
            " mate in 1 and every puzzle mate in 2."
        ),
        "objectives": [
            "Back up scores through a game tree by hand, the way minimax does.",
            (
                "Write negamax: one function that flips the sign of each reply's score"
                " and prefers the faster mate."
            ),
            (
                "Explain an alpha-beta cutoff, and show that alpha-beta gives the same"
                " score with fewer nodes."
            ),
            (
                "Explain the horizon effect, and stop it with a quiescence search that"
                " may stand pat."
            ),
            (
                "Order captures by most valuable victim, least valuable attacker, and "
                "measure the nodes it saves."
            ),
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Paper minimax": student pairs back up max and '
                        "min on a printed two-ply tree and circle the best move. A "
                        "seven-student human tree can act it out at the front of the "
                        "room."
                    ),
                ),
                (
                    15,
                    (
                        "The given code holds `minimax()` to depth 2 with a node "
                        "counter, and student pairs compare its answer with their worksheets."
                    ),
                ),
                (
                    30,
                    (
                        "Slides: negamax, the same search in one function: flip the "
                        "sign, wrap make and undo in `try/finally`, and score "
                        "checkmate as `-(MATE_SCORE - ply)`."
                    ),
                ),
                (
                    40,
                    (
                        "Student pairs write `negamax()` until the tests show it agrees with "
                        "minimax and leaves the root state unchanged."
                    ),
                ),
                (
                    80,
                    "Show and choose for `negamax()`.",
                ),
            ],
            2: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Fewest flips": the same tree as '
                        "face-down cards. Student pairs turn a card only when the answer could"
                        " still change."
                    ),
                ),
                (
                    15,
                    "Slides: alpha and beta, and the cutoff.",
                ),
                (
                    25,
                    (
                        "Student pairs write `alpha_beta()` beside `negamax()` and run "
                        "`compare_search.py`: the same score, fewer nodes."
                    ),
                ),
                (
                    55,
                    (
                        "Student pairs work through `python_sorting.py`: `insert()` puts the "
                        'biggest victim first, `float("inf")`, and timing a perft '
                        "run."
                    ),
                ),
            ],
            3: [
                (
                    0,
                    (
                        "Puzzle: at depth 2 Remus takes a defended pawn with its "
                        "queen. Why? The class names the horizon effect."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: quiescence keeps searching captures until the "
                        "position is quiet. The given code holds `capture_moves()`."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs write `quiescence()`, which may stand pat with the "
                        "evaluation or try a capture that does better."
                    ),
                ),
                (
                    70,
                    "Student pairs run the puzzle again: Remus keeps its queen.",
                ),
                (
                    80,
                    "Show and choose for `quiescence()`.",
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Slides: alpha-beta cuts more when the best move comes first. "
                        "Most valuable victim, least valuable attacker (MVV-LVA)."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `mvv_lva_score()`. The given code holds "
                        "`order_moves()` and the check extension."
                    ),
                ),
                (
                    40,
                    (
                        "Student pairs measure node counts before and after ordering with "
                        "`compare_search.py`."
                    ),
                ),
                (
                    65,
                    "Student pairs run the mate puzzles.",
                ),
                (
                    80,
                    "Checkpoint: every mate in 1 and every puzzle mate in 2.",
                ),
            ],
        },
        "checkpoint": (
            "Remus finds every mate in 1 and every puzzle mate in 2, and alpha-beta "
            "returns the same score as negamax with fewer nodes."
        ),
    },
    9: {
        "theme": "The clock and the enhanced engines",
        "summary": (
            "Day 9 gives Remus a clock, then splits the class into ten enhancement "
            "enhanced engines. Each student pair adds one idea to the same engine, Remus-WHITE, and "
            "tests it. In period 4 the student pairs carry their enhanced engines to each other's laptops "
            "on USB sticks and battle. By 4:30 every enhanced engine passes its tests and "
            "has played two battles."
        ),
        "objectives": [
            (
                "Search deeper one step at a time and keep the best move of the "
                "deepest search that finished before time ran out."
            ),
            (
                "Read the `info` lines Remus sends to Lucas Chess: depth, score, "
                "nodes, and the principal variation."
            ),
            "Use a dict as a cache with a tuple as its key.",
            (
                "Add one enhancement to Remus-WHITE, test it, and say what it should "
                "change in a game."
            ),
            (
                "Play two enhanced engines against each other, and read the result "
                "with its uncertainty."
            ),
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        "Slides: the clock. The teacher reads `go movetime`, `wtime`, "
                        "and `btime`, turns them into a thinking time, and writes "
                        "`format_info()`."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `think()` (the iterative deepening loop): depth "
                        "1, then 2, then 3, keeping the best move of the deepest "
                        "search that finished."
                    ),
                ),
                (
                    55,
                    (
                        "Show and choose for `think()`. The chosen code makes "
                        "Remus-WHITE, the Remus with none of the enhancements and the "
                        "starting point of every enhanced engine."
                    ),
                ),
                (
                    65,
                    (
                        "The class watches Remus-WHITE play a 5-minute game against "
                        "Stockfish at 1500 Elo in Lucas Chess and reads the `info` "
                        "lines as it thinks."
                    ),
                ),
            ],
            2: [
                (
                    0,
                    (
                        "Student pairs work through `python_caches.py`: a dict remembers "
                        "answers, `math.dist()`, and `random.seed()`."
                    ),
                ),
                (
                    20,
                    (
                        "Slides: the ten enhanced engines. Each one is the period 1 "
                        "Remus with one enhancement added, such as RED (transposition table) or BLUE "
                        "(killer moves). The folder names use colors so that no engine "
                        "sounds better than another."
                    ),
                ),
                (
                    30,
                    (
                        "Each student pair opens its enhanced engine in `engines/student`, "
                        "reads the version README, and writes the enhanced engine's stubbed "
                        "code."
                    ),
                ),
            ],
            3: [
                (
                    0,
                    (
                        "Student pairs finish their engine enhancement, then open "
                        "`run_tests.py` in their engine folder in "
                        "`engines/student` and press Run until every test "
                        "passes. The table above links each engine folder."
                    ),
                ),
                (
                    40,
                    (
                        "Each student pair opens `basic_test.py` in its engine folder and "
                        "presses Run in VS Code: one 2-minute game against "
                        "Remus-WHITE, which checks only that the engine plays legal "
                        "moves to the end."
                    ),
                ),
                (
                    70,
                    (
                        "Each student pair writes one sentence on the board: what its "
                        "enhancement should change, and how the class will see it."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Slides: how a battle works. Each student pair copies its "
                        "finished engine folder, such as `engines/student/10 Remus-RED - "
                        "Transposition table`, onto its USB stick. The teacher posts the "
                        "pairings for two rounds; in each round five student pairs host and "
                        "five visit."
                    ),
                ),
                (
                    10,
                    (
                        "Round 1. The visiting student pair pastes its engine folder "
                        "into the same path on the host laptop, `engines/student`, "
                        "and replaces the folder of the same name. The host opens `play_battle.py` in its own "
                        "engine folder, sets `VISITING_ENGINE` to the visitor's engine "
                        "color, and presses Run in VS Code. Two 10-minute games run side by side, one with "
                        "each piece color. Each student pair writes the score on the board."
                    ),
                ),
                (
                    40,
                    "Round 2: the student pairs that visited now host, against new opponents.",
                ),
                (
                    45,
                    (
                        "While the round 2 games run, each student pair turns its round 1 "
                        "result into an Elo gap with a margin of error in "
                        "`demo_results.py`, then tries its engine's league games."
                    ),
                ),
                (
                    70,
                    (
                        "The class reads the board: which engines won, and why two "
                        "games prove little. The teacher shows the league table, 110 "
                        "games for each engine, and compares."
                    ),
                ),
                (
                    85,
                    (
                        "Each visiting student pair takes its USB stick back. The visitor's "
                        "folder stays on the host laptop in place of an engine the host "
                        "student pair never writes, so the host's own engine folder is "
                        "untouched."
                    ),
                ),
            ],
        },
        "checkpoint": (
            "Every enhanced engine passes its tests and its one-game test match, and "
            "has played two battles against other enhanced engines."
        ),
    },
    10: {
        "theme": "Solve a science problem using chess AI",
        "summary": (
            "Day 10 aims the engine's ideas at real science. The same generate, score,"
            " and choose loop picks where to measure a hidden peak, and the full tree "
            "search, with make and undo, names the crystal phases in an X-ray powder "
            "pattern. The day ends with each student pair reporting its science results, and "
            "every student pair takes its code home."
        ),
        "objectives": [
            (
                "Map the parts of a chess engine onto a science problem: moves, make "
                "and undo, evaluation, and search."
            ),
            (
                "Choose the next measurement by trading off exploring the unknown "
                "against exploiting what the readings predict."
            ),
            (
                "Score a guess about which phases are in a powder, and compare a "
                "greedy agent with a full search."
            ),
            (
                "Verify a search on known answers, and say when the right answer is "
                '"can\'t tell".'
            ),
            (
                "Report a science result with its counts, and explain one decision "
                "the science AI made."
            ),
        ],
        "periods": {
            1: [
                (
                    0,
                    (
                        'Unplugged warm-up, "Find the hidden peak": a 10x10 grid '
                        "hides a hot spot, and each student pair gets five measurements to "
                        "find it."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: the map from chess to science. Legal moves become "
                        "squares not yet measured, and the evaluation becomes "
                        "predicted value plus distance to the nearest reading."
                    ),
                ),
                (
                    25,
                    (
                        "Student pairs write `candidate_squares()`, `score_candidate()`, and "
                        "`choose_next_measurement()` in `hidden_peak.py`."
                    ),
                ),
                (
                    65,
                    (
                        "Student pairs tune `explore_weight` and post their 100-grid benchmark"
                        " average on the board, next to random guessing."
                    ),
                ),
            ],
            2: [
                (
                    0,
                    (
                        "A scientist (or the teacher) shows the NSLS-II PDF beamline "
                        "and its daily question: which crystal phases are in this "
                        "powder?"
                    ),
                ),
                (
                    15,
                    (
                        'Unplugged warm-up, "Name the powder": student pairs lay paper '
                        "fingerprint strips over a printed mystery pattern."
                    ),
                ),
                (
                    30,
                    (
                        "Student pairs write `score()` in `phase_hunt.py`: a point for each "
                        "explained peak, and a point lost for each extra peak, missing"
                        " peak, and phase used."
                    ),
                ),
                (
                    55,
                    (
                        "Student pairs write `greedy_phases()`, which adds the best phase "
                        "again and again with `append` and `pop`. Greedy names 166 of "
                        "200 powders right and 34 wrong, and it mistakes silver for "
                        "gold."
                    ),
                ),
            ],
            3: [
                (
                    0,
                    (
                        "The teacher draws the tree of phase sets next to Remus's game"
                        " tree: a set is a position, adding a phase is a move, and "
                        "taking it back is the undo."
                    ),
                ),
                (
                    15,
                    (
                        "Student pairs write `search()`, which scores every set of up to three"
                        " phases and keeps every set that ties for the best score."
                    ),
                ),
                (
                    50,
                    (
                        "The class verifies on 200 known powders: 139 right, 52 "
                        "\"can't tell\", and 9 wrong, against greedy's 34 wrong. Student pairs"
                        " change `PHASE_COST` and `MISSING` and watch the verdicts "
                        "move."
                    ),
                ),
                (
                    75,
                    (
                        "The teacher closes with the programs that search the same "
                        "tree on real synchrotron data, and the beamline agent at "
                        "Brookhaven."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Each student copies the student pair's Remus folder to a USB drive "
                        "in File Explorer, leaving out the `.venv` folder, and checks "
                        "that the copy opens in VS Code."
                    ),
                ),
                (
                    15,
                    (
                        "Each student pair runs `hidden_peak.py` and `phase_hunt.py` once more "
                        "and fills in its results table: measurements against random "
                        "guessing, and right, wrong, and can't-tell counts for greedy "
                        "and for search. The class collects every student pair's numbers on "
                        "the board."
                    ),
                ),
                (
                    40,
                    (
                        "Each student pair picks one powder its search named and one it "
                        "answered with can't tell, and works out which measurement "
                        "would settle the second."
                    ),
                ),
                (
                    55,
                    (
                        "Each student pair presents its results and its two powders in three "
                        "minutes."
                    ),
                ),
                (
                    80,
                    (
                        "The class closes with what comes next: AI agents that steer "
                        "real experiments at light sources such as NSLS-II."
                    ),
                ),
            ],
        },
        "checkpoint": (
            "Every student pair's `choose_next_measurement()` beats random guessing, every "
            "student pair's `search()` makes fewer wrong calls than greedy, and every student pair has "
            "reported its results and taken its code home."
        ),
    },
}


def main():
    print(f"Periods with objectives: {len(OBJECTIVES)}  (expected 40)")
    print(f"Functions with a change note: {len(CHANGE_NOTES)}  (expected 65)")
    print(f"Lab and demo periods: {len(LABS)}  (expected 16)")
    print(f"Days with an overview: {len(DAY_GUIDES)}  (expected 10)")


if __name__ == "__main__":
    main()
