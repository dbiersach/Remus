#!/usr/bin/env -S uv run
"""make_white_map.py

Map the Python files of Remus-WHITE across the course. The script writes two things
into misc/students/remus_program_overview.md:

1. An import diagram, misc/students/images/code/remus_white_imports.svg: one box per
   engine file, with an arrow from each file to every file that imports it.
2. A table with one row per engine file (the files a game loads) and one column per
   day and period, which marks the period where the file appears and the periods
   where student pairs edit it.

The table comes from the Day folders: each period's instructor folder and its
"Day_NN_Period_NN_Goals.md" file. The script lays out the diagram itself: each
file sits in a row one below the lowest file that imports it, the rows are ordered to
keep crossings few, and every arrow runs straight down or bends at right angles,
leaving and reaching a box at its own spot on the edge. Run it from the top Remus
folder with `uv run misc/designer/make_white_map.py` after `make_student_folders.py`.
"""

import ast
import random
import re
import textwrap
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder
WHITE = ROOT / "engines" / "instructor" / "00 Remus-WHITE - No enhancements"
OVERVIEW = ROOT / "misc" / "students" / "remus_program_overview.md"
IMAGE = ROOT / "misc" / "students" / "images" / "code" / "remus_white_imports.svg"
HEADING = "## Remus-WHITE across the course"  # The section this script rewrites

# The program Lucas Chess and every match start: the diagram shows this file and
# every file it imports, directly or through another file, and nothing else
ENGINE_START = "uci_engine"

# Day 9 periods 2 and 3: each student pair edits these files in its own enhanced
# engine folder, a copy of Remus-WHITE in engines/student
ENHANCED_FILES = ("evaluation.py", "move_ordering.py", "search.py")

BOX_HEIGHT = 34  # Pixels tall for each file's box
BOX_MIN_WIDTH = 150  # Pixels wide for a file's box with few arrows
PORT_GAP = 16  # Pixels between two arrows that leave or reach one side of a box
LANE_WIDTH = 16  # Pixels wide for an arrow passing a row of boxes
NODE_GAP = 26  # Pixels between two boxes in a row
TRACK_GAP = 9  # Pixels between two horizontal arrow segments in one channel
MARGIN = 20  # Pixels of white space around the drawing
# One color per importing file, so the eye can follow each file's arrows
ARROW_COLORS = (
    "#1f6fb4",
    "#c2551b",
    "#2e8b57",
    "#8e44ad",
    "#b8860b",
    "#c0392b",
    "#16808a",
    "#6b5b3e",
    "#d6338a",
    "#4b5d9c",
)


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
    """Return every (importer, imported) pair of the modules a game of chess loads."""
    modules = set()
    for name in white_files():
        modules.add(name[:-3])
    # Follow the imports from uci_engine.py, so tests, demos, and match runners,
    # which no game loads, stay out of the diagram
    engine = set()
    waiting = [ENGINE_START]
    while waiting:
        module = waiting.pop()
        if module not in engine:
            engine.add(module)
            waiting.extend(imports_of(module + ".py", modules))
    edges = []
    for module in sorted(engine):
        for imported in sorted(imports_of(module + ".py", modules)):
            edges.append((module, imported))
    return edges


def layers_of(nodes, edges):
    """Return each file's row: 0 for files that import nothing, one more per level."""
    layer = {}

    def depth(node):
        if node not in layer:
            below = [depth(v) for (u, v) in edges if u == node]
            layer[node] = 1 + max(below) if below else 0
        return layer[node]

    for node in nodes:
        depth(node)
    # Move each file to the row that makes its arrows shortest
    for _ in range(20):
        for node in nodes:
            below = [layer[v] for (u, v) in edges if u == node]
            above = [layer[u] for (u, v) in edges if v == node]
            low = max(below) + 1 if below else 0
            high = min(above) - 1 if above else max(layer.values())
            if not below:
                continue
            best = layer[node]
            best_cost = None
            for row in range(low, high + 1):
                cost = sum(row - b for b in below) + sum(a - row for a in above)
                if (
                    best_cost is None
                    or cost < best_cost
                    or (cost == best_cost and row == layer[node])
                ):
                    best, best_cost = row, cost
            layer[node] = best
    return layer


def split_edges(edges, layer):
    """Return the chain of points (real files and pass-through lanes) of each arrow."""
    chains = []
    for u, v in edges:
        chain = [u]
        for row in range(layer[u] - 1, layer[v], -1):
            chain.append(("lane", u, v, row))
        chain.append(v)
        chains.append(chain)
    return chains


def crossings(upper, lower, links):
    """Count the crossings between two neighboring rows."""
    up = {n: i for i, n in enumerate(upper)}
    low = {n: i for i, n in enumerate(lower)}
    pairs = sorted((up[a], low[b]) for a, b in links if a in up and b in low)
    count = 0
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            if pairs[i][0] != pairs[j][0] and pairs[i][1] > pairs[j][1]:
                count += 1
    return count


def order_rows(rows, links, seed=2016, restarts=12, sweeps=16):
    """Order the boxes of every row to keep crossing arrows few."""
    rng = random.Random(seed)
    down = {}
    upn = {}
    for a, b in links:
        down.setdefault(a, []).append(b)
        upn.setdefault(b, []).append(a)
    tops = sorted(rows)[::-1]

    def total(order):
        return sum(
            crossings(order[tops[i]], order[tops[i + 1]], links)
            for i in range(len(tops) - 1)
        )

    best, best_count = None, None
    for attempt in range(restarts):
        order = {r: list(rows[r]) for r in rows}
        if attempt:
            for row in order.values():
                rng.shuffle(row)
        for sweep in range(sweeps):
            sequence = tops[1:] if sweep % 2 == 0 else tops[::-1][1:]
            for r in sequence:
                other = r + 1 if sweep % 2 == 0 else r - 1
                pos = {n: i for i, n in enumerate(order[other])}
                neighbors = upn if sweep % 2 == 0 else down
                keyed = []
                for i, n in enumerate(order[r]):
                    near = [pos[m] for m in neighbors.get(n, []) if m in pos]
                    keyed.append((sum(near) / len(near) if near else i, i, n))
                keyed.sort()
                order[r] = [n for _, _, n in keyed]
            # Swap neighbors when the swap removes crossings
            for r in tops:
                improved = True
                while improved:
                    improved = False
                    for i in range(len(order[r]) - 1):
                        before = total_near(order, r, links, tops)
                        order[r][i], order[r][i + 1] = order[r][i + 1], order[r][i]
                        if total_near(order, r, links, tops) < before:
                            improved = True
                        else:
                            order[r][i], order[r][i + 1] = order[r][i + 1], order[r][i]
            count = total(order)
            if best_count is None or count < best_count:
                best, best_count = {r: list(order[r]) for r in order}, count
    return best, best_count


def total_near(order, r, links, tops):
    """Count the crossings next to one row."""
    count = 0
    if r + 1 in order:
        count += crossings(order[r + 1], order[r], links)
    if r - 1 in order:
        count += crossings(order[r], order[r - 1], links)
    return count


def text_width(text):
    """Return the rough width in pixels of a file name in the boxes' font."""
    return 8.0 * len(text)


def layout_svg(edges):
    """Return the rows, the x of every box and lane, and the links between rows."""
    nodes = sorted({n for e in edges for n in e})
    layer = layers_of(nodes, edges)
    chains = split_edges(edges, layer)
    rows = {}
    for n in nodes:
        rows.setdefault(layer[n], []).append(n)
    links = []
    for chain in chains:
        for a, b in pairwise(chain):
            if isinstance(a, tuple):
                rows.setdefault(a[3], [])
                if a not in rows[a[3]]:
                    rows[a[3]].append(a)
            links.append((a, b))
    order, count = order_rows(rows, links)

    # Ports: how many arrows touch the top and the bottom of each box
    out_count = {}
    in_count = {}
    for a, b in links:
        out_count[a] = out_count.get(a, 0) + 1
        in_count[b] = in_count.get(b, 0) + 1

    def width(n):
        if isinstance(n, tuple):
            return LANE_WIDTH
        ports = max(out_count.get(n, 0), in_count.get(n, 0))
        return max(BOX_MIN_WIDTH, text_width(f"{n}.py") + 30, ports * PORT_GAP + 20)

    # Place boxes: start packed, then pull each toward its neighbors
    x = {}
    for r in order:
        cursor = 0.0
        for n in order[r]:
            x[n] = cursor + width(n) / 2
            cursor += width(n) + NODE_GAP
    neighbors = {}
    for a, b in links:
        neighbors.setdefault(a, []).append(b)
        neighbors.setdefault(b, []).append(a)
    tops = sorted(order)[::-1]
    for step in range(400):
        sequence = tops if step % 2 == 0 else tops[::-1]
        for r in sequence:
            row = order[r]
            desired = []
            for n in row:
                total, weight = 0.0, 0.0
                for m in neighbors.get(n, []):
                    w = 1.0
                    if isinstance(n, tuple) and isinstance(m, tuple):
                        w = 12.0
                    elif isinstance(n, tuple) or isinstance(m, tuple):
                        w = 3.0
                    total += w * x[m]
                    weight += w
                desired.append(total / weight if weight else x[n])
            placed = place_row(row, desired, width)
            for n, value in zip(row, placed):
                x[n] = value
    # Snap the lanes of each long arrow onto one straight line where the rows allow
    chains = {}
    for r in order:
        for n in order[r]:
            if isinstance(n, tuple):
                chains.setdefault((n[1], n[2]), []).append(n)
    for _ in range(6):
        for lanes in chains.values():
            values = sorted(x[n] for n in lanes)
            target = values[len(values) // 2]
            for n in lanes:
                row = order[n[3]]
                i = row.index(n)
                low = (
                    -1e9
                    if i == 0
                    else x[row[i - 1]] + width(row[i - 1]) / 2 + NODE_GAP + width(n) / 2
                )
                high = (
                    1e9
                    if i == len(row) - 1
                    else x[row[i + 1]] - width(row[i + 1]) / 2 - NODE_GAP - width(n) / 2
                )
                x[n] = min(max(target, low), high)
    # A lane that sits within a few pixels of the lane above it lines up with it
    for lanes in chains.values():
        lanes.sort(key=lambda n: -n[3])
        for above, below in pairwise(lanes):
            if abs(x[above] - x[below]) < 8:
                x[below] = x[above]
    left = min(x[n] - width(n) / 2 for n in x)
    for n in x:
        x[n] += MARGIN - left
    return order, x, width, links, layer, count


def place_row(row, desired, width):
    """Return x positions closest to the desired ones that keep the row's order."""
    # Pool adjacent violators: blocks of boxes pushed together share one offset
    blocks = []
    for i, n in enumerate(row):
        blocks.append([i, i, desired[i], 1])
        while len(blocks) > 1:
            a, b = blocks[-2], blocks[-1]
            a_end = offset_x(a, desired, row, width)
            b_start = offset_x(b, desired, row, width)
            if b_start[0] >= a_end[1] + NODE_GAP:
                break
            merged = [a[0], b[1], 0, 0]
            blocks.pop()
            blocks[-1] = merged
    positions = []
    for block in blocks:
        start, end = block[0], block[1]
        # Offsets of each box from the block's first box
        offsets = [0.0]
        for i in range(start + 1, end + 1):
            offsets.append(
                offsets[-1] + width(row[i - 1]) / 2 + NODE_GAP + width(row[i]) / 2
            )
        weights = [lane_weight(row[i]) for i in range(start, end + 1)]
        shift = sum(
            weights[i - start] * (desired[i] - offsets[i - start])
            for i in range(start, end + 1)
        )
        shift /= sum(weights)
        for i in range(start, end + 1):
            positions.append(shift + offsets[i - start])
    return positions


def offset_x(block, desired, row, width):
    """Return the left and right edges of a block placed at its best shift."""
    start, end = block[0], block[1]
    offsets = [0.0]
    for i in range(start + 1, end + 1):
        offsets.append(
            offsets[-1] + width(row[i - 1]) / 2 + NODE_GAP + width(row[i]) / 2
        )
    weights = [lane_weight(row[i]) for i in range(start, end + 1)]
    shift = sum(
        weights[i - start] * (desired[i] - offsets[i - start])
        for i in range(start, end + 1)
    )
    shift /= sum(weights)
    return (shift - width(row[start]) / 2, shift + offsets[-1] + width(row[end]) / 2)


def ports(order, x, links):
    """Return where each link leaves its upper box and enters its lower box."""
    leave = {}
    enter = {}
    outgoing = {}
    incoming = {}
    for link in links:
        outgoing.setdefault(link[0], []).append(link)
        incoming.setdefault(link[1], []).append(link)
    for node, group in outgoing.items():
        group.sort(key=lambda link: (x[link[1]], str(link[1])))
        spread(node, group, x, leave)
    for node, group in incoming.items():
        group.sort(key=lambda link: (x[link[0]], str(link[0])))
        spread(node, group, x, enter)
    return leave, enter


def spread(node, group, x, result):
    """Space the arrows of one box side PORT_GAP apart, centered on the box."""
    if isinstance(node, tuple):
        for link in group:
            result[link] = x[node]
        return
    k = len(group)
    for i, link in enumerate(group):
        result[link] = x[node] + (i - (k - 1) / 2) * PORT_GAP


def assign_tracks(segments):
    """Give each bending segment in one channel a track, top track 0."""
    bends = [s for s in segments if abs(s[1] - s[2]) > 0.5]
    above = {s[0]: set() for s in bends}  # s must sit above these

    def overlap(s, t):
        lo1, hi1 = sorted((s[1], s[2]))
        lo2, hi2 = sorted((t[1], t[2]))
        return lo1 <= hi2 + 4 and lo2 <= hi1 + 4

    def inside(value, s):
        lo, hi = sorted((s[1], s[2]))
        return lo - 0.5 <= value <= hi + 0.5

    def reaches(a, b):
        seen, stack = set(), [a]
        while stack:
            n = stack.pop()
            if n == b:
                return True
            if n not in seen:
                seen.add(n)
                stack.extend(above[n])
        return False

    pairs = []
    for i, s in enumerate(bends):
        for t in bends[i + 1 :]:
            if overlap(s, t):
                # Crossings when s sits above t, and when t sits above s
                s_over = inside(t[1], s) + inside(s[2], t)
                t_over = inside(s[1], t) + inside(t[2], s)
                pairs.append((abs(s_over - t_over), s, t, s_over <= t_over))
    pairs.sort(key=lambda p: -p[0])
    for _, s, t, s_first in pairs:
        a, b = (s, t) if s_first else (t, s)
        if not reaches(b[0], a[0]):
            above[a[0]].add(b[0])
        else:
            above[b[0]].add(a[0])
    track = {}

    def depth(n):
        if n not in track:
            track[n] = 0
            parents = [m for m in above if n in above[m]]
            track[n] = 1 + max(depth(m) for m in parents) if parents else 0
        return track[n]

    for s in bends:
        depth(s[0])
    return track


def draw(edges, path):
    """Draw the diagram into an SVG file and return its count of lane crossings."""
    order, x, width, links, layer, count = layout_svg(edges)
    leave, enter = ports(order, x, links)
    tops = sorted(order)[::-1]
    channel_tracks = {}
    for r in tops:
        segments = []
        for link in links:
            row_of = link[0][3] if isinstance(link[0], tuple) else layer[link[0]]
            if row_of == r:
                segments.append((link, leave[link], enter[link]))
        channel_tracks[r] = assign_tracks(segments)
    y = {}
    cursor = MARGIN
    track_y = {}
    for r in tops:
        y[r] = cursor
        cursor += BOX_HEIGHT
        tracks = channel_tracks[r]
        n_tracks = 1 + max(tracks.values()) if tracks else 0
        channel = max(40, (n_tracks + 1) * TRACK_GAP + 16)
        for link, t in tracks.items():
            track_y[link] = cursor + 8 + (t + 1) * TRACK_GAP
        cursor += channel
    height = cursor - 40 + MARGIN
    right = max(x[n] + width(n) / 2 for n in x) + MARGIN
    sources = sorted({e[0] for e in edges}, key=lambda n: (-layer[n], x[n]))
    color_of = {n: ARROW_COLORS[i % len(ARROW_COLORS)] for i, n in enumerate(sources)}
    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {right:.0f} {height:.0f}" width="{right:.0f}" '
            f'height="{height:.0f}" font-family="Helvetica, Arial, sans-serif">'
        ),
        f'<rect width="{right:.0f}" height="{height:.0f}" fill="white"/>',
    ]
    for color in ARROW_COLORS:
        parts.append(
            f'<marker id="head{color[1:]}" viewBox="0 0 10 10" refX="10" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
        )
    for u, v in edges:
        chain = [u]
        for row in range(layer[u] - 1, layer[v], -1):
            chain.append(("lane", u, v, row))
        chain.append(v)
        points = []
        for a, b in pairwise(chain):
            link = (a, b)
            r = a[3] if isinstance(a, tuple) else layer[a]
            x1, x2 = leave[link], enter[link]
            y1 = y[r] + BOX_HEIGHT
            y2 = y[r - 1]
            if isinstance(a, tuple):
                points.append((x1, y[r]))
            points.append((x1, y1))
            if link in track_y:
                points.append((x1, track_y[link]))
                points.append((x2, track_y[link]))
            points.append((x2, y2))
        color = color_of[u]
        parts.append(
            f'<path d="{rounded(points)}" fill="none" stroke="{color}" '
            f'stroke-width="1.6" marker-start="url(#head{color[1:]})"/>'
        )
    for r in order:
        for n in order[r]:
            if isinstance(n, tuple):
                continue
            w = width(n)
            parts.append(
                f'<rect x="{x[n] - w / 2:.1f}" y="{y[r]}" width="{w:.1f}" '
                f'height="{BOX_HEIGHT}" rx="9" fill="#eef3fb" stroke="#33415c" '
                'stroke-width="1.4"/>'
            )
            parts.append(
                f'<text x="{x[n]:.1f}" y="{y[r] + BOX_HEIGHT / 2 + 5}" '
                f'text-anchor="middle" font-size="15" fill="#1b2433">{n}.py</text>'
            )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")
    return count


def rounded(points, radius=5):
    """Return an SVG path through the points with small rounded corners."""
    clean = [points[0]]
    for p in points[1:]:
        if abs(p[0] - clean[-1][0]) > 0.01 or abs(p[1] - clean[-1][1]) > 0.01:
            clean.append(p)
    # Drop points in the middle of a straight run
    simple = [clean[0]]
    for i in range(1, len(clean) - 1):
        a, b, c = simple[-1], clean[i], clean[i + 1]
        if (abs(a[0] - b[0]) < 0.01 and abs(b[0] - c[0]) < 0.01) or (
            abs(a[1] - b[1]) < 0.01 and abs(b[1] - c[1]) < 0.01
        ):
            continue
        simple.append(b)
    simple.append(clean[-1])
    d = f"M{simple[0][0]:.1f},{simple[0][1]:.1f}"
    for i in range(1, len(simple) - 1):
        a, b, c = simple[i - 1], simple[i], simple[i + 1]
        r1 = min(radius, dist(a, b) / 2)
        r2 = min(radius, dist(b, c) / 2)
        p1 = toward(b, a, r1)
        p2 = toward(b, c, r2)
        d += f" L{p1[0]:.1f},{p1[1]:.1f} Q{b[0]:.1f},{b[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    d += f" L{simple[-1][0]:.1f},{simple[-1][1]:.1f}"
    return d


def dist(a, b):
    """Return the distance between two points on one straight run."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def toward(b, a, r):
    """Return the point r pixels from b toward a."""
    length = dist(a, b)
    if length == 0:
        return b
    return (b[0] + (a[0] - b[0]) * r / length, b[1] + (a[1] - b[1]) * r / length)


def lane_weight(node):
    """Lanes weigh more, so a long arrow keeps one straight line."""
    return 6.0 if isinstance(node, tuple) else 1.0


def draw_diagram(edges: list[tuple[str, str]]):
    """Draw the import diagram as an SVG picture."""
    crossing_count = draw(edges, IMAGE)
    print(f"Drew {len(edges)} imports in {IMAGE}, {crossing_count} crossings")


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
            text = goals_text(period_folder)
            new = bullet_list(text, "New files this period:")
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
                if enhanced and name in ENHANCED_FILES and "E" not in mark:
                    mark += "E"
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
    drawn = {name for edge in edges for name in edge}
    diagram_count = len(drawn)
    others = []
    for name in files:
        if name[:-3] not in drawn and not name.startswith("test_"):
            others.append(f"`{name}`")
    left_out = ", ".join(others[:-1]) + ", and " + others[-1]
    board_arrows = 0
    for _, imported in edges:
        if imported == "board":
            board_arrows += 1
    text = f"{HEADING}\n\n"
    text += paragraph(
        "Remus-WHITE is the finished Day 9 Remus, in "
        "`engines/instructor/00 Remus-WHITE - No enhancements`. "
        f"It holds {len(files)} Python files."
    )
    text += "### Which file imports which\n\n"
    text += paragraph(
        f"The diagram shows the {diagram_count} files that a game of chess runs: "
        "`uci_engine.py`, the program that Lucas Chess and every match start, and "
        "every file it imports, directly or through another file. An arrow points from a file to each file "
        "that imports it: `evaluation.py` points at `search.py` because "
        "`search.py` calls `evaluate()`. A two-headed arrow would mean two files "
        "import each other; no two Remus files do. Every arrow points up the "
        "page, from the code that is used to the code that uses it. "
        "`uci_engine.py` sits at the top, because no file imports it, and each "
        "file sits one row below "
        "the lowest file that imports it. `board.py` imports no Remus file and "
        "almost every file imports it, so it sits alone in the bottom row, where "
        f"its {board_arrows} arrows leave side by side along its top edge. Every arrow runs "
        "straight up or bends at right angles, leaves and reaches a box at its "
        "own spot, and takes the color of the file it points at, so the eye can "
        "follow the arrows that gather at one file. The test files and "
        f"{left_out} are left out: they check Remus or run its matches, and no "
        "game loads them."
    )
    text += (
        "![Import diagram of Remus-WHITE](images/code/remus_white_imports.svg)\n\n"
    )
    text += "### When each engine file appears and changes\n\n"
    text += paragraph(
        "The table follows the same files as the diagram, the ones a game of chess "
        "loads. Each row is one file, in the order the class meets it. Each column "
        "is a period that brings a new engine file or has the student pairs edit "
        "one; D07 P2 means Day 7, period 2. N marks the period the file first "
        "appears, and E marks a period when the student pairs write code in it. "
        "On Day 9, periods 2 and 3, each student pair edits its own enhanced "
        "engine's copy of the file in `engines/student`. Between those periods the "
        "student pairs type nothing in the file: any other code it gains is "
        "already written in that period's folder when the student pairs open it."
    )
    engine_files = []
    for name in files:
        if name[:-3] in drawn:
            engine_files.append(name)
    text += table_text(engine_files) + "\n"
    return text


def write_section(section: str):
    """Put the section into the overview page, before "The three boundaries"."""
    text = OVERVIEW.read_text()
    if HEADING in text:
        start = text.index(HEADING)
        end = text.index("\n## ", start) + 1
        text = text[:start] + section + text[end:]
    else:
        anchor = text.index("## The three boundaries")
        text = text[:anchor] + section + text[anchor:]
    OVERVIEW.write_text(text)
    print(f"Wrote the Remus-WHITE section of {OVERVIEW}")


def main():
    files = white_files()
    edges = import_edges()
    draw_diagram(edges)
    write_section(section_text(files, edges))
    print(f"Mapped {len(files)} Remus-WHITE files  (expected 25)")


if __name__ == "__main__":
    main()
