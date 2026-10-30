# The test files: checking that Remus works

## The big picture

A test is a small program that checks one fact about Remus. For example: "from the
start, there are 20 legal moves." If the fact is wrong, the test fails and says where.

Every period folder has its own tests, next to the code they check. A test can only check code that exists, so `period2` of a day has fewer tests than `period4`. When you finish a
function, you run the tests to see whether it works.

## Where this piece fits

Tests use the engine files. No engine file uses the tests. Some tests also use
python-chess as an outside judge, to compare its answers with Remus's.

## Words to know

- **test:** a function whose name starts with `test_`. It checks one fact.
- **assert:** a line that says "this must be true". If it is false, the test fails.
- **pytest:** the program that finds and runs all the tests.
- **expected value:** the answer we write down before we run the code.

## Which test file checks what

Each test file name links to its copy in the `period4/instructor` folder of its Day, the finished code of that day. `test_upgrades.py` links to Remus-GOLD's copy, which checks all ten enhancements.

| Test file | Day | What it checks |
| --- | --- | --- |
| [`test_board.py`](../../../Day%2001%20-%20Draw%20the%20board/period4/instructor/test_board.py) | 1 | The start board and square names |
| [`test_make_move.py`](../../../Day%2002%20-%20Make%20and%20undo%20moves/period4/instructor/test_make_move.py) | 2 | Make and undo put the state back exactly |
| [`test_move_generation.py`](../../../Day%2003%20-%20Generate%20piece%20moves/period4/instructor/test_move_generation.py) | 3 | Moves for each piece, such as 14 for a rook on d4 |
| [`test_legal_moves.py`](../../../Day%2004%20-%20Keep%20only%20legal%20moves/period4/instructor/test_legal_moves.py) | 4 | Check, pins, and the legal-move filter |
| [`test_special_moves.py`](../../../Day%2005%20-%20Add%20castling%2C%20en%20passant%2C%20and%20promotion/period4/instructor/test_special_moves.py) | 5 | Castling, en passant, and promotion |
| [`test_perft.py`](../../../Day%2006%20-%20Count%20positions%20and%20read%20FEN/period4/instructor/test_perft.py) | 6 | Position counts match the published numbers |
| [`test_game.py`](../../../Day%2006%20-%20Count%20positions%20and%20read%20FEN/period4/instructor/test_game.py) | 6 | FEN, and from Day 7 SAN, game endings, and the UCI engine |
| [`test_search.py`](../../../Day%2007%20-%20Play%20full%20games%20and%20score%20positions/period4/instructor/test_search.py) | 7 | Evaluation and the first brains, then minimax, negamax, alpha-beta, and mates |
| [`test_upgrades.py`](../../../engines/instructor/11%20Remus-GOLD%20-%20All%20enhancements/test_upgrades.py) | 9 | The enhancement of each enhanced engine, such as the transposition table of Remus-RED; Remus-GOLD's copy checks all ten |
| [`test_hidden_peak.py`](../../../Day%2010%20-%20Solve%20a%20science%20problem%20using%20chess%20AI/period4/instructor/test_hidden_peak.py) | 10 | The hidden-peak Science AI: the hidden grid, the greedy choice, and the benchmark against random guessing |
| [`test_phase_hunt.py`](../../../Day%2010%20-%20Solve%20a%20science%20problem%20using%20chess%20AI/period4/instructor/test_phase_hunt.py) | 10 | The phase hunt: the score, the greedy agent, the tree search with make and undo, and the benchmark |

## How a test works

1. Set up a small position, often from a FEN line.
2. Run one Remus function on it.
3. `assert` that the answer matches the expected value.

Here is a real test from `test_legal_moves.py`:

```python
def test_twenty_legal_moves_from_the_start() -> None:
    assert len(legal_moves(new_game())) == 20
```

## Try it

Open `run_tests.py` in the folder you are working in and click the Run Python File
button (the triangle at the top right of the editor). It runs every test in the
folder.

A dot means a test passed. An `F` means it failed, with a report below. The teacher
runs the tests of every finished `instructor/` folder with
`misc/scripts/run_all_tests.py`, listed in `misc/scripts/README.md`.

## Puzzle questions

1. Why do we write the expected value before we run the code?
2. A test fails after you change `make_move.py`. Which other test files might fail too?
