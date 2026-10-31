# uci_engine.py: Talk to Lucas Chess

*First appears in `Day 05 - Add castling, en passant, and promotion/period4/instructor`.*

## The big picture

Lucas Chess draws the board and runs the clocks. Remus does the thinking. The two
programs talk by sending lines of text, in a language called UCI.

This file reads Lucas Chess's commands and sends back Remus's answers.

## Where this piece fits

uci_engine.py sits at the top of the puzzle. It uses fen.py, make_move.py, legal_moves.py, search.py, and opening_book.py. remus.bat starts it.

A first, small version arrives on Day 5, period 4. It follows games from the starting position and plays a random legal move, so student pairs can play their own Remus in Lucas Chess before the week ends. The teacher hands it out ready to run. On Day 7 the class reads every command, and the full version reads FEN and calls the brains in search.py.

- **Uses:** [`fen.py`](fen.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md), [`opening_book.py`](opening_book.md), [`search.py`](search.md)
- **Used by:** no other Remus file

## Words to know

- **UCI:** Universal Chess Interface, the text language between chess GUIs and engines.
- **GUI:** graphical user interface: the window with the board you click on.
- **standard input and output:** the lines a program reads in and prints out.

## What it stores

A short conversation:

```text
Lucas Chess -> uci                          Remus -> id name Remus ... uciok
Lucas Chess -> isready                      Remus -> readyok
Lucas Chess -> position startpos moves e2e4
Lucas Chess -> go wtime 60000 btime 60000   Remus -> info depth 3 ... bestmove e7e5
```

## How it works

1. `main()` reads one line at a time.
2. `position` builds the game with `set_position()`.
3. `go` picks the brain. In Remus-GREEN and Remus-GOLD, a book move comes first if there is one.
4. `thinking_time()` turns the clock into seconds to think. It plans to spend a thirtieth of the clock, but
   it never counts the last 3 seconds, because sending each move costs a little time
   the search does not see. Without that reserve, a long game with no increment
   runs the clock out.
5. On `go`, `think()` searches until its time is up, and Remus sends `bestmove` before it reads the next command.
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
    think()  [search.py]
    move_to_uci()  [moves.py]
    send()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `send` | Sends one line to Lucas Chess right away. | Day 5, period 4 |
| `set_position` | Builds the game state from a position command. | Day 5, period 4 |
| `thinking_time` | Decides how many seconds to think from the clock. | Day 9, period 1 |

## How the file grows

- **Day 5, period 4:** `send`, `set_position`
- **Day 9, period 1:** `thinking_time`

## Try it

Open `uci_engine.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: Nothing at first. Type `uci`, then `isready`, then `go`. Type `quit` to stop.

## Puzzle questions

1. Why must debug messages go to standard error and not standard output?
2. What should Remus send when it has no legal move?

## Slides

Slides 1.1, 5.6, 7.5, 9.3 in the [slide plan](../course/slide_plan.md).
