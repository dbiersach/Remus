#!/usr/bin/env -S uv run
"""make_student_folders.py

Build every student folder from the finished code in the instructor folder beside it.

Each period folder of each Day holds an instructor folder and a student folder.
The student folder holds the same files as the instructor folder, except that the
functions the students write in that period are stubs: the signature and docstring
stay, and the body raises NotImplementedError. The tests stay complete, so they
fail until the student pair writes each function. Functions from earlier periods are
complete, so every student folder starts from working code.

It adds the timed flow of the period and the student pairs' exact tasks to each period's
goals file, such as "Day_03_Period_02_Goals.md", and writes
misc/teachers/student_edit_plan.md and the syllabus, "Day_NN_Syllabus.md", at the
top of every Day folder, from DAY_GUIDES in period_guides.py.

Run this script again whenever the instructor code changes, after
make_period_folders.py.
"""

import ast
import shutil
from pathlib import Path
from typing import Any

from make_version_folders import ENGINE_SKIPS, VERSIONS_TABLE
from period_guides import CODE_NOTES, DAY_GUIDES, LABS

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder, above misc/designer/


def instructor_folders() -> list[Path]:
    """Return every period's instructor folder, Day 01 period1 first."""
    return sorted(ROOT.glob("Day */period*/instructor"))


MAX_TYPED_LINES = 40  # Most lines of code a student pair types in one period
EditRow = dict[str, Any]  # One function a student pair writes: file, name, line, tests

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
    Return the "What you edit" section of a goals file or version README.

    Parameters
    ----------
    rows : list[EditRow]
        One row per function the student pair writes in the period.

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
            "Every other function is finished. Change only these, and only below each "
            "docstring:"
        ),
        "",
        "| File | Function | Starts at line | Lines to type | Tests that check it |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        tests = ", ".join(f"`{test}`" for test in row["tests"]) or "`run_tests.py`"
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


CODE_INTRO = (
    "Each block below shows the code to type with a few lines around it, so you can "
    "find the spot. A line marked `+` is one you type; a line marked `|` is already "
    "in the file. Type the code without the number and the mark, and keep the indent "
    "shown. Lines that start with `#` are comments: they explain the code, and "
    "typing them is optional."
)
CODE_NUMBERS = (
    "The number at the left of each line is its line number once the code is typed. "
    "When one file holds two functions to write, type the higher one first: until "
    "it is typed, the stub of a function lower down sits a few lines higher than "
    "these numbers say."
)


def snippet_block(numbered: list[tuple[int, str, str]]) -> str:
    """Return a Markdown code block from (line number, mark, text); number 0 is a gap."""
    width = len(str(numbered[-1][0]))
    out = "```python\n"
    for number, mark, text in numbered:
        if number == 0:
            out += " " * width + "   " + text + "\n"  # Lines left out, such as "..."
        else:
            out += f"{number:>{width}} {mark} {text}".rstrip() + "\n"
    return out + "```\n"


def body_span(text: str, name: str) -> tuple[int, int, int, int]:
    """Return (def line, docstring end, body start, body end) of a function, from 1."""
    for node in ast.parse(text).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            docstring_end = node.body[0].end_lineno or node.lineno
            return node.lineno, docstring_end, docstring_end + 1, node.end_lineno or 0
    raise ValueError(f"No function named {name}")


def callers(folder: Path, name: str, home: str) -> list[str]:
    """Return "`caller()` in `file`" for every engine function in a folder that calls name."""
    found = []
    for path in sorted(folder.glob("*.py")):
        if path.name.startswith("test_"):
            continue
        for node in ast.parse(path.read_text()).body:
            if not isinstance(node, ast.FunctionDef) or node.name == name:
                continue
            if node.name == "main" and path.name == home:
                continue  # The file's own main() only runs its self-check
            for item in ast.walk(node):
                called = isinstance(item, ast.Call) and (
                    (isinstance(item.func, ast.Name) and item.func.id == name)
                    or (isinstance(item.func, ast.Attribute) and item.func.attr == name)
                )
                if called:
                    found.append(f"`{node.name}()` in `{path.name}`")
                    break
    return found


def function_code(student: Path, answer: Path, row: EditRow) -> str:
    """Return the "code you type" part for one function: where, the code, and how."""
    name, file_name = row["function"], row["file"]
    lines = answer.read_text().splitlines()
    def_number, docstring_end, first, last = body_span(answer.read_text(), name)
    numbered = [(def_number, "|", lines[def_number - 1])]
    context_start = max(def_number + 1, docstring_end - 1)
    if context_start > def_number + 2:
        # Show the line that opens the docstring, so the highlighter sees a string
        numbered.append((def_number + 1, "|", lines[def_number]))
        numbered.append((0, "", "..."))  # The middle of a long docstring
    elif context_start > def_number + 1:
        context_start = def_number + 1
    for number in range(context_start, docstring_end + 1):
        numbered.append((number, "|", lines[number - 1]))
    for number in range(first, last + 1):
        numbered.append((number, "+", lines[number - 1]))
    # Show the lines after the function up to the next line that holds code
    for number in range(last + 1, min(last + 3, len(lines)) + 1):
        numbered.append((number, "|", lines[number - 1]))
        if lines[number - 1].strip():
            break
    called_by = callers(student.parent, name, file_name)
    if name.startswith("test_"):
        used = "`run_tests.py` runs it with every other test in the folder."
    elif called_by:
        used = "It is called by " + ", ".join(called_by) + "."
    else:
        used = "The tests call it directly."
    span = f"line {first}" if first == last else f"lines {first} to {last}"
    where = (
        f"**Where:** {span} of `{file_name}`, inside `{name}()`, "
        f"in place of the stub below the docstring. {used}"
    )
    parts = [f"### `{name}()` in `{file_name}`", "", where, "", snippet_block(numbered)]
    if (file_name, name) not in CODE_NOTES:
        raise KeyError(
            f"Write CODE_NOTES[({file_name!r}, {name!r})] in period_guides.py"
        )
    parts += [f"**How it works:** {CODE_NOTES[(file_name, name)]}", ""]
    return "\n".join(parts)


def lab_groups(student_text: str, answer_text: str) -> list[tuple[str, str, list[int]]]:
    """
    Return (heading, note key, blank line numbers) for each part of a lab file.

    A blank belongs to the Part heading or the function above it. A blank at the
    left edge of the file takes its heading from its answer: the imports, a class,
    or a new function.
    """
    answers = answer_text.splitlines()
    groups: list[tuple[str, str, list[int]]] = []
    heading, key = "", ""
    for number, line in enumerate(student_text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("def "):
            key = stripped[4:].split("(")[0]
            heading = f"`{key}()`"
        elif stripped.startswith(('print("Part #', "print('Part #")):
            # print("Part #2 - Sets") gives the heading Part #2 - Sets
            heading = "Part #" + stripped.split("Part #", 1)[1][:-2]
            key = heading.split(" - ")[0]
        elif line == "#":
            answer = answers[number - 1]
            if answer.startswith(("import ", "from ")):
                heading, key = "The imports", "imports"
            elif answer.startswith("def "):
                key = answer[4:].split("(")[0]
                heading = f"`{key}()`"
            elif answer.startswith(("@", "class ")):
                for text in answers[number - 1 :]:
                    if text.startswith("class "):
                        key = text[6:].split("(")[0].rstrip(":")
                        break
                heading = f"The `{key}` class"
        if stripped == "#":
            if not groups or groups[-1][1] != key:
                groups.append((heading, key, []))
            groups[-1][2].append(number)
    return groups


def lab_code(name: str, student: Path, answer: Path, with_heading: bool = True) -> str:
    """Return the "code you type" part of a lab or demo, with its heading if asked."""
    student_lines = student.read_text().splitlines()
    answer_lines_all = answer.read_text().splitlines()
    out = ["## The code you type", "", CODE_INTRO, ""] if with_heading else []
    groups = lab_groups(student.read_text(), answer.read_text())
    for heading, key, blanks in groups:
        out += [f"### {heading}", ""]
        # Split a part into blocks wherever two blanks sit more than four lines apart
        blocks = [[blanks[0]]]
        for number in blanks[1:]:
            if number - blocks[-1][-1] > 4:
                blocks.append([])
            blocks[-1].append(number)
        for block in blocks:
            numbered = []
            start = max(1, block[0] - 2)
            stop = min(len(student_lines), block[-1] + 2)
            for number in range(start, stop + 1):
                if number in block:
                    numbered.append((number, "+", answer_lines_all[number - 1]))
                else:
                    numbered.append((number, "|", student_lines[number - 1]))
            out += [snippet_block(numbered)]
        if (name, key) not in CODE_NOTES:
            raise KeyError(f"Write CODE_NOTES[({name!r}, {key!r})] in period_guides.py")
        out += [f"**How it works:** {CODE_NOTES[(name, key)]}", ""]
    return "\n".join(out)


def code_section(folder: Path, answers: Path, rows: list[EditRow]) -> str:
    """Return the "code you type" section for the functions of one period or version."""
    out = ["## The code you type", "", CODE_INTRO, "", CODE_NUMBERS, ""]
    for row in rows:
        out.append(function_code(folder / row["file"], answers / row["file"], row))
    return "\n".join(out)


def lab_section(name: str, count: int) -> str:
    """Return the "What you edit" section of a lab or demo period's goals file."""
    lines = [
        "## What you edit in the lab"
        if name.startswith("python_")
        else "## What you edit in the demo",
        "",
        (
            f"Open `{name}.py` in the `student` folder. Under each `Part` heading, every line that holds only a "
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
            "Open the `bug_hunt` folder inside `student` and run `hunt.py` there in VS Code. Each root move "
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


def pairs_write(day: int, period: int, rows: dict, version_note: str) -> str:
    """Return what the student pairs write in one period, with the lines each one takes."""
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
        parts.append(f"their enhanced engine's functions, {version_note}")
    writes = "; ".join(parts)
    return writes[:1].upper() + writes[1:]


# The clock time each period starts, in minutes after midnight, and the break after it
PERIOD_STARTS = {1: 8 * 60 + 30, 2: 10 * 60 + 30, 3: 13 * 60, 4: 15 * 60}
PERIOD_MINUTES = 90
FLOW_HEADING = (
    "## The period step by step"  # Starts the part of a goals file this script writes
)
BREAKS = {1: "Break", 2: "Lunch", 3: "Break"}


def clock(minutes: int) -> str:
    """Return a time of day such as 8:30 or 1:00, from minutes after midnight."""
    hour = (minutes // 60 - 1) % 12 + 1
    return f"{hour}:{minutes % 60:02}"


def day_readme(day: int, rows: dict) -> str:
    """Return the syllabus at the top of one Day folder: the day's overview."""
    from make_period_folders import PERIOD_TITLES  # Imported here: it imports this file

    guide = DAY_GUIDES[day]
    out = [f"# Day {day}: {guide['theme']}", "", guide["summary"], ""]
    out += ["## Objectives for the day", "", "By 4:30, each student pair can:", ""]
    out += [f"- {objective}" for objective in guide["objectives"]]
    out += [
        "",
        "## The day at a glance",
        "",
        "| Period | Time | Title | Student pairs write |",
        "| --- | --- | --- | --- |",
    ]
    for period in range(1, 5):
        start = PERIOD_STARTS[period]
        end = start + PERIOD_MINUTES
        writes = pairs_write(day, period, rows, "from the version README")
        out.append(
            f"| P{period} | {clock(start)} to {clock(end)} | "
            f"{PERIOD_TITLES[(day, period)]} | {writes or 'Nothing: given code'} |"
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
                f"[`Day_{day:02}_Period_{period:02}_Goals.md`]"
                f"(period{period}/Day_{day:02}_Period_{period:02}_Goals.md) "
                "lists the period's learning objectives, how each one is measured, "
                "every change the student pairs make, and their exact tasks."
            ),
        ]
    out += [
        "",
        "## By the end of the day",
        "",
        f"**Checkpoint:** {guide['checkpoint']}",
        "",
        (
            "Each period folder starts from working code, so a student pair that falls behind "
            "opens the next period's folder with the rest of the class."
        ),
    ]
    return "\n".join(out) + "\n"


def flow_section(day: int, period: int) -> str:
    """Return the timed steps of one period, from DAY_GUIDES, as a Markdown table."""
    start = PERIOD_STARTS[period]
    lines = [FLOW_HEADING, "", "| Time | Activity |", "| --- | --- |"]
    steps = DAY_GUIDES[day]["periods"][period]
    for i, (offset, text) in enumerate(steps):
        stop = steps[i + 1][0] if i + 1 < len(steps) else PERIOD_MINUTES
        # A link in DAY_GUIDES starts from the Day folder, one level above the goals file
        text = text.replace("](../", "](../../")
        lines.append(f"| {clock(start + offset)} to {clock(start + stop)} | {text} |")
    return "\n".join(lines) + "\n"


def write_goals(day: int, period: int, sections: list[str]) -> None:
    """
    Add the flow of the period and the student pairs' tasks to the period's goals file.

    make_period_folders.py writes the first part of the file. Everything from
    FLOW_HEADING on is rewritten here, so running this script twice gives the
    same file.
    """
    from make_period_folders import goals_path  # Imported here: it imports this file

    file_path = goals_path(day, period)
    text = file_path.read_text()
    text = text.split("\n" + FLOW_HEADING)[0].rstrip("\n") + "\n"
    for section in [flow_section(day, period), *sections]:
        text += "\n" + section
    file_path.write_text(text)


def write_day_readmes(rows: dict) -> None:
    """Write the syllabus, "Day_NN_Syllabus.md", at the top of every Day folder."""
    count = 0
    for folder in sorted(ROOT.glob("Day *")):
        day = int(folder.name[4:6])
        (folder / "README.md").unlink(missing_ok=True)
        (folder / f"Day_{day:02}_Syllabus.md").write_text(day_readme(day, rows))
        count += 1
    print(f"Wrote the syllabus of {count} Day folders  (expected 10)")


def write_edit_plan(rows: dict[tuple[int, int], list[EditRow]]) -> None:
    """Write misc/teachers/student_edit_plan.md: what changes and what student pairs write, by period."""
    from make_period_folders import PERIOD_TITLES  # Imported here: it imports this file

    out = [
        "# Student Edit Plan: Who Writes What, Period by Period",
        "",
        (
            "`make_student_folders.py` writes this page from the code, so it always matches "
            "the folders. For every period it names the files that arrive or grow, which "
            "hold given code, and the functions the student pairs write, which are stubs in "
            "each `student` folder and finished in the `instructor` folder beside it. Each "
            "period's "
            "goals file, such as `Day_03_Period_02_Goals.md`, has the same list with line numbers and the tests that check "
            "each function."
        ),
        "",
    ]
    before = None
    for folder in instructor_folders():
        day = int(folder.parent.parent.name[4:6])
        period = int(folder.parent.name.removeprefix("period"))
        if period == 1:
            out += [f"## {folder.parent.parent.name}", ""]
            out += [
                "| Period | Title | New files | Files that grow | Student pairs write |"
            ]
            out += ["| --- | --- | --- | --- | --- |"]
        new, changed = changed_files(folder, before)
        writes = pairs_write(day, period, rows, "in the table below")
        out.append(
            f"| P{period} | {PERIOD_TITLES[(day, period)]} | "
            f"{', '.join(f'`{name}`' for name in new) or 'None'} | "
            f"{', '.join(f'`{name}`' for name in changed) or 'None'} | "
            f"{writes or 'Nothing: a demo or given code'} |"
        )
        if period == 4:
            out.append("")
        before = folder
    out += [
        "## Enhanced engines (Day 9, periods 2 and 3)",
        "",
        "Each student pair writes the functions of one enhanced engine in `engines/student`.",
        "",
        "| Enhanced engine | Student pairs write |",
        "| --- | --- |",
    ]
    for version in VERSIONS_TABLE:
        if not version["students"]:
            continue  # Remus-GOLD stays in the teacher's folders
        written = rows.get(("version", version["folder"]), [])  # type: ignore[arg-type]
        writes = "; ".join(
            f"`{row['function']}()` in `{row['file']}` ({lines_text(row['typed'])})"
            for row in written
        )
        out.append(
            f"| {version['folder']} | {writes or 'Nothing: a finished engine'} |"
        )
    file_path = ROOT / "misc" / "teachers" / "student_edit_plan.md"
    file_path.write_text("\n".join(out) + "\n")
    print(f"Wrote {file_path}")


def main():
    stubbed = 0
    typed: dict[
        tuple[int, int], int
    ] = {}  # (day, period) -> lines the student pairs type
    rows: dict = {}  # (day, period), or ("version", folder), -> list[EditRow]
    for folder in instructor_folders():
        day = int(folder.parent.parent.name[4:6])
        period = int(folder.parent.name.removeprefix("period"))
        target = folder.parent / "student"
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
            ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "*.svg", "target"),
        )
        for stub_day, stub_period, file_name, function in STUDENT_FUNCTIONS:
            if (stub_day, stub_period) != (day, period):
                continue
            file_path = target / file_name
            text = file_path.read_text()
            count = typed_lines(text, function)
            typed[(day, period)] = typed.get((day, period), 0) + count
            row = {"file": file_name, "function": function, "typed": count}
            row["line"] = def_line((folder / file_name).read_text(), function)
            row["tests"] = checking_tests(folder, function)
            rows.setdefault((day, period), []).append(row)
            file_path.write_text(stub_function(text, function, stub_day, stub_period))
            stubbed += 1
        sections = []
        if (day, period) in rows:
            sections.append(edit_section(rows[(day, period)]))
            sections.append(code_section(target, folder, rows[(day, period)]))
        if (day, period) in LABS:
            # A student folder holds the lab with blanks, never the answer file
            name = LABS[(day, period)]
            (target / f"{name}_instructor.py").unlink()
            lab_path = target / f"{name}.py"
            lab_path.write_text(lab_text, newline="")
            if (target / "run_tests.py").exists():
                # make_period_folders imports this file, so it is imported here
                from make_period_folders import run_tests_text

                # run_tests.py names the student lab file, not the answer file
                (target / "run_tests.py").write_text(run_tests_text(target))
            lab_path.chmod(0o755)  # Each script runs on its own
            count = lab_blanks(lab_path.read_text())
            typed[(day, period)] = typed.get((day, period), 0) + count
            row = {"file": f"{name}.py", "function": "", "typed": count}
            rows.setdefault((day, period), []).append(row)
            sections.append(lab_section(name, count))
            # A period with functions to write already opened "The code you type"
            first = not any(row["function"] for row in rows[(day, period)])
            code = lab_code(name, lab_path, folder / f"{name}_instructor.py", first)
            if first:
                sections.append(code)
            else:
                sections[-2] += "\n" + code
        if (target / "bug_hunt").exists():
            count = write_bug_hunt_student(target)
            typed[(day, period)] = typed.get((day, period), 0) + count
            row = {"file": "bug_hunt/", "function": "", "typed": count}
            rows.setdefault((day, period), []).append(row)
            sections.append(bug_hunt_section(count))
        write_goals(day, period, sections)
    # Each engine folder stubs the functions its student pair writes on Day 9.
    # engines/student holds Remus-WHITE and the ten enhanced engines, but not
    # Remus-GOLD, which stays in engines/instructor.
    engines = ROOT / "engines" / "instructor"
    student_engines = ROOT / "engines" / "student"
    white = "00 Remus-WHITE - No enhancements"
    if (student_engines / white).exists():
        shutil.rmtree(student_engines / white)
    # The student Remus-WHITE is the Day 9 period1 student folder, stubs and all
    shutil.copytree(
        next(ROOT.glob("Day 09 - *")) / "period1" / "student",
        student_engines / white,
        ignore=shutil.ignore_patterns(*ENGINE_SKIPS),
    )
    shutil.copy2(engines / white / "README.md", student_engines / white / "README.md")
    for version in VERSIONS_TABLE:
        folder = engines / version["folder"]
        target = student_engines / version["folder"]
        if target.exists():
            shutil.rmtree(target)
        if not version["students"]:
            continue
        shutil.copytree(
            folder,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pgn", "*.svg"),
        )
        color = version["folder"].split(" - ")[0].split(" ")[1].removeprefix("Remus-")
        count = 0
        for file_name, function in version["students"]:
            file_path = target / file_name
            text = file_path.read_text()
            row = {"file": file_name, "function": function}
            row["typed"] = typed_lines(text, function)
            row["line"] = def_line((folder / file_name).read_text(), function)
            row["tests"] = checking_tests(folder, function)
            rows.setdefault(("version", version["folder"]), []).append(row)
            count += row["typed"]
            file_path.write_text(stub_function(text, function, 9, 2))
            stubbed += 1
        if version["students"]:
            with (target / "README.md").open("a") as file:
                written = rows[("version", version["folder"])]
                file.write("\n" + edit_section(written))
                file.write("\n" + code_section(target, folder, written))
        print(f"Remus-{color}: {count} lines to type")
        if count > MAX_TYPED_LINES:
            print(f"  Too long: Remus-{color} asks for {count} lines")
    print("Wrote every student folder")
    write_edit_plan(rows)
    write_day_readmes(rows)
    print(
        f"Functions turned into stubs: {stubbed}  (expected "
        f"{len(STUDENT_FUNCTIONS) + sum(len(st['students']) for st in VERSIONS_TABLE)})"
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
