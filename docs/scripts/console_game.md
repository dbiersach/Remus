# console_game.py: Play chess in the terminal

*First appears in `instructor/Day 07 - Play full games and score positions/period2`.*

## The big picture

Before Lucas Chess, you can play right in the terminal. Type moves like `e4` and
`Nf3`.

With `remus` after the command, Remus plays Black.

## Where this piece fits

console_game.py uses board.py, fen.py, notation.py, make_move.py, game_end.py, and search.py.

- **Uses:** [`board.py`](board.md), [`fen.py`](fen.md), [`game_end.py`](game_end.md), [`make_move.py`](make_move.md), [`notation.py`](notation.md), [`opening_book.py`](opening_book.md), [`search.py`](search.md)
- **Used by:** no other Remus file

## Words to know

- **terminal:** the text window where you type commands.
- **loop:** code that repeats until something stops it.

## What it stores

The loop keeps going until `game_result()` says the game is over.

## How it works

1. Print the board.
2. If it is Remus's turn, Remus picks a move. Otherwise, read your move with `parse_san()`.
3. A bad move prints an error and asks again. Typing `quit` stops the game.
4. Make the move and repeat.
5. At the end, print the result and the reason.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    state_from_fen()  [fen.py]
    load_book()  [opening_book.py]
    print_board()  [board.py]
    game_result()  [game_end.py]
    make_move()  [make_move.py]
    book_move()  [opening_book.py]
    think_move()  [search.py]
    parse_san()  [notation.py]
    move_to_san()  [notation.py]
```

## Try it

Open `console_game.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: The board and a prompt like `White to move:`.

## Puzzle questions

1. What happens if you type `Ke2` at the start?
2. Which file decides when the loop stops?

## Slides

Slides 1.1 in the [slide plan](../slide_plan.md).
