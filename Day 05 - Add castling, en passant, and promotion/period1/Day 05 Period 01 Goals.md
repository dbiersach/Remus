# Day 5, Period 1: Python lab 7: sets, in, string replacement

## Learning objectives

By the end of this period, each student pair can:

- Use sets and `in` to test membership, and change strings with `replace()`. **Measured by:** The lab removes `"K"` from `"KQkq"` when the h1 rook moves.

## The files

The lab is `python_sets.py` in the `student` folder, with the answers in `python_sets_instructor.py` in the `instructor` folder beside it. Open `python_sets.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The student pairs fill in the blanks of `python_sets.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_sets_instructor.py`.

Part #1 adds squares to a set. A set holds each item once, so adding h1 a second time changes nothing.

Parts #2 and #3 ask questions with `in`, of a set and of a dict. The dict `rights_lost` names the castling rights each home square guards: a piece leaving e1 removes K and Q, and a piece leaving h1 removes K.

Part #4 removes rights with `replace()`, one letter at a time, starting from `"KQkq"`. `update_castling_rights()` in `make_move.py` does exactly this in period 2.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a set holds each item once, `in` asks a yes-or-no question, and a dict looks up a value by its key. |
| 8:45 to 9:35 | Student pairs work through the four parts of `python_sets.py`, ending with `replace()` removing "K" from "KQkq" when the h1 rook moves. |
| 9:35 to 9:50 | The class lists, on the board, every move that removes a castling right. |
| 9:50 to 10:00 | Wrap-up and a preview of castling. |

## What you edit in the lab

Open `python_sets.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 14. Check the work by running `python_sets.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### Part #1 - A Set Holds Each Item Once

```text
13 |     print("Part #1 - A Set Holds Each Item Once")
14 |     # The squares that pieces have moved away from, with no repeats
15 +     moved = set()
16 +     moved.add("h1")
17 +     moved.add("e1")
18 +     moved.add("h1")
19 +     print(f"Squares in the set: {len(moved)}  (expected 2: h1 counts once)")
20 |
21 |     print("Part #2 - Ask a Question with in")
```

### Part #2 - Ask a Question with in

```text
20 |
21 |     print("Part #2 - Ask a Question with in")
22 +     print(f"Has the h1 rook moved? {'h1' in moved}  (expected True)")
23 +     print(f"Has the a1 rook moved? {'a1' in moved}  (expected False)")
24 |
25 |     print("Part #3 - Look Up a Right in a Dict")
```

### Part #3 - Look Up a Right in a Dict

```text
26 |     # Each home square guards castling rights: K is White's king side, q Black's queen side
27 |     rights_lost = {"e1": "KQ", "h1": "K", "a1": "Q", "e8": "kq", "h8": "k", "a8": "q"}
28 +     print(f"A piece leaving h1 removes: {rights_lost['h1']}  (expected K)")
29 +     print(f"Is d1 a home square? {'d1' in rights_lost}  (expected False)")
30 |
31 |     print("Part #4 - Remove Rights with replace()")
```

### Part #4 - Remove Rights with replace()

```text
32 |     rights = "KQkq"
33 |     # replace("K", "") gives back a new string with every K taken out
34 +     rights = rights.replace("K", "")
35 +     print(f"After the h1 rook moves: {rights}  (expected Qkq)")
36 |     # Remove each letter a home square guards, one letter at a time
37 +     for letter in rights_lost["e8"]:
38 +         rights = rights.replace(letter, "")
39 +     print(f"After the Black king moves: {rights}  (expected Q)")
40 |     rights = rights.replace("k", "")
41 |     print(f"Replacing a letter that is gone changes nothing: {rights}  (expected Q)")
```
