//! move_ordering.rs
//!
//! Put the moves most likely to be best first. Alpha-beta cuts off more of the tree
//! when it meets a strong move early, so a good order means fewer positions to visit.
//!
//! Captures come first, ordered by MVV-LVA: Most Valuable Victim, Least Valuable
//! Attacker. Pawn takes queen comes before queen takes pawn. Killer moves, quiet
//! moves that caused a cutoff in a sibling position, come right after the captures.

use crate::board::{Board, EMPTY, piece_at};
use crate::evaluation::piece_value;
use crate::moves::Move;

const KILLER_SCORE: i32 = 50; // Ranks a killer move above quiet moves and below every capture

/// Score a move for ordering: 0 for a quiet move; for a capture, ten times the
/// victim's value minus the attacker's value. A promotion counts like capturing
/// the new piece.
pub fn mvv_lva_score(mv: Move, board: &Board) -> i32 {
    let victim = piece_at(board, mv.to_square);
    let attacker = piece_at(board, mv.from_square);
    let mut score = 0;
    if victim != EMPTY {
        score = 10 * piece_value(victim.to_ascii_uppercase()) - piece_value(attacker.to_ascii_uppercase());
    }
    if let Some(promotion) = mv.promotion {
        score += 10 * piece_value(promotion.to_ascii_uppercase());
    }
    score
}

/// Return the moves sorted best first: highest MVV-LVA score first, killers after
/// the captures, and `first` (such as the best move of a shallower search) at the front.
pub fn order_moves(moves: &[Move], board: &Board, first: Option<Move>, killers: &[Move]) -> Vec<Move> {
    let mut ordered: Vec<Move> = Vec::with_capacity(moves.len());
    let mut scores: Vec<i32> = Vec::with_capacity(moves.len());
    for &mv in moves {
        let mut score = mvv_lva_score(mv, board);
        if score == 0 && killers.contains(&mv) {
            score = KILLER_SCORE;
        }
        // Step past every move that scores at least as high, so ties keep their order
        let mut place = 0;
        while place < scores.len() && scores[place] >= score {
            place += 1;
        }
        ordered.insert(place, mv);
        scores.insert(place, score);
    }
    if let Some(first) = first
        && let Some(index) = ordered.iter().position(|&mv| mv == first)
    {
        ordered.remove(index);
        ordered.insert(0, first);
    }
    ordered
}
