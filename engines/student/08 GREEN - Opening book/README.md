# Remus-GREEN: Opening book

Play the first moves of well-known openings from a book instead of searching.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

`opening_book.txt` holds 43 well-known openings, five moves for each side, written in SAN: `e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7` is the Ruy Lopez. `load_book()` plays every line on a board from the starting position and records, for each position it passes, which moves the book plays there. After 1. e4 the book holds seven replies: ...e5, ...c5, ...e6, ...c6, ...d5, ...d6, and ...Nf6. `book_move()` picks one of them at random, so Remus-GREEN does not play the same opening every game. Once the game leaves the book, Remus searches as usual.

## Why it makes Remus stronger

Searching the opening is slow and not very good: at depth 4 Remus cannot see why 1. e4 e5 2. Nf3 Nc6 3. Bb5 works. A book move costs no thinking time and comes from a century of human play. Every book move also passes through `parse_san()` and Remus's own legal move generator, so a typo in the book file is reported and skipped, never played.

## What it costs

Nothing during the search: the book is read once when the engine starts, and asking it is one dict lookup. Positions per second and positions per depth are the same as Remus-WHITE's, because the search itself does not change.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-GREEN | 431,212 | 100% | 5,049 | 3.2 |

## What to expect

The time saved goes to later moves. Remus thinks about one thirtieth of its remaining clock per move, so five instant book moves leave roughly a minute and a half more for the middlegame. Every version match game starts from one of 32 openings three moves deep, and 24 of those positions are in the book, so Remus-GREEN usually gets two more instant moves before it searches. The book saves the most time in games that start from the first move. In the designer's league, Remus-GREEN rated +7 over Remus-WHITE when its games started three moves deep, and +58 when they started from the first move. The benchmark below never asks the book, so its numbers match Remus-WHITE's exactly.

## Where your code fits

`uci_engine.py` and `console_game.py` ask `book_move()` before they search. `None` means the position is not in the book, and the engine calls `think()` as Remus-WHITE does.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `00 WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `load_book()` in `opening_book.py`, `book_move()` in `opening_book.py`.

## The changes and why

### `load_book()` in `opening_book.py`

Reads the book file line by line, checks every SAN move with Remus's own rules, and stores the moves by position. A missing file or a typo only prints a note, so a bad book never stops Remus from playing.

### `book_move()` in `opening_book.py`

Looks the position up in the book and picks one of its moves at random, or returns None when the game has left the book. The random pick keeps Remus from playing the same opening every game.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `smoke_test.py` in VS Code and press Run: Remus-GREEN plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-GREEN plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the folder above this one.

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `opening_book.py` | `load_book()` | 58 | 24 | `test_upgrades.py::test_opening_book_is_legal_and_answers_e4`, `test_upgrades.py::test_book_typo_is_skipped_without_touching_stdout`, `test_upgrades.py::test_trap_line_stores_only_the_defenders_moves`, `test_upgrades.py::test_book_answers_scholars_mate_but_never_tries_it`, `test_upgrades.py::test_missing_book_never_stops_play` |
| `opening_book.py` | `book_move()` | 101 | 2 | `test_upgrades.py::test_opening_book_is_legal_and_answers_e4`, `test_upgrades.py::test_trap_line_stores_only_the_defenders_moves`, `test_upgrades.py::test_book_answers_scholars_mate_but_never_tries_it`, `test_upgrades.py::test_missing_book_never_stops_play` |

Lines to type in all: 26. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `load_book()` in `opening_book.py`

**Where:** lines 74 to 98 of `opening_book.py`, inside `load_book()`, in place of the stub below the docstring. It is called by `main()` in `console_game.py`, `main()` in `uci_engine.py`.

```text
 58 | def load_book(file_path: Path = BOOK_PATH) -> dict[str, list[Move]]:
      ...
 72 |         The dict is empty if the file does not exist.
 73 |     """
 74 +     book = {}
 75 +     if not file_path.exists():
 76 +         print(
 77 +             f"No opening book at {file_path}; Remus searches every move",
 78 +             file=sys.stderr,
 79 +         )
 80 +         return book
 81 +     for line in file_path.read_text().splitlines():
 82 +         if not line.strip() or line.startswith("#"):
 83 +             continue
 84 +         defender, words = read_defender(line)
 85 +         state = state_from_fen(START_FEN)
 86 +         for text in words:
 87 +             try:
 88 +                 move = parse_san(state, text)
 89 +             except ValueError:
 90 +                 print(f"Book line skipped at {text!r}: {line}", file=sys.stderr)
 91 +                 break
 92 +             # A trap line teaches the defense, so the attacker's moves stay out
 93 +             if defender is None or state["turn"] == defender:
 94 +                 moves_here = book.setdefault(position_key(state), [])
 95 +                 if move not in moves_here:
 96 +                     moves_here.append(move)
 97 +             make_move(state, move)
 98 +     return book
 99 |
100 |
101 | def book_move(book: dict[str, list[Move]], state: dict) -> Move | None:
```

**How it works:** The book is a dict from a position key to a list of moves. If the file is missing, the function prints a note to stderr (not stdout, which belongs to the UCI conversation) and returns the empty book, so Remus still plays. Otherwise it reads the file line by line and skips blank lines and comments. `read_defender` splits a line such as "Black: e4 e5 Bc4 Nc6" into the side it teaches and its moves. Each line replays from the starting position: `parse_san` turns text such as Nc6 into a Move, and a move that is not legal skips the rest of the line. Before making each move, the code stores it under the current position's key, but in a trap line only for the defending side. `setdefault` makes a new empty list the first time a position appears, and `if move not in moves_here` keeps a move from appearing twice when two openings share it.

### `book_move()` in `opening_book.py`

**Where:** lines 103 to 104 of `opening_book.py`, inside `book_move()`, in place of the stub below the docstring. It is called by `main()` in `console_game.py`, `main()` in `uci_engine.py`.

```text
101 | def book_move(book: dict[str, list[Move]], state: dict) -> Move | None:
102 |     """Return a random book move for this position, or None when out of book."""
103 +     choices = book.get(position_key(state))
104 +     return random.choice(choices) if choices else None
105 |
106 |
107 | def main():
```

**How it works:** `book.get` looks up the current position's key and returns its list of moves, or None if the position is not in the book. `random.choice` picks one of the moves, so Remus does not play the same opening every game. When the list is missing, the function returns None and the search chooses the move instead.
