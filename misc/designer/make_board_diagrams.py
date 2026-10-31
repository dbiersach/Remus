#!/usr/bin/env -S uv run
"""make_board_diagrams.py

Draw the chess board diagrams that the READMEs and code pages show beside their examples.

A course designer tool, like the other make_*.py scripts. Each diagram in DIAGRAMS
names a position in FEN, the arrows to draw, and the squares to color. The script
draws each one with python-chess's chess.svg, with the files a to h and the ranks
1 to 8 on the edges, and saves it as an SVG file in misc/students/images/boards/. A
diagram marked "row_col" also prints Remus's column numbers along the top and its
row numbers down the right side, so a reader sees that row 0 is rank 8. The README
text in period_guides.py links each picture with board_image(), and the pages in
misc/students/engine_code/ link them by hand. VS Code's
Markdown preview and GitHub both show SVG pictures, and python-chess is already in
the dev dependency group, so `uv run misc/designer/make_board_diagrams.py` needs
nothing else.
"""

import re
from pathlib import Path

import chess
import chess.svg

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder, above misc/designer/
OUT = ROOT / "misc" / "students" / "images" / "boards"
SIZE = 300  # Width and height of each diagram in pixels

# Arrow colors: green for a move played, red for a threat or a check, blue for Black
GOOD = "#15781BB0"
THREAT = "#882020B0"
BLACK_MOVE = "#003088B0"

# Square colors, half transparent so the square's own shade shows through
SHIELD = "#2E9E3F80"  # A shield pawn or a square that counts
HOLE = "#D0302080"  # A weak square or a missing shield pawn
MARK = "#E0B00080"  # A square the text names
KING_STEP = "#3060C080"  # A square the checked king steps to
REACH = "#2E9E3F80"  # A square a piece can move to
LOOK = "#3060C060"  # A square the attack test looks at

ROW_COL_COLOR = "#F0C040"  # Remus's row and column numbers, apart from a-h and 1-8

# One entry per diagram: the file name, the FEN, the arrows, and the colored squares.
# Arrows are (from, to, color) and squares are (square, color), with square names.
DIAGRAMS = {
    # GRAY: White's three shield pawns in front of the castled king
    "gray_shield_full": {
        "fen": "r1bq1rk1/pp2bppp/2n1pn2/3p4/3P4/2NBPN2/PP3PPP/R2Q1RK1 w - - 0 9",
        "arrows": [],
        "fill": [("f2", SHIELD), ("g2", SHIELD), ("h2", SHIELD)],
    },
    # GRAY: the h-pawn has gone to h4, so h2 and h3 hold no shield pawn
    "gray_shield_broken": {
        "fen": "r1bq1rk1/pp2bppp/2n1pn2/3p4/3P3P/2NBPN2/PP3PP1/R2Q1RK1 b - - 0 9",
        "arrows": [("h2", "h4", THREAT)],
        "fill": [("f2", SHIELD), ("g2", SHIELD), ("h2", HOLE), ("h3", HOLE)],
    },
    # RED: 1. Nf3 Nf6 2. d4 and 1. d4 Nf6 2. Nf3 reach the same position
    "red_transposition": {
        "fen": "rnbqkb1r/pppppppp/5n2/8/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 0 2",
        "arrows": [("g1", "f3", GOOD), ("d2", "d4", GOOD), ("g8", "f6", BLACK_MOVE)],
        "fill": [],
    },
    # GREEN: the seven replies the book holds after 1. e4
    "green_book_replies": {
        "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
        "arrows": [("e2", "e4", GOOD)],
        "fill": [
            ("e5", MARK),
            ("c5", MARK),
            ("e6", MARK),
            ("c6", MARK),
            ("d5", MARK),
            ("d6", MARK),
            ("f6", MARK),
        ],
    },
    # BLUE: the quiet move Qh5 threatens mate on f7
    "blue_killer_qh5": {
        "fen": "r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 3 3",
        "arrows": [("h5", "f7", THREAT), ("c4", "f7", THREAT)],
        "fill": [("f7", HOLE)],
    },
    # YELLOW: White is a rook behind but checks forever with Qg5+ and Qf6+
    "yellow_perpetual": {
        "fen": "1q3rk1/ppp2p1p/8/8/8/4Q3/PP3PPP/6K1 w - - 0 1",
        "arrows": [("e3", "g5", THREAT)],
        "fill": [("g5", HOLE), ("f6", HOLE), ("g8", KING_STEP), ("h8", KING_STEP)],
    },
    # PURPLE: doubled c-pawns and an isolated e-pawn
    "purple_pawns": {
        "fen": "4k3/8/3p4/4p3/4P3/2P5/2P5/4K3 w - - 0 1",
        "arrows": [],
        "fill": [("c2", MARK), ("c3", MARK), ("e4", HOLE)],
    },
    # CYAN: the losing king in the center earns a small bonus
    "cyan_king_center": {
        "fen": "8/8/8/4k3/8/8/2K5/7R w - - 0 1",
        "arrows": [],
        "fill": [("d4", MARK), ("e4", MARK), ("d5", MARK), ("e5", MARK)],
    },
    # CYAN: the losing king on the edge, with the winning king close, earns more
    "cyan_king_edge": {
        "fen": "4k3/8/4K3/8/8/8/8/7R w - - 0 1",
        "arrows": [],
        "fill": [("d4", MARK), ("e4", MARK), ("d5", MARK), ("e5", MARK)],
    },
    # board.md: Remus's (row, col) numbers beside the square names
    "board_row_col": {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "arrows": [],
        "fill": [("e2", MARK)],
        "row_col": True,
    },
    # moves.md: the move e2 to e4 is Move((6, 4), (4, 4))
    "moves_e2e4": {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "arrows": [("e2", "e4", GOOD)],
        "fill": [],
        "row_col": True,
    },
    # Day 3: a knight in the middle reaches 8 squares
    "jump_knight_d4": {
        "fen": "8/8/8/8/3N4/8/8/8 w - - 0 1",
        "arrows": [],
        "fill": [
            ("b3", REACH),
            ("b5", REACH),
            ("c2", REACH),
            ("c6", REACH),
            ("e2", REACH),
            ("e6", REACH),
            ("f3", REACH),
            ("f5", REACH),
        ],
        "size": 240,
    },
    # Day 3: a knight in the corner keeps only 2 of its 8 jumps
    "jump_knight_a1": {
        "fen": "8/8/8/8/8/8/8/N7 w - - 0 1",
        "arrows": [],
        "fill": [("b3", REACH), ("c2", REACH)],
        "size": 240,
    },
    # Day 3: a king in the corner keeps only 3 of its 8 steps
    "jump_king_a1": {
        "fen": "8/8/8/8/8/8/8/K7 w - - 0 1",
        "arrows": [],
        "fill": [("a2", REACH), ("b2", REACH), ("b1", REACH)],
        "size": 240,
    },
    # Day 3: a rook slides until the edge or a piece stops it
    "slide_rook": {
        "fen": "8/8/3P4/8/3R1n2/8/8/8 w - - 0 1",
        "arrows": [
            ("d4", "d5", GOOD),
            ("d4", "d1", GOOD),
            ("d4", "a4", GOOD),
            ("d4", "f4", THREAT),
        ],
        "fill": [("d6", MARK), ("f4", HOLE)],
    },
    # Day 4: a knight attacks e5 from the squares a knight on e5 could jump to
    "attack_knight_e5": {
        "fen": "8/8/8/8/8/5n2/8/8 w - - 0 1",
        "arrows": [("f3", "e5", THREAT)],
        "fill": [
            ("e5", MARK),
            ("c4", LOOK),
            ("c6", LOOK),
            ("d3", LOOK),
            ("d7", LOOK),
            ("f3", LOOK),
            ("f7", LOOK),
            ("g4", LOOK),
            ("g6", LOOK),
        ],
    },
    # Day 4: a pawn moves straight but attacks diagonally
    "attack_pawn": {
        "fen": "8/8/8/8/4P3/8/8/8 w - - 0 1",
        "arrows": [("e4", "e5", GOOD), ("e4", "d5", THREAT), ("e4", "f5", THREAT)],
        "fill": [("d5", HOLE), ("f5", HOLE)],
    },
    # Day 4: a rook on e8 checks the king on e1
    "pin_check": {
        "fen": "k3r3/8/8/8/8/8/8/4K3 w - - 0 1",
        "arrows": [("e8", "e1", THREAT)],
        "fill": [],
    },
    # Day 4: a knight on e2 blocks the check, so it is pinned
    "pin_knight": {
        "fen": "k3r3/8/8/8/8/8/4N3/4K3 w - - 0 1",
        "arrows": [("e8", "e2", THREAT)],
        "fill": [("e2", HOLE)],
    },
    # Day 5: the six home squares that hold the castling rights
    "castling_rights": {
        "fen": "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
        "arrows": [("h1", "h5", GOOD)],
        "fill": [
            ("a1", MARK),
            ("e1", MARK),
            ("h1", HOLE),
            ("a8", MARK),
            ("e8", MARK),
            ("h8", MARK),
        ],
    },
    # Day 5: exd6 en passant lands on d6 and removes the pawn on d5
    "en_passant": {
        "fen": "4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 2",
        "arrows": [("e5", "d6", GOOD)],
        "fill": [("d6", MARK), ("d5", HOLE)],
    },
    # Day 5: the promotion puzzle, where only a knight wins
    "promotion_puzzle": {
        "fen": "8/1P6/kBK5/8/8/8/8/8 w - - 0 1",
        "arrows": [("b7", "b8", GOOD)],
        "fill": [("b8", MARK)],
    },
}


def add_row_col(svg: str) -> str:
    """
    Swap the top and right square labels for Remus's column and row numbers.

    chess.svg prints a to h along the top and bottom and 1 to 8 down both sides
    of a 390 by 390 picture with a 15-pixel border. The top labels sit at
    y = 1 and the right labels at x = 375, so those two sets are removed and
    the numbers 0 to 7 are written in their place: columns left to right, and
    rows top to bottom, because row 0 is rank 8.
    """
    label = r'<g transform="translate\(({}), ({})\) scale\(0\.75, 0\.75\)"[^>]*>.*?</g>'
    svg = re.sub(label.format(r"\d+", "1"), "", svg, flags=re.DOTALL)
    svg = re.sub(label.format("375", r"\d+"), "", svg, flags=re.DOTALL)
    numbers = ""
    for i in range(8):
        middle = 15 + 45 * i + 22.5  # Center of square i along the edge
        numbers += (
            f'<text x="{middle}" y="12" font-size="12" font-weight="bold" '
            f'font-family="sans-serif" text-anchor="middle" '
            f'fill="{ROW_COL_COLOR}">{i}</text>'
            f'<text x="382.5" y="{middle + 4}" font-size="12" font-weight="bold" '
            f'font-family="sans-serif" text-anchor="middle" '
            f'fill="{ROW_COL_COLOR}">{i}</text>'
        )
    return svg.replace("</svg>", numbers + "</svg>")


def draw(spec: dict) -> str:
    """Return the SVG text of one diagram."""
    board = chess.Board(spec["fen"])
    arrows = []
    for start, end, color in spec["arrows"]:
        arrow = chess.svg.Arrow(
            chess.parse_square(start), chess.parse_square(end), color=color
        )
        arrows.append(arrow)
    fill = {}
    for square, color in spec["fill"]:
        fill[chess.parse_square(square)] = color
    svg = chess.svg.board(
        board,
        size=spec.get("size", SIZE),
        coordinates=True,
        arrows=arrows,
        fill=fill,
    )
    if spec.get("row_col"):
        svg = add_row_col(svg)
    return svg


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, spec in DIAGRAMS.items():
        file_path = OUT / f"{name}.svg"
        file_path.write_text(draw(spec), encoding="utf-8")
        print(f"Saved {file_path}")
    print(f"Diagrams drawn: {len(DIAGRAMS)}  (expected 22)")


if __name__ == "__main__":
    main()
