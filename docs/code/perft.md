# perft.py: Count positions to prove the rules

*First appears in `instructor/Day 06 - Count positions and read FEN/period2`.*

## The big picture

How do we know the rules are right? We count.

From the start, White has 20 moves. After Black replies, there are 400 positions.
Experts have published these counts. If Remus gets the same numbers, its rules work.

## Where this piece fits

perft.py uses legal_moves.py and make_move.py. Nothing else in the engine depends on it. It is a test tool.

- **Uses:** [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md)
- **Uses only in its self-check:** [`game_state.py`](game_state.md)
- **Used by:** no other Remus file

## Words to know

- **perft:** short for performance test. It counts the positions a fixed number of moves ahead.
- **depth:** how many moves ahead to look. One move by one side is one ply.
- **divide:** split the count by first move, to find which move hides a bug.
- **recursion:** a function that calls itself on a smaller problem.

## What it stores

Counts from the starting position:

| Depth | Positions |
| --- | --- |
| 1 | 20 |
| 2 | 400 |
| 3 | 8,902 |
| 4 | 197,281 |

## How it works

1. At depth 0, count 1: this position.
2. Otherwise, for every legal move: make it, count one level deeper, then undo it.
3. Add up the counts.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
divide()
    legal_moves()  [legal_moves.py]
    make_move()  [make_move.py]
    perft()
        legal_moves()  [legal_moves.py]
        make_move()  [make_move.py]
        perft()  (calls itself again, one move deeper)
        undo_move()  [make_move.py]
    undo_move()  [make_move.py]
    move_to_uci()  [moves.py]
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `perft` | Counts the positions reached after a fixed number of moves. | Day 6, period 2 |
| `divide` | Gives the count under each first move separately. | Day 6, period 2 |

## Try it

Open `perft.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: `perft(1) = 20`, `perft(2) = 400`, `perft(3) = 8,902`, and how long each took.

## Puzzle questions

1. If perft(2) came out as 401, what kind of bug could that be?
2. Why does perft also test `undo_move()`?

## Slides

Slides 6.1, 6.2, 6.3 in the [slide plan](../course/slide_plan.md).
