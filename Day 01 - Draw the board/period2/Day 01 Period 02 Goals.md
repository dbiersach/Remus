# Day 1, Period 2: Python lab 1: scripts, strings, ord and chr, f-strings

## Learning objectives

By the end of this period, each student pair can:

- Pick single characters out of a string by index, counting from 0. **Measured by:** Part #1 of `python_strings.py` prints file letter e and rank digit 2 for `"e2"`.
- Turn letters into numbers and back with `ord()` and `chr()`. **Measured by:** Part #2 prints file number 4 for e2, and Part #3 builds `"g7"` from file number 6 and rank 7.
- Tell White and Black pieces apart by uppercase and lowercase. **Measured by:** Part #4 prints `RNBQKBNR` from `rnbqkbnr` and `True` for `"N".isupper()`.
- Explain why file a is number 0. **Measured by:** Without running code, the student pair says the file number of h4 (7) and of a1 (0), and why.

## The files

This period comes before any Remus code. The lab is `python_strings.py` in the `student` folder, with the answers in `python_strings_instructor.py` in the `instructor` folder beside it. Open `python_strings.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

## The changes and why

The student pairs fill in the blanks of `python_strings.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_strings_instructor.py`.

Part #1: you pick the file letter and the rank digit out of "e2" by index. Index 0 is the first character, the same counting Remus uses for rows and columns.

Part #2: `ord()` turns a letter into its code number. Subtracting `ord("a")` makes file a number 0 and file e number 4, which is exactly how `parse_square()` finds a column on Day 1, period 4.

Part #3: `chr()` goes the other way, so file number 6 becomes "g". Joining it with the rank gives "g7", the job of `square_name()`.

Part #4: `upper()` turns Black's pieces into White's, and `isupper()` tells the piece colors apart. Remus's `is_white()` on Day 2 is this one call.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Slides: a script, `print()`, variables, and strings indexed from 0. |
| 10:45 to 10:55 | The teacher shows `ord()` and `chr()` on the projector: the letter e is file number 4 because a is 0. |
| 10:55 to 11:40 | Student pairs work through the four parts of `python_strings.py`, running the file after each part. |
| 11:40 to 11:50 | Check together without running code: what is the file number of h4, and of a1? Why does file a count as 0? |
| 11:50 to 12:00 | Student pairs compare their printouts with the student pair next to them. |

## What you edit in the lab

Open `python_strings.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 13. Check the work by running `python_strings.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### Part #1 - Strings and Indexing

```text
13 |     square = "e2"
14 |     # Index 0 is the first character of a string, index 1 the second
15 +     file_letter = square[0]
16 +     rank_digit = square[1]
17 +     print(f"{square}: file letter {file_letter}, rank digit {rank_digit}")
18 |     print("  (expected file letter e, rank digit 2)")
19 |
```

**How it works:** A string is a row of characters, and `[ ]` reads one of them by its index. `square[0]` is the first character, the file letter e, and `square[1]` is the second, the rank digit 2. The f-string prints both.

### Part #2 - Letters Are Numbers: ord() and chr()

```text
23 |     print(f"chr(98) is {chr(98)}  (expected b)")
24 |     # Counting from file a = 0, file e is 4 letters after a
25 +     file_number = ord(file_letter) - ord("a")
26 +     rank_number = int(rank_digit)
27 +     print(f"{square} is file number {file_number}, rank number {rank_number}")
28 |     print("  (expected file number 4, rank number 2)")
29 |
```

**How it works:** `ord()` turns a letter into its number in the computer's character table, and the letters a to h have numbers in a row. Subtracting `ord("a")` gives 0 for a, 1 for b, and 4 for e: a file number. `int()` turns the text "2" into the number 2, so Python can do arithmetic with it.

### Part #3 - Numbers Back to a Square Name

```text
30 |     print("Part #3 - Numbers Back to a Square Name")
31 |     # File number 6 is the g-file: start at "a" and count 6 letters on
32 +     letter = chr(ord("a") + 6)
33 +     name = f"{letter}{7}"
34 +     print(f"File number 6, rank 7 is the square {name}  (expected g7)")
35 |
36 |     print("Part #4 - Upper and Lower Case")
```

**How it works:** `chr()` goes the other way, from a number back to a letter. Adding 6 to the number of "a" lands on "g". The f-string then glues the letter and the rank 7 into the square name g7.

### Part #4 - Upper and Lower Case

```text
37 |     # In Remus, uppercase letters are White pieces and lowercase are Black
38 |     black_back_rank = "rnbqkbnr"
39 +     white_back_rank = black_back_rank.upper()
40 +     print(f"Black: {black_back_rank}  White: {white_back_rank}")
41 |     print("  (expected Black: rnbqkbnr  White: RNBQKBNR)")
42 +     is_white = "N".isupper()
43 +     print(f"Is N a White piece? {is_white}  (expected True)")
44 |
45 |
```

**How it works:** `upper()` returns a new string with every letter in uppercase, which turns Black's back rank into White's. Remus uses the same rule as FEN: uppercase is White and lowercase is Black. `"N".isupper()` asks whether a letter is uppercase and gives True or False.
