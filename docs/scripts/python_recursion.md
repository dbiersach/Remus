# python_recursion.py: A function that calls itself

*Day 6, period 1. The lab file is `student/Day 06 - Count positions and read FEN/period1/python_recursion.py`, and the answers are in `instructor/Day 06 - Count positions and read FEN/period1/python_recursion_instructor.py`.*

## The big picture

Some problems hold a smaller copy of themselves. To count the positions two moves
ahead, count the positions one move ahead after each first move. A function that
calls itself on the smaller problem is recursive. This lab writes two recursive
functions and reads a third.

## Where this piece fits

The lab does not import Remus. On Day 6, period 2, `perft()` in `perft.py` has the
shape of `knight_paths()` in Part #3: at depth 0 return 1, otherwise add up the count
after every move.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`perft.py`](perft.md)

## Words to know

- **recursion:** a function that calls itself on a smaller problem.
- **base case:** the smallest problem, answered without another call, such as 0 in the countdown.
- **leaf:** a position at the bottom of the tree, with no moves under it in the count.

## How it works

1. Part #1: `countdown()` prints a number and calls itself with the number minus 1, until 0.
2. Part #2: `count_leaves()` counts 1 for a move name and adds up the counts of a list's branches.
3. Part #3: read `knight_paths()`, predict its counts from a1, and run it.

The pair types 11 lines.

## Try it

Open `python_recursion.py` in `student/Day 06 - Count positions and read FEN/period1` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 3, 2, 1, Go!; 6 leaves and 2 under e4; and 2, 12, and 64 knight paths from a1.

## Puzzle questions

1. What happens to `countdown()` without its base case?
2. Draw the calls of `knight_paths(7, 0, 2)`: how many calls return 1?
