# Remus

Remus is a chess engine written in plain Python, built one lesson at a time for
the "From Chess Engines to Science AI" workshop. The name echoes Rimush, the son and heir of
Sargon of Akkad, in tribute to Sargon (1978), the microcomputer chess program
whose complete source was published so that people could learn from it.

The lesson plan is in [`workshop_roadmap.md`](workshop_roadmap.md).

## Setup

Remus uses [uv](https://docs.astral.sh/uv/) and Python 3.14.

```bash
uv sync
uv run pytest
```

The engine uses only the Python standard library. The development group adds
`python-chess`, which the tests use as an outside reference for move counts,
along with `pytest` and `ruff`. PyChess, the optional desktop GUI, is installed
separately and talks to Remus over UCI.

## License

BSD 3-Clause. See [`LICENSE`](LICENSE).
