# Course designer scripts

This folder holds every course designer tool that is not part of a chess engine.
Students and teachers never need it in class: everything they run during the
workshop runs with the Run button in VS Code. Each script finds the top Remus folder from its own path, so run
each one from the top Remus folder:

```bash
uv run misc/scripts/run_all_tests.py
```

`version_match.py` is not in this folder. Every student pair runs it from the Day 9
`period2/student/engines` folder in the Day 9 battles, so it stays
beside the color versions.

## Build the folders

After any change to the instructor code, run the three builders in this order:

```bash
uv run misc/scripts/make_period_folders.py
uv run misc/scripts/make_version_folders.py
uv run misc/scripts/make_student_folders.py
```

| Script | What it does |
| --- | --- |
| `make_period_folders.py` | Builds the `instructor/` folders of `period1` to `period3` of every Day from `period4`, and on Day 9 writes periods 2 to 4 with no engine code, keeping `period2/instructor/engines`. Its `ARRIVALS` table says in which period each file arrives, and its `CHANGES` table says what the earlier periods leave out. It also writes the first part of every period goals file (`Day NN Period NN Goals.md`) and plants the three bugs in Day 6, period 3 `bug_hunt/`. |
| `make_version_folders.py` | Builds the ten color versions in the Day 9 `period2/instructor/engines` folder from the Day 9 `period1` code (Remus-WHITE) and the hand-written `Remus-GOLD` beside them, and writes every version README. |
| `make_student_folders.py` | Builds each period's `student/` folder from its `instructor/` folder, with each period's student functions as stubs. It also writes the syllabus at the top of each Day folder (`Day NN Syllabus.md`) and `misc/docs/course/student_edit_plan.md`, and prints the most lines a student pair types in one period. |
| `period_guides.py` | Holds the text the builders write into the READMEs: learning objectives, how each is measured, a paragraph for every change, the version guides, and the Day overviews. Edit README text here, not in the READMEs. |
| `make_phase_hunt_figures.py` | Draws the pictures in `misc/docs/images/phase_hunt/` for the Day 10 phase hunt README. It installs matplotlib for itself alone. |

## Test

| Script | What it does |
| --- | --- |
| `run_all_tests.py` | Runs pytest on every instructor period folder and every version folder, one folder at a time, then `test_reference_tools.py`. The full run takes about 6 minutes. |
| `test_reference_tools.py` | Checks that python-chess is installed and counts 20 moves and 400 positions from the start. `uv run pytest` from the top folder runs it. |

## Play and rate the Remus versions

Every game these scripts play goes into `misc/games/remus_games.pgn`. The designer's league
ran on Rust copies of the 12 versions; only Niram-GOLD is kept, so `--niram` rates
those saved games and plays none.

| Script | What it does |
| --- | --- |
| `version_league.py` | Plays a round robin of all 12 versions on a 10-minute clock and fits one Elo rating each, with Remus-WHITE pinned at 0. `--rate-only` prints the ratings from saved games. |
| `version_elo.py` | Rates all 12 versions, and Niram-GOLD with `--niram-gold`, against Stockfish at four strengths near an even score, and prints the tables for `misc/docs/engines/engines_elo.md`. `--report-only` prints the tables from saved games. |

## Compare Remus with Niram

| Script | What it does |
| --- | --- |
| `engine_parity.py` | Checks that Niram-GOLD matches Remus-GOLD on 49 positions: evaluation, legal moves, book moves, and every search depth's score, node count, and best line. It writes `misc/docs/engines/remus-niram parity.md` and exits with code 1 if anything differs. |
| `remus_benchmark.py` | Times one Remus version, such as `GOLD`, on the ten positions of `compare_search.py`, so the speed of Remus-GOLD can be compared with the Niram-GOLD benchmark. |
