# The class demos

Some periods hold a demo instead of a Remus function: a short program the class runs
together to see an idea, such as why a pawn becomes a knight or how much work
alpha-beta saves. A demo with blanks works like a lab: each `#` line in the
`student` folder's file is one line you type, and the answer is in the `instructor`
folder. The demos live only in their period folders; no engine folder holds them.
This page has one section per demo, in course order.

| Demo | When | Page section |
| --- | --- | --- |
| `show_board.py` | Day 1, period 4, and Day 3, period 2 | [Draw the board as a picture](#show_boardpy-draw-the-board-as-a-picture) |
| `demo_practice_positions.py` | Day 4, period 4 | [Predict, then count](#demo_practice_positionspy-predict-then-count) |
| `demo_promotion.py` | Day 5, period 4 | [Why a pawn becomes a knight](#demo_promotionpy-why-a-pawn-becomes-a-knight) |
| `hunt.py` | Day 6, period 3 | [Find three planted bugs](#huntpy-find-three-planted-bugs) |
| `compare_search.py` | Day 8, period 2 | [Prove that alpha-beta saves work](#compare_searchpy-prove-that-alpha-beta-saves-work) |
| `demo_results.py` | Day 9, period 4 | [Read a battle result](#demo_resultspy-read-a-battle-result) |

## show_board.py: Draw the board as a picture

*First appears in `Day 01 - Draw the board/period4/instructor`.*

### The big picture

Remus keeps its board as letters in a list. That is easy for Python, but hard on the eyes.

This file turns a Remus board into a real picture of a chessboard and opens it in the web browser. From Day 3 on, it also draws an arrow for each move, so you can see the moves your own code finds.

### Where this piece fits

show_board.py is a helper beside the engine. It uses board.py, and from Day 3 on, move_generation.py, game_state.py, and moves.py. No Remus file uses it.

It is the one engine-side file that imports python-chess. python-chess only draws the picture. Remus never asks it about the rules.

- **Uses:** [`board.py`](engine_code/board.md), [`moves.py`](engine_code/moves.md)
- **Uses only in its self-check:** [`game_state.py`](engine_code/game_state.md), [`move_generation.py`](engine_code/move_generation.md)
- **Used by:** no other Remus file

### Words to know

- **SVG:** a picture file made of shapes, which any web browser can show.
- **python-chess:** a chess library for Python. Remus uses it only to draw pictures and to check its own answers in tests.
- **arrow:** a line from the square a piece starts on to the square it lands on.

### What it stores

The picture is saved as `board.svg` in the same folder as the script. Each run saves over the last picture.

python-chess numbers its squares from a1 = 0 to h8 = 63. Remus uses (row, col) with row 0 at rank 8, so the file turns rank `8 - row` into python-chess's rank number `7 - row`.

### How it works

1. `to_python_chess()` copies every piece onto an empty python-chess board.
2. `show_board()` asks python-chess for the picture, saves it, and opens the browser.
3. From Day 3, `show_moves()` turns each Move into an arrow and calls `show_board()`.

### Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
show_moves()
    show_board()
        to_python_chess()
    python_chess_square()
```

### The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `to_python_chess` | Copies a Remus board into a python-chess board. | Day 1, period 4 |
| `show_board` | Saves a picture of the board and opens it in the browser. | Day 1, period 4 |
| `python_chess_square` | Turns a Remus (row, col) square into a python-chess square number. | Day 3, period 2 |
| `show_moves` | Draws the board with one arrow for each move. | Day 3, period 2 |

### How the file grows

- **Day 1, period 4:** `to_python_chess`, `show_board`
- **Day 3, period 2:** `python_chess_square`, `show_moves`

### Try it

Open `show_board.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: A picture of the board in the web browser. On Day 3 and later, four arrows show the knight moves from the start.

### Puzzle questions

1. Why does row 0 become python-chess rank 7?
2. Change main() to draw the moves of a rook on d4 of an empty board. How many arrows do you expect?

### Slides

Slides 1.6, 3.6 in the [slide plan](../teachers/slide_plan.md).

## demo_practice_positions.py: Predict, then count

*Day 4, period 4. The demo file is `Day 04 - Keep only legal moves/period4/student/demo_practice_positions.py`, and the answers are in `Day 04 - Keep only legal moves/period4/instructor/demo_practice_positions_instructor.py`.*

### The big picture

A rule in the code is right only if it gives the right answer on positions where
you already know the answer. This demo builds three small positions, and for each
the student pair writes a prediction before Remus counts the legal moves.

### Where this piece fits

The demo runs in the Day 4, period 4 folder and uses the legal-move filter that the
student pairs finished in period 3. Its positions are the same as the practice-position tests
in `test_legal_moves.py`.

- **Uses:** [`board.py`](engine_code/board.md), [`game_state.py`](engine_code/game_state.md), [`attacks.py`](engine_code/attacks.md), [`legal_moves.py`](engine_code/legal_moves.md), [`moves.py`](engine_code/moves.md)
- **Used by:** nothing; the tests in `test_legal_moves.py` check the same positions

### Words to know

- **check:** the king is attacked. Every legal move must end the check.
- **pin:** a piece that cannot move because moving it would expose its own king.
- **prediction:** the count the student pair expects, written down before running the code.

### How it works

1. `position()` builds a state from a dict such as `{"e1": "K", "e8": "r"}`.
2. Part #1: predict the moves from the start position, then compare with Remus.
3. Part #2: a rook on e8 checks the king on e1. Predict how many squares the king can escape to.
4. Part #3: add a White knight on e2 and count only the moves that start on e2.
5. Part #4: change the pieces and predict again.

![A Black rook on e8 checks the White king on e1](images/boards/pin_check.svg) ![A White knight on e2 blocks the check and is pinned](images/boards/pin_knight.svg)

*Left, Part #2: the rook on e8 checks the king on e1 down the e-file. Right, Part #3:
the knight on e2 blocks the check, so it is pinned.*

The student pair types 14 lines.

### Try it

Open `demo_practice_positions.py` in `Day 04 - Keep only legal moves/period4/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: each board with "You predicted ..., Remus finds ...": 20, 4, and 4 legal moves, and 0 legal knight moves.

### Puzzle questions

1. Why does the king in Part #2 have 4 moves and not 5?
2. Would a pinned rook on e2 have any legal moves? Try it in Part #4.

## demo_promotion.py: Why a pawn becomes a knight

*Day 5, period 4. The demo file is `Day 05 - Add castling, en passant, and promotion/period4/student/demo_promotion.py`, and the answers are in `Day 05 - Add castling, en passant, and promotion/period4/instructor/demo_promotion_instructor.py`.*

### The big picture

A pawn that reaches the last rank may become a queen, a rook, a bishop, or a
knight. Nearly always the queen is best, but not here: White's pawn on b7 promotes on
b8, and a queen, a rook, or a bishop leaves Black's king with no move and no check.
That is stalemate, a draw. Only the knight gives check, and it is checkmate.

![White king c6, bishop b6, and pawn b7 against the Black king on a6](images/boards/promotion_puzzle.svg)

*The puzzle position, White to move. The green arrow is the promotion on b8.*

### Where this piece fits

The demo runs in the Day 5, period 4 folder and uses the promotion code the teacher
adds to `make_move.py` in this period, together with `legal_moves()` and `in_check()`.

- **Uses:** [`board.py`](engine_code/board.md), [`game_state.py`](engine_code/game_state.md), [`attacks.py`](engine_code/attacks.md), [`legal_moves.py`](engine_code/legal_moves.md), [`make_move.py`](engine_code/make_move.md), [`moves.py`](engine_code/moves.md)
- **Used by:** nothing; `test_special_moves.py` tests the four promotions

### Words to know

- **promotion:** a pawn on the last rank becomes another piece.
- **underpromotion:** promoting to a rook, a bishop, or a knight instead of a queen.
- **stalemate:** the side to move has no legal move and is not in check: the game is a draw.
- **checkmate:** the side to move has no legal move and is in check: the game is lost.

### How it works

1. `puzzle_state()` sets up White's king c6, bishop b6, and pawn b7 against Black's king a6.
2. Part #1: for each of Q, R, B, and N, make the promotion, count Black's replies, name the result, and undo the move.
3. Part #2: compare the state with a snapshot taken before Part #1.

The student pair types 12 lines.

### Try it

Open `demo_promotion.py` in `Day 05 - Add castling, en passant, and promotion/period4/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: the puzzle board, stalemate for Q, R, and B, checkmate for N, and True for the snapshot.

### Puzzle questions

1. Which squares around a6 does the queen on b8 cover? Which square is left, and why can the king not go there?
2. Why does the knight give check from b8 when the queen does not?

## hunt.py: Find three planted bugs

*Day 6, period 3. The demo file is `bug_hunt/hunt.py` in the period folder. `make_period_folders.py` keeps it when it rebuilds the folder and plants three bugs in that folder's Remus files.*

### The big picture

Perft counts tell you that something is wrong; `divide()` tells you where. This
demo runs `divide()` on four standard positions with a copy of Remus that has three
planted bugs, compares each root move's count with python-chess, and prints the root
moves that disagree. The student pair reads those moves, finds each bug, and fixes it.

### Where this piece fits

`hunt.py` and the buggy copy live in `bug_hunt/`, a folder inside the Day 6, period 3
folder, so the correct Remus beside it stays untouched. python-chess is the reference,
the same way it is in `test_perft.py`.

- **Uses:** [`perft.py`](engine_code/perft.md) and the buggy copies of the Remus files in `bug_hunt/`
- **Used by:** nothing; the instructor's `bug_hunt/README.md` lists the answers

### Words to know

- **divide:** a perft count split by root move, so a wrong total shrinks to one wrong move.
- **reference:** a second program whose answers are trusted, here python-chess.
- **planted bug:** a mistake put in the code on purpose, to practice finding one.

### How it works

1. Run `hunt.py` in `bug_hunt/` in VS Code and read the root moves it prints.
2. For each move, ask which rule that move or the replies to it need: castling, en passant, or promotion.
3. Find the line in `bug_hunt/` that breaks the rule, fix it, and run the hunt again.

The student pair fixes 3 lines.

### Try it

Open `hunt.py` in `Day 06 - Count positions and read FEN/period3/student/bug_hunt` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 13 root moves that disagree before any fix, and 0 once all three bugs are fixed.

### Puzzle questions

1. Why does a castling bug show up under knight moves such as e5f7?
2. Why does a missing promotion piece show up as a missing root move, while the other two bugs change the counts under a move?

## compare_search.py: Prove that alpha-beta saves work

*First appears in `Day 08 - Search ahead with alpha-beta/period2/instructor`.*

### The big picture

Alpha-beta should find the same score as negamax with much less work. This file
checks that on ten positions.

### Where this piece fits

compare_search.py uses search.py and fen.py. It is a Day 8 experiment, and it lives
only in the Day 8 period folders: Day 9 and the engine folders leave it out, and no game
of chess ever runs it.

- **Uses:** [`fen.py`](engine_code/fen.md), [`search.py`](engine_code/search.md)
- **Used by:** no other Remus file

### Words to know

- **node:** one position the search visits.

### What it stores

Each line shows both searches at depth 3. Alpha-beta visits less than a fifth of the
positions, with the same score.

### How it works

1. Load each of the ten positions.
2. Search it with `negamax()`, then with `alpha_beta()`.
3. Check that the scores match and print both node counts.

### Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    state_from_fen()  [fen.py]
    negamax()  [search.py]
    alpha_beta()  [search.py]
```

### Try it

Open `compare_search.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: Ten lines like `negamax 24,942 positions, alpha-beta 4,226 positions, same score`.

### Puzzle questions

1. Which position saved the most work? Why might that be?

### Slides

Slides 8.5 in the [slide plan](../teachers/slide_plan.md).

## demo_results.py: Read a battle result

*Day 9, period 4. The demo file is `Day 09 - Add the clock and build enhanced engines/period4/student/demo_results.py`, and the answers are in `Day 09 - Add the clock and build enhanced engines/period4/instructor/demo_results_instructor.py`.*

### The big picture

A match ends with a score, but luck plays a part, and luck plays a larger part the
fewer games there are. This demo turns wins, draws, and losses into an Elo gap and a
margin of error, and says whether the result shows a real difference. A student pair puts in
its two battle games first, then its engine's games from the designer's league,
and sees the margin shrink as the games add up.

### Where this piece fits

The demo runs in the Day 9, period 4 folder, during the second round of battles, and uses only Python's `math` module.
`estimate_elo.py` and `version_league.py` fit ratings with the same Elo formula.

- **Uses:** nothing from Remus
- **Used by:** nothing; each student pair uses it to read its battle and its engine's league result

### Words to know

- **score:** points per game: a win is 1, a draw one half, a loss 0.
- **Elo gap:** the rating difference that the Elo formula expects for a score. A score of 0.55 is a gap of about 35.
- **margin of error:** how far the true value may lie from the measured one, 95 times out of 100.

### How it works

1. Part #1: count the games and points, and turn the score into an Elo gap.
2. Part #2: work out the margin, the lowest and highest gap it allows, and whether the range includes 0.

The student pair types 13 lines.

### Try it

Open `demo_results.py` in `Day 09 - Add the clock and build enhanced engines/period4/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 11.0 points of 20, a gap of +35 between -121 and +208, and "more games are needed".

### Puzzle questions

1. How many games would make the margin half as wide?
2. Put your own engine's result into Part #1. Is your enhancement's gap larger than its margin?
