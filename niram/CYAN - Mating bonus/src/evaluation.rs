//! evaluation.rs
//!
//! Remus-CYAN's evaluate(), from the terms in rules/src/evaluation.rs.

use niram_rules::evaluation::{material, mating_bonus, placement};
use niram_rules::game_state::{State, WHITE};

/// Score the position for the side to move: material, placement, and the mating bonus in centipawns,
/// positive when the side to move stands better. Negamax search needs the score
/// from the mover's side.
pub fn evaluate(state: &State) -> i32 {
    let board = &state.board;
    let white_score = material(board) + placement(board) + mating_bonus(board);
    if state.turn == WHITE { white_score } else { -white_score }
}
