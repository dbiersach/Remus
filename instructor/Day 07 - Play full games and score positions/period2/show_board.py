#!/usr/bin/env -S uv run
"""show_board.py

Draw a Remus board as a picture and open it in the web browser, with an arrow for
each move a move generator returns.

The python-chess library draws the picture. Remus itself never imports this file
or python-chess: the engine keeps its own board, and this file only copies that
board into python-chess to draw it.
"""

import webbrowser
from pathlib import Path

import chess
import chess.svg
from board import EMPTY, new_board
from game_state import WHITE
from move_generation import knight_moves
from moves import Move

PICTURE_PATH = Path(__file__).parent / "board.svg"  # The picture, beside this file


def to_python_chess(board: list[list[str]]) -> chess.Board:
    """
    Copy a Remus board into a python-chess board, which knows how to draw itself.

    Parameters
    ----------
    board : list[list[str]]
        The Remus board, row 0 first (rank 8).

    Returns
    -------
    chess.Board
        A python-chess board with the same pieces on the same squares.
    """
    picture_board = chess.Board(None)  # None means an empty board
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != EMPTY:
                # Row 0 is rank 8, but python-chess counts ranks from rank 1 at 0
                square = chess.square(col, 7 - row)
                picture_board.set_piece_at(square, chess.Piece.from_symbol(piece))
    return picture_board


def show_board(
    board: list[list[str]], arrows: list | None = None, file_path: Path = PICTURE_PATH
) -> Path:
    """
    Save a picture of the board and open it in the web browser.

    Parameters
    ----------
    board : list[list[str]]
        The Remus board to draw.
    arrows : list | None
        Arrows to draw on top of the board, or None for no arrows.
    file_path : Path
        Where to save the picture.

    Returns
    -------
    Path
        The path of the saved picture.
    """
    picture = chess.svg.board(to_python_chess(board), arrows=arrows or [], size=480)
    file_path.write_text(picture)
    webbrowser.open(file_path.as_uri())
    return file_path


def python_chess_square(square: tuple[int, int]) -> int:
    """Return the python-chess number of a Remus (row, col) square."""
    row, col = square
    return chess.square(col, 7 - row)  # Row 0 is rank 8; python-chess rank 0 is rank 1


def show_moves(board: list[list[str]], moves: list[Move]) -> Path:
    """
    Draw the board with one arrow per move, from where the piece starts to where
    it lands.

    Parameters
    ----------
    board : list[list[str]]
        The Remus board to draw.
    moves : list[Move]
        The moves to draw as arrows.

    Returns
    -------
    Path
        The path of the saved picture.
    """
    arrows = []
    for move in moves:
        tail = python_chess_square(move.from_square)
        head = python_chess_square(move.to_square)
        arrows.append(chess.svg.Arrow(tail, head))
    return show_board(board, arrows)


def main():
    board = new_board()
    # Try your own: a rook on d4 of an empty board shows 14 arrows
    moves = knight_moves(board, (7, 1), WHITE) + knight_moves(board, (7, 6), WHITE)
    file_path = show_moves(board, moves)
    print(f"Saved the start board with {len(moves)} knight moves to {file_path}")
    print("  (expected 4 arrows: b1 to a3 and c3, g1 to f3 and h3)")


if __name__ == "__main__":
    main()
