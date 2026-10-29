#!/usr/bin/env -S uv run
"""period_guides.py

The teaching text of every period goals file: the learning objectives, each with a way
to measure it, and one paragraph for every change the pairs make to the code. It
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
                "`python-chess installed: True` on the pair's laptop."
            ),
        ),
        (
            "Store text in a variable and print it inside an f-string.",
            (
                "Part #2 of `python_setup.py` greets the pair's own team name and counts "
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
                "Without running code, the pair says the file number of h4 (7) and of "
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
                "Part #3 prints the starting position, and the pair names the square "
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
                '`parse_square("i9")` raises `ValueError`, and the pair explains which '
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
                "`uv run pytest` shows the lab's tests passing, and one deliberately "
                "wrong `assert` fails with a clear report."
            ),
        ),
        (
            "Pack two numbers into a tuple and unpack them.",
            "The pair writes `row, col = square` and explains what each name holds.",
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
                "The pair predicts, then shows, that `b2 = board` changes both boards, "
                "and that a copy does not."
            ),
        ),
        (
            "Describe a record with a `dataclass`.",
            "The pair makes a small `dataclass` and prints one of its fields.",
        ),
    ],
    (2, 3): [
        (
            "Tell the color of a piece, and handle an empty square.",
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
                "The pair names what a capture destroys (the captured piece) and where "
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
                'The pair writes the tuple for "up and to the right" (-1, 1) and '
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
                "Running `show_board.py` draws one arrow per king move, and the pair "
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
            "The pair traces `slide()` by hand on a board with one friend and one enemy.",
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
                "The lab's two files run together, and `uv run` on the imported file "
                "alone prints its own self-check only through `main()`."
            ),
        ),
        (
            "Save work with git: switch to a branch, commit, and read the log.",
            "`git log --oneline` shows the pair's commit on its own branch.",
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
                "The pair marks the two squares a White pawn on e4 attacks (d5, f5) on "
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
                "In `demo_practice_positions.py` the pair types its prediction for "
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
            "Six-position quiz on castling: each pair gets at least five right.",
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
            "The pair names the removed pawn's square for exd6 (d5) on the printed board.",
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
                "and checkmate for b8=N, and the pair says why the queen only draws."
            ),
        ),
        (
            "Play Remus in Lucas Chess.",
            (
                "The pair registers `remus.bat`, plays one game, and sees a random legal "
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
            "The pair draws the calls of a depth-2 count and the value each one returns.",
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
                "Running `hunt.py` in `bug_hunt/` points at three bugs; the pair fixes at "
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
                "their names, and the pair labels them on the worksheet."
            ),
        ),
    ],
    (7, 1): [
        (
            (
                "Name every way a game ends: checkmate, stalemate, insufficient "
                "material, repetition, and the fifty-move rule."
            ),
            "Six-position quiz: each pair gets at least five right.",
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
            "Play a whole game in the console.",
            (
                "Two students play `console_game.py` to a finish and the program prints "
                "the right result."
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
                "The pair explains `position`, `go`, and `bestmove` from a printed "
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
                "The pair says why a knight scores more on d4 than on a1, using the "
                "number of squares it attacks (8 and 2)."
            ),
        ),
    ],
    (8, 1): [
        (
            "Back up scores through a tree with minimax.",
            "Paper minimax: the pair's best move matches `minimax()` on the same tree.",
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
                '"Fewest flips": the pair reaches the right move while turning fewer '
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
            "The pair explains why depth 2 takes a defended pawn with the queen.",
        ),
        (
            "List the moves quiescence searches.",
            (
                'The `quiescence` tests pass, and the pair explains what "stand pat" '
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
            "The pair records node counts before and after ordering for one position.",
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
            "The color version's own tests pass in its folder.",
        ),
    ],
    (9, 3): [
        (
            "Test an enhancement before trusting it.",
            (
                "The color version passes `uv run pytest` and a one-game smoke test against "
                "Remus-WHITE with no illegal moves."
            ),
        ),
        (
            "Predict what the enhancement changes.",
            (
                "Each pair writes one sentence on the board: what should change, and how "
                "the class will see it in the match results."
            ),
        ),
    ],
    (9, 4): [
        (
            "Run a fair match between two color versions.",
            (
                "The pair copies its color folder to another pair's laptop, plays two "
                "games against that pair's color, one with each color, and writes the "
                "result on the board."
            ),
        ),
        (
            "Read a match result with its margin of error.",
            (
                "`demo_results.py` turns the pair's two battle games, and then its "
                "color's league games, into an Elo gap and margin, and the pair says "
                "which gap is larger than its margin and why two games cannot show "
                "which enhancement is stronger."
            ),
        ),
    ],
    (10, 1): [
        (
            "Map the chess engine's loop onto a measurement problem.",
            (
                "The pair fills in the chess-to-science table: legal moves, evaluation, "
                "and greedy move each have a science partner."
            ),
        ),
        (
            "Balance exploring and exploiting.",
            (
                "The pair's `choose_next_measurement()` beats random guessing on the "
                "100-grid benchmark, and the pair names the explore weight it chose."
            ),
        ),
    ],
    (10, 2): [
        (
            "Score a guess about what a powder holds.",
            (
                "The `score` test passes, and the pair explains why an extra phase "
                "costs a point even when every peak is explained."
            ),
        ),
        (
            "Build an answer greedily, one best step at a time.",
            (
                "The `greedy_phases` tests pass, and the pair explains why greedy "
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
                "than greedy, and the pair names the extra measurement that would "
                "tell gold from silver."
            ),
        ),
    ],
    (10, 4): [
        (
            "Report a science result the way a scientist does.",
            (
                "The pair's results table gives the hidden-peak benchmark against "
                "random guessing and the phase hunt's right, wrong, and can't-tell "
                "counts for greedy and for search, from the pair's own runs."
            ),
        ),
        (
            "Explain one decision the science AI made.",
            (
                "Each pair presents one powder its search named and one it answered "
                "with can't tell, and says which measurement would settle the second."
            ),
        ),
        (
            "Take the code home.",
            "Each student's USB copy opens and runs `uv run pytest`.",
        ),
    ],
}

# Objectives for the version READMEs, the same for every color
VERSION_OBJECTIVES = [
    (
        "Explain the idea of the color version's enhancement in two sentences.",
        "The pair explains the idea to another pair, who can restate it.",
    ),
    (
        "Add the enhancement without breaking the rules.",
        "`uv run pytest` passes in the version folder.",
    ),
    (
        "Run a fair experiment: same opening, both colors.",
        (
            "In the Day 9 battles, `play_battle.py` in the version folder plays both "
            "10-minute games with no illegal moves or crashes when the pair presses "
            "Run in VS Code, and the pair says why two games cannot show which "
            "enhancement is stronger."
        ),
    ),
]

# The long explanation in each version README, by color. Each section is Markdown:
# "example" walks through one concrete case, "why" says how the idea makes Remus
# stronger, "cost" says what it spends (positions per second, memory, re-searches),
# "expect" says what the pair should see in the numbers and in games, and "fits"
# traces where the pair's code is called from.
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
            "Every color version is Remus-WHITE plus exactly one change. Playing each "
            "color version against Remus-WHITE is a fair experiment: same openings, both "
            "colors, and only one thing different."
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
            "In the teacher's league, where every version searched about as deep "
            "as Remus does in a game of several hours, Remus-GOLD scored 85 "
            "percent and rated +339 plus or minus 91 over Remus-WHITE, far ahead "
            "of every single color version. It gains more the longer the clock, "
            "because null moves and late move reductions save work only at depth 3 "
            "and deeper."
        ),
    },
    "RED": {
        "example": (
            "1. Nf3 Nf6 2. d4 and 1. d4 Nf6 2. Nf3 reach the same position by two "
            "different move orders. Chess players call that a transposition. A "
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
            "Remus-RED is the only single color version that rated clearly above "
            "Remus-WHITE in the teacher's league: +101 plus or minus 67. "
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
            "...c5, ...e6, ...c6, ...d5, ...d6, and ...Nf6. `book_move()` picks one of them at random, so Remus-GREEN does "
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
            "start from the first move. In the teacher's league, Remus-GREEN rated "
            "+7 over Remus-WHITE when its games started three moves deep, and +58 "
            "when they started from the first move. The benchmark below never asks "
            "the book, so its numbers match Remus-WHITE's exactly."
        ),
        "fits": (
            "`uci_engine.py` and `console_game.py` ask `book_move()` before they "
            "search. `None` means the position is not in the book, and the engine "
            "calls `think()` as Remus-WHITE does."
        ),
    },
    "BLUE": {
        "example": (
            "Black has just made a weak move, and White's quiet move Qh5 threatens "
            "mate on f7. Deep in the search, the same Qh5 refutes many different "
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
            "forever. Inside its search, Remus-WHITE scores the position after the "
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
            "pawn on the d- or f-file beside it). Remus-PURPLE scores each doubled "
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
            "line, so a pair can see the term in any position."
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
            "and 4 points for each step the winning king has closed in. Now every "
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
            "no longer shelters the king: 30 points. The bonus counts only while "
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

# Each version's search on the ten positions of compare_search.py, measured with
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
PHASE_HUNT_IMAGES = "../../misc/docs/images/phase_hunt"

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

![Gold's and silver's four peaks side by side, each pair inside the 0.3 degree
tolerance]({PHASE_HUNT_IMAGES}/gold_and_silver.png)

Run `phase_hunt.py` in VS Code when both functions pass their tests. Greedy names 166 of
the 200 benchmark powders right and 34 wrong. In period 3 you write `search()`, which
scores every guess of up to three phases, 176 of them, and keeps every guess that
ties for the best score. When gold and silver tie, the search can answer "can't
tell", and a scientist knows to take a second measurement.

## Real scientists do this

Naming the phases in a powder pattern is called **phase identification**, and
beamline scientists do it every day. At the NSLS-II Pair Distribution Function (PDF)
beamline, Brookhaven's Crystallography Companion Agent names phases while the data
comes in. The CrystalShift program (Cornell, 2025) and the Dara program (Berkeley Lab,
2025) search a tree of phase sets the way your code will in period 3, on real
patterns from the synchrotrons SSRL and CHESS and from a self-driving lab.
`misc/docs/course/science_tree_search_survey.md` lists the papers.

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
    "`isupper()` tells the colors apart.",
    ("game_state.py", "color_of"): 'Returns "w", "b", or None for an empty '
    "square. Move generation asks this about every square a piece might land on: a "
    "friend blocks the move, an enemy can be captured, and None means the square is "
    "free.",
    ("moves.py", "move_to_uci"): "Writes a move as text such as e2e4, adding a "
    "lowercase piece letter for a promotion (e7e8q). UCI is the language Lucas "
    "Chess speaks, so this is how Remus tells the GUI which move it chose.",
    ("moves.py", "move_from_uci"): "Reads text such as e7e8q back into a Move. The "
    "promotion letter becomes uppercase for White and lowercase for Black, so the "
    "new piece gets the right color on the board.",
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
    "both jump to fixed squares; only their list of jumps differs.",
    ("move_generation.py", "slide"): "Walks one direction from a square, adding a "
    "move for each empty square, and stops at the edge or at the first piece. An "
    "enemy piece can be captured, so its square is added before the walk stops; a "
    "friendly piece is not. Rooks, bishops, and queens all use this walk with "
    "different directions.",
    ("move_generation.py", "pawn_pushes"): "Moves a pawn one square forward if it is "
    "empty, and two squares from its starting row if both are empty. White pawns "
    "move toward row 0, because row 0 is rank 8. Pawns are the only pieces that "
    "move one way and capture another, which is why pushes get their own function.",
    ("attacks.py", "piece_at_offsets"): "Stands on the square and looks at each "
    "offset for one piece, such as an enemy knight. Attacks work backward: instead "
    "of asking where every enemy piece can go, the test looks out from the square. "
    "A knight attacks e5 from exactly the squares a knight on e5 could jump to, so "
    "the knight, the king, and the pawn all share this one loop, the way "
    "`jump_moves()` serves both the knight and the king.",
    ("attacks.py", "attacked_by_pawn"): "Looks diagonally for an enemy pawn on the "
    "row behind the square, from the attacker's point of view. A pawn captures "
    "diagonally even though it moves straight, so its two offsets differ from its "
    "push, and they depend on its color.",
    ("attacks.py", "attacked_by_king"): "Looks one step away in all eight directions "
    "for the enemy king, with the same `KING_STEPS` the king moves by. Kings can "
    "never stand next to each other, and this check is what stops a king from "
    "walking up to the other king.",
    ("attacks.py", "in_check"): "Finds the king of one color and asks whether the "
    "other color attacks its square. Check decides which moves are legal, whether "
    "a game is over, and later how deep the search looks.",
    ("legal_moves.py", "legal_moves"): "Tries every pseudo-legal move: makes it, "
    "keeps it if the mover's king is not in check, and undoes it. Testing after the "
    "move catches pins and discovered checks without any special rules, which is why "
    "the code is so short.",
    ("make_move.py", "update_castling_rights"): "Removes castling rights when a king "
    "or rook leaves its square, or when a rook is captured on its square. Rights only "
    'ever disappear, so `replace()` deletes letters from a string such as "KQkq".',
    ("make_move.py", "en_passant_victim_square"): "Returns the square of the pawn that "
    "an en passant capture removes: the capturer's starting row and the landing "
    "column. It is the only capture where the victim is not on the landing square.",
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
    "all stand on squares of one color. The bishops' square colors come from "
    "(row + col) % 2.",
    ("game_end.py", "game_result"): "Checks every way a game ends, in order: no legal "
    "moves (checkmate or stalemate), insufficient material, threefold repetition, and "
    "the fifty-move rule. It returns the result and the reason, so the console and "
    "the GUI can say why a game is over.",
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
        "test is how a pair shows it understands the two slots."
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

# (day, period) -> paragraphs about the lab file, one per part the pairs type
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
            "the colors apart. Remus's `is_white()` on Day 2 is this one call."
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
            "when a check fails. `uv run pytest python_functions.py` runs the same tests "
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
            "`board.py` on its own in VS Code, and Part #4 makes a git branch, a "
            "commit, and the log in the terminal."
        ),
    ],
    (4, 4): [
        (
            "`demo_practice_positions.py` builds three positions from a dict of "
            "{square: piece} and prints each board with Remus's legal-move count. The "
            "pair types each position and its prediction before running the file, so "
            "every count is a test of the pair's own reasoning as well as of the code."
        ),
        (
            "Part #2 puts a rook check on the White king, and Part #3 adds a knight "
            "on e2 that blocks the check but cannot move: it is pinned. The loop at the "
            "end counts only the moves that start on e2, the same check as "
            "`test_pinned_knight_has_no_moves()`."
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
            "to the Black king on a6. The pair writes the loop that tries all four "
            "promotion pieces, counts Black's legal replies, and names the result."
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
            "each with its name, the map the pair needs before writing `fen.py`. Then "
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
            "Part #1: `remembered_perft()` stores each answer in a dict under the tuple "
            "key `(name, depth)`. The second call finds the answer and returns at once. "
            "The RED color version's transposition table remembers search results the same way."
        ),
        (
            "Parts #2 and #3 use `math.dist()` for the straight-line distance from d4 "
            "to g7, which the CYAN color version needs, and `random.seed()`, which makes a "
            "random choice repeat on every run."
        ),
    ],
    (9, 4): [
        (
            "Parts #1 and #2 of `demo_results.py` turn a match result into a score and "
            "an Elo gap, then into a range that holds the true gap 95 times out of "
            "100. When the range includes 0, the match has not shown that the "
            "enhancement helped, and more games are needed. Each pair puts in its own "
            "two battle games, then its color's league games from the teacher's "
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
            "Day 1 forms the pairs, checks the laptops, and teaches the first Python: "
            "strings and lists. In the last period each pair writes its first Remus "
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
                    15,
                    (
                        "The story of the name: Sargon, the 1978 chess program, and "
                        "Rimush, the first son of Sargon of Akkad. Remus is a son of "
                        "Sargon."
                    ),
                ),
                (
                    25,
                    (
                        "Form the ten pairs. The driver types and the navigator reads "
                        "and checks; the two swap roles every period. Each pair picks "
                        "a team name for `CONTRIBUTORS.md`."
                    ),
                ),
                (
                    40,
                    (
                        "Notation on the demonstration board: square names, SAN for "
                        "people (`Nf3`, `Bxh8`, `e8=Q`), and UCI for programs "
                        "(`g1f3`)."
                    ),
                ),
                (
                    55,
                    (
                        "Pairs type the 6 lines of `python_setup.py` and run it. It "
                        "checks the laptop, greets the team, and prints a first chess "
                        "line. The teacher and the assistant check that every laptop "
                        "passes `uv run pytest` and opens Lucas Chess."
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
                        "Pairs work through the four parts of `python_strings.py`, "
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
                    "Pairs compare their printouts with the pair next to them.",
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
                        "Pairs work through the four parts of `python_lists.py`: a "
                        "list of pieces, a loop over every square, the board as a list"
                        " of rows, and the pawns in a row."
                    ),
                ),
                (
                    75,
                    (
                        "Without running code, each pair names `board[4][4]` (e4) and "
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
                        "Pairs write `print_board()`, `square_name()`, "
                        "`parse_square()`, and `piece_at()` in `board.py` and run `uv "
                        "run pytest` after each one."
                    ),
                ),
                (
                    60,
                    (
                        "Pairs run `show_board.py`, which draws their board as a "
                        "picture in the web browser."
                    ),
                ),
                (
                    70,
                    (
                        "Show and choose: two or three pairs show their "
                        "`parse_square()` on the projector, the class picks one for "
                        "clarity, and the teacher adds it to the class repository with"
                        " the pair's team name in `CONTRIBUTORS.md`."
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
                        "Pairs work through Parts #1 to #3 of `python_functions.py`: "
                        "call a function, write their own, and unpack a square tuple "
                        "such as `row, col = (6, 4)`."
                    ),
                ),
                (
                    55,
                    (
                        "Slides: `assert` and pytest. The teacher breaks a function on"
                        " purpose and the class reads the failing test together."
                    ),
                ),
                (
                    65,
                    (
                        "Pairs finish Part #4, which checks their functions with "
                        "`assert`."
                    ),
                ),
                (
                    80,
                    (
                        "Wrap-up: each pair says what a failing test tells them and "
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
                        "Pairs work through Parts #1 and #2 of `python_dicts.py` and "
                        "watch `b2 = board` change both boards."
                    ),
                ),
                (
                    45,
                    (
                        "The teacher explains aliasing on the whiteboard: two names, "
                        "one list. Then pairs write Parts #3 and #4: a real copy, and "
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
                        "Pairs write `is_white()` and `color_of()` in `game_state.py`,"
                        " then `move_to_uci()` and `move_from_uci()` in `moves.py`, "
                        "with `uv run pytest` after each."
                    ),
                ),
                (
                    65,
                    (
                        "Pairs run `game_state.py` and `moves.py` and compare the "
                        "printouts with the expected answers."
                    ),
                ),
                (
                    75,
                    (
                        "Show and choose: the class picks one `move_from_uci()` for "
                        "the class repository."
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
                        "Pairs write `make_move()` and `undo_move()` in `make_move.py`"
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
            " pairs' code finds."
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
                        "Pairs work through the four parts of `python_loops.py`: "
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
                        'Unplugged warm-up, "Shade the reach": pairs shade every '
                        "square a knight on d4, a knight on a1, and a bishop on c1 can"
                        " reach, and compare counts with the next pair (8, 2, and 7)."
                    ),
                ),
                (
                    15,
                    (
                        "Slides: an offset list for the knight. The teacher writes "
                        "`knight_moves()` on the projector."
                    ),
                ),
                (
                    30,
                    (
                        "Pairs write `king_moves()` the same way and "
                        "pass the jumping-piece tests: a knight on a1 has 2 moves and "
                        "a king on a1 has 3."
                    ),
                ),
                (
                    50,
                    (
                        "Pairs run `show_board.py`, which draws an arrow for every "
                        "move their generator returns, and count the arrows."
                    ),
                ),
                (
                    70,
                    (
                        "Pairs try their own squares, such as a king in a corner, and "
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
                        "Pairs write `slide()` in `move_generation.py`. The teacher's "
                        "`slider_moves()` calls it with the rook, bishop, and queen "
                        "directions."
                    ),
                ),
                (
                    60,
                    (
                        "Exercise: a rook on an empty board has 14 moves. Pairs check "
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
                        "or two squares, and capture diagonally. The teacher writes "
                        "the captures and the four promotion choices."
                    ),
                ),
                (
                    15,
                    (
                        "Pairs write `pawn_pushes()`: the single step and the double "
                        "step from the start rank."
                    ),
                ),
                (
                    55,
                    (
                        "Pairs run the tests and the arrow picture on the start "
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
            "Day 4 teaches modules and git, then the rule that makes a move legal: the"
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
                "Save work with git: fetch, switch to a new branch, commit, and read "
                "the log."
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
                        "Pairs work through Parts #1 to #3 of `python_modules.py`: "
                        "every file has a `__name__`, use yesterday's `board.py` and "
                        "`move_generation.py`, and list the knight moves from g1."
                    ),
                ),
                (
                    50,
                    (
                        "Slides: git. The teacher shows `fetch`, `switch -c`, "
                        "`commit`, and `log` on the projector."
                    ),
                ),
                (
                    60,
                    ("Pairs finish Part #4 and save the lab with their first commit."),
                ),
                (
                    80,
                    ("Every pair shows its `git log` to the teacher or the assistant."),
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
                        "The teacher writes `attacked_by_knight()` and the "
                        "sliding-line part."
                    ),
                ),
                (
                    30,
                    (
                        "Pairs write `piece_at_offsets()`, then `attacked_by_pawn()` "
                        "and `attacked_by_king()` on top of it."
                    ),
                ),
                (
                    70,
                    "Pairs run the attack tests and the file's self-check.",
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
                        "pairs cross out every move that leaves the mover's king "
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
                        "Pairs write `in_check()` and `legal_moves()` until the tests "
                        "pass."
                    ),
                ),
                (
                    65,
                    "Pairs compare Remus's answers with their pin hunt worksheets.",
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
                        "In `demo_practice_positions.py` pairs type each position and "
                        "write their prediction of its legal move count before Remus "
                        "counts."
                    ),
                ),
                (
                    50,
                    (
                        "Part #4: each pair builds a position of its own and trades it"
                        " with the next pair, who predict before they run it."
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
            "first week with a payoff: by 4:30 every pair plays its own Remus in Lucas"
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
                        "Pairs work through the four parts of `python_sets.py`, ending"
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
                        "Slides: the teacher's castling generation and the "
                        "attacked-square checks."
                    ),
                ),
                (
                    30,
                    (
                        "Pairs write `update_castling_rights()`, the table of which "
                        "moves remove K, Q, k, or q."
                    ),
                ),
                (
                    50,
                    (
                        "Pairs run the castling tests and build one castling position "
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
                        "Pairs write `en_passant_victim_square()`, "
                        "then trace a capture and its undo on the printed board."
                    ),
                ),
                (
                    55,
                    (
                        "Pairs run the en passant tests, including the rare capture "
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
                        "In `demo_promotion.py` pairs write the loop that tries all "
                        "four promotions and prints stalemate or checkmate for each."
                    ),
                ),
                (
                    45,
                    (
                        "The teacher hands out `uci_engine.py` and `remus.bat`. Pairs "
                        "register `remus.bat` from the period's `student` folder in Lucas Chess, "
                        "following the [Lucas Chess guide](../misc/docs/course/lucas_chess_guide.md)."
                    ),
                ),
                (
                    60,
                    (
                        "Pairs play their own Remus, which answers with random legal "
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
                        "Pairs work through the three parts of `python_recursion.py`: "
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
                        "against king position, pairs list every move two plies deep "
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
                        "Pairs write `perft()` and run it on the warm-up position to "
                        "check their cards."
                    ),
                ),
                (
                    55,
                    (
                        "Pairs run `perft.py` from the start: 20, 400, and 8,902. The "
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
                        "three planted bugs. Pairs run `hunt.py` there and race to "
                        "find each bug from the root moves whose counts disagree."
                    ),
                ),
                (
                    70,
                    "Pairs explain each bug they found and the rule it broke.",
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
                    "Pairs work through `python_fen_fields.py`.",
                ),
                (
                    30,
                    (
                        "Pairs write `fen_placement()` and `board_from_placement()` in"
                        " `fen.py`. The teacher writes the other five fields."
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
                        "Slides: the halfmove clock and `position_key()`, which the "
                        "teacher writes."
                    ),
                ),
                (
                    30,
                    (
                        "Pairs write `insufficient_material()` and `game_result()` in "
                        "`game_end.py`."
                    ),
                ),
                (
                    75,
                    (
                        "Pairs check their answers on the quiz positions, then show "
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
                        "Pairs write `parse_san()`: build the SAN of every legal move "
                        "and return the one that matches."
                    ),
                ),
                (
                    35,
                    (
                        "Pairs play each other with `console_game.py`, typing moves in"
                        " SAN."
                    ),
                ),
                (
                    50,
                    (
                        "Pairs work through `python_input_output.py`: "
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
                    "Pairs write `random_move()` and `greedy_move()`.",
                ),
                (
                    40,
                    (
                        "The class reads the Day 5 `uci_engine.py` line by line. The "
                        "teacher extends it with FEN positions and a choice of brains."
                    ),
                ),
                (
                    60,
                    (
                        "Pairs register `remus.bat` from the `student` folder in Lucas Chess "
                        "again and play greedy Remus."
                    ),
                ),
                (
                    75,
                    (
                        "Pairs run `play_match.py`: random Remus against greedy Remus "
                        "for 20 games, with the score at the end."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Pairs rank three printed positions and write one reason for "
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
                    "Pairs write `material()` in centipawns, scored for White.",
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
                        "Each pair proposes one change to one table, and the class "
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
                        'Unplugged warm-up, "Paper minimax": pairs back up max and '
                        "min on a printed two-ply tree and circle the best move. A "
                        "seven-student human tree can act it out at the front of the "
                        "room."
                    ),
                ),
                (
                    15,
                    (
                        "The teacher writes `minimax()` to depth 2 with a node "
                        "counter, and pairs compare its answer with their worksheets."
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
                        "Pairs write `negamax()` until the tests show it agrees with "
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
                        "face-down cards. Pairs turn a card only when the answer could"
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
                        "Pairs write `alpha_beta()` beside `negamax()` and run "
                        "`compare_search.py`: the same score, fewer nodes."
                    ),
                ),
                (
                    55,
                    (
                        "Pairs work through `python_sorting.py`: `insert()` puts the "
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
                        "position is quiet. The teacher writes `capture_moves()`."
                    ),
                ),
                (
                    30,
                    (
                        "Pairs write `quiescence()`, which may stand pat with the "
                        "evaluation or try a capture that does better."
                    ),
                ),
                (
                    70,
                    "Pairs run the puzzle again: Remus keeps its queen.",
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
                        "Pairs write `mvv_lva_score()`. The teacher writes "
                        "`order_moves()` and the check extension."
                    ),
                ),
                (
                    40,
                    (
                        "Pairs measure node counts before and after ordering with "
                        "`compare_search.py`."
                    ),
                ),
                (
                    65,
                    "Pairs run the mate puzzles.",
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
            "color versions. Each pair adds one idea to the same engine, Remus-WHITE, and "
            "tests it. In period 4 the pairs carry their colors to each other's laptops "
            "on USB sticks and battle. By 4:30 every color version passes its tests and "
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
                "Play two color versions against each other, and read the result "
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
                        "Pairs write `think()` (the iterative deepening loop): depth "
                        "1, then 2, then 3, keeping the best move of the deepest "
                        "search that finished."
                    ),
                ),
                (
                    55,
                    (
                        "Show and choose for `think()`. The chosen code makes "
                        "Remus-WHITE, the Remus with none of the enhancements and the "
                        "starting point of every color version."
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
                        "Pairs work through `python_caches.py`: a dict remembers "
                        "answers, `math.dist()`, and `random.seed()`."
                    ),
                ),
                (
                    20,
                    (
                        "Slides: the ten color versions. Each is Remus-WHITE plus one "
                        "enhancement, such as RED (transposition table) or BLUE "
                        "(killer moves). Colors name the color versions so that no color version "
                        "sounds better than another."
                    ),
                ),
                (
                    30,
                    (
                        "Each pair opens its color version in `period2/student/engines`, "
                        "reads the version README, and writes the color version's stubbed "
                        "code."
                    ),
                ),
            ],
            3: [
                (
                    0,
                    "Pairs finish their color version code and pass its tests.",
                ),
                (
                    40,
                    (
                        "Each pair opens `smoke_test.py` in its version folder and "
                        "presses Run in VS Code: one 2-minute game against "
                        "Remus-WHITE, which checks only that the engine plays legal "
                        "moves to the end."
                    ),
                ),
                (
                    70,
                    (
                        "Each pair writes one sentence on the board: what its "
                        "enhancement should change, and how the class will see it."
                    ),
                ),
            ],
            4: [
                (
                    0,
                    (
                        "Slides: how a battle works. Each pair copies its own color "
                        "folder from `period2/student/engines` onto its USB stick. The teacher posts the "
                        "pairings for two rounds; in each round five pairs host and "
                        "five visit."
                    ),
                ),
                (
                    10,
                    (
                        "Round 1. The visiting pair copies its color folder over the "
                        "folder of the same color in the host laptop's `engines` "
                        "folder. The host opens `play_battle.py` in its own color "
                        "folder, presses Run in VS Code, and types the visitor's "
                        "color. Two 10-minute games run side by side, one with each "
                        "color. Each pair writes the score on the board."
                    ),
                ),
                (
                    40,
                    "Round 2: the pairs that visited now host, against new opponents.",
                ),
                (
                    45,
                    (
                        "While the round 2 games run, each pair turns its round 1 "
                        "result into an Elo gap with a margin of error in "
                        "`demo_results.py`, then tries its color's league games."
                    ),
                ),
                (
                    70,
                    (
                        "The class reads the board: which colors won, and why two "
                        "games prove little. The teacher shows the league table, 110 "
                        "games for each color, and compares."
                    ),
                ),
                (
                    85,
                    (
                        "Each host restores the visitor's folder with `git restore` so "
                        "its own repository holds only its own color."
                    ),
                ),
            ],
        },
        "checkpoint": (
            "Every color version passes its tests and its one-game test match, and "
            "has played two battles against other colors."
        ),
    },
    10: {
        "theme": "Solve a science problem using chess AI",
        "summary": (
            "Day 10 aims the engine's ideas at real science. The same generate, score,"
            " and choose loop picks where to measure a hidden peak, and the full tree "
            "search, with make and undo, names the crystal phases in an X-ray powder "
            "pattern. The day ends with each pair reporting its science results, and "
            "every pair takes its code home."
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
                        "hides a hot spot, and each pair gets five measurements to "
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
                        "Pairs write `candidate_squares()`, `score_candidate()`, and "
                        "`choose_next_measurement()` in `hidden_peak.py`."
                    ),
                ),
                (
                    65,
                    (
                        "Pairs tune `explore_weight` and post their 100-grid benchmark"
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
                        'Unplugged warm-up, "Name the powder": pairs lay paper '
                        "fingerprint strips over a printed mystery pattern."
                    ),
                ),
                (
                    30,
                    (
                        "Pairs write `score()` in `phase_hunt.py`: a point for each "
                        "explained peak, and a point lost for each extra peak, missing"
                        " peak, and phase used."
                    ),
                ),
                (
                    55,
                    (
                        "Pairs write `greedy_phases()`, which adds the best phase "
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
                        "Pairs write `search()`, which scores every set of up to three"
                        " phases and keeps every set that ties for the best score."
                    ),
                ),
                (
                    50,
                    (
                        "The class verifies on 200 known powders: 139 right, 52 "
                        "\"can't tell\", and 9 wrong, against greedy's 34 wrong. Pairs"
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
                        "Each student copies the pair's repository to a USB drive "
                        "with `git clone --no-hardlinks` and checks that the copy "
                        "opens and runs `uv run pytest`."
                    ),
                ),
                (
                    15,
                    (
                        "Each pair runs `hidden_peak.py` and `phase_hunt.py` once more "
                        "and fills in its results table: measurements against random "
                        "guessing, and right, wrong, and can't-tell counts for greedy "
                        "and for search. The class collects every pair's numbers on "
                        "the board."
                    ),
                ),
                (
                    40,
                    (
                        "Each pair picks one powder its search named and one it "
                        "answered with can't tell, and works out which measurement "
                        "would settle the second."
                    ),
                ),
                (
                    55,
                    (
                        "Each pair presents its results and its two powders in three "
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
            "Every pair's `choose_next_measurement()` beats random guessing, every "
            "pair's `search()` makes fewer wrong calls than greedy, and every pair has "
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
