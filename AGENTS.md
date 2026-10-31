# Remus Project Rules and Python Style Guide

Remus is a chess engine written in pure, native Python as a teaching project for the
**"Turning a Chess Engine into Science AI"** workshop. The course plan,
[`misc/docs/course/remus_course_plan.md`](misc/docs/course/remus_course_plan.md), holds the
teaching principles, the thirteen lessons and their gates, and the day-by-day schedule;
read it before starting any lesson. [`misc/docs/engine_comparison/remus_program_overview.md`](misc/docs/engine_comparison/remus_program_overview.md)
explains how the code fits together.

This file holds every project and style rule, so that every AI tool used with this
repository builds Remus the same way. `CLAUDE.md` imports it and adds only the rules
that are specific to Claude Code. The Python style follows David's course repositories
(qis101, scicomp101, cse101), adapted for a chess engine and a younger audience.

# Part 1: The project

## Why the name "Remus"

- **Sargon (1978)** was the landmark microcomputer chess program by Dan and Kathe
  Spracklen. Written in Z80 assembly for the Wavemate Jupiter II, it won the first
  microcomputer chess tournament (West Coast Computer Faire, 1978) with a perfect 5-0.
  Its complete source was published as a book, *Sargon: A Computer Chess Program*
  (Hayden, 1978), so people could read and learn from a real engine. It spawned Sargon II,
  2.5, III (ported to the first Macintosh), and later commercial versions.
- **Sargon of Akkad** (c. 2335 to 2279 BC, middle chronology) founded the Akkadian Empire,
  the first known great empire. He was succeeded by his sons **Rimush** (c. 2279 to 2270
  BC), who put down widespread revolts and was possibly assassinated by courtiers, and then
  **Manishtushu** (c. 2270 to 2255 BC), who campaigned south along the Tigris and into the
  Persian Gulf. Manishtushu's son Naram-Sin brought the empire to its height.
- **Remus** echoes **Rimush**, the first son and heir of Sargon. The engine is meant to be
  a "son of Sargon": an heir to that tradition of small, readable chess programs whose
  internals are laid open for learners, rebuilt in modern Python.
- The name leaves room for the family line: a later, stronger engine could take the name
  of the next heir (Manishtushu) or grandson (Naram-Sin).

## Project goals

- Build a legal, complete chess engine one understandable lesson at a time.
- A working game comes first; stronger play comes later.
- Every lesson: explain the chess idea, show the code, inspect a small example, end with
  an exercise. Success means a learner can explain a move, trace an undo, and say why a
  search result is legal and preferred.

## Audience and course format

- Remus is an instructional engine for a **two-week, 60-hour course** taught to
  students about **13 years old**: 10 days, four 90-minute periods a day (8:30 to 10:00,
  10:30 to 12:00, 1:00 to 2:30, 3:00 to 4:30). The day-by-day plan lives in
  [`misc/docs/course/remus_course_plan.md`](misc/docs/course/remus_course_plan.md), and the code is split into modules
  and checkpoints that follow that plan period by period.
- 20 students work in **10 student pairs** (driver and navigator, swapping every period). Each
  student pair gets an identical, preconfigured **Windows 11** class laptop with VS Code and
  Lucas Chess. Remus targets Windows only (David, 2026-10-28): the
  repository holds no Mac or Linux launchers or setup scripts.
- Python skills labs come before the engine code that needs each skill. Students
  **write real Remus code**: small functions with a ready-made signature,
  docstring, and failing tests. The class picks one student pair's version as the clearest, and
  `CONTRIBUTORS.md` records who wrote it. Keep student functions short enough for a student pair
  to finish in 20 to 40 minutes.
- **Student pairs write the most important and most enlightening code, never plumbing**
  (David, 2026-10-27). Each student function holds a central idea of the lesson, such
  as making a move and recording its undo, negamax's sign flip, an alpha-beta cutoff,
  or quiescence standing pat, in code simple enough that a student pair can explain every line
  it types. Text formatting, protocol strings, and helpers that only move data around
  stay given code. A lab must never become a typing exercise.
- **No hands-on lab asks a student pair to type more than about 30 to 40 lines of code** in
  one period, counted across every function and lab blank of that period (David,
  2026-10-27). Many 13-year-olds cannot touch-type, so a longer lab spends class time
  on typing instead of thinking. When an idea needs more code, the course designer writes the
  rest beforehand as given code and the student pair writes the core. The teacher
  writes no code during the workshop (David, 2026-10-31): every line a student pair
  does not type is already in the period folder. `make_student_folders.py` prints the
  largest count per period and flags any period above `MAX_TYPED_LINES = 40`.
- Short unplugged warm-ups (paper, cards, and a printed board at the desk) come before
  the hardest ideas. They replace part of the teacher's explanation, never the time a
  student pair spends typing code.
- Students know how the pieces move. Lessons remind them of the rarer rules right before
  the code that needs each one: castling conditions, en passant, promotion and
  underpromotion, stalemate, threefold and fivefold repetition, the fifty and 75-move
  rules, and insufficient material.
- **Progressive elaboration.** Every functional area (board, make/undo, move generation,
  attacks, game end, evaluation, search, interface) starts with the smallest correct
  version, then gains completeness, then power, then efficiency in later blocks. The
  whole engine also gets two passes: first it plays legal moves, then it plays good moves.
- Every day ends with an engine that runs (on Day 10, Remus-GOLD). Each period's
  `student/` folder starts from the finished code of the periods before, so a student pair
  that falls behind rejoins by opening the next period's folder.
- Write code, comments, and lesson text for a 13-year-old reading the idea for the first
  time: short functions, concrete names, and one small example position per idea.
- The class never builds a GUI. Every laptop uses **Lucas Chess** (David,
  2026-10-27), which runs Remus as a UCI engine through `remus.bat`.
  [`misc/docs/course/lucas_chess_guide.md`](misc/docs/course/lucas_chess_guide.md) shows students, step by step
  with screenshots, how to add Remus and watch it play Stockfish at 1500 Elo.
  `python-chess` runs matches and checks results from outside the engine.
- **No GitHub for students.** They are minors, so they create no online accounts.
  Cloning the public repository needs none.
- **git and `uv` only at setup** (David, 2026-10-29). On Day 1, period 1, the teacher
  walks each student through installing git and `uv`, cloning the repository, and
  running `uv sync` once to build `.venv`. After that setup no student or teacher uses git or
  `uv` at any point in the workshop: no fetch, branch, commit, restore, or clone, and
  no `uv run`. Code never moves between laptops through git: each period's `student/`
  folder already holds the code it needs, the Day 9 battles copy an engine folder on a
  USB stick in File Explorer, and on Day 10 each student copies the Remus folder,
  without `.venv`, to a USB drive in File Explorer to take home. Never plan a step that
  needs a student account, pushes student code online, or asks a student or teacher
  to type a git or `uv` command after setup.
- `CONTRIBUTORS.md` credits student pairs by a team name they choose, not by full names.
- **Three people use the repository** (David, 2026-10-29), and every document names
  the right one:
  - **Students**, the student pairs, who write Remus in the `student/` folders.
  - **Teachers**, who run the class. A teacher does everything in VS Code: open a
    file and press the Run Python File button (`run_tests.py`, `play_match.py`,
    `play_battle.py`, `estimate_elo.py`, a lab, a demo) or open a Markdown page. No
    step of the two-week workshop asks a student or a teacher to type a command.
  - **The course designer** (David), who builds the course. The tools in
    `misc/scripts/` (the builders, `run_all_tests.py`, the league, the Stockfish
    ratings, the benchmark, and the parity check) are designer tools, and only they
    may need `uv run` in a terminal. Write "the designer's league", never "the
    teacher's league".
- Documents describe the course as it stands, with no dates of past events ("the
  league finished on 2026-10-28", "a survey from October 2026"), the same rule as
  for code comments. The David dates in this file record when a rule was set and
  stay here only.

## Hard rules for the engine code

1. **Clarity over speed.** Plain lists, dicts, tuples, strings, functions. Small classes
   or `dataclass` only when they make ownership clearer. Slow is fine.
2. **No third-party libraries inside the engine.** Standard library only. No bitboards,
   magic numbers, compiled extensions, clever caches, or framework machinery.
3. **Engine is the single source of truth** for board, rules, legal moves, game state,
   search, evaluation, and move choice. A GUI only sends moves and displays results.
4. **`python-chess` and Lucas Chess are boundary tools only.** Lucas Chess is the
   desktop GUI, which runs Remus over UCI. `python-chess` runs matches and serves as an
   external cross-check in tests, never as the engine's hidden implementation.
5. **Exact make/undo.** `undo_move(make_move(state, move))` must restore the full state,
   including clocks, rights, en passant target, side to move, and history. Search must
   leave the live position unchanged even if it stops early (use `try/finally`).
6. **Separate rules from search.** Legal move generation must be correct (perft-verified)
   before minimax, alpha-beta, books, tables, or GUI work. The one early exception is
   the ready-made UCI plug at the end of Day 5, which plays random legal moves so
   students see their rules on a real board; the UCI lesson itself waits for Day 7,
   after perft.
7. **One idea at a time.** Simple correct version first; an advanced version only with an
   explanation of why it is needed.
8. Opening books and endgame tables are optional boundary features. Validate every book
   move with the native generator; an absent book or table must never stop play.

## Representation conventions

- Board: 8x8 list of lists of one-character strings. Uppercase = White, lowercase =
  Black, `.` = empty.
- **Coordinates: row 0 is rank 8, column 0 is file `a`.** Repeat this in comments.
- State: a plain dict (or small `GameState`) with `board`, `turn`, `castling`
  (e.g. `"KQkq"`), `en_passant`, `halfmove_clock`, `fullmove_number`, `position_history`.
- Squares: `(row, col)` tuples inside the engine.
- Moves: a simple record with `from_square`, `to_square`, `promotion`.
- People type and read moves in standard algebraic notation (SAN: `d4`, `Nc3`, `Bxh8`,
  `O-O`, `e8=N+`). The GUI link uses UCI (`e2e4`, `e7e8q`). Convert only at the I/O
  boundary.

## Architecture boundaries

| Part | Responsibility |
| --- | --- |
| Native Python engine | Board, rules, legal moves, state, search, evaluation, move choice |
| Console printout | `print_board()` and each file's `main()` self-check, for lessons and debugging |
| UCI adapter | `uci`, `isready`, `ucinewgame`, `position startpos/fen ...`, `go`, `stop`, `quit`; protocol on stdout, debug on stderr; `bestmove 0000` only with no legal move |
| GUI | Lucas Chess, which starts `remus.bat` and hosts Remus as an external UCI engine |

The engine must run without Lucas Chess or `python-chess` installed.

## Lesson roadmap (summary)

1. Draw the board and convert coordinates
2. Describe a move; make/undo ordinary moves
3. Pseudo-legal move generation
4. Attacks, check, legal-move filter
5. Special moves: castling, en passant, promotion/underpromotion, double push
6. Record a complete game; FEN in/out; position history
7. End the game: mate, stalemate, repetition, fifty-move, insufficient material
8. Evaluate a position (material first, then explainable terms)
9. Search: minimax/negamax, then alpha-beta
10. Improve search: iterative deepening, ordering, quiescence, time limits, PV, null-window, PVS
11. Transposition table (plain dict), opening list, tablebase probing at the boundary
12. UCI loop and play in Lucas Chess
13. Science AI: aim the same generate, score, and choose loop at a hidden-peak
    measurement problem (`hidden_peak.py`), then the full tree search at X-ray phase
    identification (`phase_hunt.py`)

Each lesson has a "Ready to move on when" gate in the course plan. Don't skip a gate.

The course plan maps these 13 lessons onto the ten days. Students see their board as a
picture on Day 1 and their moves as arrows on Day 3, and play a random-move Remus in
Lucas Chess at the end of Day 5. The UCI lesson and the first real brains come on
Day 7, after perft has verified the rules.

## Verification

- Write expected results before running. Use small named positions (see the course plan's
  ten verification exercises: 20 moves from start, check, pins, castling cases,
  en passant cases, promotions, two queens, mate vs stalemate, repetition with rights,
  long make/undo sequences).
- Run `perft` against trusted reference counts; diagnose mismatches with divide by root move.
- For search lessons, record root moves, chosen move, score, PV, node count, and whether
  the root state is unchanged.

## Lesson rhythm

Name the rule, then draw a minimal position or tree, trace the state before and after,
write the simplest correct code together, run focused examples including one failure, let
learners extend it, and save open questions. Never drop in a complete optimized engine.

## Project setup

- Remus is a `uv` project on Python 3.14 (`.python-version`, `pyproject.toml`).
  Run `uv sync` once, then `uv run pytest` and `uv run ruff check .`.
- The project has no runtime dependencies. The `dev` dependency group holds
  `python-chess` (imported as `chess`), `pytest`, and `ruff`. Engine modules never
  import `chess`; only tests and optional display code (`show_board.py`) may.
- Lucas Chess is a desktop application, not a Python dependency. It hosts Remus as an
  external UCI engine and comes preinstalled on the class laptops.
- The top folder holds one folder per workshop day, named `Day NN - <what the new
  code does>`, such as `Day 04 - Keep only legal moves` (David, 2026-10-28). Each Day
  folder holds four period folders, `period1` to `period4`, and each period folder
  holds two folders: `instructor/`, the finished, ready-to-run reference code, and
  `student/`, the code students write and change. Each `instructor/` folder is a
  complete, runnable copy of Remus as it stands at the end of that period (Day 10
  holds only its science files, and Day 9 periods 2 to 4 hold no engine code: see
  below). Beside `instructor/` and `student/` sits one goals file for the period,
  such as `Day 03 Period 02 Goals.md` (David, 2026-10-29), which replaces separate
  instructor and student READMEs. It names the period, its new and growing files,
  and the functions student pairs write. Every period goals file and enhanced engine README
  also holds (David, 2026-10-27):
  - **Learning objectives** as a bulleted list, each with a **Measured by** line that
    says how the teacher sees a student pair has learned it: a named test that passes, a
    printed result, or something the student pair explains without running code.
  - **The changes and why**: one paragraph for every function or lab part the student pair
    writes, saying what the code does, why it is written that way, and how it fits
    the whole engine.
  Every enhanced engine README (David, 2026-10-28) also explains its enhancement in enough
  detail for a student pair to work from it alone: a worked example, why it makes Remus
  stronger, what it costs, a table of positions per depth and positions per second
  measured against Remus-WHITE, what to expect in games, and where the student pair's code
  is called from.
  Each Day folder also has one syllabus at its top, `Day NN Syllabus.md` (David,
  2026-10-28), that paints the whole day: what the day is about, its
  objectives, a table of the four periods with what the student pairs write in each, a timed
  sequence of activities for every period, and the checkpoint at 4:30.
  The text lives in `period_guides.py` (`OBJECTIVES`, `CHANGE_NOTES`, `LAB_NOTES`,
  `VERSION_OBJECTIVES`, `VERSION_GUIDES`, `VERSION_MEASURES`, `PERIOD_GUIDES`
  for a period that needs an illustrated guide, such as the Day 10 phase hunt, and
  `DAY_GUIDES` for the Day syllabi, which `make_student_folders.py` writes); the
  builders write it into the READMEs, so edit it there. The phase hunt pictures live
  in `misc/docs/images/phase_hunt/`, drawn by `uv run misc/scripts/make_phase_hunt_figures.py`,
  which installs matplotlib for itself alone. The chess board diagrams in the enhanced
  engine READMEs, the goals files, and the `misc/docs/engine_code/` pages live in
  `misc/docs/images/boards/`, drawn with python-chess's `chess.svg` by
  `uv run misc/scripts/make_board_diagrams.py`. `board_image()` and
  `goals_board_image()` in `period_guides.py` link a diagram into the README and
  goals text; the code pages link theirs by hand. Measure `VERSION_MEASURES` again after any
  change to an enhanced engine's search or evaluation.
  Each goals file also lists the timed steps of its period (from `DAY_GUIDES`) and
  a "What you edit this period" table with the line where
  each stub starts, the lines to type, and the tests that check it. Every goals
  file and enhanced engine README then has "The code you type" (David, 2026-10-29):
  for each function and lab part, the lines to type marked `+`, with the lines
  around them and their line numbers, where the code sits and what calls it, and
  how it works, from `CODE_NOTES` in `period_guides.py`.
  `make_student_folders.py` writes the code blocks from the code itself, and a test
  in `test_reference_tools.py` checks every quoted line against its file.
  `misc/docs/course/student_edit_plan.md` lists the edit plan for the whole course.
- Each Python skills lab lives in its own period folder (David, 2026-10-28; there is
  no separate `labs/` folder): the student file with `#` blanks, `<name>.py`, in the
  student period folder, and the answer file, `<name>_instructor.py`, in the
  instructor one. `period_guides.LABS` names the period of each. Both files are
  written by hand, and the builders read them before a rebuild and write them back,
  so edit a lab in place. Every period that has no Remus
  function for the student pairs holds a lab or a short demo (`demo_*.py`) with blanks,
  except Day 10, period 4 (David, 2026-10-28), where the student pairs report their science
  results and take their code home. Day 10 is about the science only; the chess
  matches end with the Day 9 battles.
  Demos that use the engine run only inside their period folder. Day 6, period 3
  also gets `bug_hunt/`, which `make_period_folders.py` builds by planting the three
  bugs of `PLANTED_BUGS` in a copy of the period's code.
  Nothing in a period folder imports from another folder. Modules import each other
  by name (`from board import new_board`), so any module runs from inside its folder
  with the Run button.
- Every course designer tool that is not part of an engine lives in `misc/scripts/`
  (David, 2026-10-28): the builders `make_period_folders.py`,
  `make_version_folders.py`, `make_student_folders.py`,
  `make_phase_hunt_figures.py`, `make_board_diagrams.py`, and `make_white_map.py`, the README text in `period_guides.py`,
  `run_all_tests.py`, `test_reference_tools.py`, `version_match.py`, `version_league.py`,
  `version_elo.py`, `remus_benchmark.py`, and `engine_parity.py`. Each one finds the
  top Remus folder from its own path, so it
  runs from the top folder with `uv run misc/scripts/<name>.py`. Students never open
  `misc/scripts/`. Files a student pair opens or runs in class stay beside the code they belong to:
  `play_battle.py` and `basic_test.py` in each engine folder for the battles
  (they run `misc/scripts/version_match.py`, David, 2026-10-29), and `play_match.py`, `estimate_elo.py`, and the tests inside their
  period and version folders. Put a new course designer tool in `misc/scripts/`, and list every
  script there in `misc/scripts/README.md` with what it does (David, 2026-10-28).
- `period4/instructor` holds the finished code of the day, and it is the only period
  folder to edit by hand. Day 9 is the exception (David, 2026-10-28): its engine, Remus-WHITE,
  is finished in `period1/instructor`, which is the folder to edit by hand, and
  periods 2 to 4 hold only their goals file and the period 2 lab.
  `make_period_folders.py` builds the other instructor period folders from it: its
  `ARRIVALS` table says in which period each file takes its finished form, and its
  `CHANGES` table says what the earlier periods leave out of a file that grows during
  the day. Run it after any change to the instructor code.
- Each period's `student/` folder mirrors the `instructor/` folder beside it. In each
  student folder, the functions the students write in that period are stubs: the
  signature and docstring stay and the body raises `NotImplementedError`, so the
  tests fail until a student pair writes the function. `make_student_folders.py` builds
  every `student/` folder from its `instructor/` sibling and lists every student function by day and period;
  run it after `make_period_folders.py`, and never edit a student stub by hand.
- The Remus versions live in the top `engines/` folder (David, 2026-10-29), which
  holds `engines/instructor`, `engines/student`, and `engines/Niram`. Each of
  `instructor` and `student` holds one engine folder per Remus version, named by its
  engine color. `00 Remus-WHITE - No enhancements` is Remus-WHITE,
  the finished Day 9 Remus with none of the ten enhancements (named by David on
  2026-10-27): a copy of the Day 9 `period1/instructor` folder in `instructor`
  and of `period1/student` in `student`, without `show_board.py`, which only the
  Day 1 and Day 3 lessons run. Every engine folder holds only three kinds of file
  (David, 2026-10-30): the files a game loads (`uci_engine.py`, `remus.bat`, and every
  module `uci_engine.py` imports), the match runners (`play_match.py`,
  `play_battle.py`, `basic_test.py`, `estimate_elo.py`), and the tests with the files
  they need (`perft.py`, `game_end.py`, `notation.py`, `mate_puzzles.epd`). Class
  demos and experiments, such as `compare_search.py`, stay in their period folders.
  Remus has no console game: every game runs in Lucas Chess or a match script. `01 Remus-GRAY - King safety` to `10 Remus-RED -
  Transposition table` are the ten enhanced engines, each Remus-WHITE plus one
  enhancement. `11 Remus-GOLD - All enhancements` is Remus-GOLD, the finished Remus with
  all ten (David, 2026-10-27), and only `engines/instructor` holds it. `engines/Niram`
  holds Niram, the same engine in Rust. Remus-GOLD is the engine of Day 10 (David,
  2026-10-28): the Day 10 period folders hold only the science files
  (`hidden_peak.py`, `phase_hunt.py`, their tests, and the results demo), and their
  READMEs point to Remus-GOLD for the engine, Lucas Chess, and `estimate_elo.py`.
  Remus-GOLD is written by hand, like a `period4/instructor` folder; edit the finished engine
  there. `make_version_folders.py` copies Remus-WHITE and builds the ten enhanced
  engines in `engines/instructor` from the Day 9 `period1/instructor` code and
  Remus-GOLD, and rewrites only the GOLD README. `make_student_folders.py` copies the
  Day 9 `period1/student` folder to `engines/student` as Remus-WHITE and stubs each
  enhanced engine's functions there; no student pair ever writes GOLD. The folder names use colors only so that no
  engine sounds better than another. A two-digit prefix (David, 2026-10-28) orders the
  folders by each version's Elo over WHITE in the designer's league (Niram league 1,
  660 games at 10 minutes a side, with GREEN's and GOLD's games started from move 1
  so their book plays): 01 Remus-GRAY, 02 Remus-YELLOW, 03 Remus-CYAN, 04 Remus-PINK, 05 Remus-ORANGE, 06 Remus-BROWN,
  07 Remus-PURPLE, 08 Remus-GREEN, 09 Remus-BLUE, 10 Remus-RED. `misc/scripts/version_match.py` plays an enhanced engine
  against Remus-WHITE or another enhanced engine, and `play_battle.py` in each engine folder
  runs it for the Day 9 battles. `version_league.py` plays a round robin of all 12
  versions, Remus-WHITE and Remus-GOLD included, and fits one Elo rating per version
  with Remus-WHITE pinned at 0. `version_elo.py` rates all 12 versions, and
  Niram with `--niram`, against Stockfish at four UCI_Elo levels near an
  even score, from frozen copies of the versions. With `--bracket` it sets each
  round's Stockfish level to the engine's rating so far; the bracket ratings of
  Remus-WHITE, Remus-GOLD, and Niram are the ones
  `misc/docs/engine_comparison/engines_elo.md` reports beside the league table.
- `engines/Niram` holds Niram, Remus-GOLD rewritten in Rust, named for
  Naram-Sin, Sargon's grandson: one Cargo package whose `src/` folder
  holds every Rust file. It is a course designer's tool that runs the same engine about
  15 times faster; students never edit it. Each `.rs` file matches the Python file of
  the same name, and Niram must visit exactly the same number of positions as
  Remus-GOLD at each depth (`cargo test --release` inside `engines/Niram`;
  `uv run misc/scripts/remus_benchmark.py GOLD` times Remus-GOLD on the same positions).
  `uv run misc/scripts/engine_parity.py` checks the two engines on 49 positions: evaluation,
  legal moves, book moves, and every depth's score, node count, and principal
  variation must match, and the results go to `misc/docs/engine_comparison/remus-niram same algorithms.md`. A
  change to Remus-GOLD's rules, evaluation, search, or opening book needs the same
  change in Niram and a clean `engine_parity.py` run. The Rust copies of WHITE
  and the ten enhanced engines were deleted (David, 2026-10-28) after Niram league 1, whose
  games stay in the games file: `version_league.py --niram --rate-only` rates those
  saved games, with Niram-WHITE pinned at 0, and `version_elo.py --niram` plays Niram
  against Stockfish beside the Remus versions. The
  Python style rules above do not apply to the Rust code, which follows `cargo fmt`
  and `cargo clippy`.
- Every game any script plays (`play_match.py`, `estimate_elo.py`,
  `version_match.py`, `version_league.py`, `version_elo.py`) is added to `misc/games/remus_games.pgn` at the top of the
  repository, which git ignores so each computer keeps its own games.
- A module keeps one file name from the day it appears to Day 10. When a later lesson
  makes a file smarter, the new code goes into the same file under a new function
  name next to the function it improves (`negamax`, then `alpha_beta`, then
  `upgraded_search`), and the older function stays. Never add version numbers to file
  names.
- The Science AI lessons are `hidden_peak.py` (Day 10, `period1` on) and
  `phase_hunt.py`, X-ray phase identification by tree search (Day 10, `period2`
  on). Both use the standard
  library only and do not import the engine: they reuse the engine's ideas, not its
  code.
- Tests sit next to the modules in each period folder. The module names repeat from
  folder to folder, so pytest runs one folder at a time
  (`uv run pytest "Day 04 - Keep only legal moves/period3/instructor"`);
  `uv run misc/scripts/run_all_tests.py` runs them all, and `uv run pytest` from the top
  folder runs `misc/scripts/test_reference_tools.py`. The ten mate puzzles,
  `mate_puzzles.epd`, sit beside `test_search.py` in every Day 8
  and Day 9 period folder and every version folder that reads them. A test
  that uses `python-chess` as a reference states the expected count in its docstring
  or assertion before comparing against Remus.
- Every `.py` file a student modifies or reads has a page, the
  "puzzle box top" for that file, in the docs folder of its kind (see below): the big picture first, then where it fits (uses and
  used by), words to know, a call tree, a plain-language line for each function, and
  questions. Each Python skills lab (`python_*.py`) has its page in
  `misc/docs/learning_python/` instead. Write the pages for middle school readers, in
  short sentences, and do not repeat the code's comments line by line. When a file
  changes, update its page.
- `misc/` holds everything that is not a Day folder (David, 2026-10-28): `docs/`,
  `games/`, and `scripts/`, so the top folder shows the ten Day folders and little
  else.
- `misc/docs/` holds its folders and a `README.md` that maps them (David, 2026-10-28).
  `misc/docs/engine_code/` holds only pages named after an engine `.py` file (David,
  2026-10-30): a module that every engine folder holds, which a game loads or the
  engine's tests check. Every other page goes into the folder of its subject.
  - `misc/docs/course/`: the course plan, the slide plan, the Lucas Chess
    guide, the science survey, the two briefing PDFs, `file_versions.md`, and
    `student_edit_plan.md`, which `make_student_folders.py` writes.
  - `misc/docs/engine_code/`: one page for every engine `.py` file, named after that
    file (`board.py` has `board.md`).
  - `misc/docs/class_demos/`: one page for every class demo and experiment that lives
    only in its period folders, such as `demo_promotion.py`, `compare_search.py`, and
    `show_board.py`. No engine folder holds these files.
  - `misc/docs/science/`: the Day 10 science files, `hidden_peak.py` and `phase_hunt.py`.
  - `misc/docs/learning_python/`: one page for every Python skills lab, named after
    its file (`python_lists.py` has `python_lists.md`).
  - `misc/docs/chess_instruction/`: pages about chess itself (how to play, the rules,
    chess notation) rather than about Remus or Python, such as `chess_notation.md`.
  - `misc/docs/engine_comparison/`: the program overview, `remus_program_overview.md`;
    `tests.md`, how the test files check Remus; and the Remus versions and Niram: `remus_versions.md`,
    the ten enhanced engines and Remus-GOLD; `engines_elo.md`, the league and Stockfish
    ratings; `remus-niram same algorithms.md`, which `engine_parity.py` writes; and the
    pages of the match tools in the engine folders, `play_match.py` and `estimate_elo.py`.
  Pictures live in `misc/docs/images/` (`boards/`, `code/`, `lucas_chess/`, and `phase_hunt/`). A new page goes
  into the folder of its subject; nothing else sits at the top of `misc/docs/`.
- Remus-WHITE, the ten enhanced engines (Remus-RED, Remus-BLUE, ...), and Remus-GOLD
  are the **Remus versions** (David, 2026-10-28). Call them Remus versions or enhanced
  engines, never "stations", in file names, code, and prose. Game records keep the
  Event names `Station match`, `Station league`, and `Station Elo test`, so the
  games already in `misc/games/remus_games.pgn` still count toward the ratings.
  `version_elo.py` plays a new test under the Event `Engine Elo test`, which keeps
  the four-level run apart from the five-level `Station Elo test` games.
- **Say which color** (David, 2026-10-29). Chess pieces have a color (White or
  Black), and so does each Remus version (WHITE, GRAY, ..., RED, GOLD). Every
  Markdown file, and every text the builders write into one, qualifies a bare
  "color" as **piece color** or **engine color**: "5 games with each piece color",
  "the visitor's engine color, such as `RED`". A Remus
  version's folder, such as `10 Remus-RED - Transposition table`, is its **engine
  folder**, never a "color folder". Code identifiers such as `color_of()` and
  `--colors` keep their names.
- **Color is a folder label, not an identity** (David, 2026-10-29). The engine color
  only tells the engine folders apart. Name a Remus version by its enhancement
  ("the transposition table engine", "this enhancement") or by its engine name
  (Remus-RED), and call the ten of them the **enhanced engines** or the **engine
  enhancements**, never "color versions". Write "Engine enhancements: test and
  measure" and "engine battles", not "Color versions" or "color battles". Use
  "engine color" only where the text means the color word in a folder name, such as
  the `VISITING_ENGINE` setting.
- **Say "student pairs"** (David, 2026-10-29). The students work in pairs, and every
  document, comment, and builder text names them "student pairs" or "the student
  pair", never a bare "pairs": "the functions the student pairs write". A pair of
  games or a `(row, col)` pair keeps its plain word.

# Part 2: Python style

## General principles

- Code should be **clear, explicit, and readable**.
- Prefer **teaching-oriented explanations** over compact or clever code.
- Write as if the reader is a **student learning the concept for the first time**.
- Avoid unnecessary abstraction unless it improves understanding.

## Script and module structure

Every Python file starts the same way: a shebang line that runs it through `uv`, then a
docstring whose first line is the filename. A longer docstring adds a blank line and a
short description of what the file teaches or does.

```python
#!/usr/bin/env -S uv run
"""perft.py

Count the leaf positions of the legal move tree to a fixed depth.
"""
```

On Linux and macOS a script marked executable runs with the project's environment and no
manual activation. Windows ignores the shebang; there VS Code's Run button runs a
script with the project's `.venv`, which the workspace file selects.

The parts of a file come in this order:

1. Shebang and filename docstring.
2. Imports, standard library first, then the project's own modules, each group sorted
   (ruff's `I` rule enforces the order). Engine modules import only the standard
   library and each other.
3. Module constants in `UPPER_CASE`, each with a comment that says what it means, such
   as `MATE_SCORE = 100_000  # Larger than any material count`.
4. Functions, simplest first, so a reader meets each helper before the code that calls it.
5. A `main()` function that runs the file's visible self-check.
6. The guard that calls `main()`:

```python
def main():
    state = new_game()
    moves = legal_moves(state)
    print(f"Legal moves from the start: {len(moves)}  (expected 20)")


if __name__ == "__main__":
    main()
```

The guard matters more in Remus than in a stand-alone lab script. Engine modules import
each other, and the UCI engine imports nearly all of them; a module that printed at
import time would send stray text to Lucas Chess and break the protocol. Every print
in an engine module therefore lives inside `main()` or a function `main()` calls.

### Every script produces visible output

Never write a script that runs silently. When a file exists mainly to define functions,
`main()` exercises them on a simple case and prints the result next to the expected
answer, as in the 20 legal moves above. The check doubles as a worked example and as
proof that the file ran.

## Python code style

### Type hints

- Use type hints for every reusable function and class, in modern Python 3.14 syntax:
  `list[str]`, `tuple[int, int]`, `str | None`, `dict[str, int]`.
- Give complex types a name once and reuse it, such as `Square = tuple[int, int]`, so a
  13-year-old reads `Square` instead of a nested bracket expression.
- `main()` and short lab scripts may leave out hints.

### Docstrings

Use **NumPy-style docstrings** for reusable functions:

```python
def square_name(row: int, col: int) -> str:
    """
    Convert board coordinates to an algebraic square name.

    Parameters
    ----------
    row : int
        Board row, where row 0 is rank 8.
    col : int
        Board column, where column 0 is file a.

    Returns
    -------
    str
        The square name, such as "e4".
    """
```

Short helper functions may use a one-line docstring:
`"""Return True if the piece is White."""`

### Names

- Functions and variables use `snake_case` with whole words: `legal_moves`,
  `captured_piece`, `halfmove_clock`. Abbreviate only where chess itself does (`fen`,
  `san`, `uci`, `pv`).
- Booleans read as yes-or-no questions: `is_sorted`, `in_check`, `swap_needed`.
- Loop variables may be short where the meaning is plain: `row`, `col`, `i`. Never use
  `l`, `O`, or `I` as a name.
- Do not shadow built-in names such as `sum`, `list`, `max`, or `input`.

### Idioms used throughout

- f-strings for all output. Self-documenting `f"{moves=}"` is fine in labs and quick
  checks.
- Thousands separators make counts readable: `197_281` in code and `f"{nodes:,}"` in
  output.
- `time.perf_counter()` for timing, reported as `f"Total run time (sec): {elapsed:.3f}"`.
- Seed the random generator (`random.seed(2016)`) wherever a lab or test must give the
  same result on every run.
- Plain loops over clever one-liners, everywhere in the repository (David,
  2026-10-27). Simple code for middle school readers matters more than the most
  Pythonic or the fastest form, and every file follows the same rule:
  - Build text with `+` or `+=` in a loop, never with `str.join()`.
  - Find the best item with a loop that remembers the best so far, never with
    `max(..., key=lambda ...)` or `sorted(..., key=...)`. Do not use `lambda` at all.
  - Fill a list with a loop and `append`, never with a list, set, or dict
    comprehension. Check every item with a loop and a yes-or-no variable, never
    with `any()` or `all()` over a generator expression.
  - `min()` and `max()` of two numbers, and `sum()` of a list, are fine.
  - The build scripts (`make_*.py`, `period_guides.py`, `run_all_tests.py`) are
    course designer tools that no student reads, so they may keep the compact forms.

## Comments

Comments are **functional and explanatory**. They say what a step means in chess or why
the code is written this way, not what the syntax already shows.

- Explain purpose and meaning: `# Row 0 is rank 8, so White pawns move toward row 0`.
- Address the student where a step needs a nudge: `# Try a rook on d4: it has 14 moves`.
- Avoid decorative comments (banner lines, boxes of `#` characters) and comments that
  restate the code (`i += 1  # add one to i`).
- A short comment above a block beats a long comment at the end of a line.

### Present tense only

Comments describe the code **as it stands now**, in the present tense. The reader
sees only the current version, so anything about the code's past is confusing noise.

- **Never refer to a prior version of the code**, an earlier approach, or how the
  code used to behave.
- **Never describe a past mistake or bug**, or frame the current code as a "fix,"
  "correction," or improvement over something that came before.
- Do not use words like *now*, *again*, *still*, *no longer*, *previously*, *used
  to*, or *the old way* to contrast with an earlier state.
- State what the code does and **why it is written this way**, on its own terms. If
  a design choice needs justifying, justify it by the requirement it meets, not by
  the alternative it replaced.

Example: instead of "The king-safety check is the fix: the old filter let a pinned
knight move," write "A move is legal only if the mover's king is not attacked after
the move is made. Testing after the move catches pins, discovered checks, and en
passant captures that expose the king."

## Student and instructor files

Python skills labs use the same pattern as David's course repositories: a student file
with blanks and an instructor file with the answers.

- The student file `Day 02 .../period2/student/python_dicts.py` prints a heading for each part
  (`print("Part #1 - Create a Dict and Read Items")`) and leaves one `#` line for each
  line the student writes.
- The instructor file `Day 02 .../period2/instructor/python_dicts_instructor.py`
  mirrors it line for line with the answers filled in. Its filename docstring names the instructor file.
- Keeping the two files line-aligned lets the teacher diff them and lets a student
  compare a finished lab with the answer.

Engine code uses scaffolds instead: the period's `student/` folder holds the
signature, docstring, and failing tests, with the body set to `raise
NotImplementedError`. The `instructor/` folder beside it holds the teacher's solution.

## File naming

- Use lowercase `snake_case` for all files, Python and data alike.
- File names should be **descriptive and topic-based**, for example `board_display.py`,
  `move_generation.py`, `perft.py`.
- Instructor answer files add `_instructor` and live in the `instructor/` folder beside
  the period's `student/` folder.

## File input and output

Every file a script reads or writes lives in the same folder as the script, or in a
folder named relative to it. A bare filename resolves against the current working
directory, so the same script run from another folder writes somewhere else. Anchor
the path to the script and pass `file_path` to every call that touches the file:

```python
file_path = Path(__file__).parent / "perft_positions.epd"
print(f"Reading {file_path}")
```

Print the full `file_path` rather than the bare name when reporting a save.

Build `file_path` from `Path(__file__).parent`, never from the bare name, and pass
`file_path` itself to every call that touches the file. Computing `file_path` and then
handing the bare name to `open()` looks correct at a glance and silently reads or
writes in the wrong folder.

## No notebooks

Remus and its labs are plain `.py` files. The workshop uses no Jupyter notebooks, so
the notebook rules and the `nb_check.py` hook from the course repositories do not
apply here.

## Linting and formatting

`uv run ruff check .` must pass before a commit. The settings in `pyproject.toml` match
the course repositories: ruff's default rules plus `I` (import order), `C4`
(comprehensions), `ISC` (string concatenation), `SIM` (simpler code), and `TCH`
(type-checking imports), with the default line length of 88. `uv run ruff format .`
formats the code.

The code must also show no type errors in VS Code's Pylance. Check a Day folder with
`uvx pyright "Day 03 - Generate piece moves/period4/instructor"`. When a function can return
`None`, such as `color_of()` or `game_result()`, test for `None` before using the
result.

## American spelling

Every word in this repository uses American spelling: prose, docstrings, comments,
Markdown, variable and function names, and printed output. Never use British spelling.

- `traveled`, `canceled`, `modeled`, `labeled` (one `l`), not `travelled`,
  `cancelled`, `modelled`, `labelled`.
- `color`, `favor`, `behavior`, `neighbor`, `center`, `defense`, `offense`, `gray`,
  `catalog`, `analyze`, `realize`, `recognize`, `organize`, `judgment`, `toward`,
  `while` (not `whilst`), `among` (not `amongst`).
- Library identifiers keep their own spelling, so `engine.analyse(...)` from
  python-chess stays as the API names it.
- Do not rewrite British spellings inside third-party data, quoted sources, or proper
  nouns.

## Dashes

Never use an em dash, an en dash, a minus sign, or any other long dash character
(U+2013, U+2014, U+2212, and their relatives) anywhere: not in prose, comments,
docstrings, Markdown, or f-strings. Use a colon, a comma, parentheses, or a plain
hyphen-minus (`-`) instead. Write ranges as `5 to 14` or `5-14`, results as `1-0`,
and negative numbers and scores with the ordinary hyphen.

## Editorial and style guidelines

These apply to the workshop text, course plan, README, docstrings, comments, and chat replies.

1. **Avoid robotic abstractions and nested clauses.** Prefer direct, active verbs over
   phrasal verbs like "comes with" or "results in." Say who applies a rule or what the
   program counts. Eliminate dangling final pronouns by naming the noun.
2. **Ban conversational filler.** Never open with "It's important to remember that...",
   "Crucially, ...", "Furthermore, ...", "In summary, ...", or "As previously
   mentioned...". Avoid the word "testament." Do not end an explanation with a
   superficial positive summary such as "making it both powerful and flexible." State
   what the code does and stop.
3. **Explain through concrete examples.** Start with the piece, position, square, or
   operation the reader can picture, then name the general principle. Prefer "a knight
   on a1 has two moves, to b3 and c2" to an unexplained rule about edge squares.
   Explain technical terms at first use.
4. **Make references clear.** Repeat a short, specific noun when "it," "this," or
   "that" could refer to two things. Split a sentence that changes subject midway.
5. **Preserve meaning while improving the prose.** Keep numbers, units, and
   qualifications. Do not attribute understanding to a program: describe the operation
   performed or the output recorded.
6. **Read for natural rhythm.** Vary sentence length. Use paragraphs for connected
   explanations, numbered lists for steps, and tables for comparisons. Use bold
   sparingly. Remove closing sentences that only praise the method or repeat the point.
7. **Avoid weak endings and redundancy.** Give a sentence a concrete ending. Remove a
   relative clause that repeats what the main verb already says.

Do not vouch for the text either: words such as `honestly`, `frankly`, `to be fair`,
`plainly stated`, or `it is worth stating that` spend a sentence announcing a sentence.
Give the reason to believe a claim, such as the perft count that confirms it, instead.

# Part 3: References

## Sources

- [Sargon (chess), Wikipedia](https://en.wikipedia.org/wiki/Sargon_(chess))
- [Dan Spracklen, Chess Programming Wiki](https://chessprogramming.org/Dan_Spracklen)
- [List of kings of Akkad, Wikipedia](https://en.wikipedia.org/wiki/List_of_kings_of_Akkad)
- [The Akkadian Period, The Met](https://www.metmuseum.org/es/essays/the-akkadian-period-ca-2350-2150-b-c)
