# python_functions.py: Small questions as functions

*Day 2, period 1. The lab file is `labs/day02/python_functions.py`, and the answers are in `labs/day02/instructor/python_functions_instructor.py`.*

## The big picture

Remus asks the same small questions again and again: is this piece White? Is this
square on the board? A function gives each question a name, so the code asks it in
one call. This lab writes three such functions, checks them with `assert`, and then
lets pytest run the same checks.

## Where this piece fits

The lab does not import Remus. On Day 2, period 3, `is_white()` in `game_state.py`
is the same one line as here, and `on_board()` in `move_generation.py` keeps every
move on the 64 squares.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`game_state.py`](game_state.md) and [`move_generation.py`](move_generation.md)

## Words to know

- **function:** a named block of code. `def` starts it, and `return` hands back the answer.
- **type hint:** `piece: str` and `-> bool` say what goes in and what comes out.
- **docstring:** the text in triple quotes under the `def` line that says what the function does.
- **tuple:** two or more values packed together, such as the square `(4, 4)`.
- **assert:** stops the program with an error when its test is False.
- **pytest:** a tool that finds functions named `test_...` and reports which pass.

## How it works

1. Type the one-line bodies of `is_white()` and `on_board()`; Part #1 calls them.
2. Part #2: write `is_black()` from nothing, with its type hints and docstring.
3. Part #3: unpack the square `(4, 4)` into `row` and `col`.
4. Part #4: call the two test functions, then run them again with pytest and break one on purpose.

The pair types 16 lines.

## Try it

From inside `student/Day 02 - Make and undo moves/period1`, run:

```bash
uv run python_functions.py
uv run pytest python_functions.py
```

You should see: True and False answers next to the expected ones, "Every assert passed", and then `2 passed` from pytest.

## Puzzle questions

1. Why does `on_board(8, 3)` return False when 8 is a perfectly good number?
2. What does pytest print when an `assert` fails, and which line does it point at?
