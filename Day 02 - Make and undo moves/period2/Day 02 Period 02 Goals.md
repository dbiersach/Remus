# Day 2, Period 2: Python lab 4: dicts, dataclasses, aliasing, copying

## Learning objectives

By the end of this period, each student pair can:

- Store named facts in a dict and read them back. **Measured by:** The lab's state dict answers whose turn it is and the castling rights.
- Explain aliasing: two names for one list. **Measured by:** The student pair predicts, then shows, that `b2 = board` changes both boards, and that a copy does not.
- Describe a record with a `dataclass`. **Measured by:** The student pair makes a small `dataclass` and prints one of its fields.

## The files

The lab is `python_dicts.py` in the `student` folder, with the answers in `python_dicts_instructor.py` in the `instructor` folder beside it. Open `python_dicts.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The student pairs fill in the blanks of `python_dicts.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_dicts_instructor.py`.

Part #1 keeps the facts of a game in a dict and reads them by key, the way `new_game()` in `game_state.py` holds the board, the side to move, and the castling rights.

Part #2 shows aliasing: `b2 = board` makes a second name for the same board, so a pawn put on e4 through `b2` shows up in `board` too. This is the most common surprise in a chess program that changes its board in place.

Part #3 makes a real copy with `deepcopy()`, which copies every row. The copy changes alone, and `==` compares the two boards square by square.

Part #4: you write a `dataclass` with two fields and print one of them. Remus's `Move` in `moves.py` is the same record with a third field for the promotion piece.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Slides: a dict holds named facts, and a dataclass describes a record with fixed fields. |
| 10:45 to 11:15 | Student pairs work through Parts #1 and #2 of `python_dicts.py` and watch `b2 = board` change both boards. |
| 11:15 to 11:50 | The teacher explains aliasing on the whiteboard: two names, one list. Then student pairs write Parts #3 and #4: a real copy, and a dataclass that describes a move. |
| 11:50 to 12:00 | Wrap-up: why would a chess engine break if it changed a board it meant to copy? |

## What you edit in the lab

Open `python_dicts.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 18. Check the work by running `python_dicts.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### The `Move` class

```text
16 |
17 | # A dataclass is a record with named fields, written once and used for every move
18 + @dataclass
19 + class Move:
20 +     from_square: str
21 +     to_square: str
22 |
23 |
```

**How it works:** `@dataclass` turns a short class into a record type. Each line inside names one field and its type. Python then writes the code that builds a Move from two values and prints it neatly.

### Part #1 - A Dict Holds Named Facts

```text
26 |     state = {"turn": "w", "castling": CASTLING_AT_START, "fullmove_number": 1}
27 |     # Read a value by its key, inside [ ]
28 +     print(f"Side to move: {state['turn']}  (expected w)")
29 +     print(f"Castling rights: {state['castling']}  (expected KQkq)")
30 |     # Store a new value under a key that is already there
31 +     state["turn"] = "b"
32 |     print(f"Side to move after White plays: {state['turn']}  (expected b)")
33 |
```

**How it works:** A dict stores values under keys. `state['turn']` reads the value stored under the key "turn". Inside an f-string that already uses double quotes, the key needs single quotes. `state["turn"] = "b"` replaces the value: Black is to move.

### Part #2 - Two Names for One Board

```text
37 |         board.append(["."] * 8)
38 |     # b2 = board gives the same board a second name: no new board is made
39 +     b2 = board
40 +     b2[4][4] = "P"
41 |     print(f"board[4][4] is {board[4][4]}  (expected P, the change shows in both)")
42 +     print(f"Same board? {b2 is board}  (expected True)")
43 |
44 |     print("Part #3 - A Copy Is a New Board")
```

**How it works:** `b2 = board` makes no copy. It gives the same board a second name, so writing a pawn through `b2` changes `board` too. `is` asks whether two names point to the very same object, and here the answer is True.

### Part #3 - A Copy Is a New Board

```text
44 |     print("Part #3 - A Copy Is a New Board")
45 |     # deepcopy copies the outer list and every row inside it
46 +     b3 = deepcopy(board)
47 +     b3[0][0] = "r"
48 |     print(f"board[0][0] is {board[0][0]}  (expected ., the original stays the same)")
49 +     print(f"b3[0][0] is {b3[0][0]}  (expected r)")
50 +     print(f"Same board? {b3 is board}  (expected False)")
51 +     print(f"Equal boards? {b3 == board}  (expected False, a8 differs)")
52 |
53 |     print("Part #4 - A Dataclass Describes a Move")
```

**How it works:** `deepcopy` builds a new board, a new outer list holding new copies of every row. Changing `b3` leaves `board` alone. `is` is now False, because these are two objects, and `==` compares their contents, which differ on a8.

### Part #4 - A Dataclass Describes a Move

```text
52 |
53 |     print("Part #4 - A Dataclass Describes a Move")
54 +     move = Move("e2", "e4")
55 +     print(f"The pawn lands on {move.to_square}  (expected e4)")
56 +     print(move)
57 |     print("  (expected Move(from_square='e2', to_square='e4'))")
58 |
```

**How it works:** `Move("e2", "e4")` builds a record, filling the fields in the order the class lists them. `move.to_square` reads one field by name, and `print(move)` shows all of them.
