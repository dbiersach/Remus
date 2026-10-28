#!/usr/bin/env -S uv run
"""make_student_folders.py

Build the student/ folder from the finished code in instructor/.

student/ mirrors instructor/ day by day and period by period. Each student period
folder holds the same files as the instructor period folder, except that the
functions the students write in that period are stubs: the signature and docstring
stay, and the body raises NotImplementedError. The tests stay complete, so they
fail until the pair writes each function. Functions from earlier periods are
complete, so every period folder starts from working code.

It also writes docs/student_edit_plan.md and the overview README.md at the top of
every Day folder, in instructor/ and student/ alike, from DAY_GUIDES in
period_guides.py.

Run this script again whenever the instructor code changes, after
make_period_folders.py.
"""

import ast
import shutil
from pathlib import Path
from typing import Any

from make_station_folders import STATIONS_TABLE
from period_guides import DAY_GUIDES, LABS

ROOT = Path(__file__).parent.parent  # The top Remus folder, above scripts/
INSTRUCTOR = ROOT / "instructor"
STUDENT = ROOT / "student"
MAX_TYPED_LINES = 40  # Most lines of code a pair types in one period
EditRow = dict[str, Any]  # One function a pair writes: file, name, line, tests

# (day, period, file, function) for every function the students write
STUDENT_FUNCTIONS = [
    (1, 4, "board.py", "print_board"),
    (1, 4, "board.py", "square_name"),
    (1, 4, "board.py", "parse_square"),
    (1, 4, "board.py", "piece_at"),
    (2, 3, "game_state.py", "is_white"),
    (2, 3, "game_state.py", "color_of"),
    (2, 3, "moves.py", "move_to_uci"),
    (2, 3, "moves.py", "move_from_uci"),
    (2, 4, "make_move.py", "make_move"),
    (2, 4, "make_move.py", "undo_move"),
    (3, 2, "move_generation.py", "king_moves"),
    (3, 3, "move_generation.py", "slide"),
    (3, 4, "move_generation.py", "pawn_pushes"),
    (4, 2, "attacks.py", "piece_at_offsets"),
    (4, 2, "attacks.py", "attacked_by_pawn"),
    (4, 2, "attacks.py", "attacked_by_king"),
    (4, 3, "attacks.py", "in_check"),
    (4, 3, "legal_moves.py", "legal_moves"),
    (5, 2, "make_move.py", "update_castling_rights"),
    (5, 3, "make_move.py", "en_passant_victim_square"),
    (6, 2, "perft.py", "perft"),
    (6, 4, "fen.py", "fen_placement"),
    (6, 4, "fen.py", "board_from_placement"),
    (7, 1, "game_end.py", "insufficient_material"),
    (7, 1, "game_end.py", "game_result"),
    (7, 2, "notation.py", "parse_san"),
    (7, 3, "search.py", "random_move"),
    (7, 3, "search.py", "greedy_move"),
    (7, 4, "evaluation.py", "material"),
    (8, 1, "search.py", "negamax"),
    (8, 2, "search.py", "alpha_beta"),
    (8, 3, "search.py", "quiescence"),
    (8, 4, "move_ordering.py", "mvv_lva_score"),
    (9, 1, "search.py", "think"),
    (9, 4, "mate_solver.py", "mating_move"),
    (10, 1, "hidden_peak.py", "candidate_squares"),
    (10, 1, "hidden_peak.py", "score_candidate"),
    (10, 1, "hidden_peak.py", "choose_next_measurement"),
    (10, 2, "phase_hunt.py", "score"),
    (10, 2, "phase_hunt.py", "greedy_phases"),
    (10, 3, "phase_hunt.py", "search"),
]


def typed_lines(source: str, name: str) -> int:
    """Return how many lines of code (not blank, not comments) a function's body has."""
    tree = ast.parse(source)
    node = next(
        n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name
    )
    lines = source.splitlines()[node.body[0].end_lineno : node.end_lineno]
    return sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))


def stub_function(source: str, name: str, day: int, period: int) -> str:
    """
    Replace the body of one function with a NotImplementedError stub.

    Parameters
    ----------
    source : str
        The text of a Python file.
    name : str
        The name of a top-level function in that file.
    day, period : int
        The day and period when the students write the function.

    Returns
    -------
    str
        The file text with the function's body after its docstring replaced.
    """
    tree = ast.parse(source)
    node = next(
        n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name
    )
    lines = source.splitlines(keepends=True)
    docstring = node.body[0]
    body_start = docstring.end_lineno  # Line numbers count from 1
    body_end = node.end_lineno
    indent = " " * (node.col_offset + 4)
    if name.startswith("test_"):
        hint = "The docstring above says what this test must check."
    else:
        hint = "The docstring above says what it must do; the tests check it."
    message = f'"Day {day} P{period}: write {name}()"'
    raise_line = f"{indent}raise NotImplementedError({message})\n"
    if len(raise_line) > 89:  # Wrap the way ruff format would, within 88 columns
        raise_line = (
            f"{indent}raise NotImplementedError(\n{indent}    {message}\n{indent})\n"
        )
    stub = [
        f"{indent}# Day {day}, period {period}: write this function.\n",
        f"{indent}# {hint}\n",
        raise_line,
    ]
    return "".join(lines[:body_start] + stub + lines[body_end:])


def lines_text(count: int) -> str:
    """Return "1 line" or "5 lines"."""
    return f"{count} line" if count == 1 else f"{count} lines"


def lab_blanks(source: str) -> int:
    """Return how many lines of a student lab file are a lone # for a line to type."""
    return sum(1 for line in source.splitlines() if line.strip() == "#")


def def_line(source: str, name: str) -> int:
    """Return the line number, counting from 1, where a top-level function starts."""
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node.lineno
    raise ValueError(f"No function named {name}")


def checking_tests(folder: Path, name: str) -> list[str]:
    """Return "file::test" for every test in a folder that calls a function by name."""
    tests = []
    for test_path in sorted(folder.glob("test_*.py")):
        for node in ast.parse(test_path.read_text()).body:
            if not isinstance(node, ast.FunctionDef):
                continue
            names = {item.id for item in ast.walk(node) if isinstance(item, ast.Name)}
            if node.name.startswith("test_") and name in names:
                tests.append(f"{test_path.name}::{node.name}")
    return tests


def edit_section(rows: list[EditRow]) -> str:
    """
    Return the "What you edit" section of a student README.

    Parameters
    ----------
    rows : list[EditRow]
        One row per function the pair writes in the period.

    Returns
    -------
    str
        Markdown with one table row per function: where its stub starts, how
        many lines to type, and which tests check it.
    """
    total = sum(row["typed"] for row in rows)
    lines = [
        "## What you edit this period",
        "",
        (
            "Every other function in this folder is finished. Change only these, and "
            "only below each docstring:"
        ),
        "",
        "| File | Function | Starts at line | Lines to type | Tests that check it |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        tests = ", ".join(f"`{test}`" for test in row["tests"]) or "`uv run pytest`"
        lines.append(
            f"| `{row['file']}` | `{row['function']}()` | {row['line']} | "
            f"{row['typed']} | {tests} |"
        )
    lines += [
        "",
        (
            f"Lines to type in all: {total}. Each stub is two comment lines that start "
            "with `# Day ...` and a `raise NotImplementedError` statement. Delete them "
            "and write the body in their place."
        ),
    ]
    return "\n".join(lines) + "\n"


def lab_section(name: str, count: int) -> str:
    """Return the "What you edit" section of a lab or demo period's student README."""
    lines = [
        "## What you edit in the lab"
        if name.startswith("python_")
        else "## What you edit in the demo",
        "",
        (
            f"Open `{name}.py`. Under each `Part` heading, every line that holds only a "
            "`#` is one line of code to type. Replace the `#` with the code, keeping "
            "its indent. The printed text next to each step says what the line must "
            "produce."
        ),
        "",
        (
            f"Lines to type in all: {count}. Check the work by running `{name}.py` "
            "with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it."
        ),
    ]
    return "\n".join(lines) + "\n"


def bug_hunt_section(count: int) -> str:
    """Return the "What you edit" section for the bug hunt of Day 6, period 3."""
    lines = [
        "## What you edit in the bug hunt",
        "",
        (
            "Open the `bug_hunt` folder and run `hunt.py` there in VS Code. Each root move "
            "it prints points at a planted bug in one of the Remus files of that "
            "folder. Fix each bug by changing the line that breaks the rule, and run "
            "the hunt again until every count agrees. The files outside `bug_hunt` "
            "are correct, so compare with them only after a guess."
        ),
        "",
        f"Lines to fix in all: {count}. `bug_hunt/README.md` explains the hunt.",
    ]
    return "\n".join(lines) + "\n"


def write_bug_hunt_student(target: Path) -> int:
    """Remove the answers from a student bug_hunt folder and return the lines to fix."""
    from make_period_folders import (
        PLANTED_BUGS,
        bug_hunt_readme,
    )  # It imports this file

    (target / "bug_hunt" / "README.md").write_text(bug_hunt_readme(with_answers=False))
    return len(PLANTED_BUGS)


def changed_files(folder: Path, before: Path | None) -> tuple[list[str], list[str]]:
    """Return the (new, changed) code files of a period folder, against the one before."""
    new, changed = [], []
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.name == "README.md" or path.suffix == ".pyc":
            continue
        old = before / path.name if before is not None else None
        if old is None or not old.exists():
            new.append(path.name)
        elif old.read_bytes() != path.read_bytes():
            changed.append(path.name)
    return new, changed


def pairs_write(day: int, period: int, rows: dict, station_note: str) -> str:
    """Return what the pairs write in one period, with the lines each one takes."""
    parts = []
    for row in rows.get((day, period), []):
        count = lines_text(row["typed"])
        if row["function"]:
            parts.append(f"`{row['function']}()` in `{row['file']}` ({count})")
        elif row["file"] == "bug_hunt/":
            parts.append(f"the fixes for the planted bugs in `bug_hunt/` ({count})")
        elif row["file"].startswith("demo_"):
            parts.append(f"the demo `{row['file']}` ({count})")
        else:
            parts.append(f"the lab `{row['file']}` ({count})")
    if (day, period) in [(9, 2), (9, 3)]:
        parts.append(f"their color station's functions, {station_note}")
    writes = "; ".join(parts)
    return writes[:1].upper() + writes[1:]


# The clock time each period starts, in minutes after midnight, and the break after it
PERIOD_STARTS = {1: 8 * 60 + 30, 2: 10 * 60 + 30, 3: 13 * 60, 4: 15 * 60}
PERIOD_MINUTES = 90
BREAKS = {1: "Break", 2: "Lunch", 3: "Break"}


def clock(minutes: int) -> str:
    """Return a time of day such as 8:30 or 1:00, from minutes after midnight."""
    hour = (minutes // 60 - 1) % 12 + 1
    return f"{hour}:{minutes % 60:02}"


def day_readme(day: int, rows: dict) -> str:
    """Return the README.md at the top of one Day folder: the day's overview."""
    from make_period_folders import PERIOD_TITLES  # Imported here: it imports this file

    guide = DAY_GUIDES[day]
    out = [f"# Day {day}: {guide['theme']}", "", guide["summary"], ""]
    out += ["## Objectives for the day", "", "By 4:30, each pair can:", ""]
    out += [f"- {objective}" for objective in guide["objectives"]]
    out += [
        "",
        "## The day at a glance",
        "",
        "| Period | Time | Title | Pairs write |",
        "| --- | --- | --- | --- |",
    ]
    for period in range(1, 5):
        start = PERIOD_STARTS[period]
        end = start + PERIOD_MINUTES
        writes = pairs_write(day, period, rows, "from the station README")
        out.append(
            f"| P{period} | {clock(start)} to {clock(end)} | "
            f"{PERIOD_TITLES[(day, period)]} | {writes or 'Nothing: teacher code'} |"
        )
        if period in BREAKS:
            next_start = PERIOD_STARTS[period + 1]
            out.append(
                f"| | {clock(end)} to {clock(next_start)} | {BREAKS[period]} | |"
            )
    for period in range(1, 5):
        start = PERIOD_STARTS[period]
        end = clock(start + PERIOD_MINUTES)
        out += [
            "",
            f"## Period {period}, {clock(start)} to {end}: {PERIOD_TITLES[(day, period)]}",
            "",
            "| Time | Activity |",
            "| --- | --- |",
        ]
        steps = guide["periods"][period]
        for i, (offset, text) in enumerate(steps):
            stop = steps[i + 1][0] if i + 1 < len(steps) else PERIOD_MINUTES
            out.append(f"| {clock(start + offset)} to {clock(start + stop)} | {text} |")
        out += [
            "",
            (
                f"[`period{period}/README.md`](period{period}/README.md) lists the "
                "period's learning objectives, how each one is measured, and every "
                "change the pairs make."
            ),
        ]
    out += [
        "",
        "## By the end of the day",
        "",
        f"**Checkpoint:** {guide['checkpoint']}",
        "",
        (
            "Each period folder starts from working code, so a pair that falls behind "
            "opens the next period's folder with the rest of the class."
        ),
    ]
    return "\n".join(out) + "\n"


def write_day_readmes(rows: dict) -> None:
    """Write the overview README.md at the top of every instructor and student Day."""
    for folder in sorted(INSTRUCTOR.glob("Day *")):
        day = int(folder.name[4:6])
        text = day_readme(day, rows)
        (folder / "README.md").write_text(text)
        (STUDENT / folder.name / "README.md").write_text(text)
    print("Wrote the overview README.md of every Day folder  (expected 10 of each)")


def write_edit_plan(rows: dict[tuple[int, int], list[EditRow]]) -> None:
    """Write docs/student_edit_plan.md: what changes and what pairs write, by period."""
    from make_period_folders import PERIOD_TITLES  # Imported here: it imports this file

    out = [
        "# Student Edit Plan: Who Writes What, Period by Period",
        "",
        (
            "`make_student_folders.py` writes this page from the code, so it always matches "
            "the folders. For every period it names the files that arrive or grow, which "
            "the teacher writes, and the functions the pairs write, which are stubs in "
            "`student/` and finished in `instructor/`. Each student period folder's "
            "`README.md` has the same list with line numbers and the tests that check "
            "each function."
        ),
        "",
    ]
    before = None
    for folder in sorted(INSTRUCTOR.glob("Day */period*")):
        day = int(folder.parent.name[4:6])
        period = int(folder.name.removeprefix("period"))
        if period == 1:
            out += [f"## {folder.parent.name}", ""]
            out += ["| Period | Title | New files | Files that grow | Pairs write |"]
            out += ["| --- | --- | --- | --- | --- |"]
        new, changed = changed_files(folder, before)
        writes = pairs_write(day, period, rows, "in the table below")
        out.append(
            f"| P{period} | {PERIOD_TITLES[(day, period)]} | "
            f"{', '.join(f'`{name}`' for name in new) or 'None'} | "
            f"{', '.join(f'`{name}`' for name in changed) or 'None'} | "
            f"{writes or 'Nothing: a demo or teacher code'} |"
        )
        if period == 4:
            out.append("")
        before = folder
    out += [
        "## Enhancement stations (Day 9, periods 2 and 3)",
        "",
        "Each pair writes the functions of one color station in `student/Remus`.",
        "",
        "| Station | Pairs write |",
        "| --- | --- |",
    ]
    for station in STATIONS_TABLE:
        written = rows.get(("station", station["folder"]), [])  # type: ignore[arg-type]
        writes = "; ".join(
            f"`{row['function']}()` in `{row['file']}` ({lines_text(row['typed'])})"
            for row in written
        )
        out.append(
            f"| {station['folder']} | {writes or 'Nothing: a finished engine'} |"
        )
    file_path = ROOT / "docs" / "student_edit_plan.md"
    file_path.write_text("\n".join(out) + "\n")
    print(f"Wrote {file_path}")


def main():
    stubbed = 0
    typed: dict[tuple[int, int], int] = {}  # (day, period) -> lines the pairs type
    rows: dict = {}  # (day, period), or ("station", folder), -> list[EditRow]
    for folder in sorted(INSTRUCTOR.glob("Day */period*")):
        day = int(folder.parent.name[4:6])
        period = int(folder.name.removeprefix("period"))
        target = STUDENT / folder.parent.name / folder.name
        lab_text = ""
        if (day, period) in LABS:
            # The lab file with blanks is written by hand in the student folder
            lab_path = target / f"{LABS[(day, period)]}.py"
            if not lab_path.exists():
                raise FileNotFoundError(f"{lab_path} is hand-written; restore it")
            lab_text = lab_path.read_text()
        if target.exists():
            shutil.rmtree(target)  # Rebuild each student period folder from scratch
        shutil.copytree(
            folder,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "*.svg"),
        )
        for stub_day, stub_period, file_name, function in STUDENT_FUNCTIONS:
            if (stub_day, stub_period) != (day, period):
                continue
            file_path = target / file_name
            text = file_path.read_text()
            count = typed_lines(text, function)
            typed[(day, period)] = typed.get((day, period), 0) + count
            row = {"file": file_name, "function": function, "typed": count}
            row["line"] = def_line(text, function)
            row["tests"] = checking_tests(folder, function)
            rows.setdefault((day, period), []).append(row)
            file_path.write_text(stub_function(text, function, stub_day, stub_period))
            stubbed += 1
        sections = []
        if (day, period) in rows:
            sections.append(edit_section(rows[(day, period)]))
        if (day, period) in LABS:
            # A student folder holds the lab with blanks, never the answer file
            name = LABS[(day, period)]
            (target / f"{name}_instructor.py").unlink()
            lab_path = target / f"{name}.py"
            lab_path.write_text(lab_text, newline="")
            lab_path.chmod(0o755)  # Each script runs on its own
            count = lab_blanks(lab_path.read_text())
            typed[(day, period)] = typed.get((day, period), 0) + count
            row = {"file": f"{name}.py", "function": "", "typed": count}
            rows.setdefault((day, period), []).append(row)
            sections.append(lab_section(name, count))
        if (target / "bug_hunt").exists():
            count = write_bug_hunt_student(target)
            typed[(day, period)] = typed.get((day, period), 0) + count
            row = {"file": "bug_hunt/", "function": "", "typed": count}
            rows.setdefault((day, period), []).append(row)
            sections.append(bug_hunt_section(count))
        if sections:
            with (target / "README.md").open("a") as file:
                for section in sections:
                    file.write("\n" + section)
    # Each station folder stubs the functions its pair writes during the station
    (STUDENT / "Remus").mkdir(exist_ok=True)
    shutil.copy2(INSTRUCTOR / "Remus" / "station_match.py", STUDENT / "Remus")
    for station in STATIONS_TABLE:
        folder = INSTRUCTOR / "Remus" / station["folder"]
        target = STUDENT / "Remus" / station["folder"]
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(
            folder,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "*.svg"),
        )
        color = station["folder"].split(" - ")[0].split(" ")[1]
        count = 0
        for file_name, function in station["students"]:
            file_path = target / file_name
            text = file_path.read_text()
            row = {"file": file_name, "function": function}
            row["typed"] = typed_lines(text, function)
            row["line"] = def_line(text, function)
            row["tests"] = checking_tests(folder, function)
            rows.setdefault(("station", station["folder"]), []).append(row)
            count += row["typed"]
            file_path.write_text(stub_function(text, function, 9, 2))
            stubbed += 1
        if station["students"]:
            with (target / "README.md").open("a") as file:
                file.write("\n" + edit_section(rows[("station", station["folder"])]))
        print(f"{color} station: {count} lines to type")
        if count > MAX_TYPED_LINES:
            print(f"  Too long: the {color} station asks for {count} lines")
    print(f"Wrote {STUDENT}")
    write_edit_plan(rows)
    write_day_readmes(rows)
    print(
        f"Functions turned into stubs: {stubbed}  (expected "
        f"{len(STUDENT_FUNCTIONS) + sum(len(st['students']) for st in STATIONS_TABLE)})"
    )
    longest = max(typed, key=lambda day_period: typed[day_period])
    print(
        f"Most lines typed in one period: {typed[longest]} on Day {longest[0]}, "
        f"period {longest[1]}  (expected at most {MAX_TYPED_LINES})"
    )
    for (day, period), count in sorted(typed.items()):
        if count > MAX_TYPED_LINES:
            print(f"  Too long: Day {day}, period {period} asks for {count} lines")


if __name__ == "__main__":
    main()
