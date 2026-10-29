#!/usr/bin/env -S uv run
"""make_board_diagrams.py

Draw the chess board diagrams that the enhanced engine READMEs show beside their examples.

A course designer tool, like the other make_*.py scripts. Each diagram in DIAGRAMS
names a position in FEN, the arrows to draw, and the squares to color. The script
draws each one with python-chess's chess.svg, with the files a to h and the ranks
1 to 8 on the edges, and saves it as an SVG file in misc/docs/images/boards/. The
README text in period_guides.py links each picture with board_image(). VS Code's
Markdown preview and GitHub both show SVG pictures, and python-chess is already in
the dev dependency group, so `uv run misc/scripts/make_board_diagrams.py` needs
nothing else.
"""

from pathlib import Path

import chess
import chess.svg

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder, above misc/scripts/
OUT = ROOT / "misc" / "docs" / "images" / "boards"
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
}


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
    return chess.svg.board(board, size=SIZE, coordinates=True, arrows=arrows, fill=fill)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, spec in DIAGRAMS.items():
        file_path = OUT / f"{name}.svg"
        file_path.write_text(draw(spec), encoding="utf-8")
        print(f"Saved {file_path}")
    print(f"Diagrams drawn: {len(DIAGRAMS)}  (expected 9)")


if __name__ == "__main__":
    main()
