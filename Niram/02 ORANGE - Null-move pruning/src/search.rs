//! search.rs
//!
//! Remus-ORANGE's search, line for line: null_move_search, the Day 9 search plus one upgrade.
//! think() runs it one depth deeper at a time until the clock runs out.

use std::time::Instant;

use niram_rules::attacks::in_check;
use niram_rules::game_state::State;
use niram_rules::legal_moves::legal_moves;
use niram_rules::make_move::{make_move, undo_move};
use niram_rules::move_ordering::order_moves;
use niram_rules::moves::Move;
use niram_rules::search_tools::{
    MATE_SCORE, NULL_MOVE_REDUCTION, SearchInfo, SearchResult, SearchTimeout, capture_moves, check_time, format_info,
    has_pieces, make_null_move, new_search_info, undo_null_move, with_first_move,
};

use crate::evaluation::evaluate;

/// Keep searching captures until the position is quiet, then evaluate it. The side
/// to move may "stand pat" with the current score, or try a capture that might do
/// better. This stops the horizon effect: a queen taking a pawn, with the pawn's
/// defender about to take the queen back.
pub fn quiescence(state: &mut State, mut alpha: i32, beta: i32, info: &mut SearchInfo) -> Result<i32, SearchTimeout> {
    info.nodes += 1;
    check_time(info)?;
    let stand_pat = evaluate(state);
    if stand_pat >= beta {
        return Ok(stand_pat);
    }
    alpha = alpha.max(stand_pat);
    let captures = capture_moves(state);
    for mv in order_moves(&captures, &state.board, None, &[]) {
        let undo = make_move(state, mv);
        let result = quiescence(state, -beta, -alpha, info);
        undo_move(state, undo);
        let score = -result?;
        if score >= beta {
            return Ok(score);
        }
        alpha = alpha.max(score);
    }
    Ok(alpha)
}

/// The Remus-ORANGE search: the Day 9 search plus null-move pruning. The side to
/// move passes, so the opponent moves twice, and runs a shallower search. If the
/// side to move still scores at least beta, the opponent would never allow this
/// position, because a real move almost always beats a pass, so the position is
/// cut off early. allow_null is false right after a null move, so that two passes
/// never follow each other.
///
/// `depth` counts the plies left before quiescence takes over, `ply` how many moves
/// from the root this position is, and alpha and beta the search window. `first` is
/// a move to try first, such as the best move of the last iteration. Returns the
/// score for the side to move, and the principal variation.
#[allow(clippy::too_many_arguments)]
pub fn null_move_search(
    state: &mut State,
    mut depth: i32,
    ply: i32,
    mut alpha: i32,
    beta: i32,
    info: &mut SearchInfo,
    first: Option<Move>,
    allow_null: bool,
) -> SearchResult {
    info.nodes += 1;
    check_time(info)?;
    let in_check_now = in_check(state, state.turn);
    if in_check_now {
        depth += 1; // Check extension: never stop the search while in check
    }
    if depth <= 0 {
        return Ok((quiescence(state, alpha, beta, info)?, Vec::new()));
    }
    // Never pass in check (passing would be illegal) or with only pawns left, where
    // passing can be better than any move (zugzwang)
    let can_pass = allow_null && ply > 0 && !in_check_now && depth >= 3;
    if can_pass && beta.abs() < MATE_SCORE - 1000 && has_pieces(&state.board, state.turn) {
        let en_passant = make_null_move(state);
        let result = null_move_search(
            state,
            depth - 1 - NULL_MOVE_REDUCTION,
            ply + 1,
            -beta,
            -beta + 1,
            info,
            None,
            false,
        );
        undo_null_move(state, en_passant);
        let score = -result?.0;
        if score >= beta {
            return Ok((beta, Vec::new()));
        }
    }
    let moves = legal_moves(state);
    if moves.is_empty() {
        let score = if in_check_now { -(MATE_SCORE - ply) } else { 0 };
        return Ok((score, Vec::new()));
    }
    let mut best_line: Vec<Move> = Vec::new();
    for mv in order_moves(&moves, &state.board, first, &[]) {
        let undo = make_move(state, mv);
        let result = null_move_search(state, depth - 1, ply + 1, -beta, -alpha, info, None, true);
        undo_move(state, undo);
        let (score, line) = result?;
        let score = -score;
        if score >= beta {
            return Ok((score, with_first_move(mv, line))); // Cutoff: the opponent will not allow this
        }
        if score > alpha {
            alpha = score;
            best_line = with_first_move(mv, line);
        }
    }
    Ok((alpha, best_line))
}

/// Search one move deeper at a time until time runs out, and return the best move
/// of the deepest search that finished. `report` gets each finished depth's info
/// line. Each depth tries the best move of the depth before it first.
pub fn think(
    state: &mut State,
    seconds: Option<f64>,
    max_depth: i32,
    report: &mut dyn FnMut(&str),
) -> (Move, SearchInfo) {
    let start = Instant::now();
    let mut info = new_search_info(start, seconds);
    let moves = legal_moves(state);
    let mut best = order_moves(&moves, &state.board, None, &[])[0];
    for depth in 1..=max_depth {
        let Ok((score, pv)) = null_move_search(
            state,
            depth,
            0,
            -MATE_SCORE - 1,
            MATE_SCORE + 1,
            &mut info,
            Some(best),
            true,
        ) else {
            break; // Keep the best move of the last depth that finished
        };
        if let Some(&first) = pv.first() {
            best = first;
        }
        report(&format_info(
            depth,
            score,
            info.nodes,
            start.elapsed().as_secs_f64(),
            &pv,
        ));
        if score.abs() > MATE_SCORE - 1000 || moves.len() == 1 {
            break; // A forced mate or a single legal move needs no deeper search
        }
    }
    (best, info)
}
