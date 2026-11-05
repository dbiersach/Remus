# Remus4-Rust

Remus4-Rust is the instructor's Remus4 written in Rust, with a larger table. It has the
same rules, the same evaluation, the same search, and the same opening book. It shows the
class that speed matters in a chess engine, not just the algorithms. No student pair
types it or edits it, and it lives only in
[`engines_instructor/Remus4-Rust`](../../../engines_instructor/Remus4-Rust). It is the
one engine with a real program, `remus4_rust.exe`, so a laptop needs no Rust installed.

## The same engine, faster

Each search below started from the same position, 1. a3, for 5 seconds:

| Engine | Depth reached | Positions searched |
| --- | ---: | ---: |
| Remus4 | 7 | 44,625 |
| Remus4-Rust | 14 | 21,885,237 |

Searched to the same depth, the two engines report the same score, visit the same
number of positions, and pick the same move, until the larger table starts to matter on
long searches. Kiwipete, a busy test position, to depth 7: both visit 292,713 positions,
Remus4 in 18.25 seconds and Remus4-Rust in 0.12 seconds. In the first table each engine
stops at the last depth it finished, so those two counts are not a pure speed ratio.

These times come from one computer, and another laptop gives other times.

## Why Rust runs so much faster

Python reads each line of Remus4 as the program runs, and every number and list in it
is a separate object in memory. Rust compiles to machine instructions ahead of time, and
Remus4-Rust uses three more tricks:

- **Bitboards.** A 64-bit number holds one yes-or-no per square, so a single instruction
  counts the squares a rook reaches.
- **No allocation in the search.** Copying a position is a copy of one small block of
  memory, and move lists live on the stack.
- **A running position key.** `make_move()` updates the key with a few exclusive-or
  steps instead of reading all 64 squares.

None of these changes which positions the search visits, so they change only the time.

## The larger table

At millions of positions per second, Remus4's table of 2 million entries fills within
seconds. Remus4-Rust uses 512 MB for 32 million entries, and a full bucket of four
entries replaces its oldest and shallowest entry instead of starting the whole table
over. On four test positions, 20 seconds of thinking reached one ply deeper than the
same engine with Remus4's table. Kiwipete to depth 13 took 13.9 seconds, against 32.9.

## Its files

Each file in `src/` matches the Remus4 Python file of the same name, and `main.rs` matches
`uci.py`. The code lines leave out blank lines and comments:

| File | Code lines |
| --- | ---: |
| `board.rs` | 204 |
| `attacks.rs` | 140 |
| `make_move.rs` | 75 |
| `move_generation.rs` | 162 |
| `evaluation.rs` | 311 |
| `exchange.rs` | 95 |
| `transposition_table.rs` | 103 |
| `opening_book.rs` | 48 |
| `search.rs` | 363 |
| `main.rs` | 161 |
| **Total** | **1,662** |
