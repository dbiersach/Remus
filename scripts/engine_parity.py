#!/usr/bin/env -S uv run
"""engine_parity.py

Check that every Niram engine thinks exactly like its Remus twin. For each of the
12 versions and each test position, the script compares what the two engines see
and choose:

- the position key, which the opening book and the repetition count use
- the version's own evaluate() of the position
- the legal moves, in the order the generator makes them
- the same moves in the order the search tries them (MVV-LVA)
- the opening book moves (GREEN and GOLD)
- a fixed-depth search: every depth's score, node count, and principal variation,
  and the best move

The positions cover openings and book lines (trap defenses included), middlegames,
tactics, checks, castling, en passant, promotion, endgames, draws by repetition,
the fifty-move rule, insufficient material, mate puzzles, checkmate, and stalemate.

Time never decides how deep a search goes, so the two engines must match exactly.
Rust is about 50 times faster, so Niram chooses the depth: for each version and
position, the deepest search that visits at most --nodes positions. Remus then
repeats that search to the same depth, one position per CPU core.

The book check compares Niram's whole opening book, position by position, with
the books Remus-GREEN and Remus-GOLD load.

Run it from the repository folder:

    uv run scripts/engine_parity.py                 All 12 versions, 25,000 nodes
    uv run scripts/engine_parity.py --nodes 100000  Deeper searches, slower Remus
    uv run scripts/engine_parity.py RED GOLD        Only some versions

The results go to docs/engines/engine_parity.md. The exit code is 1 if anything differs.
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
REMUS_FOLDER = ROOT / "instructor" / "Remus"
NIRAM = ROOT / "Niram"
REPORT_PATH = ROOT / "docs" / "engines" / "engine_parity.md"
DEFAULT_NODES = 25_000  # Remus searches this many positions in about 3 to 8 seconds
FIELDS = ["key", "eval", "legal", "ordered", "book", "info", "nodes", "best"]

# Each case is (name, what it tests, UCI position command). Cases given by moves
# from the start carry their history, which the book and repetition checks need.
CASES = [
    ("start", "Opening", "position startpos"),
    ("after-e4", "Opening", "position startpos moves e2e4"),
    ("italian", "Opening, in book", "position startpos moves e2e4 e7e5 g1f3 b8c6 f1c4"),
    (
        "najdorf",
        "Opening, in book",
        "position startpos moves e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6",
    ),
    (
        "queens-gambit",
        "Opening, in book",
        "position startpos moves d2d4 d7d5 c2c4 e7e6 b1c3 g8f6",
    ),
    (
        "kings-indian",
        "Opening, in book",
        "position startpos moves d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6",
    ),
    ("grob", "Opening, out of book", "position startpos moves g2g4 e7e5 f1g2 d7d5"),
    (
        "scholars-trap",
        "Trap line, Black defends",
        "position startpos moves e2e4 e7e5 f1c4 b8c6 d1h5",
    ),
    (
        "blackburne-shilling",
        "Trap line, White defends",
        "position startpos moves e2e4 e7e5 g1f3 b8c6 f1c4 c6d4",
    ),
    (
        "trap-attacker",
        "Trap line, attacker's turn",
        "position startpos moves e2e4 e7e5 g1f3 b8c6 f1c4",
    ),
    (
        "giuoco-middlegame",
        "Middlegame",
        "position fen r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2PP1N2/PP3PPP/RNBQ1RK1 w - - 0 7",
    ),
    (
        "kiwipete",
        "Middlegame, castling, en passant",
        "position fen r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    ),
    (
        "pinned-bishops",
        "Middlegame, pins",
        "position fen r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
    ),
    (
        "wac-001",
        "Tactic",
        "position fen 2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - - 0 1",
    ),
    (
        "wac-002",
        "Tactic, Black",
        "position fen 8/7p/5k2/5p2/p1p2P2/Pr1pPK2/1P1R3P/8 b - - 0 1",
    ),
    (
        "wac-003",
        "Tactic",
        "position fen 5rk1/1ppb3p/p1pb4/6q1/3P1p1r/2P1R2P/PP1BQ1P1/5RKN w - - 0 1",
    ),
    (
        "wac-004",
        "Tactic, sacrifice",
        "position fen r1bq2rk/pp3pbp/2p1p1pQ/7P/3P4/2PB1N2/PP3PPR/2KR4 w - - 0 1",
    ),
    (
        "wac-005",
        "Tactic, Black",
        "position fen 5k2/6pp/p1qN4/1p1p4/3P4/2PKP2Q/PP3r2/3R4 b - - 0 1",
    ),
    ("in-check", "Check", "position fen 4k3/8/8/8/8/8/4q3/R3K3 w Q - 0 1"),
    (
        "double-check",
        "Double check",
        "position fen 4k3/8/8/8/1b6/5n2/8/R3K2R w KQ - 0 1",
    ),
    ("castle-both", "Castling", "position fen r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"),
    (
        "castle-through-check",
        "Castling across an attacked square",
        "position fen r3k2r/8/8/8/8/8/5r2/R3K2R w KQkq - 0 1",
    ),
    (
        "castle-b-file",
        "Castling with b1 attacked",
        "position fen r3k2r/8/8/8/8/8/1r6/R3K2R w KQkq - 0 1",
    ),
    ("en-passant", "En passant", "position startpos moves e2e4 d7d5 e4e5 f7f5"),
    (
        "en-passant-pinned",
        "En passant that exposes the king",
        "position fen 8/8/8/K2pP2r/8/8/8/7k w - d6 0 1",
    ),
    ("promotion", "Promotion", "position fen 8/P7/8/8/8/8/6k1/4K3 w - - 0 1"),
    (
        "promotion-capture",
        "Promotion by capture",
        "position fen 1n2k3/P7/8/8/8/8/8/4K3 w - - 0 1",
    ),
    (
        "black-promotion",
        "Promotion, Black",
        "position fen 4k3/8/8/8/8/8/p7/4K3 b - - 0 1",
    ),
    (
        "underpromotion",
        "Knight promotion with check",
        "position fen 8/4P1k1/8/8/8/8/2q5/K7 w - - 0 1",
    ),
    ("king-and-pawn", "Endgame", "position fen 8/5k2/8/3K4/8/8/4P3/8 w - - 0 1"),
    (
        "rook-ending",
        "Endgame",
        "position fen 2r3k1/pp3ppp/8/3p4/3P4/8/PP3PPP/2R3K1 w - - 0 1",
    ),
    ("lucena", "Endgame", "position fen 1K1k4/1P6/8/8/8/8/r7/2R5 w - - 0 1"),
    ("philidor", "Endgame, Black", "position fen 3k4/8/8/3PK3/r7/8/8/7R b - - 0 1"),
    ("queen-vs-pawns", "Endgame", "position fen 4k3/8/4p3/3p4/8/8/3Q4/4K3 w - - 0 1"),
    ("pawn-race", "Endgame", "position fen 8/5ppp/8/8/8/8/PPP5/k6K w - - 0 1"),
    (
        "king-queen-king",
        "Mating with the queen",
        "position fen 8/8/8/4k3/8/8/8/3QK3 w - - 0 1",
    ),
    (
        "king-rook-king",
        "Mating with the rook",
        "position fen 8/8/8/4k3/8/8/8/R3K3 w - - 0 1",
    ),
    (
        "bishop-knight",
        "Mating with bishop and knight",
        "position fen 8/8/8/4k3/8/8/8/2B1KN2 w - - 0 1",
    ),
    ("back-rank", "Mate in one", "position fen 6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1"),
    (
        "mate-001",
        "Mate in two",
        "position fen 8/2pR2p1/2B2p2/KPk5/2p2r1r/2p2bQ1/8/8 w - - 0 1",
    ),
    (
        "mate-005",
        "Mate in two",
        "position fen 5B2/2p3p1/3n1k2/7Q/2B3P1/6P1/7K/8 w - - 0 1",
    ),
    (
        "mate-007",
        "Mate in two",
        "position fen 8/4Q3/2N5/2pp4/5p2/1p1k1p2/1P3P2/3K4 w - - 0 1",
    ),
    (
        "mate-008",
        "Mate in three",
        "position fen 6n1/1p2p3/4Q2p/4Np1p/4k1pP/4B3/3P4/4K2n w - - 0 1",
    ),
    (
        "repetition",
        "Threefold repetition one move away",
        "position startpos moves g1f3 g8f6 f3g1 f6g8 g1f3 g8f6 f3g1",
    ),
    (
        "repetition-ahead",
        "Repetition while ahead",
        "position fen 6k1/5pp1/7p/8/8/8/1Q3PPP/6K1 w - - 0 1 moves b2b8 g8h7 b8b1 h7g8 b1b8 g8h7 b8b1",
    ),
    (
        "fifty-moves",
        "Fifty-move rule near",
        "position fen 8/8/4k3/8/8/3R4/8/4K3 w - - 99 120",
    ),
    (
        "knight-only",
        "Insufficient material",
        "position fen 8/8/4k3/8/8/3N4/8/4K3 w - - 0 1",
    ),
    (
        "checkmated",
        "Checkmate on the board",
        "position startpos moves f2f3 e7e5 g2g4 d8h4",
    ),
    (
        "stalemated",
        "Stalemate on the board",
        "position fen 7k/5Q2/6K1/8/8/8/8/8 b - - 0 1",
    ),
]


def version_folders() -> list[Path]:
    """Return the 12 Remus version folders, 00 WHITE to 11 GOLD."""
    folders = []
    for folder in sorted(REMUS_FOLDER.iterdir()):
        if folder.is_dir() and " - " in folder.name:
            folders.append(folder)
    return folders


def color_of(folder: Path) -> str:
    """Return the color in a folder name: "10 RED - Transposition table" gives "RED"."""
    return folder.name.split(" - ")[0].split()[1]


def niram_program(color: str) -> Path:
    """Return the Niram program of a color, such as Niram/target/release/niram-red."""
    name = "niram-" + color.lower()
    if sys.platform == "win32":
        name += ".exe"
    return NIRAM / "target" / "release" / name


def read_results(text: str) -> dict[str, dict[str, list[str]]]:
    """Read parity output into {case name: {field: [values]}}."""
    results = {}
    current = None
    for line in text.splitlines():
        field, _, value = line.partition("\t")
        if field == "case":
            current = {}
            for name in FIELDS:
                current[name] = []
            results[value] = current
        elif current is not None and field in current:
            current[field].append(value)
        elif field == "depth" and current is not None:
            current["depth"] = [value]
    return results


def run_niram(color: str, cases_path: Path, nodes: int) -> str:
    """Run one Niram program's parity command and return its output."""
    program = niram_program(color)
    command = [str(program), "parity", str(cases_path), str(nodes)]
    return subprocess.run(command, capture_output=True, text=True, check=True).stdout


# The Remus side runs in worker processes. Every version folder holds modules with
# the same names (search.py, evaluation.py, ...), so a worker forgets the modules
# of one folder before it imports those of the next.
loaded_folder = None
loaded = {}


def load_version(folder: Path) -> dict:
    """Import one Remus version's modules into this worker and return them."""
    global loaded_folder
    if loaded_folder == folder:
        return loaded
    if loaded_folder is not None:
        sys.path.remove(str(loaded_folder))
        for name, module in list(sys.modules.items()):
            path = getattr(module, "__file__", None)
            if path is not None and Path(path).parent == loaded_folder:
                del sys.modules[name]
    sys.path.insert(0, str(folder))
    loaded.clear()

    import evaluation
    import game_state
    import legal_moves
    import move_ordering
    import moves
    import search
    import uci_engine

    # think() makes its own SearchInfo, so a SearchInfo that remembers itself lets
    # the worker read the number of positions think() visited
    searches = []

    class RecordingInfo(search.SearchInfo):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            searches.append(self)

    search.SearchInfo = RecordingInfo
    loaded.update(
        evaluate=evaluation.evaluate,
        position_key=game_state.position_key,
        legal_moves=legal_moves.legal_moves,
        order_moves=move_ordering.order_moves,
        move_to_uci=moves.move_to_uci,
        think=search.think,
        set_position=uci_engine.set_position,
        searches=searches,
        book={},
    )
    if (folder / "opening_book.py").exists():
        import opening_book

        loaded["book"] = opening_book.load_book(folder / "opening_book.txt")
    loaded_folder = folder
    return loaded


def moves_text(remus: dict, moves: list) -> str:
    """Return moves as UCI text separated by spaces."""
    text = ""
    for move in moves:
        if text:
            text += " "
        text += remus["move_to_uci"](move)
    return text


def run_remus(job: tuple[Path, str, str, int]) -> tuple[str, str, dict, float]:
    """Repeat one Niram parity case with a Remus version and return its fields."""
    folder, name, command, depth = job
    remus = load_version(folder)
    start = time.perf_counter()
    state = remus["set_position"](command.split())
    moves = remus["legal_moves"](state)
    key = remus["position_key"](state)
    result = {
        "key": [key],
        "eval": [str(remus["evaluate"](state))],
        "legal": [moves_text(remus, moves)],
        "ordered": [moves_text(remus, remus["order_moves"](moves, state["board"]))],
        "book": [moves_text(remus, remus["book"].get(key, []))],
        "depth": [str(depth)],
        "info": [],
        "nodes": [],
        "best": ["0000"],
    }
    if depth > 0:
        lines = result["info"]
        best = remus["think"](state, 1_000_000.0, depth, report=lines.append)
        result["nodes"] = [str(remus["searches"][-1].nodes)]
        result["best"] = [remus["move_to_uci"](best)]
    return color_of(folder), name, result, time.perf_counter() - start


def remus_book_lines(folder: Path) -> list[str]:
    """Return a Remus version's opening book as "key<TAB>moves" lines in key order."""
    remus = load_version(folder)
    lines = []
    for key in sorted(remus["book"]):
        lines.append(key + "\t" + moves_text(remus, remus["book"][key]))
    return lines


def first_difference(niram: dict, remus: dict) -> str | None:
    """Return a description of the first field that differs, or None if all match."""
    for field in ["depth"] + FIELDS:
        theirs = niram.get(field, [])
        ours = remus.get(field, [])
        if theirs != ours:
            for index in range(max(len(theirs), len(ours))):
                left = theirs[index] if index < len(theirs) else "(missing)"
                right = ours[index] if index < len(ours) else "(missing)"
                if left != right:
                    return f"{field}: Niram {left!r}, Remus {right!r}"
    return None


def main():
    parser = argparse.ArgumentParser(description="Check that Niram matches Remus")
    parser.add_argument("colors", nargs="*", help="versions to check (default: all)")
    parser.add_argument("--nodes", type=int, default=DEFAULT_NODES)
    parser.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    parser.add_argument("--no-build", action="store_true", help="skip cargo build")
    arguments = parser.parse_args()

    wanted = []
    for color in arguments.colors:
        wanted.append(color.upper())
    folders = []
    for folder in version_folders():
        if not wanted or color_of(folder) in wanted:
            folders.append(folder)
    if not arguments.no_build:
        print("Building Niram (cargo build --release)")
        subprocess.run(
            ["cargo", "build", "--release", "--quiet"], cwd=NIRAM, check=True
        )

    start = time.perf_counter()
    niram_results = {}
    with tempfile.TemporaryDirectory() as scratch:
        cases_path = Path(scratch) / "cases.txt"
        text = ""
        for name, _, command in CASES:
            text += name + "\t" + command + "\n"
        cases_path.write_text(text)
        for folder in folders:
            color = color_of(folder)
            niram_results[color] = read_results(
                run_niram(color, cases_path, arguments.nodes)
            )
    niram_seconds = time.perf_counter() - start
    print(
        f"Niram finished {len(folders) * len(CASES)} searches in {niram_seconds:.1f} s"
    )

    # The longest Remus searches start first, so no core sits idle at the end
    jobs = []
    for folder in folders:
        for name, _, command in CASES:
            niram = niram_results[color_of(folder)][name]
            nodes = int(niram["nodes"][0]) if niram["nodes"] else 0
            jobs.append((nodes, (folder, name, command, int(niram["depth"][0]))))
    jobs.sort(reverse=True)
    print(f"Remus repeats them on {arguments.workers} cores")

    mismatches = []
    remus_seconds = {}
    with ProcessPoolExecutor(max_workers=arguments.workers) as pool:
        work = [job for _, job in jobs]
        for done, (color, name, result, seconds) in enumerate(
            pool.map(run_remus, work), 1
        ):
            remus_seconds[color] = remus_seconds.get(color, 0.0) + seconds
            difference = first_difference(niram_results[color][name], result)
            if difference is not None:
                mismatches.append((color, name, difference))
                print(f"  MISMATCH {color} {name}: {difference}")
            if done % 50 == 0:
                print(f"  {done} of {len(work)} Remus searches done")

    book_rows = []
    niram_book = subprocess.run(
        [str(niram_program("GOLD")), "book"], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    for folder in version_folders():
        if (folder / "opening_book.py").exists():
            with ProcessPoolExecutor(max_workers=1) as pool:
                lines = pool.submit(remus_book_lines, folder).result()
            moves = 0
            for line in lines:
                moves += len(line.split("\t")[1].split())
            same_file = (folder / "opening_book.txt").read_bytes() == (
                NIRAM / "opening_book.txt"
            ).read_bytes()
            book_rows.append(
                (color_of(folder), len(lines), moves, lines == niram_book, same_file)
            )
            if lines != niram_book or not same_file:
                mismatches.append((color_of(folder), "opening book", "book differs"))
    elapsed = time.perf_counter() - start
    write_report(
        folders, niram_results, remus_seconds, mismatches, book_rows, arguments, elapsed
    )
    print(f"{len(mismatches)} differences; results written to {REPORT_PATH}")
    print(f"Total run time (sec): {elapsed:.3f}")
    sys.exit(1 if mismatches else 0)


def write_report(
    folders, niram_results, remus_seconds, mismatches, book_rows, arguments, elapsed
):
    """Write docs/engines/engine_parity.md with one row per version and one per position."""
    colors = [color_of(folder) for folder in folders]
    text = "# Engine parity: Remus and Niram\n\n"
    text += (
        "`scripts/engine_parity.py` checks that each Niram engine thinks exactly like "
        "the Remus version of the same color. For every position below, both engines "
        "report the position key, the version's evaluation, the legal moves in "
        "generation order and in search order, the book moves, and a search with no "
        "clock: each depth's score, node count, and principal variation, and the best "
        "move. Niram picks the depth, the deepest search that visits at most "
        f"{arguments.nodes:,} positions, and Remus repeats that search. Any difference "
        "in any field counts as a mismatch.\n\n"
    )
    text += (
        f"Last run: {date.today().isoformat()}, {len(colors)} versions, "
        f"{len(CASES)} positions, {len(colors) * len(CASES)} searches, "
        f"{len(mismatches)} mismatches, {elapsed / 60:.1f} minutes on "
        f"{arguments.workers} cores.\n\n"
    )
    command = "uv run scripts/engine_parity.py"
    if arguments.nodes != DEFAULT_NODES:
        command += f" --nodes {arguments.nodes}"
    text += f"Run it again with `{command}` from the repository folder.\n\n"
    text += "## Versions\n\n"
    text += "| Version | Positions matched | Positions searched | Deepest search | Remus time (s) |\n"
    text += "| --- | ---: | ---: | ---: | ---: |\n"
    for color in colors:
        bad = 0
        for mismatch in mismatches:
            if mismatch[0] == color:
                bad += 1
        nodes = 0
        deepest = 0
        for name, _, _ in CASES:
            result = niram_results[color][name]
            if result["nodes"]:
                nodes += int(result["nodes"][0])
            deepest = max(deepest, int(result["depth"][0]))
        text += (
            f"| {color} | {len(CASES) - bad} of {len(CASES)} | {nodes:,} | {deepest} | "
            f"{remus_seconds.get(color, 0.0):,.0f} |\n"
        )
    text += "\n## Opening book\n\n"
    text += (
        "Niram reads `Niram/opening_book.txt`; the check compares every position and "
        "move of its book, in order, with the book each Remus version loads.\n\n"
    )
    text += "| Version | Positions | Moves | Same as Niram's book | Same file |\n"
    text += "| --- | ---: | ---: | --- | --- |\n"
    for color, positions, moves, same_book, same_file in book_rows:
        text += f"| {color} | {positions} | {moves} | {'yes' if same_book else 'NO'} | {'yes' if same_file else 'NO'} |\n"
    text += "\n## Positions\n\n"
    text += "The depth column gives the depth each version searched, WHITE first.\n\n"
    text += "| Position | What it tests | Depths |\n| --- | --- | --- |\n"
    for name, purpose, _ in CASES:
        depths = ""
        for color in colors:
            if depths:
                depths += " "
            depths += niram_results[color][name]["depth"][0]
        text += f"| {name} | {purpose} | {depths} |\n"
    if mismatches:
        text += "\n## Mismatches\n\n| Version | Position | First difference |\n| --- | --- | --- |\n"
        for color, name, difference in mismatches:
            text += f"| {color} | {name} | `{difference}` |\n"
    REPORT_PATH.write_text(text)


if __name__ == "__main__":
    main()
