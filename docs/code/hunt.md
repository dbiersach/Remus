# hunt.py: Find three planted bugs

*Day 6, period 3. The demo file is `bug_hunt/hunt.py` in the period folder. `make_period_folders.py` keeps it when it rebuilds the folder and plants three bugs in that folder's Remus files.*

## The big picture

Perft counts tell you that something is wrong; `divide()` tells you where. This
demo runs `divide()` on four standard positions with a copy of Remus that has three
planted bugs, compares each root move's count with python-chess, and prints the root
moves that disagree. The pair reads those moves, finds each bug, and fixes it.

## Where this piece fits

`hunt.py` and the buggy copy live in `bug_hunt/`, a folder inside the Day 6, period 3
folder, so the correct Remus beside it stays untouched. python-chess is the reference,
the same way it is in `test_perft.py`.

- **Uses:** [`perft.py`](perft.md) and the buggy copies of the Remus files in `bug_hunt/`
- **Used by:** nothing; the instructor's `bug_hunt/README.md` lists the answers

## Words to know

- **divide:** a perft count split by root move, so a wrong total shrinks to one wrong move.
- **reference:** a second program whose answers are trusted, here python-chess.
- **planted bug:** a mistake put in the code on purpose, to practice finding one.

## How it works

1. Run `hunt.py` in `bug_hunt/` in VS Code and read the root moves it prints.
2. For each move, ask which rule that move or the replies to it need: castling, en passant, or promotion.
3. Find the line in `bug_hunt/` that breaks the rule, fix it, and run the hunt again.

The pair fixes 3 lines.

## Try it

Open `hunt.py` in `student/Day 06 - Count positions and read FEN/period3/bug_hunt` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 13 root moves that disagree before any fix, and 0 once all three bugs are fixed.

## Puzzle questions

1. Why does a castling bug show up under knight moves such as e5f7?
2. Why does a missing promotion piece show up as a missing root move, while the other two bugs change the counts under a move?
