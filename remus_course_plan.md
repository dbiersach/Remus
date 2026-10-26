# Turning a Chess Engine into Science AI: Remus Course Plan

This plan turns the [workshop roadmap](workshop_roadmap.md) into a
two-week course for students about 13 years old: 10 days, four 90-minute periods a day,
60 class hours in all. Students work in pairs. They learn the Python they need in short
labs, and then they write real sections of Remus: small functions that go into the
class engine and stay there.

The plan also maps the ideas in Borland's Turbo GameWorks Chess 4.0 (Kaare Danielsen,
1985 to 1987) onto the modules Remus grows, and shows where Remus connects to
`python-chess` and a desktop GUI so the class never has to build one. The standing rules
in [`CLAUDE.md`](CLAUDE.md) apply to everything below.

## Decisions this plan is built on

| Question | Decision |
| --- | --- |
| Length | Two weeks, 10 days, 4 periods of 90 minutes a day (6 class hours) |
| Daily schedule | 8:30 to 10:00 Period 1; 10:00 to 10:30 break; 10:30 to 12:00 Period 2; 12:00 to 1:00 lunch; 1:00 to 2:30 Period 3; 2:30 to 3:00 break; 3:00 to 4:30 Period 4 |
| Students | 20 students in 10 pairs: a driver types, a navigator reads and checks; they swap every period. Ten pairs keep each adult to about five pairs during labs |
| Staff | The teacher plus at least one assistant |
| Laptops | 10 identical Windows 11 laptops, one per pair, preconfigured with git, `uv`, VS Code, and En Croissant |
| GUI | En Croissant on every laptop |
| Repositories | The teacher's laptop holds the main class repository. Each pair has its own local repository and pulls from the teacher over the classroom network. No GitHub accounts: the students are minors |
| Take-home | On the last day each pair copies its repository, with its full history, onto a USB drive |
| Folder layout | A flat `remus/` folder of modules that import each other by name; pytest finds them through `pythonpath = ["remus"]` |
| Squares | `(row, col)` tuples inside the engine, row 0 is rank 8 and column 0 is file a |
| Human move text | Standard algebraic notation (SAN) for typing and displaying moves: `d4`, `Nc3`, `Bxh8`, `O-O`, `e8=N+` |
| GUI move text | UCI (`e2e4`, `e7e8q`), because that is what the GUI protocol uses |
| First GUI game | Day 7, as soon as the rules pass perft and the game can end correctly |
| Unplugged warm-ups | 10 to 15 minutes at the desk with paper and cards before each hard idea, taken from the teacher's explanation time, never from coding time |
| Tournament | A full round robin of the 10 pair engines on Day 10 |
| Mate puzzles | The ten GameWorks `MATE.00x` positions live in `tests/mate_puzzles.epd`: nine mates in 2 and one mate in 3 (`MATE.008`), each with its single key move, checked with python-chess |

## The shape of the two weeks

Week 1 builds Python skills and the rules of chess. Week 2 turns the rules into a game,
plugs it into a GUI, and teaches Remus to think.

| Day | Theme | Python skills lab | Remus can do this by 4:30 |
| --- | --- | --- | --- |
| 1 | Setup and the board | Running scripts, strings, `ord` and `chr`, lists, nested lists | Print the board; convert `e2` to `(6, 4)` and back |
| 2 | Functions and records | Functions, type hints, tuples, `assert`, pytest, dicts, dataclasses, copying | Hold a game state; make and undo a quiet move or capture |
| 3 | Loops that walk the board | `while`, `break`, direction tuples, building lists | Generate king, knight, slider, and pawn moves |
| 4 | Legal moves | Modules, imports, `__main__`, git | Detect attacks and check; keep only legal moves |
| 5 | Special moves | Sets and dict lookups | Castling, en passant, promotion and underpromotion, with exact undo |
| 6 | Counting the tree | Recursion | Perft matches the reference counts; Week 1 review |
| 7 | Notation and a whole game | `split`, `join`, exceptions, `random`, `max` with `key=`, stdin and stdout | FEN and SAN; end the game; play random and greedy moves in a GUI |
| 8 | Judging a position | Recursion review, constants | Evaluate a position; search with minimax and negamax |
| 9 | Searching smarter | `sorted` with `key=`, `time` | Alpha-beta, quiescence, move ordering, iterative deepening |
| 10 | Upgrades and tournament | Dicts as caches | One upgrade per pair; class tournament |

Week 1 is Days 1 to 5 and Week 2 is Days 6 to 10. Week 1 ends with every special move
in place, and Week 2 opens with recursion and perft. Perft on Monday gives every pair a
verified checkpoint after the weekend, and the Week 1 review in Day 6 Period 4 catches
anyone who fell behind before the game work starts.

### Progressive elaboration

Every functional area starts with the smallest correct version and grows in later
periods. The engine as a whole gets two big passes: first it plays **legal** moves (end
of Day 7), then it plays **good** moves (Days 8 to 10).

| Area | Version 1 | Version 2 | Version 3 | Version 4 and later |
| --- | --- | --- | --- | --- |
| Board | 8x8 list of lists, printed (D1) | Square names (D1) | FEN in and out (D7) | Piece lists, 0x88 as a "how 1987 did it" sidebar (D10 optional) |
| Make and undo | Quiet moves and captures (D2) | Castling, en passant, promotion (D5) | Clocks, history, repetition keys (D7) | Undo inside search with `try/finally` (D8) |
| Move generation | King and knight jumps (D3) | Sliders and pawns (D3) | Legal filter: make, test the king, undo (D4) | Captures first, MVV-LVA, killers (D9, D10) |
| Attacks | Loop over enemy pieces (D4) | Look outward from the square (D4) | Castling and legality use it (D5) | King safety in evaluation (D10 station) |
| Game end | Checkmate and stalemate (D7) | Fifty-move rule (D7) | Threefold repetition (D7) | Insufficient material, fivefold, 75-move (D7) |
| Notation | UCI text (D2) | FEN (D7) | SAN out (D7) | SAN in, by matching legal moves (D7) |
| Choosing a move | Random legal move (D7) | Greedy: biggest capture (D7) | Minimax, then negamax (D8) | Alpha-beta, quiescence, ordering, iterative deepening (D9), PVS and a transposition table (D10) |
| Evaluation | Material count (D8) | Piece-square tables (D8) | Mate scores that prefer the faster mate (D8) | Pawn structure, mating evaluation, castling bonus (D10) |
| Interface | Console printout (D1) | Console game in SAN (D7) | UCI in a GUI (D7) | `info` lines, time control, `stop` (D9) |

## How students write real Remus code

Students write about 40 small functions over the two weeks. Each one is short enough
for a pair to finish in 20 to 40 minutes, and each one ships in the engine.

1. **The scaffold.** Before the period, the teacher's checkpoint holds the function's
   signature, its NumPy docstring, and tests that fail. The body says `raise
   NotImplementedError`.
2. **The pair writes the body** until `uv run pytest tests/test_<topic>.py` passes and
   the module's own self-check prints the expected answer.
3. **Show and choose.** Two or three pairs show their version on the projector. With 10
   pairs and about 40 functions, the teacher rotates who presents so every pair ships
   three or four functions over the course. The class picks one for clarity, not cleverness, and the teacher commits it to the main
   class repository. `CONTRIBUTORS.md` records which pair wrote which function, by a
   team name the pair chooses rather than full names, since the code goes home with
   every student.
4. **Everyone moves on together.** At the start of the next period each pair fetches
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
| Hand in an engine for the tournament | Pair | `git bundle create <team>.bundle --all` onto the class USB stick; the teacher fetches each bundle into a branch on the tournament laptop |
| Take it home | Pair | `git clone --no-hardlinks . <usb>/remus` copies the source and full history but not the `.venv` folder, which only works on the laptop that built it. At home: install `uv`, run `uv sync`, register `remus.bat` in En Croissant. A student with a Mac or Linux computer at home uses `remus.sh` instead |

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
| 5 | D3 P1 | `while`, `break`, `continue`, lists of direction tuples, `append`, list comprehensions (lightly) | Walk from `d4` toward the edge in one direction, stopping at a piece |
| 6 | D4 P1 | Modules, `import`, `if __name__ == "__main__"`, git `fetch`, `switch -c`, `commit`, `log` | Split yesterday's code into two files and import one from the other |
| 7 | D5 P1 | Sets, membership with `in`, dict lookups, string replacement | Castling rights as the string `"KQkq"`: remove `"K"` when the h1 rook moves |
| 8 | D6 P1 | Recursion: base case, recursive case, call stack | Count down; count the leaves of a small tree; count paths of a knight |
| 9 | D7 P1 | `split`, `join`, `int()`, exceptions with `try` and `ValueError` | Read a FEN string and print its six fields |
| 10 | D7 P3 | `random.choice`, `max` with `key=`, `sys.stdin`, `print(..., flush=True)`, `sys.stderr` | A tiny program that echoes lines, then answers `isready` with `readyok` |
| 11 | D9 P1 | `sorted` with `key=`, `time.perf_counter()`, `float("inf")` | Sort captures by victim value; time a perft run |
| 12 | D10 P1 | Dicts as caches, tuples as keys, `threading.Event` (teacher demo) | Remember perft counts already computed |

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
| D8 P3 | **Paper minimax.** A printed two-ply tree with scores on the bottom row. Pairs back up max and min level by level and circle the best move; the class compares answers before `minimax()` runs on the same tree | Minimax | Tree worksheet |
| D9 P1 | **Fewest flips.** The same tree as a row of face-down index cards. Pairs turn a card only when the answer could still change; the pair with the fewest flips and the right move wins | Alpha-beta pruning | Deck of score cards |
| D10 P4 | **Find the hidden peak.** A 10x10 grid hides a hot spot. With five "measurements" (the teacher reads the value at a square), each pair chooses where to measure next and marks its guess | How the NSLS-II AI agent chooses the next measurement, the Science AI link | Grid worksheet |

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
| Stalemate | No legal move and not in check is a draw | D7 P2 |
| Threefold repetition | Same pieces, same side to move, same castling and en passant rights, three times, not necessarily in a row. Claimable; fivefold ends the game automatically | D7 P2 |
| Fifty-move rule | 50 moves by each side (100 plies) without a capture or pawn move. Claimable at 50, automatic at 75 | D7 P2 |
| Insufficient material | K vs K, K+B vs K, K+N vs K, and K+B vs K+B with same-colored bishops are draws | D7 P2 |
| Piece values and tactics | Pawn 1, knight 3, bishop 3, rook 5, queen 9; fork, pin, skewer | D8 P1 |

## Teacher preparation

1. **Build the reference engine first.** The teacher's Remus is complete before the
   course, with a scaffold tag and a solution tag for every period (`d3-p2-start`,
   `d3-p2-end`). The start tag holds the stubs and failing tests; the end tag holds
   the teacher's answer, which a pair can check out if it falls behind.
2. **Finish the laptop image.** The 10 Windows 11 laptops arrive with git, `uv`, VS Code,
   and En Croissant. Check that the image also has Python 3.14 cached by `uv` and the
   VS Code extensions from `install_vscode_extensions.ps1`. Clone the class repository as
   described in "Sharing code without GitHub", then run `uv sync` and `uv run pytest`
   on every laptop before Day 1, so no laptop needs the internet on Day 1.
3. **Register Remus in En Croissant.** Add the reference Remus as a local engine through
   `remus.bat` and play one full game on one laptop. If the image is identical, the same
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
   check that every laptop runs `uv run pytest` and opens En Croissant.
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
  the Sargon and Rimush story from `CLAUDE.md`. Form pairs, check every laptop runs
  `uv run pytest`, and review SAN and UCI notation on the demonstration board.
- **P2. Python lab 1:** scripts, strings, `ord` and `chr`, f-strings.
- **P3. Python lab 2:** lists and nested lists. Unplugged warm-up: "Call the square"
  drills "row 0 is rank 8" on the printed board before anyone types it.
- **P4. `board.py`.** The teacher writes `new_board()`.
  **Students write:** `print_board()`, `square_name(row, col)`,
  `parse_square(name)` (which rejects `"i9"`), `piece_at(board, square)`.

**Checkpoint `d1-p4-end`:** `uv run remus/board.py` prints the start board and
"b1 holds N, expected N".

### Day 2: Functions and records

- **P1. Python lab 3:** functions, type hints, tuples, `assert`, pytest.
- **P2. Python lab 4:** dicts, dataclasses, aliasing, copying.
- **P3. `game_state.py` and `moves.py`.** The teacher writes the state dict in
  `new_game()` and the `Move` dataclass (`from_square`, `to_square`, `promotion`).
  **Students write:** `is_white(piece)`, `color_of(piece)`, `move_to_uci(move)`,
  `move_from_uci(text)`.
- **P4. `make_move.py`, ordinary moves.** Unplugged warm-up: "Undo from the card."
  The teacher writes `make_move()` returning an undo record.
  **Students write:** `undo_move()` for quiet moves and captures, and
  `state_snapshot(state)` for the "make ten moves, undo ten moves, compare" test.

**Checkpoint `d2-p4-end`:** ten moves made and undone return the exact start state.

### Day 3: Loops that walk the board

- **P1. Python lab 5:** `while`, `break`, direction tuples.
- **P2. Jumping pieces.** Unplugged warm-up: "Shade the reach." The teacher writes
  `knight_moves()` from an offset list.
  **Students write:** `king_moves()` the same way. Exercise: a knight on `a1` has two
  moves, to `b3` and `c2`.
- **P3. Sliding pieces.** **Students write:** `slide(board, square, direction)`, the
  loop that walks one direction and stops at the first piece, capturing it if it is
  an enemy. The teacher writes `slider_moves()` that calls it with rook, bishop, and
  queen directions. Exercise: a rook on an empty board has 14 moves.
- **P4. Pawns.** **Students write:** `pawn_pushes()` (single step and double step from
  the start rank). The teacher writes pawn captures and the four promotion choices.
  Exercise: `pseudo_legal_moves()` from the start returns 20.

**Checkpoint `d3-p4-end`:** 20 pseudo-legal moves from the start position.

### Day 4: Legal moves

- **P1. Python lab 6:** modules, imports, `__main__`, git.
- **P2. Attacks.** Refresher on check, pins, and discovered check. `attacks.py`
  version 1 loops over the enemy pieces, as GameWorks `Attacks` does. Version 2 stands
  on the square and looks outward like a "super piece."
  **Students write:** `attacked_by_knight()`, `attacked_by_pawn()`, `attacked_by_king()`.
  The teacher writes the sliding-line part, which reuses `slide()`.
- **P3. Check and the legal filter.** Unplugged warm-up: "Pin hunt." **Students write:** `in_check(state, color)` and
  `legal_moves(state)`: make each pseudo-legal move, reject it if the mover's king is
  attacked, undo it.
- **P4. Practice positions.** Pairs build tests for the workshop's first three
  verification exercises: 20 moves from the start, a king in check, and a pinned piece.

**Checkpoint `d4-p4-end`:** a pinned knight has zero legal moves; a king in check has
only escapes.

### Day 5: Special moves

- **P1. Python lab 7:** sets, `in`, string replacement for castling rights.
- **P2. Castling.** Refresher with the five conditions on the board. The teacher writes
  castling generation and the attacked-square checks.
  **Students write:** `update_castling_rights(rights, move, captured)`, the table of
  which moves remove `K`, `Q`, `k`, or `q`, including a rook captured on its home square.
- **P3. En passant and the double step.** **Students write:** the line in `make_move`
  that sets the en passant target after a double step, and `en_passant_victim_square()`.
  The teacher writes the en passant make and undo.
- **P4. Promotion and underpromotion.** Puzzle: promoting to a knight wins, promoting to
  a queen stalemates. **Students write:** promotion in `make_move` and `undo_move`.
  Pairs write tests from the workshop's special-move checklist.

**Checkpoint `d5-p4-end`:** every special-move test passes, and every special move
undoes exactly.

## Week 2: A game, a GUI, and a thinking engine

### Day 6: Counting the tree

- **P1. Python lab 8:** recursion.
- **P2. Perft.** Unplugged warm-up: "Count by hand." **Students write:**
  `perft(state, depth)`, the recursive count of leaf
  positions. The teacher writes `divide()`, which prints the count under each root move.
  Expected: 20, 400, 8,902 from the start.
- **P3. Perft against python-chess, and bug hunt.** `tests/test_perft.py` compares Remus
  with `python-chess` on the standard positions. The teacher plants three bugs in a copy
  (en passant pawn left on the board, castling through check, a missing promotion
  piece); pairs race to find them with `divide`.
- **P4. Week 1 review and catch-up.** Pairs that are behind check out `d6-p3-end`; pairs
  that are ahead time perft at depth 4 (197,281) and look for the slowest function.

**Checkpoint `d6-p4-end`:** perft matches the reference at depth 3 for the start and
the standard positions. Rule 6 of `CLAUDE.md` is now met.

### Day 7: Notation and a whole game

- **P1. Python lab 9:** `split`, `join`, exceptions. Then `fen.py`.
  **Students write:** `fen_placement(board)` (the part of FEN before the first space)
  and `board_from_placement(text)`. The teacher writes the other five FEN fields.
- **P2. Ending the game.** Refresher on stalemate, repetition, the fifty and 75-move
  rules, and insufficient material, with a six-position quiz. The teacher writes the
  halfmove clock and `position_key()`. **Students write:** `insufficient_material(board)`
  and the result-and-reason checks in `game_result(state)`.
- **P3. SAN and the console game.** The teacher writes `move_to_san()`, including
  disambiguation (`Nbd2`) and the `+` and `#` suffixes. **Students write:**
  `parse_san(state, text)`, which builds the SAN of every legal move and returns the one
  that matches what the player typed. Then `console_game.py` lets two people play in SAN.
  Python lab 10 (stdin, stdout, `random`, `max` with `key=`) closes the period.
- **P4. First brains and the GUI.** **Students write:** `random_move()` and
  `greedy_move()` (take the most valuable capture, else a random move). The teacher
  writes `uci_engine.py` and the launchers. Every pair registers Remus in the GUI and
  plays greedy Remus. `tools/play_match.py` plays random Remus against greedy Remus for
  20 games and prints the score.

**Checkpoint `d7-p4-end`:** a full game in the GUI ends with the correct result and
reason. This is the "legal moves" milestone.

### Day 8: Judging a position

- **P1. What makes a position good?** Pairs rank three positions and write one reason
  each; those reasons become evaluation terms. **Students write:** `material(board)` in
  centipawns (pawn 100, knight 300, bishop 300, rook 500, queen 900), scored for White.
- **P2. Piece-square tables.** A knight on `d4` attacks eight squares; on `a1` it
  attacks two. **Students write:** one table each (knight, bishop, rook, pawn, king);
  the class votes on each table that goes into Remus. The teacher writes
  `explain_evaluation()`, which prints every term so Remus can say why it prefers a
  position.
- **P3. Minimax.** Unplugged warm-up: "Paper minimax," with the optional human tree at
  the front of the room. The teacher writes `minimax()` to depth 2 with a node
  counter, and pairs compare its answer with their worksheets.
- **P4. Negamax and mates.** The teacher rewrites the search as `negamax()` with
  `try/finally` around each make and undo. **Students write:** the leaf scoring when
  there are no legal moves (checkmate scores `-(MATE_SCORE - ply)` so Remus prefers the
  faster mate; stalemate scores 0), and the test that the root state is unchanged after
  every search.

**Checkpoint `d8-p4-end`:** Remus finds every mate in 1 and mate in 2 in the test set.

### Day 9: Searching smarter

- **P1. Python lab 11** and alpha-beta. Unplugged warm-up: "Fewest flips" finds the
  cards nobody needs to turn over. The teacher writes `alpha_beta()` beside `negamax()`.
  **Students write:** the comparison script: for ten positions, both must pick the same
  move and score, and alpha-beta must count fewer nodes.
- **P2. The horizon effect and quiescence.** Puzzle: at depth 2 Remus takes a defended
  pawn with its queen. The teacher writes `quiescence()`. **Students write:**
  `capture_moves(state)`, the filter quiescence searches.
- **P3. Move ordering.** **Students write:** `mvv_lva_score(move, board)` (most valuable
  victim, least valuable attacker) and the `sorted(..., key=...)` call that uses it.
  Pairs measure node counts before and after. The teacher adds the check extension.
- **P4. Iterative deepening, the clock, and UCI info.** The teacher writes the deepening
  loop, reads `go movetime`, `wtime`, `btime`, `winc`, and `binc`, and moves the search
  into a thread with a stop flag. **Students write:** `format_info(depth, score, nodes,
  pv)`, which prints `info depth 3 score cp 35 nodes 4120 pv e2e4 e7e5 g1f3` so the GUI
  shows Remus thinking.

**Checkpoint `d9-p4-end`:** Remus at depth 3 or more beats greedy Remus in a 10-game
match and never loses on time.

### Day 10: Upgrades and tournament

- **P1 and P2. Upgrade stations.** Python lab 12 opens P1. Each pair picks one station,
  builds it, and shows a measured gain: fewer nodes, deeper search in the same time, or
  more match points. With 10 pairs and eight stations, two stations get a second pair,
  and those pairs compare their measurements at the end of P2.

| Station | What the pair builds | GameWorks idea it echoes |
| --- | --- | --- |
| Transposition table | A dict from `position_key` to depth, score, bound (`exact`, `lower`, `upper`), and best move | (not in GameWorks) |
| Opening book | `opening_book.txt` of SAN move lines from openings the students like; every move is checked with `legal_moves()` | `OPENING.LIB` |
| Killer moves | Two quiet moves per ply that caused a cutoff, tried right after captures | `KillingMove` |
| Pawn structure | Penalties for doubled and isolated pawns, a bonus for passed pawns | `PawnStrVal`, `PassPawnRank` |
| Mating evaluation | With a big material lead, push the losing king to the edge and bring the winning king close | `Mating` mode in `CalcPVTable` |
| Principal variation search | Full window on the first move, null window on the rest, re-search on a surprise | `ZeroWindow` in `SEARCH.CH` |
| Draw sense | Score a repeated position as 0 inside the search | `DrawGame` |
| Mate solver | Solve the ten GameWorks puzzles with a mate-only search | `MateSearch` and `MATE.00x` |

- **P3. Tournament.** `tools/tournament.py` (python-chess) runs a full round robin: each
  of the 10 engines plays every other engine once, 45 games in all, with colors
  balanced. At 2 minutes plus 1 second a move per side, a game lasts at most about 6
  minutes. Four games at once on the teacher's laptop (eight engine processes, so a
  laptop with at least 8 cores) finish the 45 games in about 70 minutes. The
  script saves every game as PGN and prints the standings after each round on the
  projector. Each pair hands in its engine as a git bundle on the class USB stick
  during P2. Pairs replay their wins and losses in En Croissant.
- **P4. Presentations, take-home, and wrap-up.** Unplugged warm-up: "Find the hidden
  peak" connects choosing a move to choosing an experiment. Each student copies the pair's repository
  to their own USB drive with `git clone --no-hardlinks`, then checks that the copy opens.
- **Presentations.** Each pair explains one move its engine chose, with
  the score and principal variation. Close with what comes next: bitboards, Zobrist
  hashing, null-move pruning, endgame tablebases, and a stronger "Manishtushu" engine.

**Checkpoint `d10-p4-end`:** the tournament finishes with no illegal moves, crashes, or
lost synchronization.

## Code breakdown by day

The engine lives in one flat folder of plain modules. Each module ends with a visible
self-check, as `CLAUDE.md` requires, so a pair can run any file with
`uv run remus/perft.py`.

| File | Created | Grows on | Holds |
| --- | --- | --- | --- |
| `remus/board.py` | D1 | D10 (optional piece list) | Board, coordinates, printing |
| `remus/game_state.py` | D2 | D5, D7 | State dict, `new_game()` |
| `remus/moves.py` | D2 | D3 (promotion) | `Move` record, UCI text |
| `remus/make_move.py` | D2 | D5, D7 | `make_move()`, `undo_move()`, undo record |
| `remus/move_generation.py` | D3 | D4, D5 | Pseudo-legal and legal moves |
| `remus/attacks.py` | D4 | D10 (king safety) | `is_square_attacked()`, `in_check()` |
| `remus/perft.py` | D6 | | `perft()`, `divide()` |
| `remus/fen.py` | D7 | | FEN in and out |
| `remus/notation.py` | D7 | | SAN in and out |
| `remus/game_end.py` | D7 | | `game_result()` and reason |
| `remus/console_game.py` | D7 | | Two people play in SAN; later, a person against Remus |
| `remus/search.py` | D7 | D8, D9, D10 | Random, greedy, minimax, negamax, alpha-beta, quiescence, iterative deepening |
| `remus/uci_engine.py` | D7 | D9 | UCI loop |
| `remus/evaluation.py` | D8 | D10 | Material, tables, explanation |
| `remus/move_ordering.py` | D9 | D10 | MVV-LVA, killers |
| `remus/transposition_table.py` | D10 | | Station |
| `remus/opening_book.py`, `remus/opening_book.txt` | D10 | | Station |
| `remus.bat` | D7 | | En Croissant launcher on the class laptops |
| `remus.sh` | D10 | | Take-home launcher for students with a Mac or Linux computer at home |
| `tools/play_match.py`, `tools/tournament.py` | D7, D10 | | python-chess match runners (dev only) |
| `tests/test_<topic>.py` | every period | | Expected results written first |
| `labs/dayNN/<skill>.py`, `labs/dayNN/instructor/<skill>_instructor.py` | each lab | | Python skills labs: student file with blanks, instructor file with answers |
| `tests/mate_puzzles.epd` | before D1 | | The ten GameWorks mate puzzles as FEN |
| `CONTRIBUTORS.md` | D1 | every period | Which pair wrote which function |

When a newer version teaches by comparison, the older function stays beside it:
`minimax` and `alpha_beta` both remain in `search.py` so pairs can print node counts
side by side. When a newer version only replaces the older one, as in the attack test,
the older code survives in the checkpoint tag.

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

`python-chess` is a library, not a GUI. Remus uses it in three places, all outside the
engine, and the engine never imports it.

1. **GUI play through UCI.** En Croissant starts a launcher and talks to Remus over stdin and
   stdout. `remus.bat` changes to its own folder and runs `uv run python
   remus/uci_engine.py`. For students who take Remus home to a Mac or Linux computer,
   `remus.sh` does the same; it must be marked executable with `chmod +x remus.sh`, and
   it calls `uv` by its full path (usually `~/.local/bin/uv`) because a desktop app
   does not read the shell's `PATH`.
2. **Matches and the tournament.** `tools/play_match.py` uses
   `chess.engine.SimpleEngine.popen_uci()` to start two Remus processes, plays them on a
   `chess.Board`, and saves PGN with `chess.pgn`. python-chess rejects any illegal move
   an engine sends, so match play doubles as a rules test.
3. **Reference checks in tests.** `tests/` compares Remus perft counts, legal move lists,
   FEN round trips, SAN text, and game results with `chess.Board` on the same position.
   Each test writes the expected value before the comparison.

Three habits keep the UCI link from breaking: print protocol lines with `flush=True`;
send all debug text to `sys.stderr`; and never print anything when a module is imported.
