//! evaluation.rs
//!
//! Remus-GOLD's evaluate(): all five terms, from rules/src/evaluation.rs.

use niram_rules::evaluation::{king_safety, material, mating_bonus, pawn_structure, placement};
use niram_rules::game_state::{State, WHITE};

/// Score the position for the side to move: material, placement, pawn structure,
/// the mating bonus, and king safety, positive when the side to move stands better.
/// Negamax search needs the score from the mover's side.
pub fn evaluate(state: &State) -> i32 {
    let board = &state.board;
    let white_score =
        material(board) + placement(board) + pawn_structure(board) + mating_bonus(board) + king_safety(board);
    if state.turn == WHITE { white_score } else { -white_score }
}
