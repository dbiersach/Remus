# Turning a Chess Engine into Science AI: Remus Course Plan

This plan turns the [workshop roadmap](workshop_roadmap.md) into a
two-week course for students about 13 years old: 10 days, four 90-minute periods a day,
60 class hours in all. Students work in pairs. They learn the Python they need in short
labs, and then they write real sections of Remus: small functions that go into the
class engine and stay there.

The plan also maps the ideas in Borland's Turbo GameWorks Chess 4.0 (Kaare Danielsen,
1985 to 1987) onto the modules Remus grows, and shows where Remus connects to
`python-chess` and a desktop GUI so the class never has to build one. The standing rules
in [`AGENTS.md`](../AGENTS.md) apply to everything below.

## Decisions this plan is built on

| Question | Decision |
| --- | --- |
| Length | Two weeks, 10 days, 4 periods of 90 minutes a day (6 class hours) |
| Daily schedule | 8:30 to 10:00 Period 1; 10:00 to 10:30 break; 10:30 to 12:00 Period 2; 12:00 to 1:00 lunch; 1:00 to 2:30 Period 3; 2:30 to 3:00 break; 3:00 to 4:30 Period 4 |
| Students | 20 students in 10 pairs: a driver types, a navigator reads and checks; they swap every period. Ten pairs keep each adult to about five pairs during labs |
| Staff | The teacher plus at least one assistant |
| Laptops | 10 identical Windows 11 laptops, one per pair, preconfigured with git, `uv`, VS Code, and Lucas Chess |
| GUI | Lucas Chess on every laptop |
| Repositories | The teacher's laptop holds the main class repository. Each pair has its own local repository and pulls from the teacher over the classroom network. No GitHub accounts: the students are minors |
| Take-home | On the last day each pair copies its repository, with its full history, onto a USB drive |
| Folder layout | The finished reference code lives in `instructor/`, one folder per day, such as `instructor/Day 04 - Keep only legal moves`, with four period folders inside, `period1` to `period4`. Each period folder holds a complete, runnable copy of Remus at the end of that period, with its tests beside the modules and a `README.md` for the period. A module keeps one file name all course; a smarter version is a new function beside the old one in the same file (`negamax`, then `alpha_beta`) |
| Squares | `(row, col)` tuples inside the engine, row 0 is rank 8 and column 0 is file a |
| Human move text | Standard algebraic notation (SAN) for typing and displaying moves: `d4`, `Nc3`, `Bxh8`, `O-O`, `e8=N+` |
| GUI move text | UCI (`e2e4`, `e7e8q`), because that is what the GUI protocol uses |
| First pictures | Day 1: `show_board.py` draws the students' board in the browser with python-chess. Day 3: it draws an arrow for every move their generator finds |
| First GUI game | Day 5 Period 4: a teacher-written `uci_engine.py` plays random legal moves in Lucas Chess once every special move works. Day 7 explains UCI and adds the brains, after the rules pass perft and Remus reads FEN |
| Unplugged warm-ups | 10 to 15 minutes at the desk with paper and cards before each hard idea, taken from the teacher's explanation time, never from coding time |
| Matches | Day 10: each pair's color station plays Remus-WHITE twice at 10 minutes a side, once with each color, all ten laptops at once. The teacher then shows Remus-GOLD's results against every color and Remus-WHITE from the teacher's league |
| Mate puzzles | The ten GameWorks `MATE.00x` positions live in `tests/mate_puzzles.epd`: nine mates in 2 and one mate in 3 (`MATE.008`), each with its single key move, checked with python-chess |
| Documentation | `docs/remus_program_overview.md` for the whole program, one page per major script in `docs/scripts/`, and `docs/slide_plan.md` for the PowerPoint slides |

## The shape of the two weeks

Week 1 builds Python skills and the rules of chess. Week 2 turns the rules into a game,
plugs it into a GUI, and teaches Remus to think.

| Day | Theme | Python skills lab | Remus can do this by 4:30 |
| --- | --- | --- | --- |
| 1 | Setup and the board | Running scripts, strings, `ord` and `chr`, lists, nested lists | Print the board; convert `e2` to `(6, 4)` and back |
| 2 | Functions and records | Functions, type hints, tuples, `assert`, pytest, dicts, dataclasses, copying | Hold a game state; make and undo a quiet move or capture |
| 3 | Loops that walk the board | `while`, `break`, direction tuples, building lists | Generate king, knight, slider, and pawn moves |
| 4 | Legal moves | Modules, imports, `__main__`, git | Detect attacks and check; keep only legal moves |
| 5 | Special moves | Sets and dict lookups | Castling, en passant, promotion and underpromotion, with exact undo; play random Remus in Lucas Chess |
| 6 | Counting the tree, and FEN | Recursion; `split`, exceptions | Perft matches the reference counts; FEN in and out |
| 7 | A whole game, and judging a position | `random`, a loop that keeps the best so far, stdin and stdout | SAN; end the game; play random and greedy moves in a GUI; evaluate a position |
| 8 | Searching ahead, then smarter | Recursion review, keeping a list in order with `insert` | Minimax, negamax, alpha-beta, quiescence, move ordering |
| 9 | The clock and the stations | `time`, dicts as caches, tuples as keys | Iterative deepening (Remus-WHITE); one enhancement station per pair; a mate solver |
| 10 | Science AI at the beamline | `math.dist`, `random.seed`, `append` and `pop` as make and undo | A measurement AI that finds a hidden peak; a phase hunt that names the crystals in an X-ray pattern; results and the tournament against Remus-WHITE |

Week 1 is Days 1 to 5 and Week 2 is Days 6 to 10. Week 1 ends with every special move
in place, and Week 2 opens with recursion and perft. Perft on Monday gives every pair a
verified checkpoint after the weekend. Week 2 moves fast so that Day 9 can hold the
enhancement stations and Day 10 the science problem, so a pair that falls behind
rejoins from the period's end tag instead of a catch-up period.

### Progressive elaboration

Every functional area starts with the smallest correct version and grows in later
periods. The engine as a whole gets two big passes: first it plays **legal** moves (end
of Day 7), then it plays **good** moves (Days 7 to 10).

| Area | Version 1 | Version 2 | Version 3 | Version 4 and later |
| --- | --- | --- | --- | --- |
| Board | 8x8 list of lists, printed (D1) | Square names (D1) | FEN in and out (D6) | GameWorks's 0x88 board as a "how 1987 did it" sidebar talk (D10 optional, no code) |
| Make and undo | Quiet moves and captures (D2) | Castling, en passant, promotion (D5) | Clocks, history, repetition keys (D7) | Undo inside search with `try/finally` (D8) |
| Move generation | King and knight jumps (D3) | Sliders and pawns (D3) | Legal filter: make, test the king, undo (D4) | Captures first, MVV-LVA, killers (D8, D9) |
| Attacks | Loop over enemy pieces (D4) | Look outward from the square (D4) | Castling and legality use it (D5) | Check extension in the search (D8) |
| Game end | Checkmate and stalemate (D7) | Fifty-move rule (D7) | Threefold repetition (D7) | Insufficient material (D7) |
| Notation | UCI text (D2) | FEN (D6) | SAN out (D7) | SAN in, by matching legal moves (D7) |
| Choosing a move | Random legal move (D7) | Greedy: biggest capture (D7) | Minimax, then negamax (D8) | Alpha-beta, quiescence, ordering (D8), iterative deepening (D9), the ten enhancement stations (D9) |
| Evaluation | Material count (D7) | Piece-square tables (D7) | Mate scores that prefer the faster mate (D8) | Pawn structure, mating bonus, and king safety stations (D9) |
| Science AI | Paper hidden-peak game and greedy measurement choice (D10 P1) | Explore and exploit weight tuned on a benchmark (D10 P1) | Phase hunt: score a guess about a powder, and a greedy agent (D10 P2) | Search every set of phases with make and undo, keep every tie, and verify on known powders (D10 P3) |
| Interface | Console printout and a board picture (D1) | Move arrows (D3) and random Remus in Lucas Chess (D5) | Console game in SAN and full UCI (D7) | `info` lines, time control, `stop` (D9) |

## How students write real Remus code

Students write about 40 small functions over the two weeks. Each one is short enough
for a pair to finish in 20 to 40 minutes, and each one ships in the engine.

1. **The scaffold.** Before the period, the teacher's checkpoint holds the function's
   signature, its NumPy docstring, and tests that fail. The body says `raise
   NotImplementedError`.
2. **The pair writes the body** until `uv run pytest test_<topic>.py` passes inside the day's folder and
   the module's own self-check prints the expected answer.
3. **Show and choose.** Two or three pairs show their version on the projector. With 10
   pairs and about 40 functions, the teacher rotates who presents so every pair ships
   three or four functions over the course. The class picks one for clarity, not cleverness, and the teacher commits it to the main
   class repository. `CONTRIBUTORS.md` records which pair wrote which function, by a
   team name the pair chooses rather than full names, since the code goes home with
   every student.
4. **Everyone moves on together.** `student/` mirrors `instructor/` day by day and
   period by period. Each student period folder holds the finished code of the
   periods before plus that period's scaffolds, which `make_student_folders.py`
   builds from the instructor code. Each period opens with its slides; then pairs
   open the period folder, read its `README.md`, and write or fix the stubbed
   functions in the files it names. Pairs work only inside the current period
   folder, so earlier periods stay as a record of how Remus grew. `instructor/` holds the matching finished code, which runs as it is. At the start of the next period each pair fetches
   from the teacher and starts a new branch from that period's start tag, so the whole
   room builds the same engine. The pair's own branches stay in its repository, so a
   pair whose version was not picked keeps its own code too.

## Sharing code without GitHub

The teacher's laptop holds the main class repository. Students never create accounts,
and nothing leaves the classroom except on the USB drives at the end.

| Step | Who | How |
| --- | --- | --- |
| Share the class repository | Teacher | Run a read-only `git daemon` on the teacher's laptop for the classroom network: `git daemon --export-all --base-path=<parent folder> --reuseaddr`. Git for Windows includes it |
| First copy, before Day 1 | Teacher | Clone the class repository onto every laptop and add the remote `instructor` (`git remote add instructor git://<teacher-laptop>/remus`) |
| Start a period | Pair | `git fetch instructor --tags`, then `git switch -c d3-p3 d3-p3-start`. One branch per period keeps each period's work separate and easy to find |
| Catch up after falling behind | Pair | `git switch -c d3-p3-catchup d3-p3-end` |
| Hand in a picked function | Pair and teacher | The teacher copies the function from the pair's screen or from a file the pair saves to the class USB stick, then commits it with a `CONTRIBUTORS.md` line |
| Take it home | Pair | `git clone --no-hardlinks . <usb>/remus` copies the source and full history but not the `.venv` folder, which only works on the laptop that built it. At home: install `uv`, run `uv sync`, install the free Lucas Chess (Windows or Linux) from its download page, and register `remus.bat` as in [`lucas_chess_guide.md`](lucas_chess_guide.md). A student with a Mac or Linux computer at home uses `remus.sh` instead; Lucas Chess has no Mac version, so a Mac needs another UCI chess app |

School Wi-Fi sometimes blocks laptops from reaching each other. Test `git fetch
instructor` from one class laptop in the room before Day 1. If the network
blocks it, the same steps work through the USB stick: the teacher writes
`git bundle create class.bundle --all` at the end of each period, and pairs run
`git fetch <usb>/class.bundle "refs/tags/*:refs/tags/*"`.

The "Students write" lines in each day below list these functions. The teacher writes
the parts whose difficulty is in the chess rules rather than the Python, such as SAN
disambiguation or the castling legality check, and walks through them line by line.

## Python skills labs

Each lab is 30 to 90 minutes: the teacher demonstrates, pairs complete short drills, and
every drill uses chess data so the skill is fresh when the engine needs it.

| Lab | Day | Skills | Chess drill |
| --- | --- | --- | --- |
| 1 | D1 P2 | VS Code, terminal, `uv run file.py`, `print`, variables, strings, indexing, `ord` and `chr`, f-strings | Turn `"e2"` into file number 4 and rank number 2 |
| 2 | D1 P3 | Lists, `for` and `range`, `len`, nested lists, `board[row][col]` | Print an 8x8 grid of dots, then count the pawns in a row |
| 3 | D2 P1 | Functions, parameters, `return`, type hints, docstrings, tuples and unpacking, `assert`, pytest | `is_white("N")`, `on_board(row, col)` with tests |
| 4 | D2 P2 | Dicts, `dataclass`, `None`, mutation, aliasing, `copy` and `deepcopy`, `==` on lists | Show `b2 = board` changing both boards; fix it with a copy |
| 5 | D3 P1 | `while`, `break`, `continue`, lists of direction tuples, `append` | Walk from `d4` toward the edge in one direction, stopping at a piece |
| 6 | D4 P1 | Modules, `import`, `if __name__ == "__main__"`, git `fetch`, `switch -c`, `commit`, `log` | Import yesterday's `board.py` and `move_generation.py` and list the knight moves from `g1` |
| 7 | D5 P1 | Sets, membership with `in`, dict lookups, string replacement | Castling rights as the string `"KQkq"`: remove `"K"` when the h1 rook moves |
| 8 | D6 P1 | Recursion: base case, recursive case, call stack | Count down; count the leaves of a small tree; count paths of a knight |
| 9 | D6 P4 | `split`, `int()`, exceptions with `try` and `ValueError` | Read a FEN string and print its six fields |
| 10 | D7 P2 | `random.choice`, a loop that keeps the best so far, `sys.stdin`, `print(..., flush=True)`, `sys.stderr` | A tiny program that echoes lines, then answers `isready` with `readyok` |
| 11 | D8 P2 | keeping a list in order with `insert`, `time.perf_counter()`, `float("inf")` | Sort captures by victim value; time a perft run |
| 12 | D9 P2 | Dicts as caches, tuples as keys, `math.dist`, `random.seed` | Remember perft counts already computed; measure the distance from `d4` to `g7` |

## Unplugged warm-ups

Each hard idea gets a short warm-up away from the screen first. Pairs close the laptop,
slide it aside, and work on the desk with a printed board, sticky notes, index cards, and
a one-page worksheet. Every warm-up fits on one desk, so the room never has to be
rearranged.

The time comes out of the teacher's explanation at the board, which the warm-up
replaces: students learn the idea by doing it instead of by listening to it. The
"Students write" block of each period keeps its full time.

| When | Warm-up (10 to 15 minutes) | Idea it prepares | Materials per pair |
| --- | --- | --- | --- |
| D1 P3 | **Call the square.** The teacher calls `(6, 4)`; the navigator puts a token on the printed board and the driver names the square (`e2`). Then they swap and go the other way | Row 0 is rank 8 | Printed board labeled both ways, one token |
| D2 P4 | **Undo from the card.** One partner makes three moves with sticky-note pieces and writes an undo card for each. The other partner restores the start position from the cards alone | Undo records and exact undo | Printed board, sticky notes, three index cards |
| D3 P2 | **Shade the reach.** Shade every square a knight on `d4`, a knight on `a1`, and a bishop on `c1` can reach; compare counts with the next pair (8, 2, 7) | Offset lists and sliding | Grid worksheet |
| D4 P3 | **Pin hunt.** Four printed positions; cross out every move that leaves the mover's king attacked | The legal-move filter | Worksheet |
| D6 P2 | **Count by hand.** A king and pawn against a king; list every move two plies deep on index cards and count the leaves before running `perft` on the same position | Perft and recursion | Index cards, worksheet |
| D8 P1 | **Paper minimax.** A printed two-ply tree with scores on the bottom row. Pairs back up max and min level by level and circle the best move; the class compares answers before `minimax()` runs on the same tree | Minimax | Tree worksheet |
| D8 P2 | **Fewest flips.** The same tree as a row of face-down index cards. Pairs turn a card only when the answer could still change; the pair with the fewest flips and the right move wins | Alpha-beta pruning | Deck of score cards |
| D10 P1 | **Find the hidden peak.** A 10x10 grid hides a hot spot. With five "measurements" (the teacher reads the value at a square), each pair chooses where to measure next and marks its guess | How the NSLS-II AI agent chooses the next measurement, the Science AI link | Grid worksheet |
| D10 P2 | **Name the powder.** Five printed peak fingerprints (strips of paper with marks at their angles) and one printed mystery pattern. Pairs lay strips over the pattern to find which two phases made it, and count the peaks each guess leaves over or misses | Scoring a guess, and why a fingerprint that fits half the peaks is a trap | Fingerprint strips, pattern sheet |

For the minimax warm-up, the teacher can also run a seven-student "human tree" at the
front of the room: one root, two "min" players, and four leaves holding score cards,
while the other pairs predict the answer on paper.

## Chess rules to refresh

Students know how the pieces move. These rules trip up nearly everyone, so a short
refresher with a demonstration board comes right before the code that needs each one.

| Rule | What to stress | When |
| --- | --- | --- |
| Coordinates and notation | Files a to h, ranks 1 to 8; SAN (`Nf3`, `Bxh8`, `e8=Q`) for people, UCI (`g1f3`) for programs | D1 P1 |
| Check, pins, discovered check | A move is legal only if your own king is safe afterward | D4 P2 |
| Castling | King and that rook never moved; squares between empty; king not in check, not passing through or landing on an attacked square. The rook may cross an attacked square (b1). Capturing a rook on its home square removes that right | D5 P2 |
| En passant | Only on the very next move after a two-square push. The captured pawn is not on the destination square. Rare trap: the capture can expose your king along the rank | D5 P3 |
| Promotion and underpromotion | Queen, rook, bishop, or knight. A knight can promote with check and a fork; a queen can stalemate. One side can have two queens | D5 P4 |
| Stalemate | No legal move and not in check is a draw | D7 P1 |
| Threefold repetition | Same pieces, same side to move, same castling and en passant rights, three times, not necessarily in a row. Claimable; fivefold ends the game automatically | D7 P1 |
| Fifty-move rule | 50 moves by each side (100 plies) without a capture or pawn move. Claimable at 50, automatic at 75 | D7 P1 |
| Insufficient material | K vs K, K+B vs K, K+N vs K, and K+B vs K+B with same-colored bishops are draws | D7 P1 |
| Piece values and tactics | Pawn 1, knight 3, bishop 3, rook 5, queen 9; fork, pin, skewer | D7 P4 |

## Teacher preparation

1. **Build the reference engine first.** The teacher's Remus is complete before the
   course, with a scaffold tag and a solution tag for every period (`d3-p2-start`,
   `d3-p2-end`). The start tag holds the stubs and failing tests; the end tag holds
   the teacher's answer, which a pair can check out if it falls behind.
2. **Finish the laptop image.** The 10 Windows 11 laptops arrive with git, `uv`, VS Code,
   and Lucas Chess. Check that the image also has Python 3.14 cached by `uv` and the
   VS Code extensions from `install_vscode_extensions.ps1`. Clone the class repository as
   described in "Sharing code without GitHub", then run `uv sync` and `uv run pytest`
   on every laptop before Day 1, so no laptop needs the internet on Day 1.
3. **Register Remus in Lucas Chess.** Add the reference Remus as an external engine
   through `remus.bat`, following [`lucas_chess_guide.md`](lucas_chess_guide.md), and play
   one full game on one laptop. Start Lucas Chess from the Start menu or its desktop
   icon: it runs engine-against-engine games only when it starts from its own folder. If the image is identical, the same
   engine path works on all 10; check that the repository sits at the same folder on
   every laptop.
4. **Print handouts:** a board diagram labeled with both `e2` and `(6, 4)`, the rules
   refresher table, a SAN and UCI cheat sheet, a perft reference table, and a blank game
   tree for Day 8.
5. **Collect test positions as FEN:** the ten verification exercises in the workshop
   file, the standard perft positions, mate-in-1 and mate-in-2 puzzles, the ten
   GameWorks mate puzzles, and a horizon-effect position.
6. **Plan for 20 students.** Print 20 copies of each handout. Buy 20 USB drives, so
   both partners take the code home, plus one class stick for bundles. Give the assistant
   the Day 1 checklist. With preconfigured laptops, Day 1 Period 1 needs only a quick
   check that every laptop runs `uv run pytest` and opens Lucas Chess.
7. **Prepare unplugged materials:** for each pair, a printed board, sticky-note
   pieces, a deck of index cards, and the warm-up worksheets listed under "Unplugged
   warm-ups"; for the room, a large demonstration board and score cards for the human
   minimax tree.
8. **Set speed expectations.** Plain Python searches thousands to tens of thousands of
   positions per second. Depth 3 to 4 with alpha-beta and quiescence in a few seconds
   is a realistic target, so students compare Remus with other Python engines, not
   with Stockfish.

## Week 1: Python and the rules

### Day 1: Setup and the board

- **P1. Welcome and setup.** Watch the finished reference Remus play in the GUI. Tell
  the Sargon and Rimush story from `AGENTS.md`. Form pairs, check every laptop runs
  `uv run pytest`, and review SAN and UCI notation on the demonstration board. Each
  pair runs `python_setup.py`, which checks the laptop and prints the team's first
  greeting (6 typed lines).
- **P2. Python lab 1, `python_strings.py`:** scripts, strings, `ord` and `chr`,
  f-strings (13 typed lines).
- **P3. Python lab 2, `python_lists.py`:** lists and nested lists (25 typed lines).
  Unplugged warm-up: "Call the square" drills "row 0 is rank 8" on the printed board
  before anyone types it.
- **P4. `board.py`.** The teacher writes `new_board()` and hands out `show_board.py`,
  which draws the board as a picture in the web browser (python-chess draws it; the
  engine never imports python-chess).
  **Students write:** `print_board()`, `square_name(row, col)`,
  `parse_square(name)` (which rejects `"i9"`), `piece_at(board, square)`.

**Checkpoint `d1-p4-end`:** `uv run board.py` prints the start board and
"b1 holds N, expected N".

### Day 2: Functions and records

- **P1. Python lab 3, `python_functions.py`:** functions, type hints, tuples, `assert`, pytest.
- **P2. Python lab 4, `python_dicts.py`:** dicts, dataclasses, aliasing, copying.
- **P3. `game_state.py` and `moves.py`.** The teacher writes the state dict in
  `new_game()` and the `Move` dataclass (`from_square`, `to_square`, `promotion`).
  **Students write:** `is_white(piece)`, `color_of(piece)`, `move_to_uci(move)`,
  `move_from_uci(text)`.
- **P4. `make_move.py`, ordinary moves.** Unplugged warm-up: "Undo from the card."
  The teacher writes `state_snapshot(state)` for the "make ten moves, undo ten moves,
  compare" test. **Students write:** `make_move()`, which moves the piece and returns
  an undo record of everything the move destroys, and `undo_move()`, which uses that
  record to take back quiet moves and captures.

**Checkpoint `d2-p4-end`:** ten moves made and undone return the exact start state.

### Day 3: Loops that walk the board

- **P1. Python lab 5, `python_loops.py`:** `while`, `break`, direction tuples.
- **P2. Jumping pieces.** Unplugged warm-up: "Shade the reach." The teacher writes
  `knight_moves()` from an offset list.
  **Students write:** `king_moves()` the same way. Exercise: a knight on `a1` has two
  moves, to `b3` and `c2`. `uv run show_board.py` draws an arrow for every move the
  generator returns, so pairs see their own moves on a real board.
- **P3. Sliding pieces.** **Students write:** `slide(board, square, direction)`, the
  loop that walks one direction and stops at the first piece, capturing it if it is
  an enemy. The teacher writes `slider_moves()` that calls it with rook, bishop, and
  queen directions. Exercise: a rook on an empty board has 14 moves.
- **P4. Pawns.** **Students write:** `pawn_pushes()` (single step and double step from
  the start rank). The teacher writes pawn captures and the four promotion choices.
  Exercise: `pseudo_legal_moves()` from the start returns 20.

**Checkpoint `d3-p4-end`:** 20 pseudo-legal moves from the start position.

### Day 4: Legal moves

- **P1. Python lab 6, `python_modules.py`:** modules, imports, `__main__`, git.
- **P2. Attacks.** Refresher on check, pins, and discovered check. `attacks.py`
  version 1 loops over the enemy pieces, as GameWorks `Attacks` does. Version 2 stands
  on the square and looks outward like a "super piece."
  **Students write:** `piece_at_offsets()`, the one loop that looks for a knight, a
  king, or a pawn a fixed step away, then `attacked_by_pawn()` and `attacked_by_king()`
  on top of it. The teacher writes `attacked_by_knight()` as the model call, and the
  sliding-line part, `first_piece()` and `attacked_along_lines()`.
- **P3. Check and the legal filter.** Unplugged warm-up: "Pin hunt." **Students write:** `in_check(state, color)` and
  `legal_moves(state)`: make each pseudo-legal move, reject it if the mover's king is
  attacked, undo it.
- **P4. Practice positions.** Pairs build tests for the workshop's first three
  verification exercises: 20 moves from the start, a king in check, and a pinned piece.
  In `demo_practice_positions.py` each pair types the three positions and a
  prediction for each, then lets Remus count the legal moves.

**Checkpoint `d4-p4-end`:** a pinned knight has zero legal moves; a king in check has
only escapes.

### Day 5: Special moves

- **P1. Python lab 7, `python_sets.py`:** sets, `in`, string replacement for castling rights.
- **P2. Castling.** Refresher with the five conditions on the board. The teacher writes
  castling generation and the attacked-square checks.
  **Students write:** `update_castling_rights(rights, move, captured)`, the table of
  which moves remove `K`, `Q`, `k`, or `q`, including a rook captured on its home square.
- **P3. En passant and the double step.** **Students write:**
  `en_passant_victim_square()`, the square of the pawn an en passant capture removes,
  which is not the square the capturing pawn lands on. The teacher writes the en
  passant make and undo, including the line that sets the target after a double step.
- **P4. Promotion and underpromotion.** Puzzle: promoting to a knight wins, promoting to
  a queen stalemates. The teacher writes promotion in `make_move` and `undo_move`,
  and pairs write tests from the workshop's special-move checklist. In
  `demo_promotion.py` pairs write the loop that tries all four promotions on the
  puzzle and prints stalemate for the queen, rook, and bishop and checkmate for the
  knight. To close the week,
  the teacher hands out `uci_engine.py` and `remus.bat` as a ready-made plug: pairs
  register `remus.bat` in Lucas Chess and play their own Remus, which answers with a
  random legal move; [`lucas_chess_guide.md`](lucas_chess_guide.md) shows each click.
  Nobody reads the UCI code yet; Day 7 explains it.

**Checkpoint `d5-p4-end`:** every special-move test passes, every special move
undoes exactly, and Remus plays random legal moves in Lucas Chess.

## Week 2: A game, a GUI, and a thinking engine

Week 2 is tight by design. Days 6 to 8 move faster than Week 1, so that Day 9 can hold
the enhancement stations and Day 10 can hold the science problem. There is no spare
catch-up period: a pair that falls behind checks out the period's end tag and rejoins.

### Day 6: Counting the tree, and FEN

- **P1. Python lab 8, `python_recursion.py`:** recursion.
- **P2. Perft.** Unplugged warm-up: "Count by hand." **Students write:**
  `perft(state, depth)`, the recursive count of leaf
  positions. The teacher writes `divide()`, which prints the count under each root move.
  Expected: 20, 400, 8,902 from the start.
- **P3. Perft against python-chess, and bug hunt.** `test_perft.py` compares Remus
  with `python-chess` on the standard positions. The teacher plants three bugs in a copy
  (en passant pawn left on the board, castling through check, a missing promotion
  piece); pairs race to find them with `divide`. The copy is the `bug_hunt` folder
  inside the period folder, and `uv run hunt.py` there prints every root move whose
  count disagrees with `python-chess`.
- **P4. Python lab 9 and FEN.** The lab, `python_fen_fields.py`, covers `split` and
  exceptions. Then
  `fen.py`. **Students write:** `fen_placement(board)` (the part of FEN before the
  first space) and `board_from_placement(text)`. The teacher writes the other five FEN
  fields, and `test_perft.py` switches to Remus's own FEN reader.

**Checkpoint `d6-p4-end`:** perft matches the reference at depth 3 for the start and
the standard positions, and every test position loads from FEN. Rule 6 of `AGENTS.md`
is now met.

### Day 7: A whole game, and judging a position

- **P1. Ending the game.** Refresher on stalemate, repetition, the fifty and 75-move
  rules, and insufficient material, with a six-position quiz. The teacher writes the
  halfmove clock and `position_key()`. **Students write:** `insufficient_material(board)`
  and the result-and-reason checks in `game_result(state)`.
- **P2. SAN and the console game.** The teacher writes `move_to_san()`, including
  disambiguation (`Nbd2`) and the `+` and `#` suffixes. **Students write:**
  `parse_san(state, text)`, which builds the SAN of every legal move and returns the one
  that matches what the player typed. Then `console_game.py` lets two people play in SAN.
  Python lab 10, `python_input_output.py` (stdin, stdout, `random`, and a loop that keeps the best so far),
  closes the period.
- **P3. First brains and the GUI.** **Students write:** `random_move()` and
  `greedy_move()` (take the most valuable capture, else a random move). The class
  reads the Day 5 `uci_engine.py` line by line, and the teacher extends it with FEN
  positions and a choice of brains. Every pair registers Remus in the GUI again and
  plays greedy Remus. `play_match.py` plays random Remus against greedy Remus for
  20 games and prints the score.
- **P4. What makes a position good?** Pairs rank three positions and write one reason
  each; those reasons become evaluation terms. **Students write:** `material(board)` in
  centipawns (pawn 100, knight 300, bishop 300, rook 500, queen 900), scored for White.
  The teacher shows the piece-square tables (a knight on `d4` attacks eight squares; on
  `a1` it attacks two) and `explain_evaluation()`, which prints every term so Remus can
  say why it prefers a position. Each pair proposes one change to one table, and the
  class votes.

**Checkpoint `d7-p4-end`:** a full game in the GUI ends with the correct result and
reason, and `explain_evaluation()` gives 0 for the start position. This is the "legal
moves" milestone.

### Day 8: Searching ahead, then searching smarter

- **P1. Minimax, negamax, and mates.** Unplugged warm-up: "Paper minimax," with the
  optional human tree at the front of the room. The teacher writes `minimax()` to
  depth 2 with a node counter, and pairs compare its answer with their worksheets.
  **Students write:** `negamax()`, the same search in one function: each reply's score
  with its sign flipped, `try/finally` around each make and undo, and checkmate scored
  as `-(MATE_SCORE - ply)` so Remus prefers the faster mate. The tests check that it
  agrees with minimax and leaves the root state unchanged.
- **P2. Python lab 11 and alpha-beta.** Unplugged warm-up: "Fewest flips" finds the
  cards nobody needs to turn over. **Students write:** `alpha_beta()` beside
  `negamax()`, then run `compare_search.py`: both pick the same score, and alpha-beta
  counts fewer nodes. The lab, `python_sorting.py`, covers keeping a list in order with `insert()`,
  `float("inf")`, and timing a perft run.
- **P3. The horizon effect and quiescence.** Puzzle: at depth 2 Remus takes a defended
  pawn with its queen. The teacher writes `capture_moves(state)`, the filter of
  captures and promotions. **Students write:** `quiescence()`, which may "stand pat"
  with the evaluation or try a capture that does better.
- **P4. Move ordering.** **Students write:** `mvv_lva_score(move, board)` (most valuable
  victim, least valuable attacker). The teacher writes `order_moves()`, the loop that
  slides each move into place behind every higher score, and the check extension.
  Pairs measure node counts before and after.

**Checkpoint `d8-p4-end`:** Remus finds every mate in 1 and every GameWorks mate in 2,
and alpha-beta returns the same score as negamax with fewer nodes.

### Day 9: The clock, and the enhancement stations

- **P1. Iterative deepening, the clock, and UCI info.** The teacher reads `go
  movetime`, `wtime`, `btime`, `winc`, and `binc`, turns the clock into a thinking
  time, and writes `format_info()`, which prints `info depth 3 score cp 35 nodes
  4120 pv e2e4 e7e5 g1f3` so the GUI shows Remus thinking. **Students write:**
  `think()`, the deepening loop: depth 1, then 2, then 3, keeping the best move of the
  deepest search that finished before the clock ran out. The Remus at the end of this period is **Remus-WHITE**, with
  none of the enhancements. The period ends with the class watching Remus-WHITE play
  a full 5-minute game against Stockfish at 1500 Elo in Lucas Chess, set up as in
  [`lucas_chess_guide.md`](lucas_chess_guide.md), Part 3.
- **P2. Python lab 12 and the enhancement stations.** The lab, `python_caches.py`,
  covers dicts as caches and tuples as keys (7 typed lines, so a station of 30 lines
  stays within the limit). Then each of the 10 pairs takes one color station from
  `Stations/`: Remus-WHITE plus one enhancement, with the pair's function stubbed (at
  most 30 typed lines). Colors replace numbers so no station sounds better than
  another. The stations are described in [stations.md](stations.md).

| Color | Station | GameWorks idea it echoes |
| --- | --- | --- |
| RED | Transposition table: a dict from `position_key` to depth, score, bound, and best move | (not in GameWorks) |
| GREEN | Opening book: SAN lines checked with `legal_moves()` | `OPENING.LIB` |
| BLUE | Killer moves: two quiet moves per ply that caused a cutoff | `KillingMove` |
| PINK | Principal variation search: null window on every move after the first | `ZeroWindow` in `SEARCH.CH` |
| YELLOW | Draw sense: a repeated position scores 0 inside the search | `DrawGame` |
| PURPLE | Pawn structure: doubled, isolated, and passed pawns | `PawnStrVal`, `PassPawnRank` |
| CYAN | Mating bonus: push the losing king to the edge | `Mating` mode in `CalcPVTable` |
| ORANGE | Null-move pruning: give the opponent two moves in a row; if Remus is still too far ahead, stop searching | (not in GameWorks) |
| BROWN | Late move reductions: search late, quiet moves one ply shallower | (not in GameWorks) |
| GRAY | King safety: reward the pawn shield while queens are on | (not in GameWorks) |

- **P3. Enhancement stations: test and measure.** Each pair finishes its station,
  passes its tests, and plays one short smoke-test game against Remus-WHITE with
  `uv run station_match.py <COLOR> --games 1 --minutes 2`, which only checks that the
  engine plays legal moves to the end. Each pair writes one sentence on the board:
  what its enhancement should change, and how the class will see it.
- **P4. The mate solver.** The class meets the ten GameWorks mate puzzles.
  **Students write:** `mating_move(state, moves_left)` in `mate_solver.py`, the
  yes-or-no search that solves all ten, including the mate in 3 (`MATE.008`).

**Checkpoint `d9-p4-end`:** every station passes its tests and its one-game smoke
test, and the mate solver solves all ten puzzles.

### Day 10: Science AI at the beamline

- **P1. Science AI: `hidden_peak.py`.** Unplugged warm-up: "Find the hidden
  peak." Then the teacher shows the map from chess to science on the board:

  | Chess engine | Hidden-peak search |
  | --- | --- |
  | Legal moves | Squares not yet measured |
  | `make_move` and `undo_move` | Add a pretend reading, then take it back |
  | Evaluation: material plus mobility | Score: predicted value (exploit) plus distance to the nearest reading (explore) |
  | `greedy_move()` | Measure the best-scoring square now |
  | Minimax: the opponent picks the minimum | Expectimax: average over a high or low reading, because nature is not an opponent |
  | Match against greedy Remus | Benchmark: average measurements to find the peak over 100 hidden grids |

  The teacher writes `make_grid(seed)`, `measure(grid, square)`,
  `predicted_value(square, readings)`, and `benchmark(strategy)`. **Students write:**
  `candidate_squares(readings)`, `score_candidate(square, readings, explore_weight)`,
  and `choose_next_measurement(readings, explore_weight)`. Pairs tune
  `explore_weight` and post their benchmark average on the board, next to random
  guessing.
- **P2. The phase hunt: score a guess, and the greedy agent.** A scientist visit (or
  the teacher) shows the NSLS-II PDF beamline and the question it answers every day:
  which crystal phases are in this powder? Each phase makes its own fingerprint of
  X-ray peaks, so a powder that mixes phases shows all their peaks at once.
  `phase_hunt.py` holds a library of ten real phases, each with its four strongest
  peaks, computed with Bragg's law from published lattice sizes. Unplugged warm-up:
  pairs lay paper fingerprint strips over a printed mystery pattern. The teacher
  writes `matches()`, `predicted_peaks()`, `make_pattern(seed)` (a mixture of one to
  three phases with missing and shifted peaks), and the benchmark. **Students
  write:** `score(phases, measured)`, the evaluation: a point for each explained
  peak, and a point lost for each peak left over, each predicted peak missing, and
  each phase used; then `greedy_phases(measured)`, which adds the best phase again
  and again with append and pop, like `greedy_move()`. Greedy names 166 of 200
  powders right and 34 wrong. It names gold for a powder that holds silver, because
  gold and silver have almost the same peaks.
- **P3. The phase hunt: search every set, and verify.** The teacher draws the tree of
  phase sets next to Remus's game tree: a set is a position, adding a phase is a
  move, and taking it back is the undo. Quartz then rutile is the same set as rutile
  then quartz, so the search adds phases in library order only, which cuts the tree
  from 821 sets to 176, the way move ordering lets alpha-beta skip work. **Students
  write:** `search(phases, measured, depth, start, hunt)`, which scores every set of
  up to three phases with append and pop and keeps every set that ties for the best
  score. Then the class verifies on 200 known powders, the science version of perft
  against python-chess: the search names 139 right, says "can't tell" for 52 (most of
  them gold or silver), and is wrong on 9, against greedy's 34 wrong. Pairs change
  `PHASE_COST` and `MISSING` and watch the verdicts move. The teacher closes with the
  published programs that search the same tree on real synchrotron data,
  CrystalShift (SSRL and CHESS) and Dara (Berkeley Lab), and with Brookhaven's
  Crystallography Companion Agent, which answers the same question live at the PDF
  beamline. A "can't tell" sends the scientist back for a second measurement, such as
  X-ray fluorescence, which tells gold from silver at once.
- **P4. Results, tournament, take-home, and wrap-up.** The tournament comes first.
  Every pair runs `uv run station_match.py <COLOR>` in the `Stations` folder on its
  own laptop, all ten at once: its color plays two 10-minute games against
  Remus-WHITE from the same opening, with White in game 1 and Black in game 2. The two
  games run side by side and take about 20 to 30 minutes, while each student copies
  the pair's repository to their own USB drive with `git clone --no-hardlinks` and
  checks that the copy opens. Each pair writes its two results on the board. Then the
  teacher shows Remus-GOLD's results against every color and Remus-WHITE from the
  teacher's 10-minute league (`uv run station_league.py --rate-only --player GOLD`),
  and Remus-GOLD's Stockfish rating (about 1960 at 10 minutes a game, from
  [`station_elo.md`](station_elo.md)), as a class discussion: two games cannot tell
  one enhancement from another, and 66 games barely can. In `demo_results.py` each
  pair turns its two games, and then its color's 66 league games, into an Elo gap with
  a margin of error and lets Remus explain one move. Each pair then
  explains one move its engine chose, with the score and principal variation, and one
  powder its phase hunt named. Close with what comes next: bitboards, Zobrist
  hashing, endgame tablebases, and a stronger "Manishtushu" engine.

**Checkpoint `d10-p4-end`:** every pair's `choose_next_measurement()` beats random
guessing on the 100-grid benchmark, every pair's `search()` makes fewer wrong calls
than greedy on the 200-powder benchmark, and the tournament games finished with no illegal
moves, crashes, or lost synchronization.

## Code breakdown by day

The finished reference code lives in `instructor/`, one folder per day. Each Day folder
holds `period1` to `period4`, and each period folder is a complete copy of Remus at
the end of that period. `period4` is the finished code of the day, and
`make_period_folders.py` builds the three earlier periods from it.
[`file_versions.md`](file_versions.md) lists which period adds or grows each file. The
table names the folders without the `instructor/` prefix. Every module ends with a visible self-check, as `AGENTS.md`
requires, so a pair can run any file from inside the folder with `uv run perft.py`.
The full description of each script is in `docs/scripts/`.

| Folder | New files | Files that grow |
| --- | --- | --- |
| `Day 01 - Draw the board` | `board.py`, `show_board.py`, `test_board.py` | |
| `Day 02 - Make and undo moves` | `game_state.py`, `moves.py`, `make_move.py`, `test_make_move.py` | `board.py` (`set_piece`) |
| `Day 03 - Generate piece moves` | `move_generation.py`, `test_move_generation.py` | `show_board.py` (`show_moves`) |
| `Day 04 - Keep only legal moves` | `attacks.py`, `legal_moves.py`, `test_legal_moves.py` | |
| `Day 05 - Add castling, en passant, and promotion` | `uci_engine.py`, `remus.bat`, `test_special_moves.py` | `make_move.py`, `move_generation.py`, `legal_moves.py` |
| `Day 06 - Count positions and read FEN` | `perft.py`, `test_perft.py`, `fen.py`, `test_game.py` | |
| `Day 07 - Play full games and score positions` | `notation.py`, `game_end.py`, `search.py`, `console_game.py`, `play_match.py`, `evaluation.py`, `test_search.py` | `game_state.py` (`position_key`), `make_move.py` (history), `fen.py` (history), `uci_engine.py` (FEN, brains) |
| `Day 08 - Search ahead with alpha-beta` | `compare_search.py`, `move_ordering.py` | `search.py` (minimax, negamax, alpha-beta, quiescence), `uci_engine.py` and `console_game.py` (negamax brain) |
| `Day 09 - Add the clock and build the stations` | `mate_solver.py` | `search.py` (`think`), `uci_engine.py` (clock, thinking time), `console_game.py` (uses `think`); the station folders live in `Stations/` |
| `Day 10 - Aim Remus at a science problem` | `transposition_table.py`, `opening_book.py`, `opening_book.txt`, `hidden_peak.py`, `phase_hunt.py`, `remus.sh`, `estimate_elo.py`, `test_upgrades.py`, `test_phase_hunt.py` | `evaluation.py` (pawns, mating, king safety), `move_ordering.py` (killers), `search.py` (`upgraded_search`), `uci_engine.py` (book) |

Outside the Day folders:

| Path | Holds |
| --- | --- |
| `tests/mate_puzzles.epd` | The ten GameWorks mate puzzles as FEN |
| `tests/test_reference_tools.py` | Checks that python-chess is installed and agrees with known counts |
| `run_all_tests.py` | Runs pytest on each instructor period folder in turn |
| `make_period_folders.py` | Builds `period1` to `period3` of each instructor Day folder from `period4` |
| `student/`, `make_student_folders.py` | The student copy of every period folder, with that period's student functions as stubs, and the script that builds it |
| `docs/` | This plan, the roadmap, the program overview, the script pages, the slide plan, and the two briefing PDFs |
| `<skill>.py` in the student period folder, `<skill>_instructor.py` in the instructor one | Python skills labs: student file with blanks, instructor file with answers, both in the period folder of their lab (`period_guides.LABS` lists the 16 lab and demo periods) |
| `period_guides.py` | The learning objectives, how each is measured, and the paragraph on every change, which the builders write into every period README |
| `docs/student_edit_plan.md` | Generated by `make_student_folders.py`: what the pairs write in every period, with line counts |
| `CONTRIBUTORS.md` | Which pair wrote which function (starts on Day 1) |

A module keeps one file name all course. When a newer version teaches by comparison,
the older function stays beside it in the same file: `is_attacked_by_scanning` next to
`is_square_attacked`, `minimax` and `negamax` next to `alpha_beta`, and
`alpha_beta_with_quiescence` next to `upgraded_search`, so pairs can print node counts
side by side and every import keeps working.

## GameWorks to Remus map

| GameWorks file | What it does | Remus home | Remus differs because |
| --- | --- | --- | --- |
| `CHESS.PAS` | Includes every module; constants `MaxPly = 23`, `Back = -104` | `uci_engine.py`, `console_game.py` | Separate modules instead of one program built from include files |
| `BOARD.CH` | 0x88 board (`a1 = 0`, `h8 = $77`), `PieceTab` piece list, `MoveType`, `Perform` for make and take back | `board.py`, `moves.py`, `make_move.py` | 8x8 list with row 0 at rank 8; the undo record holds castling rights, en passant, and clocks, not only pieces |
| `MOVGEN.CH` | Direction tables, `AttackTab`, `Attacks`, castling from history, `FiftyMoveCnt`, `Repetition`, `KillMovGen`, captures-first generator | `move_generation.py`, `attacks.py`, `game_end.py`, `move_ordering.py` | Rights and en passant live in state; repetition counts position keys |
| `SMALL.CH` | `MakeMove`, `TakeBackMove`, `IllegalMove`, game comments (mate, stalemate, 50-move, repetition, resign), time allocation, move input | `make_move.py`, `game_end.py`, `notation.py`, `search.py` | Adds insufficient material; SAN input matches legal moves the same way `MoveCheck` does |
| `EVALU.CH` | Material (pawn 256), piece-square tables built before each search, pawn structure from file sets, mating evaluation, incremental `StateValu` | `evaluation.py` | Centipawns; a full recount each time, with incremental scoring as a sidebar |
| `SEARCH.CH` | Iterative deepening, aspiration window, alpha-beta, PVS, killers, capture search, check and seventh-rank extensions, draw scoring, mate search | `search.py`, `move_ordering.py`, `transposition_table.py` | Structured loops and `try/finally` replace `goto`; one idea per period |
| `TALK.CH` | Main loop, menus, opening library, hint, thinking on the opponent's time, board editor, `MATE` file loader | `uci_engine.py`, `opening_book.py`, `fen.py` | The GUI replaces menus; the book is readable text; positions load from FEN |
| `DISPLAY.CH`, `INPUT.CH`, `TIMELIB.CH` | DOS screen, keyboard, and clock | `print_board()`, `time.perf_counter()` | The GUI draws the board |

GameWorks has no transposition table, no FEN, and no insufficient-material rule. Remus
adds all three. Thinking on the opponent's time ("pondering") stays out of the core
course; a fast pair can try it after Day 10.

## Connecting Remus to python-chess and a GUI

`python-chess` is a library, not a GUI. Remus uses it in four places, all outside the
engine, and the engine never imports it.

1. **GUI play through UCI.** Lucas Chess starts a launcher and talks to Remus over stdin and
   stdout. `remus.bat` changes to its own folder and runs `uv run python
   uci_engine.py`. For students who take Remus home to a Mac or Linux computer,
   `remus.sh` does the same; it must be marked executable with `chmod +x remus.sh`, and
   it calls `uv` by its full path (usually `~/.local/bin/uv`) because a desktop app
   does not read the shell's `PATH`.
2. **Matches and the tournament.** `play_match.py` and `station_match.py` use
   `chess.engine.SimpleEngine.popen_uci()` to start two Remus processes and play them
   on a `chess.Board`, and `station_match.py` saves every game as PGN with `chess.pgn`.
   python-chess rejects any illegal move
   an engine sends, so match play doubles as a rules test.
3. **Reference checks in tests.** The tests in each period folder compare Remus perft counts, legal move lists,
   FEN round trips, SAN text, and game results with `chess.Board` on the same position.
   Each test writes the expected value before the comparison.
4. **Pictures.** `show_board.py` copies a Remus board into a `chess.Board` and saves
   `chess.svg.board()` as `board.svg` beside the script, with arrows for moves from
   Day 3 on. It only draws; the rules stay in Remus.

Three habits keep the UCI link from breaking: print protocol lines with `flush=True`;
send all debug text to `sys.stderr`; and never print anything when a module is imported.
