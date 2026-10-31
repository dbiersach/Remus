# The Python labs

Thirteen periods start with a Python skills lab, a short file named `python_*.py`
that teaches one Python skill with chess data, right before the Remus code that
needs it. The student file in the period's `student` folder has one `#` line for
each line you type, and the answer file, `<name>_instructor.py`, sits in the
`instructor` folder beside it. This page has one section per lab, in course order.
Each section says what the lab is for, the words to know, how it works, and what you
should see when it runs.

| Lab | When | Page section |
| --- | --- | --- |
| `python_setup.py` | Day 1, period 1 | [Is the laptop ready?](#python_setuppy-is-the-laptop-ready) |
| `python_strings.py` | Day 1, period 2 | [Square names are text](#python_stringspy-square-names-are-text) |
| `python_lists.py` | Day 1, period 3 | [A board is a list of rows](#python_listspy-a-board-is-a-list-of-rows) |
| `python_functions.py` | Day 2, period 1 | [Small questions as functions](#python_functionspy-small-questions-as-functions) |
| `python_dicts.py` | Day 2, period 2 | [A dict, a copy, and a dataclass](#python_dictspy-a-dict-a-copy-and-a-dataclass) |
| `python_loops.py` | Day 3, period 1 | [Walk until something stops you](#python_loopspy-walk-until-something-stops-you) |
| `python_modules.py` | Day 4, period 1 | [One file uses another](#python_modulespy-one-file-uses-another) |
| `python_sets.py` | Day 5, period 1 | [Castling rights as letters](#python_setspy-castling-rights-as-letters) |
| `python_recursion.py` | Day 6, period 1 | [A function that calls itself](#python_recursionpy-a-function-that-calls-itself) |
| `python_fen_fields.py` | Day 6, period 4 | [The six fields of FEN](#python_fen_fieldspy-the-six-fields-of-fen) |
| `python_input_output.py` | Day 7, period 2 | [Read commands, answer at once](#python_input_outputpy-read-commands-answer-at-once) |
| `python_sorting.py` | Day 8, period 2 | [Sort, start at minus infinity, time it](#python_sortingpy-sort-start-at-minus-infinity-time-it) |
| `python_caches.py` | Day 9, period 2 | [Remember answers in a dict](#python_cachespy-remember-answers-in-a-dict) |

## python_setup.py: Is the laptop ready?

*Day 1, period 1. The lab file is `Day 01 - Draw the board/period1/student/python_setup.py`, and the answers are in `Day 01 - Draw the board/period1/instructor/python_setup_instructor.py`.*

### The big picture

Before a student pair writes any chess code, the laptop has to run Python. This lab checks
that, and it is the student pair's first program: it prints a greeting with the team name and
picks the king out of White's back rank.

### Where this piece fits

The lab does not import Remus, and no Remus file imports it. The skills it practices,
variables, f-strings, and indexing a string, show up in `board.py` on Day 1, period 4.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`board.py`](engine_code/board.md)

### Words to know

- **variable:** a name for a value, such as `team_name = "Knight Riders"`.
- **string:** text in quotes, such as `"RNBQKBNR"`.
- **f-string:** a string that starts with `f` and puts values inside `{ }` into the text.
- **index:** the position of one character. The first character has index 0.

### How it works

1. Part #1 (written for you) prints the Python version and whether python-chess is installed.
2. Part #2: store the team name, print a greeting, and count its characters with `len()`.
3. Part #3: store White's back rank as one string and print `back_rank[4]`, the king.

The student pair types 6 lines.

### Try it

Open `python_setup.py` in `Day 01 - Draw the board/period1/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: Python 3.14 or later, `python-chess installed: True`, and `K` for the king.

### Puzzle questions

1. Why is the king at index 4 and not index 5?
2. What does `len("Knight Riders")` print, and does the space count?

## python_strings.py: Square names are text

*Day 1, period 2. The lab file is `Day 01 - Draw the board/period2/student/python_strings.py`, and the answers are in `Day 01 - Draw the board/period2/instructor/python_strings_instructor.py`.*

### The big picture

People name squares with text, such as `"e2"`. Remus needs numbers to find a square
on its board. This lab turns the letter of a file into a number, turns a number back
into a letter, and tells White pieces from Black ones by their case.

### Where this piece fits

The lab does not import Remus. On Day 1, period 4, `parse_square()` and
`square_name()` in `board.py` do exactly what Parts #2 and #3 practice, and on Day 2
`is_white()` in `game_state.py` is the one call from Part #4.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`board.py`](engine_code/board.md) and [`game_state.py`](engine_code/game_state.md)

### Words to know

- **ord():** gives the code number of a character. `ord("a")` is 97.
- **chr():** turns a code number back into a character. `chr(98)` is `"b"`.
- **file number:** how far a file is from the a-file, so a is 0 and e is 4.
- **isupper():** True when a letter is uppercase, which in Remus means a White piece.

### How it works

1. Part #1: pick the file letter `"e"` and rank digit `"2"` out of `"e2"` by index.
2. Part #2: `ord("e") - ord("a")` gives file number 4; `int("2")` gives rank number 2.
3. Part #3: `chr(ord("a") + 6)` gives `"g"`, and joining it with 7 gives `"g7"`.
4. Part #4: `upper()` turns `"rnbqkbnr"` into White's pieces, and `isupper()` tells them apart.

The student pair types 13 lines.

### Try it

Open `python_strings.py` in `Day 01 - Draw the board/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: file letter e and rank digit 2, file number 4, the square g7, and `True` for `"N".isupper()`.

### Puzzle questions

1. What is the file number of h4, and of a1?
2. Why does subtracting `ord("a")` make the a-file number 0?

## python_lists.py: A board is a list of rows

*Day 1, period 3. The lab file is `Day 01 - Draw the board/period3/student/python_lists.py`, and the answers are in `Day 01 - Draw the board/period3/instructor/python_lists_instructor.py`.*

### The big picture

Remus keeps the board as a list of 8 rows, and each row is a list of 8 squares. This
lab builds that board by hand: first one row of pieces, then all eight rows, then a
move that changes two squares.

### Where this piece fits

The lab does not import Remus. Part #3 builds the same 8x8 board that `new_board()`
in `board.py` returns on Day 1, period 4, with row 0 as rank 8.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`board.py`](engine_code/board.md)

### Words to know

- **list:** values in order inside `[ ]`, such as the 8 pieces of a back rank.
- **len():** counts the items in a list.
- **for and range():** `for col in range(8)` runs the loop with col = 0, 1, ..., 7.
- **nested list:** a list whose items are lists. `board[row][col]` reads one square.

### How it works

1. Part #1: count the pieces of Black's back rank and read the piece on the d-file.
2. Part #2: print the back rank one piece at a time with a `for` loop.
3. Part #3: make 8 rows of dots, put in the pieces (row 0 is rank 8), and print the board.
4. Part #4: play 1. e4 by changing `board[6][4]` and `board[4][4]`, then count White's pawns on rank 2.

The student pair types 25 lines.

### Try it

Open `python_lists.py` in `Day 01 - Draw the board/period3/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 8 pieces, `q` on the d-file, the starting position with Black at the top, and 7 White pawns left on rank 2.

### Puzzle questions

1. Which `board[row][col]` holds the White king at the start?
2. Why does each row need its own new list of dots instead of one row used eight times?

## python_functions.py: Small questions as functions

*Day 2, period 1. The lab file is `Day 02 - Make and undo moves/period1/student/python_functions.py`, and the answers are in `Day 02 - Make and undo moves/period1/instructor/python_functions_instructor.py`.*

### The big picture

Remus asks the same small questions again and again: is this piece White? Is this
square on the board? A function gives each question a name, so the code asks it in
one call. This lab writes three such functions, checks them with `assert`, and then
lets pytest run the same checks.

### Where this piece fits

The lab does not import Remus. On Day 2, period 3, `is_white()` in `game_state.py`
is the same one line as here, and `on_board()` in `move_generation.py` keeps every
move on the 64 squares.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`game_state.py`](engine_code/game_state.md) and [`move_generation.py`](engine_code/move_generation.md)

### Words to know

- **function:** a named block of code. `def` starts it, and `return` hands back the answer.
- **type hint:** `piece: str` and `-> bool` say what goes in and what comes out.
- **docstring:** the text in triple quotes under the `def` line that says what the function does.
- **tuple:** two or more values packed together, such as the square `(4, 4)`.
- **assert:** stops the program with an error when its test is False.
- **pytest:** a tool that finds functions named `test_...` and reports which pass.

### How it works

1. Type the one-line bodies of `is_white()` and `on_board()`; Part #1 calls them.
2. Part #2: write `is_black()` from nothing, with its type hints and docstring.
3. Part #3: unpack the square `(4, 4)` into `row` and `col`.
4. Part #4: call the two test functions, then run them again with pytest and break one on purpose.

The student pair types 16 lines.

### Try it

Open `python_functions.py` in `Day 02 - Make and undo moves/period1/student` in VS Code,
and click the Run Python File button (the triangle at the top right of the editor).
Then open `run_tests.py` in the same folder and click the same button. It runs the
two test functions in `python_functions.py` with pytest.

You should see: True and False answers next to the expected ones, "Every assert passed", and then `2 passed` from pytest.

### Puzzle questions

1. Why does `on_board(8, 3)` return False when 8 is a perfectly good number?
2. What does pytest print when an `assert` fails, and which line does it point at?

## python_dicts.py: A dict, a copy, and a dataclass

*Day 2, period 2. The lab file is `Day 02 - Make and undo moves/period2/student/python_dicts.py`, and the answers are in `Day 02 - Make and undo moves/period2/instructor/python_dicts_instructor.py`.*

### The big picture

A chess game needs more than a board: whose turn it is, which castling moves are still
allowed, and more. A dict keeps each of those facts under a name. This lab also shows
the trap of two names for one board, the copy that avoids it, and a dataclass, a
small record for a move.

### Where this piece fits

The lab does not import Remus. On Day 2, period 3, `new_game()` in `game_state.py`
returns a dict like the one in Part #1, and `Move` in `moves.py` is a dataclass like
the one in Part #4.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`game_state.py`](engine_code/game_state.md) and [`moves.py`](engine_code/moves.md)

### Words to know

- **dict:** values stored under keys, such as `state["turn"]`.
- **aliasing:** two names for the same list: a change through one name shows through the other.
- **deepcopy():** makes a new board with new rows, so changing the copy leaves the original alone.
- **dataclass:** a class that lists its fields once, such as `from_square` and `to_square`.

### How it works

1. Part #1: read the side to move and the castling rights by key, then change the side to move.
2. Part #2: give the board a second name, `b2`, put a pawn on e4 through it, and see it on `board`.
3. Part #3: make a real copy with `deepcopy()`, change a1 on the copy, and compare.
4. Part #4: write the `Move` dataclass, make the move e2 to e4, and print it.

The student pair types 18 lines.

### Try it

Open `python_dicts.py` in `Day 02 - Make and undo moves/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: w, KQkq, then b; a pawn that shows on both names; a copy that changes alone; and `Move(from_square='e2', to_square='e4')`.

### Puzzle questions

1. Why can't `undo_move()` just keep `old_board = board` before a move?
2. Is `b3 == board` the same question as `b3 is board`? What does each one ask?

## python_loops.py: Walk until something stops you

*Day 3, period 1. The lab file is `Day 03 - Generate piece moves/period1/student/python_loops.py`, and the answers are in `Day 03 - Generate piece moves/period1/instructor/python_loops_instructor.py`.*

### The big picture

A rook, a bishop, or a queen slides square by square until it reaches the edge of
the board or another piece. Nobody knows in advance how many steps that takes, so the
code uses a `while` loop and leaves it with `break`. This lab walks from d4 toward g7.

### Where this piece fits

The lab does not import Remus. On Day 3, period 3, `slide()` in `move_generation.py`
is the same walk, and it collects moves instead of square names.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`move_generation.py`](engine_code/move_generation.md)

### Words to know

- **while:** repeats a block as long as its test is True.
- **break:** leaves the loop at once.
- **direction:** a tuple (row step, col step). Up and to the right is (-1, 1), because row 0 is rank 8.

### How it works

1. Part #1: count to 3 with `while`.
2. Part #2: unpack the direction `(-1, 1)` into a row step and a column step.
3. Part #3: step from d4 until the walk leaves the board or lands on a piece, and list each square.
4. Part #4: change the direction and run again.

The student pair types 14 lines.

### Try it

Open `python_loops.py` in `Day 03 - Generate piece moves/period1/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: step 0, 1, 2; the steps -1 and 1; and the squares e5 f6 g7, where the Black pawn on g7 stops the walk.

### Puzzle questions

1. Why does the walk add g7 to the list before it stops?
2. Which direction tuple walks from d4 toward a1?

## python_modules.py: One file uses another

*Day 4, period 1. The lab file is `Day 04 - Keep only legal moves/period1/student/python_modules.py`, and the answers are in `Day 04 - Keep only legal moves/period1/instructor/python_modules_instructor.py`.*

### The big picture

Remus is many files, and each one does one job. A file uses another with `import`
instead of copying its code. This lab imports four Remus files, finds the knight moves
from g1 with their functions, and shows why an imported file prints nothing.

### Where this piece fits

The lab sits in the Day 4, period 1 folder, beside the Remus code from Day 3, so its
imports find `board.py`, `game_state.py`, `move_generation.py`, and `moves.py`. Every
later Remus file starts with imports like these.

- **Uses:** [`board.py`](engine_code/board.md), [`game_state.py`](engine_code/game_state.md), [`move_generation.py`](engine_code/move_generation.md), [`moves.py`](engine_code/moves.md)
- **Used by:** nothing; it is practice for every Remus file

### Words to know

- **module:** a Python file that other files import.
- **import:** runs another file once and hands over its names, such as `new_board`.
- **__name__:** `"__main__"` in the file that VS Code runs, and the file's own name when it is imported.
- **import map:** a drawing of the files in a folder, with an arrow from each file to every file it imports.

### How it works

1. Type the four import lines at the top of the file.
2. Part #1: print `__name__` for this file and for `board.py`.
3. Part #2: build the start board and list the knight moves from g1.
4. Part #3 happens in VS Code: open `board.py` and press Run. This time `board.py` is `__main__`, so its `main()` runs and prints the board.

The student pair types 11 lines.

### Try it

Open `python_modules.py` in `Day 04 - Keep only legal moves/period1/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: `__main__`, then `board`, then the knight moves g1f3 and g1h3, then the line that tells you to run `board.py` on its own.

### Puzzle questions

1. Why would Lucas Chess break if `board.py` printed its board every time another file imported it?
2. Where does Python look for `board.py` when the lab says `import board`?

## python_sets.py: Castling rights as letters

*Day 5, period 1. The lab file is `Day 05 - Add castling, en passant, and promotion/period1/student/python_sets.py`, and the answers are in `Day 05 - Add castling, en passant, and promotion/period1/instructor/python_sets_instructor.py`.*

### The big picture

Remus keeps the castling rights as the string `"KQkq"`: K is White's king side, q
is Black's queen side. When a king or a rook leaves its home square, its letters go
away for the rest of the game. This lab practices the Python tools for that job: sets,
`in`, dict lookups, and `replace()`.

### Where this piece fits

The lab does not import Remus. On Day 5, period 2, `update_castling_rights()` in
`make_move.py` removes letters with `replace()` exactly as Part #4 does.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`make_move.py`](engine_code/make_move.md)

### Words to know

- **set:** a collection that holds each item once, such as the squares pieces have left.
- **in:** asks whether an item is in a set, a dict, or a string, and answers True or False.
- **replace():** gives back a new string with one piece of text swapped for another, such as "K" for "".

### How it works

1. Part #1: add h1, e1, and h1 again to a set, and count the squares.
2. Part #2: ask with `in` which rooks have moved.
3. Part #3: look up the rights a home square guards in a dict.
4. Part #4: remove letters from `"KQkq"` with `replace()`, one at a time.

The student pair types 14 lines.

### Try it

Open `python_sets.py` in `Day 05 - Add castling, en passant, and promotion/period1/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 2 squares, True and False, K, then the rights Qkq and Q.

### Puzzle questions

1. Which letters must go when the White king moves from e1?
2. A Black rook is captured on h8. Which letter must go, and why?

## python_recursion.py: A function that calls itself

*Day 6, period 1. The lab file is `Day 06 - Count positions and read FEN/period1/student/python_recursion.py`, and the answers are in `Day 06 - Count positions and read FEN/period1/instructor/python_recursion_instructor.py`.*

### The big picture

Some problems hold a smaller copy of themselves. To count the positions two moves
ahead, count the positions one move ahead after each first move. A function that
calls itself on the smaller problem is recursive. This lab writes two recursive
functions and reads a third.

### Where this piece fits

The lab does not import Remus. On Day 6, period 2, `perft()` in `perft.py` has the
shape of `knight_paths()` in Part #3: at depth 0 return 1, otherwise add up the count
after every move.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`perft.py`](engine_code/perft.md)

### Words to know

- **recursion:** a function that calls itself on a smaller problem.
- **base case:** the smallest problem, answered without another call, such as 0 in the countdown.
- **leaf:** a position at the bottom of the tree, with no moves under it in the count.

### How it works

1. Part #1: `countdown()` prints a number and calls itself with the number minus 1, until 0.
2. Part #2: `count_leaves()` counts 1 for a move name and adds up the counts of a list's branches.
3. Part #3: read `knight_paths()`, predict its counts from a1, and run it.

The student pair types 11 lines.

### Try it

Open `python_recursion.py` in `Day 06 - Count positions and read FEN/period1/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 3, 2, 1, Go!; 6 leaves and 2 under e4; and 2, 12, and 64 knight paths from a1.

### Puzzle questions

1. What happens to `countdown()` without its base case?
2. Draw the calls of `knight_paths(7, 0, 2)`: how many calls return 1?

## python_fen_fields.py: The six fields of FEN

*Day 6, period 4. The lab file is `Day 06 - Count positions and read FEN/period4/student/python_fen_fields.py`, and the answers are in `Day 06 - Count positions and read FEN/period4/instructor/python_fen_fields_instructor.py`.*

### The big picture

A FEN string writes a whole position in one line of six fields, separated by
spaces. This lab cuts the start FEN apart with `split()`, prints each field with its
name, and shows how `try` and `except` catch the error that `int()` raises on text
that is not a number.

### Where this piece fits

The lab does not import Remus. Later this period `state_from_fen()` in `fen.py`
starts with the same `split()`, and `board_from_placement()` cuts the first field
into rows with `split("/")`.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`fen.py`](engine_code/fen.md)

### Words to know

- **FEN:** Forsyth-Edwards Notation: the placement, the side to move, castling, en passant, and two clocks.
- **split():** cuts a string into a list at every space, or at another character you name.
- **ValueError:** the error `int()` raises when its text is not a number.
- **try and except:** run some code, and run other code instead of crashing if a named error happens.

### How it works

1. Part #1: split the start FEN and count the fields.
2. Part #2: print each field with its name.
3. Part #3: turn text into a number inside `try`, and catch `ValueError`.

The student pair types 8 lines.

### Try it

Open `python_fen_fields.py` in `Day 06 - Count positions and read FEN/period4/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 6 fields, then each field with its name, then "x is not a number".

### Puzzle questions

1. Which field changes after every move, and which only after Black's move?
2. What should a FEN reader do with the halfmove clock `"ten"`?

## python_input_output.py: Read commands, answer at once

*Day 7, period 2. The lab file is `Day 07 - Play full games and score positions/period2/student/python_input_output.py`, and the answers are in `Day 07 - Play full games and score positions/period2/instructor/python_input_output_instructor.py`.*

### The big picture

A chess GUI talks to an engine through text: it writes a command on one line, and
the engine answers on its own line. This lab picks moves the way the first brains do,
then reads commands from the keyboard and answers `isready` with `readyok`, the first
exchange of the UCI protocol.

### Where this piece fits

The lab does not import Remus. In period 3, `random_move()` and `greedy_move()` in
`search.py` use `random.choice()` and the best-value idea of Part #2, and `uci_engine.py`
reads `sys.stdin` and answers with `flush=True` as Part #4 does.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`search.py`](engine_code/search.md) and [`uci_engine.py`](engine_code/uci_engine.md)

### Words to know

- **random.choice():** picks one item of a list at random.
- **best so far:** a variable that holds the best item seen yet. A loop swaps in any item that beats it.
- **stdin and stdout:** the text a program reads and the text it prints.
- **stderr:** a second output for notes, which a GUI does not read.
- **flush=True:** sends the printed line at once, so the GUI is not left waiting.

### How it works

1. Part #1: pick a random move.
2. Part #2: pick the most valuable capture with a loop that keeps the best piece so far.
3. Part #3: print a note to `sys.stderr`.
4. Part #4: read lines from `sys.stdin` until `quit`, answering `isready` and echoing the rest.

The student pair types 16 lines.

### Try it

Open `python_input_output.py` in `Day 07 - Play full games and score positions/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: a random move, q, the note, and then readyok and echo hello for the lines you type.

### Puzzle questions

1. What would Lucas Chess do if the engine never flushed `readyok`?
2. Why do notes go to stderr and not to stdout?

## python_sorting.py: Sort, start at minus infinity, time it

*Day 8, period 2. The lab file is `Day 08 - Search ahead with alpha-beta/period2/student/python_sorting.py`, and the answers are in `Day 08 - Search ahead with alpha-beta/period2/instructor/python_sorting_instructor.py`.*

### The big picture

Three small tools make the search faster and easier to measure. A loop that
inserts each capture behind every bigger one puts the most promising captures first, a best value that starts at minus
infinity is beaten by the first real value, and `time.perf_counter()` measures how
long the work takes.

### Where this piece fits

The lab runs in the Day 8, period 2 folder and times `perft()` from `perft.py`. The
same period, `alpha_beta()` starts alpha at the lowest score, and `compare_search.py`
times negamax against alpha-beta.

- **Uses:** [`perft.py`](engine_code/perft.md), [`game_state.py`](engine_code/game_state.md)
- **Used by:** nothing; it is practice for [`search.py`](engine_code/search.md), [`move_ordering.py`](engine_code/move_ordering.md), and [`compare_search.py`](class_demos.md#compare_searchpy-prove-that-alpha-beta-saves-work)

### Words to know

- **insert():** puts an item into a list at a chosen place, such as `ordered.insert(0, piece)` for the front.
- **float("inf"):** infinity: larger than every number, so `-float("inf")` is smaller than every number.
- **time.perf_counter():** a clock for measuring how long code runs.

### How it works

1. Part #1: sort the victims, most valuable first: each piece steps past every piece worth at least as much, then goes in.
2. Part #2: find the best victim with a best value that starts at minus infinity.
3. Part #3: time `perft(3)` from the start position.

The student pair types 19 lines.

### Try it

Open `python_sorting.py` in `Day 08 - Search ahead with alpha-beta/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: `['q', 'r', 'n', 'p']`, the best victim q worth 9, and 8,902 positions with the run time.

### Puzzle questions

1. Why does Part #2 start below every value instead of at 0?
2. How much longer does `perft(4)` take than `perft(3)`? Guess first.

## python_caches.py: Remember answers in a dict

*Day 9, period 2. The lab file is `Day 09 - Add the clock and build enhanced engines/period2/student/python_caches.py`, and the answers are in `Day 09 - Add the clock and build enhanced engines/period2/instructor/python_caches_instructor.py`.*

### The big picture

A program that computes the same answer twice wastes the second computation. A dict
used as a cache keeps each answer under a key, so the second request takes no time.
This lab caches the number of paths a lone knight can take (a small perft), measures a distance with `math.dist()`, and repeats
random numbers with `random.seed()`.

### Where this piece fits

The lab runs in the Day 9, period 2 folder. Remus-RED's transposition table
caches search results the same way, and Remus-CYAN measures king distances.

- **Uses:** nothing outside the standard library; `knight_perft()` sits in the lab file itself
- **Used by:** nothing; it is practice for the enhanced engines in [`transposition_table.py`](engine_code/transposition_table.md) and [`evaluation.py`](engine_code/evaluation.md)

### Words to know

- **cache:** a dict of answers already computed.
- **tuple key:** a key made of several values, such as `((7, 6), 8)`, the square g1 and a depth of 8.
- **math.dist():** the straight-line distance between two points.

### How it works

1. Part #1: `knight_perft()` counts every path a lone knight can take in 8 moves from g1, and `remembered_perft()` computes that count only when its key is missing from the cache.
2. Part #2: measure the distance from d4 to g7.
3. Part #3: seed the random generator so a roll repeats.

The student pair types 7 lines.

### Try it

Open `python_caches.py` in `Day 09 - Add the clock and build enhanced engines/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 811,156 twice, the second at once; 4.243 squares; and True.

### Puzzle questions

1. What would go wrong if the cache key held the depth but not the square?
2. Seeding the generator makes every run roll the same numbers. Why does a test that uses random moves need that?
