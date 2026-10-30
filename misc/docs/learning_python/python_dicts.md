# python_dicts.py: A dict, a copy, and a dataclass

*Day 2, period 2. The lab file is `Day 02 - Make and undo moves/period2/student/python_dicts.py`, and the answers are in `Day 02 - Make and undo moves/period2/instructor/python_dicts_instructor.py`.*

## The big picture

A chess game needs more than a board: whose turn it is, which castling moves are still
allowed, and more. A dict keeps each of those facts under a name. This lab also shows
the trap of two names for one board, the copy that avoids it, and a dataclass, a
small record for a move.

## Where this piece fits

The lab does not import Remus. On Day 2, period 3, `new_game()` in `game_state.py`
returns a dict like the one in Part #1, and `Move` in `moves.py` is a dataclass like
the one in Part #4.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`game_state.py`](../engine_code/game_state.md) and [`moves.py`](../engine_code/moves.md)

## Words to know

- **dict:** values stored under keys, such as `state["turn"]`.
- **aliasing:** two names for the same list: a change through one name shows through the other.
- **deepcopy():** makes a new board with new rows, so changing the copy leaves the original alone.
- **dataclass:** a class that lists its fields once, such as `from_square` and `to_square`.

## How it works

1. Part #1: read the side to move and the castling rights by key, then change the side to move.
2. Part #2: give the board a second name, `b2`, put a pawn on e4 through it, and see it on `board`.
3. Part #3: make a real copy with `deepcopy()`, change a1 on the copy, and compare.
4. Part #4: write the `Move` dataclass, make the move e2 to e4, and print it.

The student pair types 18 lines.

## Try it

Open `python_dicts.py` in `Day 02 - Make and undo moves/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: w, KQkq, then b; a pawn that shows on both names; a copy that changes alone; and `Move(from_square='e2', to_square='e4')`.

## Puzzle questions

1. Why can't `undo_move()` just keep `old_board = board` before a move?
2. Is `b3 == board` the same question as `b3 is board`? What does each one ask?
