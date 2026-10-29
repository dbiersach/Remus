# Day 4, Period 1: Python lab 6: modules, imports, __main__

## Learning objectives

By the end of this period, each student pair can:

- Split code into modules and import one from another. **Measured by:** The lab's two files run together, and running the imported file alone with the Run button prints its own self-check only through `main()`.
- Draw which Remus files import which, and name the file that runs. **Measured by:** The student pair's paper import map draws arrows from `move_generation.py` to `board.py`, `game_state.py`, and `moves.py`, and marks the lab as the file named `__main__`.

## The files

The lab is `python_modules.py` in the `student` folder, with the answers in `python_modules_instructor.py` in the `instructor` folder beside it. Open `python_modules.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The student pairs fill in the blanks of `python_modules.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_modules_instructor.py`.

The lab imports `board.py`, `game_state.py`, `move_generation.py`, and `moves.py` from the same folder. An import runs the other file once and hands over its functions, so no code is copied.

Part #1 prints `__name__`: the file that VS Code runs is `__main__`, and an imported file keeps its own name. That is why `board.py` prints its board when VS Code runs `board.py` and stays silent when the lab imports it, and why every Remus print sits inside `main()`.

Part #2 calls `new_board()` and `knight_moves()` from the imported files and lists the two knight moves from g1. Part #3 runs `board.py` on its own in VS Code and shows its board, because there `board.py` is the file named `__main__`.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a module is a file, `import` reads it, and `if __name__ == "__main__"` keeps a file quiet when another file imports it. |
| 8:45 to 9:20 | Student pairs work through Parts #1 to #3 of `python_modules.py`: every file has a `__name__`, use yesterday's `board.py` and `move_generation.py`, and list the knight moves from g1. |
| 9:20 to 9:35 | Unplugged: the import map. On paper, each student pair writes the name of every `.py` file in the folder and draws an arrow from each file to every file it imports, then circles the file that runs as `__main__`. |
| 9:35 to 9:50 | Two student pairs show their maps on the projector. The teacher shows that every arrow stays inside the folder: each period folder holds a complete Remus, so its files import only each other. |
| 9:50 to 10:00 | Every student pair shows its map to the teacher or the assistant. |

## What you edit in the lab

Open `python_modules.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 11. Check the work by running `python_modules.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### The imports

```text
10 |
11 | # Each import line reads another file of this folder by its name, without the .py
12 + import board
13 + from board import new_board, parse_square
14 + from game_state import WHITE
15 + from move_generation import knight_moves
16 | from moves import move_to_uci
17 |
```

**How it works:** `import board` loads `board.py` and keeps its names behind `board.`, as in `board.__name__`. `from board import new_board, parse_square` copies those two names into this file, so they can be called without the prefix. Python finds each file by its name, without `.py`, in the same folder.

### Part #1 - Every File Has a __name__

```text
20 |     print("Part #1 - Every File Has a __name__")
21 |     # The file that VS Code runs is named "__main__"; an imported file keeps its name
22 +     print(f"This file's __name__: {__name__}  (expected __main__)")
23 +     print(f"board.py's __name__: {board.__name__}  (expected board)")
24 |     print("board.py printed no board when it was imported: its main() did not run")
25 |
```

**How it works:** Every file has a `__name__`. The file you run is called "__main__", and a file you import keeps its own name, "board". The `if __name__ == "__main__"` guard at the bottom of `board.py` is false when the file is imported, so its `main()` does not run.

### Part #2 - Use Functions from Another File

```text
25 |
26 |     print("Part #2 - Use Functions from Another File")
27 +     start = new_board()
28 +     square = parse_square("g1")
29 +     moves = knight_moves(start, square, WHITE)
30 |     names = ""
31 +     for move in moves:
32 +         names += move_to_uci(move) + " "
33 |     print(f"Knight moves from g1: {names}  (expected g1f3 g1h3)")
34 |
```

**How it works:** These lines use functions from three other files. They build the starting board, turn "g1" into a square, and ask `knight_moves` for the knight's moves. The loop adds each move's UCI text to `names`.
