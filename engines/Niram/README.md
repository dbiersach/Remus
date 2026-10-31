# Niram: Remus-GOLD in Rust

Niram is Remus rewritten in Rust. Remus echoes Rimush, the son of Sargon of Akkad;
Niram shortens Naram-Sin, Sargon's grandson, the next heir in the family line.

Niram keeps the exact rules, evaluation, and search of Remus-GOLD, in the
folder beside this one: the same board of 64 characters, the same move order, and
the same evaluation terms and search function. Given the same position and depth,
both engines visit the same number of positions and choose the same move with the
same score. Only the language changes, so Niram searches about 15 times faster.

Niram is the course designer's experiment, not part of the course. Students write Remus in
Python, and the student folders leave Niram out.

## Files

`src/` holds every Rust file. Each one matches the Remus-GOLD Python file of the
same name, with the same function names. `main.rs` starts the program `niram`,
which asks the opening book first, then searches:

| Rust file | Remus file | What it does |
| --- | --- | --- |
| `board.rs` | `board.py` | The 8x8 board and square names |
| `moves.rs` | `moves.py` | The `Move` record and UCI text |
| `game_state.rs` | `game_state.py` | The game state and `position_key` |
| `make_move.rs` | `make_move.py` | `make_move` and `undo_move` |
| `move_generation.rs` | `move_generation.py` | Pseudo-legal moves |
| `attacks.rs` | `attacks.py` | Attacked squares and check |
| `legal_moves.rs` | `legal_moves.py` | Castling and the legal-move filter |
| `evaluation.rs` | `evaluation.py` | Material, placement, pawns, mating, king safety, and `evaluate` |
| `move_ordering.rs` | `move_ordering.py` | MVV-LVA and killer moves |
| `transposition_table.rs` | `transposition_table.py` | The table of searched positions |
| `search.rs` | `search.py` | `upgraded_search`, `quiescence`, and `think` |
| `search_tools.rs` | `search.py` | The pieces every search shares: the node count, the clock, null moves, reductions |
| `fen.rs`, `notation.rs` | `fen.py`, `notation.py` | FEN and SAN |
| `opening_book.rs` | `opening_book.py` | Book moves from `opening_book.txt`, defend-only trap lines included |
| `uci_engine.rs` | `uci_engine.py` | The UCI conversation with Lucas Chess |
| `bench.rs` | `perft.py` and this benchmark | `bench`, `perft`, `parity`, `book`, and the command line |

`opening_book.txt` is a copy of the book in `Remus-GOLD`. The teaching steps that
`think` never calls (random, greedy, minimax, negamax, plain alpha-beta, and the
scanning attack test) stay in Python only.

The designer's league ran on Rust copies of all 12 Remus versions, from Niram-WHITE
to Niram. Only Niram is kept. The league's games stay in
`misc/games/remus_games.pgn`, and `uv run misc/designer/version_league.py --niram --rate-only
--event "Niram league 1"` rates them, with Niram-WHITE pinned at 0.

## Install Rust on Windows

Niram needs the Rust compiler (`rustc`) and Cargo, Rust's build tool. Both come
from rustup, the official Rust installer. Niram uses the 2024 edition of Rust, so
it needs Rust 1.85 or newer; rustup installs the latest version.

1. **Install the C++ build tools.** On Windows, Rust uses Microsoft's linker,
   which comes with the Visual Studio Build Tools. If Visual Studio with the
   "Desktop development with C++" workload is already installed, skip this step.
   Otherwise the rustup installer in step 2 offers to install the build tools for
   you: answer `1` ("Quick install via the Visual Studio Community installer") and
   accept the defaults. To install them yourself, download the Build Tools from
   [visualstudio.microsoft.com/downloads](https://visualstudio.microsoft.com/downloads/)
   and tick "Desktop development with C++" (it includes the MSVC compiler and the
   Windows SDK).
2. **Install rustup.** Download `rustup-init.exe` (64-bit) from
   [rustup.rs](https://rustup.rs) and run it. At its menu, press Enter to take
   the default installation (`1) Proceed with standard installation`). It puts
   `rustc`, `cargo`, and `rustup` in `%USERPROFILE%\.cargo\bin` and adds that
   folder to the PATH. In PowerShell, `winget install Rustlang.Rustup` installs
   the same thing.
3. **Check the install.** Close every terminal, including the one inside VS Code,
   so the new PATH takes effect. Then open a new PowerShell and run:

   ```powershell
   rustc --version    # rustc 1.85.0 or newer
   cargo --version    # cargo 1.85.0 or newer
   ```

   If Windows reports that `cargo` is not recognized, the terminal started before
   the install: open a new one, or sign out and back in.
4. **Build Niram.** In PowerShell, from the repository folder:

   ```powershell
   cd engines\Niram
   cargo build --release
   cargo test --release
   ```

   The first build downloads nothing (Niram uses only Rust's standard library)
   and takes under a minute. A linker error such as `link.exe not found` means
   the C++ build tools from step 1 are missing.

`rustup update` installs each new Rust release. The VS Code extension
`rust-lang.rust-analyzer` adds Rust highlighting and error checking, but Niram
builds without it.

## Run it

From inside this folder:

```bash
cargo build --release                        # The program, in target/release
cargo test --release                         # perft, the book, and the node count
cargo run --release -- bench            # Time Niram on ten positions, depth 4
cargo run --release -- bench 6
cargo run --release -- perft 5          # 4,865,609 from the start position
```

The matching Python benchmark runs from the repository folder:

```bash
uv run misc/designer/remus_benchmark.py GOLD      # Remus-GOLD, depth 4
```

`misc/designer/engine_parity.py` checks that Niram thinks exactly like Remus-GOLD,
on 49 positions that cover openings and book trap lines, tactics, checks,
castling, en passant, promotion, endgames, repetition, the fifty-move rule, and
mate puzzles. For each position it compares the evaluation, the legal moves in
generation and search order, the book moves, and a search with no clock: every
depth's score, node count, and principal variation, and the best move. The
program's `parity` command picks the deepest search that stays within a node
budget, and Remus repeats that search on every CPU core. `book` prints Niram's
whole opening book for the same comparison. The latest results are in
[misc/designer/remus-niram same algorithms.md](../../misc/designer/remus-niram%20same%20algorithms.md).

```bash
uv run misc/designer/engine_parity.py                  # 25,000 nodes a search
uv run misc/designer/engine_parity.py --nodes 100000   # Deeper searches (Remus takes longer)
```

To play Niram in Lucas Chess, run `cargo build --release` and add
`target/release/niram.exe` as a UCI engine, the same way the
[Lucas Chess guide](../../misc/students/lucas_chess_guide.md) adds Remus. It needs no
batch file.
