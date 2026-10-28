# Remus

Remus is a chess engine written in plain Python, built one lesson at a time for
the "Turning a Chess Engine into Science AI" workshop. The name echoes Rimush,
the son and heir of Sargon of Akkad, in tribute to Sargon (1978), the
microcomputer chess program whose complete source was published so that people
could learn from it.

The code grows one class period at a time: each `instructor/Day NN - ...` folder holds
`period1` to `period4`, and each period folder is a complete, runnable copy of Remus at
the end of that period. Each Day folder's own `README.md` gives the day's objectives
and the timed activities of its four periods. The `instructor/` folder holds
only finished, working reference code. `student/` mirrors it, with the functions
students write left as stubs for them to fill in. `scripts/` holds the teacher's
tools outside the engine: the builders that write the period, version, and student
folders, the test runner, and the league and rating scripts. Start with
[`docs/code/remus_program_overview.md`](docs/code/remus_program_overview.md); the course plan is
in [`docs/course/remus_course_plan.md`](docs/course/remus_course_plan.md).

## Setup

Remus uses [uv](https://docs.astral.sh/uv/) and Python 3.14.

```bash
uv sync
uv run scripts/run_all_tests.py
uv run "instructor/Day 06 - Count positions and read FEN/period4/perft.py"
```

The engine uses only the Python standard library. The development group adds
`python-chess`, which the tests use as an outside reference for move counts,
along with `pytest` and `ruff`. Lucas Chess, the desktop chess GUI, is installed
separately and talks to Remus over UCI.

`Niram/` holds Niram, a Rust copy of all 12 Remus versions, from Niram-WHITE to
Niram-GOLD, that searches the same trees about 50 times faster. The match and league
scripts play it with `--niram`. It is a teacher's experiment, outside the course; see
[`Niram/README.md`](Niram/README.md).

## License

BSD 3-Clause. See [`LICENSE`](LICENSE).
