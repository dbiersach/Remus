//! moves.rs
//!
//! Describe a move as a small record, and convert it to and from UCI text such as
//! "e2e4" or "e7e8q", the format chess programs use to talk to each other.

use crate::board::{Square, parse_square, square_name};

/// One move: where the piece starts, where it lands, and any promotion.
///
/// promotion is the piece a pawn becomes on the last rank ('Q', 'R', 'B', 'N' for
/// White; lowercase for Black), or None for every other move.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub struct Move {
    pub from_square: Square,
    pub to_square: Square,
    pub promotion: Option<char>,
}

impl Move {
    /// Return a move that is not a promotion.
    pub fn new(from_square: Square, to_square: Square) -> Move {
        Move {
            from_square,
            to_square,
            promotion: None,
        }
    }
}

/// Convert a move to UCI text, such as "e2e4", or "e7e8q" for a promotion.
pub fn move_to_uci(mv: Move) -> String {
    let mut text = square_name(mv.from_square.0, mv.from_square.1);
    text += &square_name(mv.to_square.0, mv.to_square.1);
    if let Some(piece) = mv.promotion {
        text.push(piece.to_ascii_lowercase());
    }
    text
}

/// Convert UCI text, such as "g1f3" or "e7e8q", to a move.
pub fn move_from_uci(text: &str, white_to_move: bool) -> Result<Move, String> {
    if text.len() < 4 || text.len() > 5 {
        return Err(format!("Not a UCI move: {text:?}"));
    }
    let from_square = parse_square(&text[0..2])?;
    let to_square = parse_square(&text[2..4])?;
    let mut promotion = None;
    if text.len() == 5 {
        let letter = text.as_bytes()[4] as char;
        if white_to_move {
            promotion = Some(letter.to_ascii_uppercase());
        } else {
            promotion = Some(letter.to_ascii_lowercase());
        }
    }
    Ok(Move {
        from_square,
        to_square,
        promotion,
    })
}
