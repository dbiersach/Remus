# CLAUDE.md - Remus

Remus is a chess engine written in pure, native Python as a teaching project for the
**Turbo GameWorks Chess Workshop**. The full lesson plan lives in
[`turbo_gameworks_chess_workshop.md`](turbo_gameworks_chess_workshop.md); read it before
starting any lesson. This file captures the standing rules and context so every session
builds Remus the same way.

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

## Hard rules for the engine code

1. **Clarity over speed.** Plain lists, dicts, tuples, strings, functions. Small classes
   or `dataclass` only when they make ownership clearer. Slow is fine.
2. **No third-party libraries inside the engine.** Standard library only. No bitboards,
   magic numbers, compiled extensions, clever caches, or framework machinery.
3. **Engine is the single source of truth** for board, rules, legal moves, game state,
   search, evaluation, and move choice. A GUI only sends moves and displays results.
4. **`python-chess` and PyChess are boundary tools only.** PyChess is the optional desktop
   GUI (via UCI). `python-chess` may be used for an optional display layer or as an
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
- Moves: a simple record with `from`, `to`, `promotion`. Pick one square format and
  document it; convert to/from algebraic and UCI only at the I/O boundary.

## Architecture boundaries

| Part | Responsibility |
| --- | --- |
| Native Python engine | Board, rules, legal moves, state, search, evaluation, move choice |
| Console driver | Human-readable board and commands for lessons and debugging |
| UCI adapter | `uci`, `isready`, `ucinewgame`, `position startpos/fen ...`, `go`, `stop`, `quit`; protocol on stdout, debug on stderr; `bestmove 0000` only with no legal move |
| Optional interface | PyChess as an external UCI engine host, or a small `python-chess` display layer |

The engine must run without PyChess or `python-chess` installed.

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
12. UCI loop and play in PyChess

Each lesson has a "Ready to move on when" gate in the workshop file. Don't skip a gate.

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
- PyChess is a desktop application, not a Python dependency. It hosts Remus as an
  external UCI engine and is installed separately.
- Tests live in `tests/`. A test that uses `python-chess` as a reference states the
  expected count in its docstring or assertion before comparing against Remus.

## Licensed local files

The `Turbo Pascal Toolbox 4.0 - GameWorks/` folder holds the original Borland disks
and archive as a historical reference for the workshop. It is copyrighted software,
excluded from git by `.gitignore`. Never stage, commit, or push anything in it, and
never edit `.gitignore` in a way that would let it through. Never quote large parts of
its source into the repository; describe the ideas and write Remus's own code.

## General principles

- Code should be **clear, explicit, and readable**.
- Prefer **teaching-oriented explanations** over compact or clever code.
- Write as if the reader is a **student learning the concept for the first time**.
- Avoid unnecessary abstraction unless it improves understanding.

## Code comments

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

## American spelling

Every word in this repository uses American spelling: prose, docstrings, comments,
and Markdown. Never use British spelling.

- `traveled`, `canceled`, `modeled`, `labeled` (one `l`), not `travelled`,
  `cancelled`, `modelled`, `labelled`.
- `color`, `favor`, `behavior`, `neighbor`, `center`, `defense`, `offense`, `gray`,
  `catalog`, `analyze`, `realize`, `recognize`, `organize`, `judgment`, `toward`,
  `while` (not `whilst`), `among` (not `amongst`).
- Library identifiers keep their own spelling, so `engine.analyse(...)` from
  python-chess stays as the API names it.

## Dashes

Never use an em dash, an en dash, a minus sign, or any other long dash character
(U+2013, U+2014, U+2212, and their relatives) anywhere: not in prose, comments,
docstrings, Markdown, or f-strings. Use a colon, a comma, parentheses, or a plain
hyphen-minus (`-`) instead. Write ranges as `5 to 14` or `5-14`, results as `1-0`,
and negative numbers and scores with the ordinary hyphen.

## File naming

- Use lowercase `snake_case` for all Python files.
- File names should be **descriptive and topic-based**, for example `board_display.py`,
  `move_generation.py`, `perft.py`.

## Script structure

Every runnable script begins with a shebang line that runs it through `uv`, so that on
Linux and macOS a script marked executable runs with the project's environment and no
manual activation. The filename docstring follows on the next line:

```python
#!/usr/bin/env -S uv run python
"""perft.py"""
```

Windows ignores the shebang; there the scripts run with `uv run python perft.py`.

Every script must produce visible output. When a script exists mainly to define
functions, end it with a short check that exercises what was just defined and
`print()` the result next to the expected answer, such as the 20 legal moves from the
starting position.

## Python code style

- Use type hints for all reusable functions and classes, in modern Python 3.14
  syntax: `list[str]`, `tuple[int, int]`, `str | None`.
- Use **NumPy-style docstrings** for reusable functions:

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

- Short helper functions may use one-line docstrings: `"""Return True if the piece is White."""`

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

## Editorial and style guidelines

These apply to the workshop text, README, docstrings, comments, and chat replies.

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

## Chat responses

Responses are read in the Claude Code panel inside VS Code, which has no MathJax or
KaTeX renderer, so LaTeX shows up as literal dollar signs and backslashes.

- Write math as plain text: `2^n`, `<=`, `sqrt(2)`. Do not use `$...$` or `$$...$$`.
- Chat replies follow the repository's American spelling and no-long-dash rules.
- Use plain paragraphs for standard explanations rather than scattered bullets or bold.

## Git commits

Commit messages must carry no trace of AI assistance. Write the message as the
repository owner would have written it.

- Do not add a `Co-Authored-By: Claude ...` trailer, or any similar
  "co-authored by Claude" line.
- Do not add a generated-by footer such as "Generated with Claude Code" or a robot
  emoji tag.
- Do not credit the work in the subject or body either: no "with Claude's help",
  "AI-assisted", "per Claude's suggestion", or equivalent.
- Do not use vague verbs like "Refactor...", "Optimize...", or "Enhance..." unless
  followed by granular specifics. Never write passive commit messages.

The ban is on **attribution**, not on the words themselves. When a change is genuinely
*about* Claude or AI tooling, name it plainly:

- Good: `Add anthropic.claude-code to the extension install scripts`
- Good: `Document the chat math convention in CLAUDE.md`
- Bad: `Update install scripts (generated with Claude Code)`

## Sources

- [Sargon (chess), Wikipedia](https://en.wikipedia.org/wiki/Sargon_(chess))
- [Dan Spracklen, Chess Programming Wiki](https://chessprogramming.org/Dan_Spracklen)
- [List of kings of Akkad, Wikipedia](https://en.wikipedia.org/wiki/List_of_kings_of_Akkad)
- [The Akkadian Period, The Met](https://www.metmuseum.org/es/essays/the-akkadian-period-ca-2350-2150-b-c)
