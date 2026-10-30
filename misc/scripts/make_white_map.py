#!/usr/bin/env -S uv run
"""make_white_map.py

Map the Python files of Remus-WHITE across the course. The script writes two things
into misc/docs/engines/remus_program_overview.md:

1. An import diagram, misc/docs/images/code/remus_white_imports.svg: one box per
   file, with an arrow from each file to every file it imports.
2. A table with one row per file and one column per day and period, which marks the
   periods where the file appears, where student pairs edit it, where the teacher's
   code in it grows, and where a goals file names it.

The table comes from the Day folders: each period's instructor folder and its
"Day NN Period NN Goals.md" file. Graphviz's dot program lays out the diagram, so
Graphviz (graphviz.org) must be installed with dot on the PATH. Run it from the top Remus folder with `uv run misc/scripts/make_white_map.py`
after `make_student_folders.py`.
"""

import ast
import re
import shutil
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder
WHITE = ROOT / "engines" / "instructor" / "00 Remus-WHITE - No enhancements"
OVERVIEW = ROOT / "misc" / "docs" / "engines" / "remus_program_overview.md"
IMAGE = ROOT / "misc" / "docs" / "images" / "code" / "remus_white_imports.svg"
HEADING = "## Remus-WHITE across the course"  # The section this script rewrites

# Files of Remus-WHITE that import no Remus module, so the diagram leaves them out
NOT_IN_DIAGRAM = ("play_match.py", "run_tests.py")

# Day 9 periods 2 and 3: each student pair edits these files in its own enhanced
# engine folder, a copy of Remus-WHITE in engines/student
ENHANCED_FILES = ("evaluation.py", "move_ordering.py", "search.py")

RAIL = "board"  # The file drawn as a rail along the bottom of the diagram
RAIL_WIDTH = 15.0  # Inches across board.py's rail, about as wide as the boxes above


def white_files() -> list[str]:
    """Return the names of the .py files in Remus-WHITE."""
    return sorted(path.name for path in WHITE.glob("*.py"))


def imports_of(file_name: str, modules: set[str]) -> set[str]:
    """Return the Remus modules that one Remus-WHITE file imports."""
    tree = ast.parse((WHITE / file_name).read_text())
    found = set()
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        for name in names:
            if name in modules and name != file_name[:-3]:
                found.add(name)
    return found


def import_edges() -> list[tuple[str, str]]:
    """Return every (importer, imported) pair of modules drawn in the diagram."""
    modules = set()
    for name in white_files():
        if not name.startswith("test_") and name not in NOT_IN_DIAGRAM:
            modules.add(name[:-3])
    edges = []
    for module in sorted(modules):
        for imported in sorted(imports_of(module + ".py", modules)):
            edges.append((module, imported))
    return edges


def dot_text(edges: list[tuple[str, str]], rail_width: float) -> str:
    """Return the Graphviz text of the import diagram, with an arrow for each import."""
    modules = sorted({name for edge in edges for name in edge} - {RAIL})
    modules.insert(0, RAIL)  # The rail comes first, which gives dot its best layout
    pairs = set(edges)
    lines = [
        "digraph remus_white {",
        (
            "  graph [nodesep=0.3, ranksep=0.55, splines=spline, remincross=true, mclimit=5, "
            'bgcolor="white", pad=0.2];'
        ),
        (
            '  node [shape=box, style="rounded,filled", fillcolor="#eef3fb", '
            'color="#33415c", fontname="Helvetica", fontsize=14, width=2.2, '
            "height=0.45, fixedsize=true, penwidth=1.4];"
        ),
        '  edge [color="#5c677d", arrowsize=0.8, penwidth=1.1];',
    ]
    for module in modules:
        if module == RAIL:
            # board.py is a wide rail along the bottom, so its arrows land side by side
            lines.append(
                f'  {{ rank=sink; "{module}" [label="{module}.py", '
                f"width={rail_width:.2f}]; }}"
            )
        else:
            lines.append(f'  "{module}" [label="{module}.py"];')
    for importer, imported in edges:
        if (imported, importer) in pairs:
            # Two files that import each other share one arrow with two heads
            if importer < imported:
                lines.append(f'  "{importer}" -> "{imported}" [dir=both];')
        else:
            lines.append(f'  "{importer}" -> "{imported}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def run_dot(text: str, output_format: str) -> str:
    """Return what Graphviz's dot program writes for a graph in one format."""
    dot = shutil.which("dot")
    if dot is None:
        raise SystemExit("Install Graphviz (graphviz.org) so that dot is on the PATH")
    result = subprocess.run(
        [dot, f"-T{output_format}"],
        input=text,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def stretch_rail(svg: str) -> str:
    """Return the SVG with board.py's rail stretched across the whole diagram."""
    view_box = re.search(r'viewBox="([\d. ]+)"', svg)
    shift = re.search(r"translate\(([\d.]+) ", svg)
    if view_box is None or shift is None:
        raise ValueError("dot wrote an SVG without a viewBox or a translate")
    width = float(view_box.group(1).split()[2]) - 2 * float(shift.group(1))
    start = svg.index(f"<title>{RAIL}</title>")
    end = svg.index("</g>", start)
    group = svg[start:end]
    path = re.search(r'<path ([^>]*?) d="([^"]+)"/>', group)
    label = re.search(r'<text text-anchor="middle" x="([\d.-]+)"', group)
    if path is None or label is None:
        raise ValueError(f"dot wrote {RAIL} without a box and a label")
    heights = []
    for number in re.findall(r",(-?[\d.]+)", path.group(2)):
        heights.append(float(number))
    top = min(heights)
    rail = (
        f'<rect {path.group(1)} x="0" y="{top}" width="{width:.2f}" '
        f'height="{max(heights) - top}" rx="10.67"/>'
    )
    group = group.replace(path.group(0), rail)
    group = group.replace(f'x="{label.group(1)}"', f'x="{width / 2:.2f}"', 1)
    return svg[:start] + group + svg[end:]


def draw_diagram(edges: list[tuple[str, str]]):
    """Draw the import diagram as an SVG picture with Graphviz's dot."""
    svg = stretch_rail(run_dot(dot_text(edges, RAIL_WIDTH), "svg"))
    IMAGE.parent.mkdir(parents=True, exist_ok=True)
    IMAGE.write_text(svg)
    print(f"Drew {len(edges)} imports in {IMAGE}")


def goals_text(period_folder: Path) -> str:
    """Return a period's goals file without the lines every goals file repeats."""
    goals = list(period_folder.glob("*Goals.md"))
    if not goals:
        return ""
    kept = []
    for line in goals[0].read_text().splitlines():
        # Every period with tests tells student pairs to run run_tests.py
        if line.startswith("Check the work with the tests"):
            continue
        kept.append(line.replace("| `run_tests.py` |", "|"))
    return "\n".join(kept) + "\n"


def bullet_list(text: str, title: str) -> str:
    """Return the bullet lines under a title such as "New files this period:"."""
    match = re.search("^" + re.escape(title) + r"\n\n((?:- .*\n)+)", text, re.MULTILINE)
    return match.group(1) if match else ""


def names_file(text: str, file_name: str) -> bool:
    """Return True if the text names the file, such as `board.py`."""
    return re.search(r"(?<![\w/])" + re.escape(file_name), text) is not None


def course_marks(files: list[str]) -> tuple[list, dict]:
    """Return the periods that touch Remus-WHITE and each file's mark per period."""
    marks = {name: {} for name in files}
    periods = []
    earlier_files = set()
    for day_folder in sorted(ROOT.glob("Day *")):
        day = int(day_folder.name[4:6])
        for period in range(1, 5):
            period_folder = day_folder / f"period{period}"
            periods.append((day, period))
            instructor = period_folder / "instructor"
            present = set()
            # Day 10 and Day 9 periods 2 to 4 hold no engine code
            if (instructor / "board.py").exists():
                present = {path.name for path in instructor.glob("*.py")}
            has_tests = (
                bool(present) and (period_folder / "student" / "run_tests.py").exists()
            )
            text = goals_text(period_folder)
            new = bullet_list(text, "New files this period:")
            grows = bullet_list(text, "Files that grow this period:")
            written = bullet_list(
                text, "Functions the student pairs write this period:"
            )
            enhanced = day == 9 and period in (2, 3)
            for name in files:
                mark = ""
                if names_file(new, name) or (
                    name in present and name not in earlier_files
                ):
                    mark += "N"
                if names_file(written, name):
                    mark += "E"
                if names_file(grows, name):
                    mark += "T"
                if enhanced and name in ENHANCED_FILES:
                    mark += "X"
                if not mark and names_file(text, name):
                    mark = "M"
                if not mark and name == "run_tests.py" and (has_tests or enhanced):
                    mark = "M"
                if mark:
                    marks[name][(day, period)] = mark
            if present:
                earlier_files = present
    used = []
    for day_period in periods:
        for name in files:
            if day_period in marks[name]:
                used.append(day_period)
                break
    return used, marks


def first_period(marks: dict) -> tuple[int, int]:
    """Return the day and period in which a file first appears."""
    first = (99, 9)
    for day_period, mark in marks.items():
        if "N" in mark:
            first = min(first, day_period)
    return first


def table_text(files: list[str]) -> str:
    """Return the Markdown table of Remus-WHITE's files by day and period."""
    used, marks = course_marks(files)
    keyed = []
    for name in files:
        keyed.append((first_period(marks[name]), name))
    keyed.sort()
    header = "| File |"
    rule = "| --- |"
    for day, period in used:
        header += f" D{day:02d} P{period} |"
        rule += " :---: |"
    rows = [header, rule]
    for _, name in keyed:
        row = f"| `{name}` |"
        for day_period in used:
            row += f" {marks[name].get(day_period, '')} |"
        rows.append(row)
    return "\n".join(rows) + "\n"


def paragraph(text: str) -> str:
    """Return one paragraph wrapped at 88 characters, then a blank line."""
    wrapped = textwrap.fill(
        text, width=88, break_long_words=False, break_on_hyphens=False
    )
    return wrapped + "\n\n"


def section_text(files: list[str], edges: list[tuple[str, str]]) -> str:
    """Return the whole Remus-WHITE section of the overview page."""
    diagram_count = len({name for edge in edges for name in edge})
    text = f"{HEADING}\n\n"
    text += paragraph(
        "Remus-WHITE is the finished Day 9 Remus, in "
        "`engines/instructor/00 Remus-WHITE - No enhancements`. "
        f"It holds {len(files)} Python files."
    )
    text += "### Which file imports which\n\n"
    text += paragraph(
        f"The diagram shows the {diagram_count} files that import another Remus "
        "file or are imported by one. An arrow points from the file that imports "
        "to the file it imports: `search.py` points at `evaluation.py` because "
        "`search.py` calls `evaluate()`. A two-headed arrow would mean two files "
        "import each other; no two Remus files do. Every arrow points down the "
        "page. The programs a person runs, such as `uci_engine.py`, sit along the "
        "top edge, because no file imports them. `board.py` imports no Remus file "
        "and almost every file imports it, so it is the wide rail along the bottom "
        "edge, where its 13 arrows land side by side. The files with the most "
        "arrows, such as `search.py` and `legal_moves.py`, sit in the middle rows. "
        "The test files, `run_tests.py`, and `play_match.py`, which starts Remus as "
        "a separate program, are left out."
    )
    text += (
        "![Import diagram of Remus-WHITE](../images/code/remus_white_imports.svg)\n\n"
    )
    text += "### When each file appears and changes\n\n"
    text += paragraph(
        "Each row is one file, in the order the class meets it: by the period the "
        "file first appears, then by name. Each column is a period that touches a "
        "Remus-WHITE file; D07 P2 means Day 7, period 2. A cell holds one or more "
        "letters:"
    )
    text += (
        "| Mark | Meaning |\n"
        "| --- | --- |\n"
        "| N | New: the file first appears in this period's folder |\n"
        "| E | Edited: the student pairs write a function in this file |\n"
        "| X | Edited in an enhanced engine: the student pairs change their own copy "
        "of this file in `engines/student` |\n"
        "| T | Teacher code: the teacher's finished code in this file grows, and the "
        "student pairs type none of it |\n"
        "| M | Mentioned: the period's goals file names the file, which the student "
        "pairs run or read |\n\n"
    )
    text += paragraph(
        "Read a row from left to right: the N cell is the period the file arrives, "
        "and the last E or X cell is the last period a student pair changes it. "
        "Student pairs run `run_tests.py` in every period that has tests. "
        "Day 10 holds only the science files, so it has no column."
    )
    text += table_text(files) + "\n"
    return text


def write_section(section: str):
    """Put the section into the overview page, before "The four boundaries"."""
    text = OVERVIEW.read_text()
    if HEADING in text:
        start = text.index(HEADING)
        end = text.index("\n## ", start) + 1
        text = text[:start] + section + text[end:]
    else:
        anchor = text.index("## The four boundaries")
        text = text[:anchor] + section + text[anchor:]
    OVERVIEW.write_text(text)
    print(f"Wrote the Remus-WHITE section of {OVERVIEW}")


def main():
    files = white_files()
    edges = import_edges()
    draw_diagram(edges)
    write_section(section_text(files, edges))
    print(f"Mapped {len(files)} Remus-WHITE files  (expected 27)")


if __name__ == "__main__":
    main()
