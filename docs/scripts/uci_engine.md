# uci_engine.py: Talk to En Croissant

*First appears in `instructor/Day 07 - Play full games in En Croissant`.*

## The big picture

En Croissant draws the board and runs the clocks. Remus does the thinking. The two
programs talk by sending lines of text, in a language called UCI.

This file reads En Croissant's commands and sends back Remus's answers.

## Where this piece fits

uci_engine.py sits at the top of the puzzle. It uses fen.py, make_move.py, legal_moves.py, search.py, and opening_book.py. remus.bat starts it.

- **Uses:** [`fen.py`](fen.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md), [`opening_book.py`](opening_book.md), [`search.py`](search.md)
- **Used by:** no other Remus file

## Words to know

- **UCI:** Universal Chess Interface, the text language between chess GUIs and engines.
- **GUI:** graphical user interface: the window with the board you click on.
- **standard input and output:** the lines a program reads in and prints out.
- **thread:** a second line of work that runs at the same time as the first.

## What it stores

A short conversation:

```text
En Croissant -> uci                          Remus -> id name Remus ... uciok
En Croissant -> isready                      Remus -> readyok
En Croissant -> position startpos moves e2e4
En Croissant -> go wtime 60000 btime 60000   Remus -> info depth 3 ... bestmove e7e5
```

## How it works

1. `main()` reads one line at a time.
2. `position` builds the game with `set_position()`.
3. `go` picks the brain. On Day 10, a book move comes first if there is one.
4. `thinking_time()` turns the clock into seconds to think.
5. `search_and_send()` runs `think()` in a thread, so Remus can still answer `isready` and `stop`.
6. `send()` prints each answer and flushes it right away.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    state_from_fen()  [fen.py]
    load_book()  [opening_book.py]
    send()
    set_position()
        state_from_fen()  [fen.py]
        make_move()  [make_move.py]
        move_from_uci()  [moves.py]
    book_move()  [opening_book.py]
    legal_moves()  [legal_moves.py]
    thinking_time()
    move_to_uci()  [moves.py]
    search_and_send()
        think()  [search.py]
        send()
        move_to_uci()  [moves.py]
```

## The functions

| Function | What it does | Day |
| --- | --- | --- |
| `send` | Sends one line to En Croissant right away. | 7 |
| `set_position` | Builds the game state from a position command. | 7 |
| `thinking_time` | Decides how many seconds to think from the clock. | 9 |
| `search_and_send` | Thinks in the background, then sends the best move. | 9 |

## How the file grows

- **Day 7:** `send`, `set_position`
- **Day 9:** `thinking_time`, `search_and_send`

## Try it

From inside a Day folder that has the file, run:

```bash
uv run uci_engine.py
```

You should see: Nothing at first. Type `uci`, then `isready`, then `go`. Type `quit` to stop.

## Puzzle questions

1. Why must debug messages go to standard error and not standard output?
2. What should Remus send when it has no legal move?

## Slides

Slides 1.1, 7.6, 9.7 in the [slide plan](../slide_plan.md).
