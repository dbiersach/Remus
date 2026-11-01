# Remus for students

This folder holds everything you read during the workshop. The code you write lives
in the Day folders at the top of Remus, and the pages here explain it.

| Page | Read it when |
| --- | --- |
| [`learn_chess.md`](learn_chess.md) | A rule trips you up: castling, en passant, promotion, the draws, or how to read a move such as `Nbd2+` |
| [`lucas_chess_guide.md`](lucas_chess_guide.md) | You want to add Remus to Lucas Chess, watch it play Stockfish, or play it yourself |
| [`remus_program_overview.md`](remus_program_overview.md) | You want the whole picture: how the engine files stack up, what the game state holds, how one move travels from Lucas Chess to `bestmove`, and what the tests check |
| [`engine_code/`](engine_code/) | You are writing a function in a file and want that file's page, such as [`board.md`](engine_code/board.md) for `board.py` |
| [`python_labs.md`](python_labs.md) | You are working on a Python lab, `python_*.py` |
| [`class_demos.md`](class_demos.md) | The class runs a demo, such as `demo_promotion.py` or `compare_search.py` |
| [`remus_versions.md`](remus_versions.md) | Day 9: the ten enhancements, how they add up to Remus-GOLD, the battles, and the league table |
| [`science_ai.md`](science_ai.md) | Day 10: `hidden_peak.py` and `phase_hunt.py` |

## Where you work

You write Remus in the `student` folders. The top of the Remus folder has one
folder for each day of the workshop, and each Day folder has four period folders,
`period1` to `period4`. Each period folder holds a `student` folder, where you work,
and an `instructor` folder with the finished code. The syllabus at the top of each
Day folder, such as `Day_01_Syllabus.md`, shows the whole day: what you will learn, and what happens in each
period, from 8:30 to 4:30.

Each `student` folder starts with working code from the periods before. The goals
file beside it, such as `Day_03_Period_02_Goals.md`, lists what you will learn and how you will show it, the files that are
new or growing, a paragraph on every change you make and why, the steps of the
period with their times, and a table of the
functions left for you to write, with the line where each one starts. Each of those
functions keeps its name, its docstring, and its type hints. Its body is a stub:

```python
    # Day 1, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 1 P4: write square_name()")
```

Thirteen periods hold a Python lab (`python_*.py`), such as `python_lists.py` on Day 1
or `python_recursion.py` on Day 6, and three hold a demo (`demo_*.py`), such as
`demo_promotion.py` on Day 5. In a lab or demo file, each line that holds only a `#`
is one line for you to type. On Day 6, period 3 the `bug_hunt` folder holds a copy
of Remus with three planted bugs for you to find and fix.

## How to work on a function

1. Read the period's goals file, then the page for the file in [`engine_code/`](engine_code/),
   such as [`board.md`](engine_code/board.md) for `board.py`.
2. Read the function's docstring. It says what the function must do.
3. Delete the two stub comments and the `raise` line, and write the body.
4. Run the tests: open `run_tests.py` in the `student` folder and press Run.
5. Run the file itself, such as `board.py`, with VS Code's Run Python File button,
   and compare with the expected answers.

A test that fails with `NotImplementedError` points to a function you have not
written yet.

## The functions you write

About 40 functions over the two weeks, from `print_board()` on Day 1 to `search()`
in `phase_hunt.py` on Day 10. The teacher's
[`student_edit_plan.md`](../teachers/student_edit_plan.md) lists every one by day and
period, with the lines to type, and each period's goals file lists the ones for that
period with the line where each starts.

On Day 9, periods 2 and 3, each student pair also writes the functions of its enhanced engine
in the `engines/student` folder at the top of the Remus folder, listed in
[`remus_versions.md`](remus_versions.md).

The finished versions are in the `instructor` folder beside each `student` folder.
Try on your own first.
