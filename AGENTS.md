# Remus Project Rules and Python Style Guide

Remus is a chess engine written in pure, native Python as a teaching project for the
**"Turning a Chess Engine into Science AI"** workshop. The full lesson plan lives in
[`workshop_roadmap.md`](workshop_roadmap.md) and the
day-by-day course in [`remus_course_plan.md`](remus_course_plan.md); read both before
starting any lesson.

This file holds every project and style rule, so that every AI tool used with this
repository builds Remus the same way. `CLAUDE.md` imports it and adds only the rules
that are specific to Claude Code. `.github/copilot-instructions.md` gives GitHub Copilot a
condensed copy; when a rule here changes, update that file to match. The Python style follows David's course repositories
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
  [`remus_course_plan.md`](remus_course_plan.md), and the code is split into modules
  and checkpoints that follow that plan period by period.
- 20 students work in **10 pairs** (driver and navigator, swapping every period). Each
  pair gets an identical, preconfigured **Windows 11** class laptop with git, `uv`,
  VS Code, and En Croissant. Classroom instructions target Windows; `remus.sh` exists
  only for students who take Remus home to a Mac or Linux computer.
- Python skills labs come before the engine code that needs each skill. Students
  **write real Remus code**: small functions with a teacher-written signature,
  docstring, and failing tests. The class picks one pair's version to merge, and
  `CONTRIBUTORS.md` records who wrote it. Keep student functions short enough for a pair
  to finish in 20 to 40 minutes.
- Short unplugged warm-ups (paper, cards, and a printed board at the desk) come before
  the hardest ideas. They replace part of the teacher's explanation, never the time a
  pair spends typing code.
- Students know how the pieces move. Lessons remind them of the rarer rules right before
  the code that needs each one: castling conditions, en passant, promotion and
  underpromotion, stalemate, threefold and fivefold repetition, the fifty and 75-move
  rules, and insufficient material.
- **Progressive elaboration.** Every functional area (board, make/undo, move generation,
  attacks, game end, evaluation, search, interface) starts with the smallest correct
  version, then gains completeness, then power, then efficiency in later blocks. The
  whole engine also gets two passes: first it plays legal moves, then it plays good moves.
- Every day ends with an engine that runs. Each period has a start tag and an end tag
  (`d3-p2-start`, `d3-p2-end`) so a pair that falls behind can rejoin.
- Write code, comments, and lesson text for a 13-year-old reading the idea for the first
  time: short functions, concrete names, and one small example position per idea.
- The class never builds a GUI. Every laptop uses **En Croissant**, which runs Remus as
  a UCI engine through `remus.bat`. `python-chess` runs
  matches and checks results from outside the engine.
- **No GitHub for students.** They are minors, so they create no online accounts. The
  teacher's laptop holds the main class repository; each pair has its own local
  repository and fetches from the teacher over the classroom network (or a git bundle
  on a USB stick). At the end of the course each pair takes its repository home on a USB
  drive. Never plan a step that needs a student account or pushes student code online.
- `CONTRIBUTORS.md` credits pairs by a team name they choose, not by full names.

## Hard rules for the engine code

1. **Clarity over speed.** Plain lists, dicts, tuples, strings, functions. Small classes
   or `dataclass` only when they make ownership clearer. Slow is fine.
2. **No third-party libraries inside the engine.** Standard library only. No bitboards,
   magic numbers, compiled extensions, clever caches, or framework machinery.
3. **Engine is the single source of truth** for board, rules, legal moves, game state,
   search, evaluation, and move choice. A GUI only sends moves and displays results.
4. **`python-chess` and En Croissant are boundary tools only.** En Croissant is the
   desktop GUI, which runs Remus over UCI. `python-chess` runs matches and serves as an
   external cross-check in tests, never as the engine's hidden implementation.
5. **Exact make/undo.** `undo_move(make_move(state, move))` must restore the full state,
   including clocks, rights, en passant target, side to move, and history. Search must
   leave the live position unchanged even if it stops early (use `try/finally`).
6. **Separate rules from search.** Legal move generation must be correct (perft-verified)
   before minimax, alpha-beta, books, tables, or GUI work.
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
| Console driver | Human-readable board and commands for lessons and debugging |
| UCI adapter | `uci`, `isready`, `ucinewgame`, `position startpos/fen ...`, `go`, `stop`, `quit`; protocol on stdout, debug on stderr; `bestmove 0000` only with no legal move |
| GUI | En Croissant, which starts `remus.bat` and hosts Remus as an external UCI engine |

The engine must run without En Croissant or `python-chess` installed.

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
12. UCI loop and play in En Croissant
13. Science AI: aim the same generate, score, and choose loop at a hidden-peak
    measurement problem (`science/hidden_peak.py`)

Each lesson has a "Ready to move on when" gate in the workshop file. Don't skip a gate.

The course plan maps these 13 lessons onto the ten days and moves the first UCI and
GUI work to Day 7, after perft has verified the rules.

## Verification

- Write expected results before running. Use small named positions (see the workshop's
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
  import `chess`; only tests and optional display code may.
- En Croissant is a desktop application, not a Python dependency. It hosts Remus as an
  external UCI engine and comes preinstalled on the class laptops.
- Engine modules live in one flat `remus/` folder and import each other by name
  (`from board import new_board`), so any module runs directly with
  `uv run remus/perft.py`. pytest finds them through `pythonpath = ["remus"]`.
- The Science AI lesson lives in a separate `science/` folder. `hidden_peak.py` uses the
  standard library only and does not import the engine: it reuses the engine's ideas,
  not its code. Add `"science"` to `pythonpath` when the folder is created.
- Tests live in `tests/`. A test that uses `python-chess` as a reference states the
  expected count in its docstring or assertion before comparing against Remus.

## Licensed local files

The `Turbo Pascal Toolbox 4.0 - GameWorks/` folder holds the original Borland disks
and archive as a historical reference for the workshop. It is copyrighted software,
excluded from git by `.gitignore`. Never stage, commit, or push anything in it, and
never edit `.gitignore` in a way that would let it through. Never quote large parts of
its source into the repository; describe the ideas and write Remus's own code. The one
approved exception (David, 2026-10-26) is the ten `MATE.00x` puzzle positions, stored
as FEN in `tests/mate_puzzles.epd`.

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
manual activation. Windows ignores the shebang; there a script runs with
`uv run remus/perft.py`.

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
import time would send stray text to En Croissant and break the protocol. Every print
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
- Plain loops over clever one-liners. A list comprehension is fine when it fits on one
  line and reads as a sentence; otherwise write the loop.

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

- The student file `labs/day02/python_dicts.py` prints a heading for each part
  (`print("Part #1 - Create a Dict and Read Items")`) and leaves one `#` line for each
  line the student writes.
- The instructor file `labs/day02/instructor/python_dicts_instructor.py` mirrors it line
  for line with the answers filled in. Its filename docstring names the instructor file.
- Keeping the two files line-aligned lets the teacher diff them and lets a student
  compare a finished lab with the answer.

Engine code uses scaffolds instead: the teacher's start tag holds the signature,
docstring, and failing tests, with the body set to `raise NotImplementedError`. The
end tag holds the teacher's solution.

## File naming

- Use lowercase `snake_case` for all files, Python and data alike.
- File names should be **descriptive and topic-based**, for example `board_display.py`,
  `move_generation.py`, `perft.py`.
- Instructor answer files add `_instructor` and live in an `instructor/` folder beside
  the student file.

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
