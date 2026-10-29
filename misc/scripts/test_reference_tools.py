"""test_reference_tools.py

Check that the reference tools used to cross-check Remus are installed and
agree with the counts the workshop expects. These tests exercise python-chess
only; the native engine's own tests are written lesson by lesson. The last tests
check that every run_tests.py names only files that sit in its own folder, and that
every line of code a goals file or version README quotes matches its file.
"""

import ast
from pathlib import Path

import chess

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder


def test_python_chess_counts_twenty_moves_from_the_start() -> None:
    """The starting position has 16 pawn moves and 4 knight moves."""
    board = chess.Board()
    assert board.legal_moves.count() == 20


def test_python_chess_perft_depth_two_from_the_start() -> None:
    """Each of White's 20 moves leaves Black 20 replies: 400 positions."""
    board = chess.Board()
    count = 0
    for move in list(board.legal_moves):
        board.push(move)
        count += board.legal_moves.count()
        board.pop()
    assert count == 400


def test_every_run_tests_names_files_in_its_own_folder() -> None:
    """A file name in run_tests.py must name a file beside it, or the tests skip it."""
    missing = []
    for run_tests in ROOT.glob("Day */**/run_tests.py"):
        tree = ast.parse(run_tests.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                name = node.value
                is_file_name = name.endswith(".py") and " " not in name
                if is_file_name and not (run_tests.parent / name).exists():
                    missing.append(f"{run_tests}: {name}")
    assert missing == []


def code_blocks(markdown: str) -> list[tuple[str, list[tuple[int, str, str]]]]:
    """Return (heading, [(number, mark, text)]) for each block of "The code you type"."""
    blocks = []
    if "## The code you type" not in markdown:
        return blocks
    section = markdown.split("## The code you type", 1)[1]
    heading = ""
    inside = False
    for line in section.splitlines():
        if line.startswith("## "):
            break
        if line.startswith("### "):
            heading = line[4:]
        elif line == "```text":
            inside = True
            blocks.append((heading, []))
        elif line == "```":
            inside = False
        elif inside and line.strip() != "...":
            number, rest = line.split(maxsplit=1)
            mark, text = rest[0], rest[2:]
            blocks[-1][1].append((int(number), mark, text))
    return blocks


def quoted_files(markdown_path: Path) -> list[tuple[str, Path, Path]]:
    """Return (heading, student file, answer file) for each heading of a Markdown file."""
    if markdown_path.name == "README.md":
        student = markdown_path.parent
        answers = ROOT / "engines" / "instructor" / student.name
    else:
        student = markdown_path.parent / "student"
        answers = markdown_path.parent / "instructor"
    lab = None
    for path in student.glob("*.py"):
        if (answers / f"{path.stem}_instructor.py").exists():
            lab = path
    result = []
    for heading, _ in code_blocks(markdown_path.read_text(encoding="utf-8")):
        if " in `" in heading:
            name = heading.split(" in `")[1].rstrip("`")
            result.append((heading, student / name, answers / name))
        else:
            assert lab is not None, f"{markdown_path}: no lab for {heading}"
            result.append((heading, lab, answers / f"{lab.stem}_instructor.py"))
    return result


def test_every_quoted_line_of_code_matches_its_file() -> None:
    """Each numbered line of "The code you type" is that line of the finished file."""
    pages = sorted(ROOT.glob("Day */period*/*Goals.md"))
    pages += sorted((ROOT / "engines" / "student").glob("*/README.md"))
    wrong = []
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        files = quoted_files(page)
        for (heading, numbered), (_, student, answer) in zip(
            code_blocks(text), files, strict=True
        ):
            answer_lines = answer.read_text(encoding="utf-8").splitlines()
            student_lines = student.read_text(encoding="utf-8").splitlines()
            is_lab = answer.stem.endswith("_instructor")
            for number, mark, quoted in numbered:
                checked += 1
                if is_lab and mark == "+":
                    good = answer_lines[number - 1] == quoted
                    good = good and student_lines[number - 1].strip() == "#"
                elif is_lab:
                    good = student_lines[number - 1] == quoted
                else:
                    # A function's numbers count the finished file; its context lines
                    # are in the student file too
                    good = answer_lines[number - 1] == quoted
                    good = good and (mark == "+" or quoted in student_lines)
                if not good:
                    wrong.append(f"{page.name} {heading} line {number}: {quoted!r}")
    assert checked > 1000, checked
    assert wrong == []
