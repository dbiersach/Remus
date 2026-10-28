#!/usr/bin/env -S uv run
"""make_move.py

Make a move on the game state, and undo it exactly. make_move returns an undo
record that holds everything the move changed, so undo_move can put it all back.

Three moves change more than two squares: castling also moves a rook, en passant
removes a pawn that is not on the landing square, and promotion swaps the pawn for
a new piece.
"""

from board import EMPTY, Square, piece_at, print_board, set_piece
from game_state import BLACK, new_game, opponent
from moves import Move, move_from_uci

CASTLING_SQUARES = {  # A move from or to one of these squares removes these rights
    (7, 4): "KQ",  # e1, the White king
    (7, 7): "K",  # h1, White's kingside rook
    (7, 0): "Q",  # a1, White's queenside rook
    (0, 4): "kq",  # e8, the Black king
    (0, 7): "k",  # h8, Black's kingside rook
    (0, 0): "q",  # a8, Black's queenside rook
}


def update_castling_rights(rights: str, move: Move) -> str:
    """
    Return the castling rights left after a move.

    Parameters
    ----------
    rights : str
        The rights before the move, such as "KQkq".
    move : Move
        The move. A king or rook leaving its home square loses the right, and so
        does a rook captured on its home square.

    Returns
    -------
    str
        The rights after the move, such as "Qkq" after the h1 rook moves.
    """
    for square in (move.from_square, move.to_square):
        for letter in CASTLING_SQUARES.get(square, ""):
            rights = rights.replace(letter, "")
    return rights


def en_passant_victim_square(move: Move) -> Square:
    """Return the square of the pawn an en passant capture removes.

    The captured pawn stands beside the capturing pawn: on the row the capture
    starts from, in the column it lands in.
    """
    return move.from_square[0], move.to_square[1]


def castling_rook_move(move: Move) -> tuple[Square, Square]:
    """Return the (from, to) squares of the rook in a castling move."""
    row = move.from_square[0]
    if move.to_square[1] == 6:  # Kingside: the rook goes from the h-file to the f-file
        return (row, 7), (row, 5)
    return (row, 0), (row, 3)  # Queenside: the rook goes from the a-file to the d-file


def make_move(state: dict, move: Move) -> dict:
    """
    Make any move, including castling, en passant, and promotion, and return the
    record needed to undo it.

    Parameters
    ----------
    state : dict
        The game state. It changes in place.
    move : Move
        The move to make. It must be a move the side to move may play.

    Returns
    -------
    dict
        The undo record: the move, the piece that moved, the piece it captured,
        and the old values of every state field the move changes.
    """
    board = state["board"]
    piece = piece_at(board, move.from_square)
    captured = piece_at(board, move.to_square)
    undo = {
        "move": move,
        "piece": piece,
        "captured": captured,
        "castling": state["castling"],
        "en_passant": state["en_passant"],
        "halfmove_clock": state["halfmove_clock"],
        "fullmove_number": state["fullmove_number"],
        "rook_move": None,
        "en_passant_victim": None,
    }

    # En passant: a pawn moves diagonally onto the empty en passant target square
    is_pawn = piece.upper() == "P"
    if is_pawn and move.to_square == state["en_passant"]:
        victim = en_passant_victim_square(move)
        undo["en_passant_victim"] = victim
        undo["captured"] = piece_at(board, victim)

    # Promotion: the pawn becomes the new piece on the last rank
    landing_piece = piece if move.promotion is None else move.promotion
    set_piece(board, move.to_square, landing_piece)
    set_piece(board, move.from_square, EMPTY)

    # Castling: a king moving two squares also moves its rook
    if piece.upper() == "K" and abs(move.to_square[1] - move.from_square[1]) == 2:
        rook_from, rook_to = castling_rook_move(move)
        set_piece(board, rook_to, piece_at(board, rook_from))
        set_piece(board, rook_from, EMPTY)
        undo["rook_move"] = (rook_from, rook_to)

    # The fifty-move clock restarts after a capture or a pawn move
    if undo["captured"] != EMPTY or is_pawn:
        state["halfmove_clock"] = 0
    else:
        state["halfmove_clock"] += 1
    if state["turn"] == BLACK:
        state["fullmove_number"] += 1

    # A double step leaves an en passant target on the square the pawn skipped
    state["en_passant"] = None
    if is_pawn and abs(move.to_square[0] - move.from_square[0]) == 2:
        skipped_row = (move.from_square[0] + move.to_square[0]) // 2
        state["en_passant"] = (skipped_row, move.from_square[1])
    state["castling"] = update_castling_rights(state["castling"], move)
    state["turn"] = opponent(state["turn"])
    return undo


def undo_move(state: dict, undo: dict) -> None:
    """
    Take back the move described by an undo record.

    Parameters
    ----------
    state : dict
        The game state, as make_move left it. It changes in place.
    undo : dict
        The record make_move returned for this move.
    """
    board = state["board"]
    move = undo["move"]
    set_piece(board, move.from_square, undo["piece"])
    if undo["en_passant_victim"] is None:
        set_piece(board, move.to_square, undo["captured"])
    else:
        set_piece(board, move.to_square, EMPTY)
        set_piece(board, undo["en_passant_victim"], undo["captured"])
    if undo["rook_move"] is not None:
        rook_from, rook_to = undo["rook_move"]
        set_piece(board, rook_from, piece_at(board, rook_to))
        set_piece(board, rook_to, EMPTY)
    state["turn"] = opponent(state["turn"])
    state["castling"] = undo["castling"]
    state["en_passant"] = undo["en_passant"]
    state["halfmove_clock"] = undo["halfmove_clock"]
    state["fullmove_number"] = undo["fullmove_number"]


def state_snapshot(state: dict) -> str:
    """Return the whole state as text, so two states can be compared with ==."""
    text = ""
    for row in state["board"]:
        for piece in row:
            text += piece
        text += "/"
    text += f" {state['turn']} {state['castling']} {state['en_passant']}"
    text += f" {state['halfmove_clock']} {state['fullmove_number']}"
    return text


def main():
    state = new_game()
    start = state_snapshot(state)
    texts = ["e2e4", "g8f6", "e4e5", "d7d5", "e5d6", "c8g4", "f1e2", "b8c6"]
    texts += ["g1f3", "d8d7", "e1g1", "e8c8", "d6c7", "a7a6", "c7d8n"]
    undo_records = []
    for text in texts:
        undo_records.append(make_move(state, move_from_uci(text)))
    print_board(state["board"])
    for undo in reversed(undo_records):
        undo_move(state, undo)
    same = state_snapshot(state) == start
    print(
        f"Fifteen moves (en passant, both castlings, a knight promotion) made and undone, back at the start: {same}  (expected True)"
    )


if __name__ == "__main__":
    main()
