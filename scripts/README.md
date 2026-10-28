# Teacher scripts

This folder holds every teacher tool that is not part of a chess engine. Students
never open it. Each script finds the top Remus folder from its own path, so run
each one from the top Remus folder:

```bash
uv run scripts/run_all_tests.py
```

`version_match.py` is not in this folder. Every pair runs it from the Day 9
`period2/engines` folder in the Day 9 battles, so it stays
beside the color versions.

## Build the folders

After any change to the instructor code, run the three builders in this order:

```bash
uv run scripts/make_period_folders.py
uv run scripts/make_version_folders.py
uv run scripts/make_student_folders.py
```

| Script | What it does |
| --- | --- |
| `make_period_folders.py` | Builds `period1` to `period3` of every instructor Day folder from `period4`, and on Day 9 writes periods 2 to 4 with no engine code, keeping `period2/engines`. Its `ARRIVALS` table says in which period each file arrives, and its `CHANGES` table says what the earlier periods leave out. It also writes every period README and plants the three bugs in Day 6, period 3 `bug_hunt/`. |
| `make_version_folders.py` | Builds the ten color versions in the Day 9 `period2/engines` folder from the Day 9 `period1` code (Remus-WHITE) and the hand-written `Remus-GOLD` beside them, and writes every version README. |
| `make_student_folders.py` | Builds `student/` from `instructor/`, with each period's student functions as stubs. It also writes the Day overview READMEs and `docs/course/student_edit_plan.md`, and prints the most lines a pair types in one period. |
| `period_guides.py` | Holds the text the builders write into the READMEs: learning objectives, how each is measured, a paragraph for every change, the version guides, and the Day overviews. Edit README text here, not in the READMEs. |
| `make_phase_hunt_figures.py` | Draws the pictures in `docs/images/phase_hunt/` for the Day 10 phase hunt README. It installs matplotlib for itself alone. |

## Test

| Script | What it does |
| --- | --- |
| `run_all_tests.py` | Runs pytest on every instructor period folder and every version folder, one folder at a time, then `test_reference_tools.py`. The full run takes about 6 minutes. |
| `test_reference_tools.py` | Checks that python-chess is installed and counts 20 moves and 400 positions from the start. `uv run pytest` from the top folder runs it. |

## Play and rate the Remus versions

Every game these scripts play goes into `games/remus_games.pgn`. The teacher's league
ran on Rust copies of the 12 versions; only Niram-GOLD is kept, so `--niram` rates
those saved games and plays none.

| Script | What it does |
| --- | --- |
| `version_league.py` | Plays a round robin of all 12 versions on a 10-minute clock and fits one Elo rating each, with Remus-WHITE pinned at 0. `--rate-only` prints the ratings from saved games. |
| `version_elo.py` | Rates all 12 versions against Stockfish at five strengths and writes the table to `docs/engines/remus_elo.md`. `--report-only` writes the table from saved games. |

## Compare Remus with Niram

| Script | What it does |
| --- | --- |
| `engine_parity.py` | Checks that Niram-GOLD matches Remus-GOLD on 49 positions: evaluation, legal moves, book moves, and every search depth's score, node count, and best line. It writes `docs/engines/engine_parity.md` and exits with code 1 if anything differs. |
| `remus_benchmark.py` | Times one Remus version, such as `GOLD`, on the ten positions of `compare_search.py`, so the speed of Remus-GOLD can be compared with the Niram-GOLD benchmark. |
