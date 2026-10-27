#!/usr/bin/env -S uv run
"""period_guides.py

The teaching text of every period README: the learning objectives, each with a way
to measure it, and one paragraph for every change the pairs make to the code.

make_period_folders.py writes this text into each instructor period README, and
make_student_folders.py into each student period README and station README. Keep
the language at a middle school reading level: short sentences, one idea each.
"""

# The Python skills lab files, by (day, period). Each name has a student file
# labs/dayNN/<name>.py and an answer file labs/dayNN/instructor/<name>_instructor.py
LABS = {
    (1, 1): "python_setup",
    (1, 2): "python_strings",
    (1, 3): "python_lists",
}

# (day, period) -> [(objective, how the teacher measures it)]
OBJECTIVES = {
    (1, 1): [
        (
            "Start VS Code, open a terminal, and run a Python file with `uv run`.",
            (
                "`uv run python_setup.py` prints Python 3.14 or later and "
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
                "`uv run board.py` prints the start board with 8 at the top and a to h "
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
                "`uv run show_board.py` draws one arrow per king move, and the pair "
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
            "Each pair writes its count for two positions first, then compares.",
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
            "Play Remus in En Croissant.",
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
            "`uv run perft.py` prints 20, 400, and 8,902 for depths 1 to 3.",
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
                "The pair finds at least two of the three planted bugs and names the "
                "root move that shows each one."
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
            "The pair labels the six fields of the start FEN on the worksheet.",
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
            "`uv run play_match.py` shows greedy Remus scoring more than random Remus.",
        ),
    ],
    (7, 4): [
        (
            "Count material in centipawns.",
            (
                "The evaluation tests pass, and `uv run evaluation.py` prints -200 for "
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
                "The `alpha_beta` tests pass, and `uv run compare_search.py` prints the "
                "same scores as negamax with fewer nodes."
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
                "in En Croissant."
            ),
        ),
        (
            "Report the search to the GUI with `info` lines.",
            (
                "En Croissant shows Remus's depth, score, and best line for each depth "
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
            "The station's own tests pass in its folder.",
        ),
    ],
    (9, 3): [
        (
            "Test an enhancement before trusting it.",
            (
                "The station passes `uv run pytest` and a two-game smoke test against "
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
            "Run a fair experiment: same opponent, same openings, both colors.",
            (
                "Each laptop's `station_match.py` run starts with no errors and adds "
                "games to the games file."
            ),
        ),
        (
            "Solve mate puzzles with a yes-or-no search.",
            "The mate-solver tests pass on all ten GameWorks puzzles.",
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
            "Estimate a value and its error from noisy readings.",
            "The `estimate` test passes: four readings cut the error in half.",
        ),
        (
            "Score an experiment by the wrong calls to expect.",
            (
                "The `expected_wrong_calls` test passes, and the pair explains why an "
                "unmeasured sample counts as 0.5."
            ),
        ),
    ],
    (10, 3): [
        (
            "Look ahead with pretend readings, the way Remus looks ahead with moves.",
            (
                "The `gain` test passes: a close call (52) gains more from a shot than "
                "a clear one (90)."
            ),
        ),
        (
            "Verify a model by comparing its predictions with results.",
            (
                "`uv run beam_time.py` shows largest gain beating equal time, and the "
                "pair compares each expected count with the real count."
            ),
        ),
    ],
    (10, 4): [
        (
            "Read an experiment's results and their error margins.",
            "Each pair says whether its color's Elo gap is larger than its margin.",
        ),
        (
            "Explain one decision your engine made.",
            (
                "Each pair presents one move with its score and principal variation, and "
                "one choice its beam time agent made."
            ),
        ),
        (
            "Take the code home.",
            "Each student's USB copy opens and runs `uv run pytest`.",
        ),
    ],
}

# Objectives for the station READMEs, the same for every color
STATION_OBJECTIVES = [
    (
        "Explain the idea of the station's enhancement in two sentences.",
        "The pair explains the idea to another pair, who can restate it.",
    ),
    (
        "Add the enhancement without breaking the rules.",
        "`uv run pytest` passes in the station folder.",
    ),
    (
        "Measure the enhancement against Remus-WHITE.",
        (
            "`uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap "
            "and margin from the output."
        ),
    ),
]

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
    "lowercase piece letter for a promotion (e7e8q). UCI is the language En "
    "Croissant speaks, so this is how Remus tells the GUI which move it chose.",
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
    ("attacks.py", "attacked_by_knight"): "Looks one knight jump away from the square "
    "for an enemy knight. Attacks work backward: instead of asking where every enemy "
    "piece can go, it stands on the square and looks out.",
    ("attacks.py", "attacked_by_pawn"): "Looks diagonally for an enemy pawn on the "
    "row behind the square, from the attacker's point of view. A pawn captures "
    "diagonally even though it moves straight, so this check differs from the push.",
    ("attacks.py", "attacked_by_king"): "Looks one step away in all eight directions "
    "for the enemy king. Kings can never stand next to each other, and this check is "
    "what stops a king from walking up to the other king.",
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
    ("mate_solver.py", "mating_move"): "Looks for a move after which every defense "
    "still loses to a mate in one move fewer. On the last move only checks are "
    "tried, because only a check can be mate. A yes-or-no question is much faster to "
    "answer than a full search with scores.",
    ("hidden_peak.py", "candidate_squares"): "Lists every square not measured yet. "
    'These are the "legal moves" of the science problem: the places the AI could '
    "measure next.",
    ("hidden_peak.py", "score_candidate"): "Scores a square by its predicted value "
    "plus a bonus for being far from earlier readings. The first part exploits what "
    "the AI knows, and the second explores where it knows little.",
    ("hidden_peak.py", "choose_next_measurement"): "Returns the candidate with the "
    "highest score, just as `greedy_move()` returns the best capture. The same "
    "generate, score, and choose loop now runs on a science problem.",
    ("beam_time.py", "estimate"): "Averages a sample's readings and works out the "
    "error: the noise divided by the square root of the number of readings. Four "
    "readings cut the error in half, which is why some samples deserve more shots.",
    ("beam_time.py", "expected_wrong_calls"): "Adds up the chance of a wrong call "
    "over all eight samples. It is the evaluation of the experiment, like "
    "`material()` for a chess position: a smaller total means a better plan.",
    ("beam_time.py", "gain"): "Looks one shot ahead: tries three pretend readings "
    "(one noise step low, on the average, one step high), averages the chance of a "
    "wrong call after each, and returns how much the chance drops. Pretend readings "
    "are like the moves Remus makes and undoes while it searches.",
    ("beam_time.py", "choose_next_sample"): "Returns the sample whose next shot has "
    "the largest gain. With it, the agent spends beam time where a call is still "
    "close, and makes fewer wrong calls than giving every sample equal time.",
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
    "returns the en passant target so it can be put back. If the position is still "
    "winning after a free move for the opponent, a real move will be too, so the "
    "search can stop early.",
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
}


def main():
    print(f"Periods with objectives: {len(OBJECTIVES)}  (expected 40)")
    print(f"Functions with a change note: {len(CHANGE_NOTES)}  (expected 53)")
    print(f"Lab periods: {len(LABS)}  (expected 3)")


if __name__ == "__main__":
    main()
