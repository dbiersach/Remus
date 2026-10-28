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
folders, the test runner, and the league and rating scripts, each listed in
[`scripts/README.md`](scripts/README.md). Start with
[`docs/code/remus_program_overview.md`](docs/code/remus_program_overview.md); the course plan is
in [`docs/course/remus_course_plan.md`](docs/course/remus_course_plan.md).

## Setup

Remus runs on Windows 11 with [Git](https://git-scm.com/),
[uv](https://docs.astral.sh/uv/), [VS Code](https://code.visualstudio.com/), and Lucas
Chess. The class laptops come with all four installed and Remus already cloned. The steps
below set up a new computer, such as the teacher's laptop or a computer at home.

1. Open **PowerShell** from the Start menu and install Git and VS Code with winget:

   ```powershell
   winget install --id Git.Git -e
   winget install --id Microsoft.VisualStudioCode -e
   ```

2. Install uv, which manages Python and the project's packages:

   ```powershell
   winget install --id astral-sh.uv -e
   ```

   Close PowerShell and open a new window, so that it finds `git`, `uv`, and `code`.

3. Clone the repository and change into its folder:

   ```powershell
   git clone https://github.com/dbiersach/Remus.git
   cd Remus
   ```

   A pair in class has no GitHub account and fetches from the teacher's laptop
   instead, or copies the repository from a USB stick.

4. Install Python 3.14 and the development tools (`python-chess`, `pytest`, and
   `ruff`) into the project:

   ```powershell
   uv sync
   ```

   uv reads `.python-version` and downloads Python 3.14 by itself, so no separate
   Python install is needed.

5. Install the VS Code extensions the class uses, then open the Remus workspace:

   ```powershell
   .\install_vscode_extensions.ps1
   code Remus.code-workspace
   ```

   The Python extension (`ms-python.python`) is the one that matters most: it adds
   the Run Python File button. The workspace file sets the font sizes, formats code
   with ruff on save, and points VS Code at the project's `.venv`. If PowerShell
   refuses to run the script, run
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

6. Install Lucas Chess, the chess board that plays against Remus. Download the
   Windows installer from
   [lucaschess.pythonanywhere.com/downloads](https://lucaschess.pythonanywhere.com/downloads)
   and run it. Lucas Chess comes with Stockfish, so no other engine is needed. The
   [Lucas Chess guide](docs/course/lucas_chess_guide.md) shows, with screenshots, how
   to add Remus through its `remus.bat` and watch it play.

From here on, every file runs inside VS Code. Open a file, such as `perft.py` in
`instructor/Day 06 - Count positions and read FEN/period4`, and click the Run Python
File button (the triangle at the top right of the editor). Each file prints its own
check, with the expected answer beside it. The teacher's tools in `scripts/`, such as
the test runner and the league, are listed with their commands in
[`scripts/README.md`](scripts/README.md).

The engine uses only the Python standard library. The development group adds
`python-chess`, which the tests use as an outside reference for move counts,
along with `pytest` and `ruff`. Lucas Chess talks to Remus over UCI.

`Niram/` holds Niram, a Rust copy of all 12 Remus versions, from Niram-WHITE to
Niram-GOLD, that searches the same trees about 50 times faster. The match and league
scripts play it with `--niram`. It is a teacher's experiment, outside the course; see
[`Niram/README.md`](Niram/README.md).

## License

BSD 3-Clause. See [`LICENSE`](LICENSE).
