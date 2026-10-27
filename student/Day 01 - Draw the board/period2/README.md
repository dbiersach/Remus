# Day 1, Period 2: Python lab 1: scripts, strings, ord and chr, f-strings

## Learning objectives

By the end of this period, each pair can:

- Pick single characters out of a string by index, counting from 0. **Measured by:** Part #1 of `python_strings.py` prints file letter e and rank digit 2 for `"e2"`.
- Turn letters into numbers and back with `ord()` and `chr()`. **Measured by:** Part #2 prints file number 4 for e2, and Part #3 builds `"g7"` from file number 6 and rank 7.
- Tell White and Black pieces apart by uppercase and lowercase. **Measured by:** Part #4 prints `RNBQKBNR` from `rnbqkbnr` and `True` for `"N".isupper()`.
- Explain why file a is number 0. **Measured by:** Without running code, the pair says the file number of h4 (7) and of a1 (0), and why.

## The files

This period comes before any Remus code. The lab is `python_strings.py` in `student/`, with the answers in `python_strings_instructor.py` in `instructor/`. Both come from `labs/day01/`. Run it with `uv run python_strings.py`.

## The changes and why

The pairs fill in the blanks of `python_strings.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_strings_instructor.py`.

Part #1: you pick the file letter and the rank digit out of "e2" by index. Index 0 is the first character, the same counting Remus uses for rows and columns.

Part #2: `ord()` turns a letter into its code number. Subtracting `ord("a")` makes file a number 0 and file e number 4, which is exactly how `parse_square()` finds a column on Day 1, period 4.

Part #3: `chr()` goes the other way, so file number 6 becomes "g". Joining it with the rank gives "g7", the job of `square_name()`.

Part #4: `upper()` turns Black's pieces into White's, and `isupper()` tells the colors apart. Remus's `is_white()` on Day 2 is this one call.

## What you edit this period

Open `python_strings.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 13. Check the work with `uv run python_strings.py` and compare each printed result with the expected value beside it.
