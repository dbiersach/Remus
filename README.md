# Remus

Remus is a chess engine written in plain Python, built one lesson at a time for
the "Turning a Chess Engine into Science AI" workshop.

Its name reaches back more than four thousand years. Sargon of Akkad (about 2335 to
2279 BC) founded the Akkadian Empire in Mesopotamia, the first known great empire. In
1978 his name went to Sargon, a chess program by Dan and Kathe Spracklen. Written in
Z80 assembly for the Wavemate Jupiter II, Sargon won the first microcomputer chess
tournament, at the West Coast Computer Faire in 1978, with a perfect 5-0. The
Spracklens then published its complete source as a book, *Sargon: A Computer Chess
Program* (Hayden, 1978), so anyone could read a real engine and learn from it. Sargon
II, 2.5, and III followed, and Sargon III ran on the first Macintosh.

Sargon of Akkad's first son and heir was Rimush (about 2279 to 2270 BC), who held the
empire together through widespread revolts. Remus echoes Rimush: a "son of Sargon," an
heir to the small, readable chess programs whose insides lie open for learners,
rebuilt in modern Python.

The code grows one class period at a time. The top folder holds one folder per day,
`Day 01 - ...` to `Day 10 - ...`, and each Day folder holds `period1` to `period4`.
Inside every period folder, `instructor/` is a complete, runnable copy of Remus at the
end of that period, and `student/` is the same code with the functions the pairs write
left as stubs for them to fill in. Beside them sits the period's goals file, such as
`Day 04 Period 03 Goals.md`: the objectives, the timed steps, and the exact tasks.
Each Day folder's syllabus, such as `Day 04 Syllabus.md`, gives the day's
objectives and the timed activities of its four periods. Everything else sits in
`misc/`: the course and code documents in `misc/docs/`, the games every script plays in
`misc/games/`, and the course designer's tools in `misc/scripts/`, which hold the builders
that write the period, version, and student folders, the test runner, and the league
and rating scripts, each listed in
[`misc/scripts/README.md`](misc/scripts/README.md). Start with
[`misc/docs/code/remus_program_overview.md`](misc/docs/code/remus_program_overview.md); the course plan is
in [`misc/docs/course/remus_course_plan.md`](misc/docs/course/remus_course_plan.md).

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
   [Lucas Chess guide](misc/docs/course/lucas_chess_guide.md) shows, with screenshots, how
   to add Remus through its `remus.bat` and watch it play.

From here on, every file runs inside VS Code. Open a file, such as `perft.py` in
`Day 06 - Count positions and read FEN/period4/instructor`, and click the Run Python
File button (the triangle at the top right of the editor). Each file prints its own
check, with the expected answer beside it. The course designer's tools in `misc/scripts/`, such as
the test runner and the league, are listed with their commands in
[`misc/scripts/README.md`](misc/scripts/README.md).

The engine uses only the Python standard library. The development group adds
`python-chess`, which the tests use as an outside reference for move counts,
along with `pytest` and `ruff`. Lucas Chess talks to Remus over UCI.

Niram-GOLD, beside Remus-GOLD in the Day 9 `period2/instructor/engines` folder, is Remus-GOLD
rewritten in Rust. It searches the same trees about 50 times faster. It is a
course designer's experiment, outside the course; see
[its README](<Day 09 - Add the clock and build enhanced engines/period2/instructor/engines/Niram-GOLD/README.md>).

## License

BSD 3-Clause. See [`LICENSE`](LICENSE).
