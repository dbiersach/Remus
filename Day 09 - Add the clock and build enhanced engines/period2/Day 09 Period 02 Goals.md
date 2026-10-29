# Day 9, Period 2: Python lab 12 and the engine enhancements

Each student pair builds one enhanced engine in `engines/student` at the top of the Remus folder, such as `engines/student/10 RED - Transposition table`. That engine folder already holds the whole Remus engine from period 1, so the student pair adds only its one enhancement there. Leave `00 WHITE - No enhancements` as it is: it is plain Remus, kept so the class can measure each enhancement against it.

## Learning objectives

By the end of this period, each student pair can:

- Use a dict as a cache with tuples as keys. **Measured by:** The lab remembers perft counts already computed and prints the time saved.
- Add one enhancement to Remus-WHITE. **Measured by:** The enhanced engine's own tests pass in its folder.

## The files

The lab is `python_caches.py` in the `student` folder, with the answers in `python_caches_instructor.py` in the `instructor` folder beside it. Open `python_caches.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

This folder holds no engine code. Your student pair works in one folder only: your own engine folder in `engines/student`, such as `10 RED - Transposition table`. That folder already holds the whole Remus engine you finished in period 1, so you add only your one enhancement there. Do not change `00 WHITE - No enhancements`: it is plain Remus with no enhancement, and it stays as it is so the class can measure every enhancement against it. The `README.md` in each engine folder explains its enhancement, and its section "The code you type" shows every line the student pair types, with line numbers, the lines around it, and how the code works.

Click your student pair's engine folder below. Its `README.md` shows the code to type, and `run_tests.py` checks it.

| Engine folder | The code you type | Tests |
| --- | --- | --- |
| [01 GRAY - King safety](../../engines/student/01%20GRAY%20-%20King%20safety) | [`README.md`](../../engines/student/01%20GRAY%20-%20King%20safety/README.md) | [`run_tests.py`](../../engines/student/01%20GRAY%20-%20King%20safety/run_tests.py) |
| [02 YELLOW - Draw sense](../../engines/student/02%20YELLOW%20-%20Draw%20sense) | [`README.md`](../../engines/student/02%20YELLOW%20-%20Draw%20sense/README.md) | [`run_tests.py`](../../engines/student/02%20YELLOW%20-%20Draw%20sense/run_tests.py) |
| [03 CYAN - Mating bonus](../../engines/student/03%20CYAN%20-%20Mating%20bonus) | [`README.md`](../../engines/student/03%20CYAN%20-%20Mating%20bonus/README.md) | [`run_tests.py`](../../engines/student/03%20CYAN%20-%20Mating%20bonus/run_tests.py) |
| [04 PINK - Principal variation search](../../engines/student/04%20PINK%20-%20Principal%20variation%20search) | [`README.md`](../../engines/student/04%20PINK%20-%20Principal%20variation%20search/README.md) | [`run_tests.py`](../../engines/student/04%20PINK%20-%20Principal%20variation%20search/run_tests.py) |
| [05 ORANGE - Null-move pruning](../../engines/student/05%20ORANGE%20-%20Null-move%20pruning) | [`README.md`](../../engines/student/05%20ORANGE%20-%20Null-move%20pruning/README.md) | [`run_tests.py`](../../engines/student/05%20ORANGE%20-%20Null-move%20pruning/run_tests.py) |
| [06 BROWN - Late move reductions](../../engines/student/06%20BROWN%20-%20Late%20move%20reductions) | [`README.md`](../../engines/student/06%20BROWN%20-%20Late%20move%20reductions/README.md) | [`run_tests.py`](../../engines/student/06%20BROWN%20-%20Late%20move%20reductions/run_tests.py) |
| [07 PURPLE - Pawn structure](../../engines/student/07%20PURPLE%20-%20Pawn%20structure) | [`README.md`](../../engines/student/07%20PURPLE%20-%20Pawn%20structure/README.md) | [`run_tests.py`](../../engines/student/07%20PURPLE%20-%20Pawn%20structure/run_tests.py) |
| [08 GREEN - Opening book](../../engines/student/08%20GREEN%20-%20Opening%20book) | [`README.md`](../../engines/student/08%20GREEN%20-%20Opening%20book/README.md) | [`run_tests.py`](../../engines/student/08%20GREEN%20-%20Opening%20book/run_tests.py) |
| [09 BLUE - Killer moves](../../engines/student/09%20BLUE%20-%20Killer%20moves) | [`README.md`](../../engines/student/09%20BLUE%20-%20Killer%20moves/README.md) | [`run_tests.py`](../../engines/student/09%20BLUE%20-%20Killer%20moves/run_tests.py) |
| [10 RED - Transposition table](../../engines/student/10%20RED%20-%20Transposition%20table) | [`README.md`](../../engines/student/10%20RED%20-%20Transposition%20table/README.md) | [`run_tests.py`](../../engines/student/10%20RED%20-%20Transposition%20table/run_tests.py) |

## The changes and why

The student pairs fill in the blanks of `python_caches.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_caches_instructor.py`.

Part #1: `remembered_perft()` stores each knight path count in a dict under the tuple key `(square, depth)`. The second call finds the answer and returns at once. Remus-RED's transposition table remembers search results the same way.

Parts #2 and #3 use `math.dist()` for the straight-line distance from d4 to g7, which Remus-CYAN needs, and `random.seed()`, which makes a random choice repeat on every run.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:50 | Student pairs work through `python_caches.py`: a dict remembers answers, `math.dist()`, and `random.seed()`. |
| 10:50 to 11:00 | Slides: the ten enhanced engines. Each one is the period 1 Remus with one enhancement added, such as RED (transposition table) or BLUE (killer moves). The folder names use colors so that no engine sounds better than another. |
| 11:00 to 12:00 | Each student pair opens its enhanced engine in `engines/student`, reads the version README, and writes the enhanced engine's stubbed code. |

## What you edit in the lab

Open `python_caches.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 7. Check the work by running `python_caches.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### `remembered_perft()`

```python
34 |     """Return knight_perft from a square, computing each (square, depth) only once."""
35 |     # A tuple can be a dict key, so one key holds both the square and the depth
36 +     key = (square, depth)
37 +     if key not in cache:
38 +         cache[key] = knight_perft(square, depth)
39 +     return cache[key]
40 |
41 |
```

**How it works:** `(square, depth)` packs two values into one tuple, such as `((7, 6), 8)` for 8 moves from g1. A tuple never changes, so Python accepts it as a dict key, and one key holds both facts. `if key not in cache` asks whether this question has been answered before. Only when it has not does the slow `knight_perft` run, and its answer goes into `cache[key]`. The last line returns the stored answer either way, so the second call with the same square and depth skips the counting and returns at once.

### Part #2 - math.dist() Measures a Straight Line

```python
56 |     print("Part #2 - math.dist() Measures a Straight Line")
57 |     # d4 is (row 4, col 3) and g7 is (row 1, col 6): three squares across, three up
58 +     distance = math.dist((4, 3), (1, 6))
59 +     print(f"From d4 to g7: {distance:.3f} squares  (expected 4.243)")
60 |
61 |     print("Part #3 - random.seed() Repeats the Same Random Numbers")
```

**How it works:** `math.dist` measures the straight-line distance between two points. d4 is (row 4, col 3) and g7 is (row 1, col 6): 3 rows and 3 columns apart, so the distance is the square root of 3 x 3 + 3 x 3 = 18, about 4.243. The f-string's `:.3f` prints three digits after the decimal point.

### Part #3 - random.seed() Repeats the Same Random Numbers

```python
60 |
61 |     print("Part #3 - random.seed() Repeats the Same Random Numbers")
62 +     random.seed(2016)
63 |     first_roll = random.randint(1, 6)
64 |     random.seed(2016)
```

**How it works:** `random.seed(2016)` sets the starting point of Python's random numbers. The code below rolls a die, seeds again with the same number, and rolls again, so both rolls are the same and the comparison prints True. Without the first seed the two rolls would match only about one time in six.
