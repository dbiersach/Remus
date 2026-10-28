# demo_practice_positions.py: Predict, then count

*Day 4, period 4. The demo file is `Day 04 - Keep only legal moves/period4/student/demo_practice_positions.py`, and the answers are in `Day 04 - Keep only legal moves/period4/instructor/demo_practice_positions_instructor.py`.*

## The big picture

A rule in the code is right only if it gives the right answer on positions where
you already know the answer. This demo builds three small positions, and for each
the pair writes a prediction before Remus counts the legal moves.

## Where this piece fits

The demo runs in the Day 4, period 4 folder and uses the legal-move filter that the
pairs finished in period 3. Its positions are the same as the practice-position tests
in `test_legal_moves.py`.

- **Uses:** [`board.py`](board.md), [`game_state.py`](game_state.md), [`attacks.py`](attacks.md), [`legal_moves.py`](legal_moves.md), [`moves.py`](moves.md)
- **Used by:** nothing; the tests in `test_legal_moves.py` check the same positions

## Words to know

- **check:** the king is attacked. Every legal move must end the check.
- **pin:** a piece that cannot move because moving it would expose its own king.
- **prediction:** the count the pair expects, written down before running the code.

## How it works

1. `position()` builds a state from a dict such as `{"e1": "K", "e8": "r"}`.
2. Part #1: predict the moves from the start position, then compare with Remus.
3. Part #2: a rook on e8 checks the king on e1. Predict how many squares the king can escape to.
4. Part #3: add a White knight on e2 and count only the moves that start on e2.
5. Part #4: change the pieces and predict again.

The pair types 14 lines.

## Try it

Open `demo_practice_positions.py` in `Day 04 - Keep only legal moves/period4/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: each board with "You predicted ..., Remus finds ...": 20, 4, and 4 legal moves, and 0 legal knight moves.

## Puzzle questions

1. Why does the king in Part #2 have 4 moves and not 5?
2. Would a pinned rook on e2 have any legal moves? Try it in Part #4.
