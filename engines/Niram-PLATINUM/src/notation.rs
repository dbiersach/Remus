//! notation.rs
//!
//! Write and read moves in Standard Algebraic Notation (SAN), the notation people
//! use: "e4", "Nf3", "Bxh8", "O-O", "e8=Q+", "Nbd2". Reading SAN uses a simple
//! idea: write the SAN of every legal move, and pick the one that matches.

use crate::attacks::in_check;
use crate::board::{EMPTY, file_letter, piece_at, rank_digit, square_name};
use crate::game_state::State;
use crate::legal_moves::legal_moves;
use crate::make_move::{make_move, undo_move};
use crate::moves::Move;

/// Return the SAN text of a legal move, with "+" for check and "#" for checkmate.
pub fn move_to_san(state: &mut State, mv: Move) -> String {
    let piece = piece_at(&state.board, mv.from_square);
    let kind = piece.to_ascii_uppercase();
    let target = square_name(mv.to_square.0, mv.to_square.1);
    let is_capture =
        piece_at(&state.board, mv.to_square) != EMPTY || (kind == 'P' && Some(mv.to_square) == state.en_passant);

    let mut text = String::new();
    if kind == 'K' && (mv.to_square.1 - mv.from_square.1).abs() == 2 {
        text += if mv.to_square.1 == 6 { "O-O" } else { "O-O-O" };
    } else if kind == 'P' {
        if is_capture {
            text.push(file_letter(mv.from_square.1));
            text.push('x');
        }
        text += &target;
        if let Some(promotion) = mv.promotion {
            text.push('=');
            text.push(promotion.to_ascii_uppercase());
        }
    } else {
        text.push(kind);
        text += &disambiguation(state, mv, piece);
        if is_capture {
            text.push('x');
        }
        text += &target;
    }

    let undo = make_move(state, mv);
    if in_check(state, state.turn) {
        if legal_moves(state).is_empty() {
            text.push('#');
        } else {
            text.push('+');
        }
    }
    undo_move(state, undo);
    text
}

/// Return the file, rank, or square that tells this move apart from another legal
/// move by the same kind of piece to the same square, such as "b" in "Nbd2".
fn disambiguation(state: &mut State, mv: Move, piece: char) -> String {
    // A rival is another piece of the same kind that can reach the same square
    let mut rivals = Vec::new();
    for other in legal_moves(state) {
        let same_target = other.to_square == mv.to_square;
        let same_start = other.from_square == mv.from_square;
        let same_piece = piece_at(&state.board, other.from_square) == piece;
        if same_target && same_piece && !same_start {
            rivals.push(other.from_square);
        }
    }
    if rivals.is_empty() {
        return String::new();
    }
    let (row, col) = mv.from_square;
    let mut file_is_unique = true;
    let mut rank_is_unique = true;
    for (rival_row, rival_col) in rivals {
        if rival_col == col {
            file_is_unique = false;
        }
        if rival_row == row {
            rank_is_unique = false;
        }
    }
    if file_is_unique {
        return file_letter(col).to_string();
    }
    if rank_is_unique {
        return rank_digit(row).to_string();
    }
    square_name(row, col)
}

/// Find the legal move that a SAN text describes, such as "Nf3", "exd5", or "O-O".
/// A trailing "+", "#", "!", or "?" is ignored, and "0-0" is accepted for "O-O".
pub fn parse_san(state: &mut State, text: &str) -> Result<Move, String> {
    let wanted = text.trim().trim_end_matches(['+', '#', '!', '?']).replace('0', "O");
    for mv in legal_moves(state) {
        if move_to_san(state, mv).trim_end_matches(['+', '#']) == wanted {
            return Ok(mv);
        }
    }
    Err(format!("Not a legal move here: {text:?}"))
}
