# Day 1, Period 3: Python lab 2: lists and nested lists

## Learning objectives

By the end of this period, each student pair can:

- Make a list, read one item by index, and count the items with `len()`. **Measured by:** Part #1 of `python_lists.py` prints 8 pieces and `q` on the d-file.
- Visit every item with `for` and `range()`. **Measured by:** Part #2 prints the back rank `r n b q k b n r` on one line.
- Build an 8x8 board as a list of rows and read `board[row][col]`. **Measured by:** Part #3 prints the starting position, and the student pair names the square `board[4][4]` (e4) without running code.
- Say where each rank lives: row 0 is rank 8. **Measured by:** Unplugged warm-up "Call the square": each student converts four squares on the printed board, such as e2 to (6, 4), with no mistakes.

## The files

This period comes before any Remus code. The lab is `python_lists.py` in the `student` folder, with the answers in `python_lists_instructor.py` in the `instructor` folder beside it. Open `python_lists.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

## The changes and why

The student pairs fill in the blanks of `python_lists.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_lists_instructor.py`.

Part #1: you count the pieces in a list with `len()` and read one by index. Index 3 is the d-file, where the queen starts.

Part #2: a `for` loop with `range(8)` visits the eight files in order. Remus walks the board with loops like this everywhere.

Part #3: you build the board as a list of eight rows, each a new list of eight dots, then put the pieces in. Row 0 is rank 8, so Black's pieces go in rows 0 and 1. This is the board `board.py` holds.

Part #4: you play 1. e4 by changing two squares, then count the White pawns left on rank 2. `board[row][col]` is how every rule in Remus reads and changes the board.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Unplugged warm-up, "Call the square": the teacher calls (6, 4), the navigator puts a token on the printed board, and the driver names the square, e2. Then the partners swap. |
| 1:15 to 1:30 | Slides: lists, `for` and `range()`, `len()`, and a list of lists. |
| 1:30 to 2:15 | Student pairs work through the four parts of `python_lists.py`: a list of pieces, a loop over every square, the board as a list of rows, and the pawns in a row. |
| 2:15 to 2:30 | Without running code, each student pair names `board[4][4]` (e4) and says why row 0 is rank 8. |

## What you edit in the lab

Open `python_lists.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 25. Check the work by running `python_lists.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### Part #1 - A List of Pieces

```python
12 |     print("Part #1 - A List of Pieces")
13 |     back_rank = ["r", "n", "b", "q", "k", "b", "n", "r"]
14 +     print(f"Pieces on Black's back rank: {len(back_rank)}  (expected 8)")
15 |     # Index 3 is the fourth square from the a-file: the d-file
16 +     print(f"The piece on the d-file: {back_rank[3]}  (expected q)")
17 |
18 |     print("Part #2 - Visit Every Square with for and range")
```

**How it works:** `len()` counts the items in a list: 8 pieces. `back_rank[3]` reads the item at index 3. Counting from 0, a is index 0 and d is index 3, so the d-file holds the queen.

### Part #2 - Visit Every Square with for and range

```python
18 |     print("Part #2 - Visit Every Square with for and range")
19 |     # range(8) counts 0, 1, 2, ..., 7: one number for each file
20 +     for col in range(8):
21 +         print(back_rank[col], end=" ")
22 +     print()
23 |     print("  (expected r n b q k b n r)")
24 |
```

**How it works:** `for col in range(8)` runs the indented line once for each number from 0 to 7. `end=" "` prints a space instead of starting a new line, so the eight pieces appear on one line. The empty `print()` after the loop ends that line.

### Part #3 - A Board Is a List of Rows

```python
25 |     print("Part #3 - A Board Is a List of Rows")
26 |     # Each row is a fresh list of 8 dots, so changing one row leaves the others alone
27 +     board = []
28 +     for row in range(8):
29 +         board.append(["."] * 8)
30 |     # Row 0 is rank 8, so Black's pieces fill rows 0 and 1, and White's rows 6 and 7
31 +     board[0] = back_rank
32 +     board[1] = ["p"] * 8
33 +     board[6] = ["P"] * 8
34 +     board[7] = ["R", "N", "B", "Q", "K", "B", "N", "R"]
35 +     for row in range(8):
36 +         line = ""
37 +         for col in range(8):
38 +             line += board[row][col] + " "
39 +         print(line)
40 |     print("  (expected the starting position, Black at the top)")
41 |
```

**How it works:** The board starts as an empty list, and the first loop appends 8 rows of 8 dots. Each `["."] * 8` builds a new list, so changing one row never changes another. The next four lines put the pieces on rows 0, 1, 6, and 7; row 0 is rank 8, Black's back rank. The last two loops build one line of text per row with `+=` and print it, so the board appears with Black at the top.

### Part #4 - Count the Pawns in a Row

```python
42 |     print("Part #4 - Count the Pawns in a Row")
43 |     # Play 1. e4: the pawn leaves e2 (row 6, col 4) and lands on e4 (row 4, col 4)
44 +     board[6][4] = "."
45 +     board[4][4] = "P"
46 +     pawns = 0
47 +     for piece in board[6]:
48 +         if piece == "P":
49 +             pawns += 1
50 +     print(f"White pawns left on rank 2: {pawns}  (expected 7)")
51 +     print(f"board[4][4] holds {board[4][4]}  (expected P, the pawn on e4)")
52 |
53 |
```

**How it works:** `board[6][4]` is row 6 (rank 2), column 4 (the e-file), the square e2. Setting it to a dot and `board[4][4]` to `P` plays 1. e4. The loop then visits each square of row 6 and adds 1 to `pawns` for every White pawn it finds: 7 are left.
