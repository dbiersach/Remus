# show_board.py: Draw the board as a picture

*First appears in `Day 01 - Draw the board/period4/instructor`.*

## The big picture

Remus keeps its board as letters in a list. That is easy for Python, but hard on the eyes.

This file turns a Remus board into a real picture of a chessboard and opens it in the web browser. From Day 3 on, it also draws an arrow for each move, so you can see the moves your own code finds.

## Where this piece fits

show_board.py is a helper beside the engine. It uses board.py, and from Day 3 on, move_generation.py, game_state.py, and moves.py. No Remus file uses it.

It is the one engine-side file that imports python-chess. python-chess only draws the picture. Remus never asks it about the rules.

- **Uses:** [`board.py`](../engine_code/board.md), [`moves.py`](../engine_code/moves.md)
- **Uses only in its self-check:** [`game_state.py`](../engine_code/game_state.md), [`move_generation.py`](../engine_code/move_generation.md)
- **Used by:** no other Remus file

## Words to know

- **SVG:** a picture file made of shapes, which any web browser can show.
- **python-chess:** a chess library for Python. Remus uses it only to draw pictures and to check its own answers in tests.
- **arrow:** a line from the square a piece starts on to the square it lands on.

## What it stores

The picture is saved as `board.svg` in the same folder as the script. Each run saves over the last picture.

python-chess numbers its squares from a1 = 0 to h8 = 63. Remus uses (row, col) with row 0 at rank 8, so the file turns rank `8 - row` into python-chess's rank number `7 - row`.

## How it works

1. `to_python_chess()` copies every piece onto an empty python-chess board.
2. `show_board()` asks python-chess for the picture, saves it, and opens the browser.
3. From Day 3, `show_moves()` turns each Move into an arrow and calls `show_board()`.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
show_moves()
    show_board()
        to_python_chess()
    python_chess_square()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `to_python_chess` | Copies a Remus board into a python-chess board. | Day 1, period 4 |
| `show_board` | Saves a picture of the board and opens it in the browser. | Day 1, period 4 |
| `python_chess_square` | Turns a Remus (row, col) square into a python-chess square number. | Day 3, period 2 |
| `show_moves` | Draws the board with one arrow for each move. | Day 3, period 2 |

## How the file grows

- **Day 1, period 4:** `to_python_chess`, `show_board`
- **Day 3, period 2:** `python_chess_square`, `show_moves`

## Try it

Open `show_board.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: A picture of the board in the web browser. On Day 3 and later, four arrows show the knight moves from the start.

## Puzzle questions

1. Why does row 0 become python-chess rank 7?
2. Change main() to draw the moves of a rook on d4 of an empty board. How many arrows do you expect?

## Slides

Slides 1.6, 3.6 in the [slide plan](../course/slide_plan.md).
