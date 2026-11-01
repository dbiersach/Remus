#!/usr/bin/env -S uv run
"""make_handouts.py

Print each handout of misc/teachers/handouts/handouts.md as its own letter-size PDF.

A course designer tool, like the other make_*.py scripts. handouts.md stays the
source of every worksheet and cheat sheet; this script reads it, cuts it at each
`---` line into one handout per section, turns the Markdown of each handout into a
small HTML page with the board diagrams embedded, and asks a Chromium-based browser
(Microsoft Edge on Windows, Chrome or Chromium elsewhere) to print the page to
handout_NN_<title>.pdf beside it. Edge comes with Windows 11, so the
designer's PC needs nothing installed. Run it after any change to handouts.md:

    uv run misc/designer/make_handouts.py

The Markdown reader below understands only what handouts.md uses: `##` headings,
paragraphs, `**bold**`, `inline code`, tables with alignment rows, fenced code
blocks, bullet and numbered lists, images, and links (printed as their text, since a
sheet of paper has nothing to click).
"""

import base64
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder, above misc/designer/
OUT = ROOT / "misc" / "teachers" / "handouts"  # One PDF per handout goes here
SOURCE = OUT / "handouts.md"  # The page every handout comes from
BROWSER_VARIABLE = (
    "REMUS_BROWSER"  # Names the browser program when the search below fails
)

# Where a Chromium-based browser usually sits. Edge is on every Windows 11 PC.
BROWSER_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/opt/pw-browsers/chromium",
]
BROWSER_NAMES = ["msedge", "google-chrome", "chromium", "chromium-browser", "chrome"]
LONG_CODE = 30  # Code spans longer than this may wrap inside a table cell

# The look of every handout: letter paper, wide lines to write on, tables that print
# well in black and white, and fonts that Windows and Linux both have.
STYLE = """
@page { size: 8.5in 11in; margin: 0.55in 0.6in 0.6in 0.6in; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", "Inter", Arial, sans-serif; font-size: 10pt;
       line-height: 1.38; color: #111; margin: 0;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
header { display: flex; justify-content: space-between; align-items: baseline;
         border-bottom: 2px solid #111; padding-bottom: 3pt; margin-bottom: 8pt; }
header .course { font-size: 8pt; letter-spacing: 0.08em; text-transform: uppercase;
                 color: #555; }
h1 { font-size: 17pt; margin: 0; line-height: 1.2; }
p { margin: 0 0 7pt 0; }
code { font-family: Consolas, "JetBrains Mono", "DejaVu Sans Mono", monospace;
       font-size: 9.5pt; background: #f1f1f1; padding: 0 2pt; border-radius: 2pt; }
pre { font-family: Consolas, "JetBrains Mono", "DejaVu Sans Mono", monospace;
      font-size: 8pt; line-height: 1.3; background: #f6f6f6; border: 1px solid #ccc;
      padding: 5pt 8pt; margin: 0 0 6pt 0; white-space: pre; overflow: hidden; }
pre code { background: none; padding: 0; font-size: inherit; }
td code { white-space: nowrap; }
td code.long { white-space: normal; word-break: break-all; }
pre, img, .position { page-break-inside: avoid; }
p:has(+ pre), p:has(+ table), p:has(+ img), p:has(+ div) { page-break-after: avoid; }
table { border-collapse: collapse; margin: 0 0 8pt 0; width: 100%; font-size: 9.5pt;
        page-break-inside: auto; }
th, td { border: 1px solid #333; padding: 2.5pt 6pt; vertical-align: top;
         text-align: left; }
th { background: #e6e6e6; }
td:empty { height: 17pt; }
.answers td:empty { min-width: 1.5in; }
.grid td:empty { height: 0.32in; }
tr { page-break-inside: avoid; }
ul, ol { margin: 0 0 7pt 0; padding-left: 20pt; }
li { margin-bottom: 3pt; }
.boards { display: flex; gap: 0.2in; justify-content: center; margin: 4pt 0 8pt 0; }
.boards img { width: 2.3in; }
img.board { display: block; margin: 4pt auto 8pt auto; width: 3.1in; }
.position { page-break-inside: avoid; }
.blank { letter-spacing: 0.02em; }
"""

Alignment = list[str | None]  # One CSS text-align per table column, or None


def slug(title: str) -> str:
    """Turn a handout title into the lowercase, underscore-joined part of its file name."""
    words = re.sub(r"[^a-z0-9]+", "_", title.lower())
    return words.strip("_")


def inline_html(text: str) -> str:
    """
    Turn the inline Markdown of one line into HTML.

    Parameters
    ----------
    text : str
        Markdown text with `code`, **bold**, and [links](url) in it.

    Returns
    -------
    str
        The same text as HTML, with the characters HTML reserves escaped.
    """
    # A link prints as its text: paper has nothing to click
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    parts = re.split(r"(`[^`]*`)", text)
    result = ""
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) >= 2:
            # A long code span, such as a FEN, may wrap inside a table cell
            tag = '<code class="long">' if len(part) > LONG_CODE else "<code>"
            result += f"{tag}{html.escape(part[1:-1])}</code>"
            continue
        piece = html.escape(part, quote=False)
        piece = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", piece)
        result += piece
    return result


def image_html(line: str) -> str:
    """
    Turn a line of Markdown images into <img> tags with the SVG files embedded.

    Parameters
    ----------
    line : str
        One or more `![alt](path)` images, with paths relative to handouts.md.

    Returns
    -------
    str
        A single board as `<img class="board">`, or several side by side in a
        `<div class="boards">`.
    """
    tags = []
    for alt, path in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", line):
        image_path = (SOURCE.parent / path).resolve()
        data = base64.b64encode(image_path.read_bytes()).decode("ascii")
        suffix = image_path.suffix.lower().lstrip(".")
        mime = "image/svg+xml" if suffix == "svg" else f"image/{suffix}"
        tags.append(f'<img alt="{html.escape(alt)}" src="data:{mime};base64,{data}">')
    if len(tags) == 1:
        return tags[0].replace("<img ", '<img class="board" ', 1)
    return '<div class="boards">' + "".join(tags) + "</div>"


def table_cells(line: str) -> list[str]:
    """Split one table row on its pipes, ignoring the pipes at both ends."""
    inner = line.strip().removeprefix("|").removesuffix("|")
    return [cell.strip() for cell in inner.split("|")]


def table_alignment(line: str) -> Alignment:
    """Read the `| --- | :---: | ---: |` row and return one text-align per column."""
    alignment: Alignment = []
    for cell in table_cells(line):
        if cell.startswith(":") and cell.endswith(":"):
            alignment.append("center")
        elif cell.endswith(":"):
            alignment.append("right")
        else:
            alignment.append(None)
    return alignment


def table_html(lines: list[str]) -> str:
    """
    Turn the lines of one Markdown table into an HTML table.

    Parameters
    ----------
    lines : list[str]
        The header row, the alignment row, and the body rows.

    Returns
    -------
    str
        The table as HTML. A header row with no text in any cell is left out, so a
        table that only draws boxes (the undo cards) prints without a gray band.
    """
    header = table_cells(lines[0])
    alignment = table_alignment(lines[1])
    rows = []
    for line in lines[2:]:
        cells = table_cells(line)
        while len(cells) < len(header):
            cells.append("")
        rows.append(cells)

    def cell(tag: str, text: str, column: int) -> str:
        align = alignment[column] if column < len(alignment) else None
        style = f' style="text-align: {align}"' if align else ""
        return f"<{tag}{style}>{inline_html(text)}</{tag}>"

    # A table whose body is mostly blank is there to write in, so its blank cells
    # get room; a wide grid such as the hidden peak keeps its cells small
    body_cells = [text for cells in rows for text in cells]
    blanks = sum(1 for text in body_cells if not text)
    mostly_blank = blanks * 2 >= len(body_cells)
    if mostly_blank and len(header) <= 4:
        result = '<table class="answers">'
    elif mostly_blank and len(header) > 6:
        result = '<table class="grid">'
    else:
        result = "<table>"
    if any(header):
        result += "<tr>"
        for column, text in enumerate(header):
            result += cell("th", text, column)
        result += "</tr>"
    for cells in rows:
        result += "<tr>"
        for column, text in enumerate(cells):
            result += cell("td", text, column)
        result += "</tr>"
    return result + "</table>"


def body_html(lines: list[str]) -> str:
    """
    Turn the Markdown lines of one handout, below its heading, into HTML.

    Parameters
    ----------
    lines : list[str]
        The handout's lines without the `## Handout N:` heading.

    Returns
    -------
    str
        The HTML of the handout's body.
    """
    result = ""
    index = 0
    in_position = False  # True while inside a pin hunt position
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
        elif stripped.startswith("```"):
            index += 1
            block = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                block.append(lines[index])
                index += 1
            index += 1
            result += f"<pre><code>{html.escape(chr(10).join(block))}</code></pre>"
        elif stripped.startswith("|"):
            table = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table.append(lines[index])
                index += 1
            result += table_html(table)
        elif stripped.startswith("!["):
            result += image_html(stripped)
            index += 1
        elif stripped.startswith("- "):
            result += "<ul>"
            while index < len(lines) and lines[index].strip().startswith("- "):
                item = lines[index].strip()[2:]
                index += 1
                # A line indented under the item continues it
                while index < len(lines) and lines[index].startswith("  "):
                    item += " " + lines[index].strip()
                    index += 1
                result += f"<li>{inline_html(item)}</li>"
            result += "</ul>"
        elif re.match(r"\d+\. ", stripped):
            result += "<ol>"
            while index < len(lines) and re.match(r"\d+\. ", lines[index].strip()):
                item = re.sub(r"^\d+\. ", "", lines[index].strip())
                index += 1
                while index < len(lines) and lines[index].startswith("   "):
                    item += " " + lines[index].strip()
                    index += 1
                result += f"<li>{inline_html(item)}</li>"
            result += "</ol>"
        elif stripped.startswith("### "):
            result += f"<h2>{inline_html(stripped[4:])}</h2>"
            index += 1
        else:
            paragraph = []
            while index < len(lines) and paragraph_continues(lines[index]):
                paragraph.append(lines[index].strip())
                index += 1
            text = inline_html(" ".join(paragraph))
            # A pin hunt position keeps its label, its board, and its move list
            # together on one page
            if text.startswith("<b>Position "):
                result += close_position(in_position) + '<div class="position">'
                in_position = True
            elif in_position and not text.startswith("Moves offered"):
                result += close_position(in_position)
                in_position = False
            result += f"<p>{text}</p>"
    return result + close_position(in_position)


def close_position(in_position: bool) -> str:
    """Return the closing tag of an open pin hunt position, or nothing."""
    return "</div>" if in_position else ""


def paragraph_continues(line: str) -> bool:
    """Return True if the line belongs to the paragraph above it."""
    stripped = line.strip()
    if not stripped:
        return False
    starts = ("|", "```", "![", "- ", "#")
    is_block_start = stripped.startswith(starts) or re.match(r"\d+\. ", stripped)
    return not is_block_start


def read_handouts() -> list[tuple[int, str, list[str]]]:
    """
    Cut handouts.md into its handouts.

    Returns
    -------
    list[tuple[int, str, list[str]]]
        For each handout, its number, its title, and the Markdown lines of its
        body. The introduction above the first `---` line is left out.
    """
    handouts = []
    sections = SOURCE.read_text(encoding="utf-8").split("\n---\n")
    for section in sections[1:]:
        lines = section.strip("\n").split("\n")
        match = re.match(r"## Handout (\d+): (.+)", lines[0])
        if match is None:
            raise ValueError(
                f"A section of {SOURCE.name} has no handout heading: {lines[0]}"
            )
        handouts.append((int(match.group(1)), match.group(2).strip(), lines[1:]))
    return handouts


def pdf_name(number: int, title: str) -> str:
    """Return the file name of one handout's PDF, such as handout_01_the_board_labeled_both_ways.pdf."""
    return f"handout_{number:02d}_{slug(title)}.pdf"


def page_html(number: int, title: str, lines: list[str]) -> str:
    """Return the complete HTML page of one handout."""
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>Handout {number}: {html.escape(title)}</title>"
        f"<style>{STYLE}</style></head><body>"
        "<header>"
        f"<h1>Handout {number}: {inline_html(title)}</h1>"
        "<div class='course'>Remus</div>"
        "</header>"
        f"{body_html(lines)}"
        "</body></html>"
    )


def find_browser() -> str:
    """
    Find a Chromium-based browser that can print a page to PDF.

    Returns
    -------
    str
        The path of the browser program: the one named by the REMUS_BROWSER
        environment variable, else the first of BROWSER_PATHS that exists, else the
        first of BROWSER_NAMES on the PATH.
    """
    named = os.environ.get(BROWSER_VARIABLE)
    if named:
        return named
    for path in BROWSER_PATHS:
        if Path(path).exists():
            return path
    for name in BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError(
        "No Chromium-based browser found. Install Microsoft Edge or Google Chrome, or set "
        f"the {BROWSER_VARIABLE} environment variable to the browser program's path."
    )


def print_to_pdf(browser: str, html_path: Path, pdf_path: Path) -> None:
    """Ask the browser to print one HTML file to one PDF, with no header or footer."""
    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(command, check=True, capture_output=True, timeout=120)
    if not pdf_path.exists():
        raise RuntimeError(f"{browser} printed nothing to {pdf_path}")


def count_pages(pdf_path: Path) -> int:
    """Count the pages of a PDF by its page objects."""
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf_path.read_bytes()))


def main() -> None:
    handouts = read_handouts()
    browser = find_browser()
    print(f"Reading {SOURCE}")
    print(f"Printing with {browser}")
    OUT.mkdir(exist_ok=True)
    expected = {pdf_name(number, title) for number, title, _ in handouts}
    for stale in sorted(OUT.glob("handout_*.pdf")):
        if stale.name not in expected:
            stale.unlink()
            print(f"Removed {stale.name}: no handout in {SOURCE.name} makes it")
    with tempfile.TemporaryDirectory() as temp_folder:
        for number, title, lines in handouts:
            html_path = Path(temp_folder) / f"handout_{number:02d}.html"
            html_path.write_text(page_html(number, title, lines), encoding="utf-8")
            pdf_path = OUT / pdf_name(number, title)
            print_to_pdf(browser, html_path, pdf_path)
            pages = count_pages(pdf_path)
            page_word = "page" if pages == 1 else "pages"
            print(f"  {pdf_path.relative_to(ROOT)}  ({pages} {page_word})")
    print(f"Wrote {len(handouts)} PDFs to {OUT}")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
