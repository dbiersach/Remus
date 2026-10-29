//! game_state.rs
//!
//! Hold everything about a game that the board alone does not show: whose turn it
//! is, which castling moves are still allowed, the en passant target, the move
//! clocks, and the history of positions that the repetition rule needs.

use crate::board::{Board, EMPTY, Square};

pub const WHITE: char = 'w'; // White's color, as FEN writes it
pub const BLACK: char = 'b'; // Black's color

/// The whole game state, the same fields as Remus's state dict.
#[derive(Clone, Debug)]
pub struct State {
    pub board: Board,
    pub turn: char,                 // 'w' or 'b', the side to move
    pub castling: String,           // The castling moves still allowed, "KQkq" at the start
    pub en_passant: Option<Square>, // The square a pawn just skipped over, or None
    pub halfmove_clock: u32,        // Moves since the last capture or pawn move
    pub fullmove_number: u32,       // Starts at 1 and grows after each Black move
    pub history: Vec<String>,       // The position_key of every position so far, this one last
}

/// Return true if the piece is White (an uppercase letter).
pub fn is_white(piece: char) -> bool {
    piece.is_ascii_uppercase()
}

/// Return Some('w') or Some('b') for a piece, or None for an empty square.
pub fn color_of(piece: char) -> Option<char> {
    if piece == EMPTY {
        return None;
    }
    if is_white(piece) {
        return Some(WHITE);
    }
    Some(BLACK)
}

/// Return the other side's color.
pub fn opponent(color: char) -> char {
    if color == WHITE {
        return BLACK;
    }
    WHITE
}

/// Return text that is the same for two positions exactly when the repetition rule
/// treats them as the same position: the pieces, the side to move, the castling
/// rights, and the en passant square, but only when a pawn of the side to move
/// stands beside the pawn that just made a double step. The clocks are left out.
pub fn position_key(state: &State) -> String {
    let board = &state.board;
    let mut key = String::with_capacity(90);
    for row in 0..8 {
        if row > 0 {
            key.push('/'); // A slash separates one rank from the next
        }
        for col in 0..8 {
            key.push(board[row][col]);
        }
    }
    key.push(' ');
    key.push(state.turn);
    key.push(' ');
    key += &state.castling;
    if let Some(target) = state.en_passant {
        let pawn = if state.turn == WHITE { 'P' } else { 'p' };
        let row = target.0 + if state.turn == WHITE { 1 } else { -1 };
        for col in [target.1 - 1, target.1 + 1] {
            if (0..8).contains(&col) && board[row as usize][col as usize] == pawn {
                key += &format!(" ({}, {})", target.0, target.1);
                break;
            }
        }
    }
    key
}
