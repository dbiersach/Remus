# Remus for the course designer

This folder holds every course designer tool that is not part of a chess engine, and
the pages only the designer reads. Students and teachers never need it in class:
everything they run during the workshop runs with the Run button in VS Code. The
rules the tools follow are in `AGENTS.md` at the top of Remus.

| Page | What it holds |
| --- | --- |
| [`engines_elo.md`](engines_elo.md) | The designer's league of the 12 Remus versions, the Stockfish bracket run, the code lines of each version, and the `version_league.py` and `version_elo.py` commands that rate them |
| [`remus-niram_same_algorithms.md`](remus-niram_same_algorithms.md) | Written by `engine_parity.py`: whether Niram and Remus-GOLD still pick the same moves at the same depth, and how fast each runs |
| [`science_tree_search_survey.md`](science_tree_search_survey.md) | The survey of published science problems that search a tree like a chess engine, which chose the Day 10 phase hunt |

Four pages elsewhere are written by scripts in this folder, so edit the script, not
the page: `make_student_folders.py` writes `misc/teachers/student_edit_plan.md` and
every `Day_NN_Syllabus.md`; `make_period_folders.py` and `make_student_folders.py`
write every period goals file from `period_guides.py`; `make_version_folders.py`
writes every engine README from `period_guides.py`; `make_white_map.py` writes the
"Remus-WHITE across the course" section of `misc/students/remus_program_overview.md`;
and `engine_parity.py` writes the parity page above. `version_elo.py` prints the
Stockfish tables that `engines_elo.md` reports.

## The scripts

Each script finds the top Remus folder from its own path, so run
each one from the top Remus folder:

```bash
uv run misc/designer/run_all_tests.py
```

`version_match.py` plays the Day 9 battles. Student pairs never open it: the
`basic_test.py` and `play_battle.py` in each engine folder run it with the Run
button and pass `--engines` with the folder that holds their engine folder.

## Build the folders

After any change to the instructor code, run the three builders in this order:

```bash
uv run misc/designer/make_period_folders.py
uv run misc/designer/make_version_folders.py
uv run misc/designer/make_student_folders.py
```

| Script | What it does |
| --- | --- |
| `make_period_folders.py` | Builds the `instructor/` folders of `period1` to `period3` of every Day from `period4`, and on Day 9 writes periods 2 to 4 with no engine code. Its `ARRIVALS` table says in which period each file arrives, and its `CHANGES` table says what the earlier periods leave out. It also writes the first part of every period goals file (`Day_NN_Period_NN_Goals.md`) and plants the three bugs in Day 6, period 3 `bug_hunt/`. |
| `make_version_folders.py` | Copies Remus-WHITE from the Day 9 `period1` code into `engines/instructor/00 Remus-WHITE - No enhancements`, builds the ten enhanced engines beside it, and writes every version README. Remus-GOLD, `11 Remus-GOLD - All enhancements`, is written by hand. |
| `make_student_folders.py` | Builds each period's `student/` folder from its `instructor/` folder, with each period's student functions as stubs. It also writes the syllabus at the top of each Day folder (`Day_NN_Syllabus.md`) and `misc/teachers/student_edit_plan.md`, and prints the most lines a student pair types in one period. |
| `period_guides.py` | Holds the text the builders write into the READMEs: learning objectives, how each is measured, a paragraph for every change, the version guides, and the Day overviews. Edit README text here, not in the READMEs. |
| `make_board_diagrams.py` | Draws the chess board diagrams in `misc/students/images/boards/` that the enhanced engine READMEs, the goals files, and the `misc/students/engine_code/` pages show beside their examples, with python-chess's `chess.svg`. A diagram marked `row_col` also prints Remus's row and column numbers on the edges. Each entry of its `DIAGRAMS` table names a FEN, the arrows, and the colored squares; `board_image()` and `goals_board_image()` in `period_guides.py` link a diagram into the README and goals text. Run it after changing a diagram, then the three builders. |
| `make_white_map.py` | Writes the "Remus-WHITE across the course" section of `misc/students/remus_program_overview.md`: an import diagram of the engine files, the ones `uci_engine.py` loads, which it lays out itself with right-angle arrows into `misc/students/images/code/remus_white_imports.svg` (no Graphviz needed), and a table that marks, for every engine file, the period where it appears and the periods where student pairs edit it. The table comes from the Day folders and their goals files. Run it after the three builders. |
| `make_phase_hunt_figures.py` | Draws the pictures in `misc/students/images/phase_hunt/` for the Day 10 phase hunt README. It installs matplotlib for itself alone. |

## Test

| Script | What it does |
| --- | --- |
| `run_all_tests.py` | Runs pytest on every instructor period folder and every version folder, one folder at a time, then `test_reference_tools.py`. The full run takes about 6 minutes. |
| `test_reference_tools.py` | Checks that python-chess is installed and counts 20 moves and 400 positions from the start. `uv run pytest` from the top folder runs it. |

## Play and rate the Remus versions

Every game these scripts play goes into `misc/games/remus_games.pgn`. The designer's league
ran on Rust copies of the 12 versions; only Niram is kept, so `--niram` rates
those saved games and plays none.

| Script | What it does |
| --- | --- |
| `version_match.py` | Plays one enhanced engine against Remus-WHITE or another engine, 2 games at 10 minutes a side, and prints the Elo gap. `play_battle.py` and `basic_test.py` in each engine folder run it with `--engines`; by hand it plays the engines in `engines/instructor`. |
| `version_league.py` | Plays a round robin of all 12 versions on a 10-minute clock and fits one Elo rating each, with Remus-WHITE pinned at 0. `--rate-only` prints the ratings from saved games. |
| `version_elo.py` | Rates all 12 versions, and Niram with `--niram`, against Stockfish at four strengths near an even score. `--bracket` instead sets each round's Stockfish strength to the engine's rating so far, the run that `misc/designer/engines_elo.md` reports. `--report-only` prints the tables from saved games. |

## Compare Remus with Niram

| Script | What it does |
| --- | --- |
| `engine_parity.py` | Checks that Niram matches Remus-GOLD on 49 positions: evaluation, legal moves, book moves, and every search depth's score, node count, and best line. It writes `misc/designer/remus-niram_same_algorithms.md` and exits with code 1 if anything differs. |
| `remus_benchmark.py` | Times one Remus version, such as `GOLD`, on the ten positions of the Day 8 `compare_search.py`, so the speed of Remus-GOLD can be compared with the Niram benchmark. |
