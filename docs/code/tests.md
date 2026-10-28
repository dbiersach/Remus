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

| Test file | Day | What it checks |
| --- | --- | --- |
| `test_board.py` | 1 | The start board and square names |
| `test_make_move.py` | 2 | Make and undo put the state back exactly |
| `test_move_generation.py` | 3 | Moves for each piece, such as 14 for a rook on d4 |
| `test_legal_moves.py` | 4 | Check, pins, and the legal-move filter |
| `test_special_moves.py` | 5 | Castling, en passant, and promotion |
| `test_perft.py` | 6 | Position counts match the published numbers |
| `test_game.py` | 6 | FEN, and from Day 7 SAN, game endings, and the UCI engine |
| `test_search.py` | 7 | Evaluation and the first brains, then minimax, negamax, alpha-beta, mates, and the mate solver |
| `test_upgrades.py` | 10 | The Day 10 upgrades and the hidden-peak Science AI |
| `test_phase_hunt.py` | 10 | The phase hunt: the score, the greedy agent, the tree search with make and undo, and the benchmark |

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

From the folder you are working in, run all of its tests:

```bash
uv run pytest
```

Or run one test file:

```bash
uv run pytest test_board.py
```

A dot means a test passed. An `F` means it failed, with a report below. The teacher
runs the tests of every finished folder in `instructor/` with
`scripts/run_all_tests.py`, listed in `scripts/README.md`.

## Puzzle questions

1. Why do we write the expected value before we run the code?
2. A test fails after you change `make_move.py`. Which other test files might fail too?
