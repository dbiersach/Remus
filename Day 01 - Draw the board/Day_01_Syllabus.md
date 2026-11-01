# Day 1: Setup and the board

Day 1 opens with the concept check and the interest survey that come back on Day 10, then forms the student pairs, sets up the laptops, and teaches the first Python: strings and lists. In the last period each student pair writes its first Remus code. By 4:30 Remus prints its own board, converts a square name such as e2 into a (row, col) pair and back, and draws the board as a picture.

## Objectives for the day

By 4:30, each student pair can:

- Open a Python file in VS Code, run it with the Run Python File button, and read what it prints.
- Turn a square name such as e2 into numbers with indexing, `ord()`, and `chr()`, and print the answer in an f-string.
- Build an 8x8 board as a list of rows and read one square with `board[row][col]`.
- Say where each rank lives: row 0 is rank 8, and column 0 is file a.
- Write the first four Remus functions in `board.py`.

## The day at a glance

| Period | Time | Title | Student pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Welcome and setup | The lab `python_setup.py` (6 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Python lab 1: scripts, strings, ord and chr, f-strings | The lab `python_strings.py` (13 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | Python lab 2: lists and nested lists | The lab `python_lists.py` (25 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | board.py: the board and its square names | `print_board()` in `board.py` (6 lines); `square_name()` in `board.py` (1 line); `parse_square()` in `board.py` (5 lines); `piece_at()` in `board.py` (2 lines) |

## Period 1, 8:30 to 10:00: Welcome and setup

| Time | Activity |
| --- | --- |
| 8:30 to 8:55 | The concept check (handout 13, 20 minutes) and the interest survey (handout 15, 5 minutes), on paper, alone, before anyone has seen Remus. Nobody is expected to answer much yet: the same two sheets come back on Day 10 to show how far each student traveled. |
| 8:55 to 9:05 | Welcome. The finished Remus plays a game in Lucas Chess on the projector while the teacher names its five parts: board, moves, rules, search, and evaluation. The story of the name: Sargon, the 1978 chess program, and Rimush, the first son of Sargon of Akkad. Remus is a son of Sargon. |
| 9:05 to 9:10 | Form the ten student pairs. The driver types and the navigator reads and checks; the two swap roles every period. Each student pair picks a team name for `CONTRIBUTORS.md`. |
| 9:10 to 9:30 | Setup, the only git and uv commands of the workshop. The teacher walks each student through installing git and uv, cloning the Remus repository, and running `uv sync` once to build the `.venv` folder. From here on every step runs from VS Code's Run button. |
| 9:30 to 9:40 | Notation on the demonstration board: square names, SAN for people (`Nf3`, `Bxh8`, `e8=Q`), and UCI for programs (`g1f3`). |
| 9:40 to 10:00 | Student pairs type the 6 lines of `python_setup.py` and run it. It checks the laptop, greets the team, and prints a first chess line. The teacher and the assistant check that every laptop runs a file with the Run button and opens Lucas Chess. |

[`Day_01_Period_01_Goals.md`](period1/Day_01_Period_01_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: Python lab 1: scripts, strings, ord and chr, f-strings

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Slides: a script, `print()`, variables, and strings indexed from 0. |
| 10:45 to 10:55 | The teacher shows `ord()` and `chr()` on the projector: the letter e is file number 4 because a is 0. |
| 10:55 to 11:40 | Student pairs work through the four parts of `python_strings.py`, running the file after each part. |
| 11:40 to 11:50 | Check together without running code: what is the file number of h4, and of a1? Why does file a count as 0? |
| 11:50 to 12:00 | Student pairs compare their printouts with the student pair next to them. |

[`Day_01_Period_02_Goals.md`](period2/Day_01_Period_02_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: Python lab 2: lists and nested lists

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Unplugged warm-up, "Call the square": the teacher calls (6, 4), the navigator puts a token on the printed board, and the driver names the square, e2. Then the partners swap. |
| 1:15 to 1:30 | Slides: lists, `for` and `range()`, `len()`, and a list of lists. |
| 1:30 to 2:15 | Student pairs work through the four parts of `python_lists.py`: a list of pieces, a loop over every square, the board as a list of rows, and the pawns in a row. |
| 2:15 to 2:30 | Without running code, each student pair names `board[4][4]` (e4) and says why row 0 is rank 8. |

[`Day_01_Period_03_Goals.md`](period3/Day_01_Period_03_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: board.py: the board and its square names

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: the Remus board is an 8x8 list of one-character strings. Uppercase is White, lowercase is Black, and `.` is empty. The teacher walks through `new_board()`. |
| 3:15 to 4:00 | Student pairs write `print_board()`, `square_name()`, `parse_square()`, and `piece_at()` in `board.py` and run `run_tests.py` after each one. |
| 4:00 to 4:10 | Student pairs run `show_board.py`, which draws their board as a picture in the web browser. |
| 4:10 to 4:25 | Show and choose: two or three student pairs show their `parse_square()` on the projector, the class picks one for clarity, and the teacher adds the student pair's team name to `CONTRIBUTORS.md`. |
| 4:25 to 4:30 | Checkpoint: running `board.py` prints the start board and "b1 holds N, expected N". |

[`Day_01_Period_04_Goals.md`](period4/Day_01_Period_04_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Running `board.py` prints the start board and "b1 holds N, expected N", and `test_board.py` passes.

Each period folder starts from working code, so a student pair that falls behind opens the next period's folder with the rest of the class.
