//! attacks.rs
//!
//! Decide whether a square is attacked, and whether a king is in check. The test
//! stands on the square and looks outward like a "super piece": along the lines
//! for rooks, bishops, and queens, and at the knight, pawn, and king squares nearby.

use crate::board::{Board, EMPTY, Square, piece_at};
use crate::game_state::{BLACK, State, WHITE, color_of};
use crate::move_generation::{BISHOP_DIRECTIONS, KING_STEPS, KNIGHT_JUMPS, ROOK_DIRECTIONS, on_board};

/// Return true if a knight of by_color is one knight jump away.
fn attacked_by_knight(board: &Board, square: Square, by_color: char) -> bool {
    let knight = if by_color == WHITE { 'N' } else { 'n' };
    for (row_change, col_change) in KNIGHT_JUMPS {
        let target = (square.0 + row_change, square.1 + col_change);
        if on_board(target.0, target.1) && piece_at(board, target) == knight {
            return true;
        }
    }
    false
}

/// Return true if the king of by_color is one step away.
fn attacked_by_king(board: &Board, square: Square, by_color: char) -> bool {
    let king = if by_color == WHITE { 'K' } else { 'k' };
    for (row_change, col_change) in KING_STEPS {
        let target = (square.0 + row_change, square.1 + col_change);
        if on_board(target.0, target.1) && piece_at(board, target) == king {
            return true;
        }
    }
    false
}

/// Return true if a pawn of by_color attacks the square. White pawns capture toward
/// row 0, so a White pawn that attacks (row, col) stands one row below it.
fn attacked_by_pawn(board: &Board, square: Square, by_color: char) -> bool {
    let pawn = if by_color == WHITE { 'P' } else { 'p' };
    let behind = if by_color == WHITE { 1 } else { -1 };
    for col_change in [-1, 1] {
        let target = (square.0 + behind, square.1 + col_change);
        if on_board(target.0, target.1) && piece_at(board, target) == pawn {
            return true;
        }
    }
    false
}

/// Return the first piece met walking from the square in a direction, or EMPTY.
fn first_piece(board: &Board, square: Square, direction: Square) -> char {
    let (row_change, col_change) = direction;
    let (mut row, mut col) = (square.0 + row_change, square.1 + col_change);
    while on_board(row, col) {
        if piece_at(board, (row, col)) != EMPTY {
            return piece_at(board, (row, col));
        }
        row += row_change;
        col += col_change;
    }
    EMPTY
}

/// Return true if a rook, bishop, or queen of by_color attacks along a line.
fn attacked_along_lines(board: &Board, square: Square, by_color: char) -> bool {
    for direction in ROOK_DIRECTIONS {
        let piece = first_piece(board, square, direction);
        if color_of(piece) == Some(by_color) && "RQ".contains(piece.to_ascii_uppercase()) {
            return true;
        }
    }
    for direction in BISHOP_DIRECTIONS {
        let piece = first_piece(board, square, direction);
        if color_of(piece) == Some(by_color) && "BQ".contains(piece.to_ascii_uppercase()) {
            return true;
        }
    }
    false
}

/// Look outward from the square for any attacker of by_color.
pub fn is_square_attacked(board: &Board, square: Square, by_color: char) -> bool {
    attacked_by_knight(board, square, by_color)
        || attacked_by_pawn(board, square, by_color)
        || attacked_by_king(board, square, by_color)
        || attacked_along_lines(board, square, by_color)
}

/// Return the (row, col) of the king of the given color.
pub fn find_king(board: &Board, color: char) -> Square {
    let king = if color == WHITE { 'K' } else { 'k' };
    for row in 0..8 {
        for col in 0..8 {
            if board[row as usize][col as usize] == king {
                return (row, col);
            }
        }
    }
    panic!("No {king} on the board");
}

/// Return true if the king of the given color is attacked.
pub fn in_check(state: &State, color: char) -> bool {
    let enemy = if color == WHITE { BLACK } else { WHITE };
    is_square_attacked(&state.board, find_king(&state.board, color), enemy)
}
