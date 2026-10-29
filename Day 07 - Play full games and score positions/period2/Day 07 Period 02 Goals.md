# Day 7, Period 2: SAN and the console game

## Learning objectives

By the end of this period, each student pair can:

- Read a move typed in SAN, such as Nf3 or O-O. **Measured by:** The `parse_san` tests pass, and a typo raises `ValueError`.
- Play a whole game in the console. **Measured by:** Two students play `console_game.py` to a finish and the program prints the right result.
- Read commands from `sys.stdin` and answer on stdout. **Measured by:** `python_input_output.py` answers `isready` with `readyok` and stops at `quit`.

## The files

The lab is `python_input_output.py` in the `student` folder, with the answers in `python_input_output_instructor.py` in the `instructor` folder beside it. Open `python_input_output.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

New files this period:

- `console_game.py`
- `notation.py`

Files that grow this period:

- `test_game.py`

Functions the student pairs write this period:

- `parse_san()` in `notation.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

The student pairs fill in the blanks of `python_input_output.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_input_output_instructor.py`.

Parts #1 and #2 pick moves the way the first brains in period 3 do: `random.choice()` takes any item, and a loop that keeps the best piece so far takes the item with the largest value.

Parts #3 and #4 talk the way a UCI engine does. The program reads one command per line from `sys.stdin`, answers `isready` with `readyok`, and sends each answer at once with `flush=True`. Notes for people go to `sys.stderr`, where the GUI does not read them.

### `parse_san()` in `notation.py`

Finds the legal move that matches typed SAN, such as Nf3, by writing the SAN of every legal move and comparing. Matching against real moves means any text Remus accepts is a legal move.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Slides: SAN. The teacher walks through `move_to_san()`, including `Nbd2` and the `+` and `#` endings. |
| 10:45 to 11:05 | Student pairs write `parse_san()`: build the SAN of every legal move and return the one that matches. |
| 11:05 to 11:20 | Student pairs play each other with `console_game.py`, typing moves in SAN. |
| 11:20 to 12:00 | Student pairs work through `python_input_output.py`: `random.choice()`, a loop that keeps the best so far, stderr, and a tiny program that answers `isready` with `readyok`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `notation.py` | `parse_san()` | 90 | 5 | `test_game.py::test_parse_san_finds_each_move` |

Lines to type in all: 5. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `parse_san()` in `notation.py`

**Where:** lines 112 to 116 of `notation.py`, inside `parse_san()`, in place of the stub below the docstring. It is called by `main()` in `console_game.py`.

```python
 90 | def parse_san(state: dict, text: str) -> Move:
 91 |     """
      ...
110 |         If no legal move matches.
111 |     """
112 +     wanted = text.strip().rstrip("+#!?").replace("0", "O")
113 +     for move in legal_moves(state):
114 +         if move_to_san(state, move).rstrip("+#") == wanted:
115 +             return move
116 +     raise ValueError(f"Not a legal move here: {text!r}")
117 |
118 |
119 | def main():
```

**How it works:** `strip()` removes spaces, `rstrip("+#!?")` removes check, mate, and comment marks from the end, and `replace("0", "O")` accepts castling typed with zeros. Then the function writes every legal move in SAN with `move_to_san` and returns the one whose text matches. Nothing matching means the text is not a legal move here, so it raises `ValueError`.

### Part #1 - random.choice() Picks One Item

```python
24 |     random.seed(2016)  # The same seed gives the same pick on every run
25 |     moves = ["e2e4", "d2d4", "g1f3", "c2c4"]
26 +     pick = random.choice(moves)
27 +     print(f"Random move: {pick}  (expected one of the four)")
28 |
29 |     print("Part #2 - A Loop Keeps the Best Item So Far")
```

**How it works:** `random.choice` picks one item from a list. The seed above it makes the pick the same on every run.

### Part #2 - A Loop Keeps the Best Item So Far

```python
30 |     # Start with the first piece, then swap in any piece worth more
31 |     victims = ["p", "q", "n"]
32 +     best = victims[0]
33 +     for piece in victims:
34 +         if victim_value(piece) > victim_value(best):
35 +             best = piece
36 +     print(f"Most valuable capture: {best}  (expected q)")
37 |
38 |     print("Part #3 - Notes Go to stderr")
```

**How it works:** The loop remembers the best item so far. It starts with the first victim, and every piece worth more takes its place. After the loop, `best` holds the most valuable piece, the queen.

### Part #3 - Notes Go to stderr

```python
38 |     print("Part #3 - Notes Go to stderr")
39 |     # A GUI reads stdout, so notes for people go to stderr where the GUI ignores them
40 +     print("This note goes to stderr", file=sys.stderr)
41 |
42 |     print("Part #4 - Read Commands from stdin and Answer")
```

**How it works:** `file=sys.stderr` sends the text to the error stream instead of the normal output. Lucas Chess reads only the normal output, so notes for people go to stderr and never confuse the GUI.

### Part #4 - Read Commands from stdin and Answer

```python
42 |     print("Part #4 - Read Commands from stdin and Answer")
43 |     print("Type isready, then hello, then quit, pressing Enter after each")
44 +     for line in sys.stdin:
45 +         command = line.strip()
46 +         if command == "quit":
47 +             break
48 |         # flush=True sends the answer right away instead of keeping it in a buffer
49 +         if command == "isready":
50 +             print("readyok", flush=True)
51 +         else:
52 +             print(f"echo {command}", flush=True)
53 |     print("  (expected readyok, then echo hello)")
54 |
```

**How it works:** `for line in sys.stdin` reads one line each time you press Enter. `strip()` removes the newline. "quit" ends the loop; "isready" gets "readyok", the answer a UCI engine gives; anything else is echoed back. `flush=True` sends each answer at once, as the UCI conversation needs.

## What you edit in the lab

Open `python_input_output.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 16. Check the work by running `python_input_output.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
