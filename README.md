# Remus

Remus is a chess engine written in plain Python, built one lesson at a time for
the "Turning a Chess Engine into Science AI" workshop. The name echoes Rimush,
the son and heir of Sargon of Akkad, in tribute to Sargon (1978), the
microcomputer chess program whose complete source was published so that people
could learn from it.

The code grows one class period at a time: each `instructor/Day NN - ...` folder holds
`period1` to `period4`, and each period folder is a complete, runnable copy of Remus at
the end of that period. The `instructor/` folder holds
only finished, working reference code. `student/` mirrors it, with the functions
students write left as stubs for them to fill in. Start with
[`docs/remus_program_overview.md`](docs/remus_program_overview.md); the course plan is
in [`docs/remus_course_plan.md`](docs/remus_course_plan.md).

## Setup

Remus uses [uv](https://docs.astral.sh/uv/) and Python 3.14.

```bash
uv sync
uv run run_all_tests.py
uv run "instructor/Day 06 - Count positions and read FEN/period4/perft.py"
```

The engine uses only the Python standard library. The development group adds
`python-chess`, which the tests use as an outside reference for move counts,
along with `pytest` and `ruff`. En Croissant, the desktop chess GUI, is installed
separately and talks to Remus over UCI.

## License

BSD 3-Clause. See [`LICENSE`](LICENSE).
