# Day 1, Period 1: Welcome and setup

Watch the finished Remus play in Lucas Chess, form pairs, and check that every laptop opens Remus in VS Code and runs a file with the Run button.

## Learning objectives

By the end of this period, each pair can:

- Start VS Code, open a Python file, and run it with the Run Python File button (the triangle at the top right of the editor). **Measured by:** Running `python_setup.py` prints Python 3.14 or later and `python-chess installed: True` on the pair's laptop.
- Store text in a variable and print it inside an f-string. **Measured by:** Part #2 of `python_setup.py` greets the pair's own team name and counts its characters correctly.
- Name the parts of a chess engine that Remus will grow: board, moves, rules, search, and evaluation. **Measured by:** Exit ticket: each student lists three of the five parts and one job of each.

## The files

This period comes before any Remus code. The lab is `python_setup.py` in the `student` folder, with the answers in `python_setup_instructor.py` in the `instructor` folder beside it. Open `python_setup.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

## The changes and why

The pairs fill in the blanks of `python_setup.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_setup_instructor.py`.

Part #1 is already written. It prints the Python version and whether python-chess is installed, so the teacher can see at a glance that the laptop is ready.

Part #2: you store your team name in a variable and print it inside an f-string. A variable is a name for a value, and an f-string puts values into text. Remus prints every result this way.

Part #3: you store White's back rank as one string and print the letter at index 4, the king. Remus writes pieces as letters too, uppercase for White.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:40 | Welcome. The finished Remus plays a game in Lucas Chess on the projector. |
| 8:40 to 8:50 | The story of the name: Sargon, the 1978 chess program, and Rimush, the first son of Sargon of Akkad. Remus is a son of Sargon. |
| 8:50 to 9:00 | Form the ten pairs. The driver types and the navigator reads and checks; the two swap roles every period. Each pair picks a team name for `CONTRIBUTORS.md`. |
| 9:00 to 9:20 | Setup, the only git and uv commands of the workshop. The course designer shows each pair how to install git and uv, clone the Remus repository, and run `uv sync` once to build the `.venv` folder. From here on every step runs from VS Code's Run button. |
| 9:20 to 9:30 | Notation on the demonstration board: square names, SAN for people (`Nf3`, `Bxh8`, `e8=Q`), and UCI for programs (`g1f3`). |
| 9:30 to 9:50 | Pairs type the 6 lines of `python_setup.py` and run it. It checks the laptop, greets the team, and prints a first chess line. The teacher and the assistant check that every laptop runs a file with the Run button and opens Lucas Chess. |
| 9:50 to 10:00 | Exit ticket: each student lists three of the five parts of a chess engine (board, moves, rules, search, evaluation) and one job of each. |

## What you edit in the lab

Open `python_setup.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 6. Check the work by running `python_setup.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
