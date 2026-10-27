//! fen.rs
//!
//! Read and write FEN (Forsyth-Edwards Notation), the one-line text that describes
//! a whole chess position. The start position is:
//!
//!     rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
//!
//! The six fields are the pieces (rank 8 first), the side to move, the castling
//! rights, the en passant square, the halfmove clock, and the fullmove number.

use crate::board::{Board, EMPTY, parse_square};
use crate::game_state::{State, position_key};

pub const START_FEN: &str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"; // The start position

/// Build a board from the piece-placement field of FEN, such as "8/8/8/4k3/8/8/8/4K3".
pub fn board_from_placement(text: &str) -> Result<Board, String> {
    let mut board = [[EMPTY; 8]; 8];
    let ranks: Vec<&str> = text.split('/').collect();
    if ranks.len() != 8 {
        return Err(format!("FEN must describe 8 ranks: {text:?}"));
    }
    for (row, rank_text) in ranks.iter().enumerate() {
        let mut col = 0;
        for character in rank_text.chars() {
            if let Some(count) = character.to_digit(10) {
                col += count as usize; // A digit counts empty squares
            } else {
                if col < 8 {
                    board[row][col] = character;
                }
                col += 1;
            }
        }
        if col != 8 {
            return Err(format!("A FEN rank must describe 8 squares: {rank_text:?}"));
        }
    }
    Ok(board)
}

/// Build a game state from a full FEN string.
pub fn state_from_fen(fen: &str) -> Result<State, String> {
    let fields: Vec<&str> = fen.split_whitespace().collect();
    if fields.len() < 4 {
        return Err(format!("FEN needs at least four fields: {fen:?}"));
    }
    let mut state = State {
        board: board_from_placement(fields[0])?,
        turn: fields[1].chars().next().unwrap_or('w'),
        castling: if fields[2] == "-" {
            String::new()
        } else {
            fields[2].to_string()
        },
        en_passant: if fields[3] == "-" {
            None
        } else {
            Some(parse_square(fields[3])?)
        },
        halfmove_clock: fields.get(4).and_then(|text| text.parse().ok()).unwrap_or(0),
        fullmove_number: fields.get(5).and_then(|text| text.parse().ok()).unwrap_or(1),
        history: Vec::new(),
    };
    let key = position_key(&state);
    state.history.push(key);
    Ok(state)
}
