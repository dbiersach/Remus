//! search.rs
//!
//! Remus-PINK's search, line for line: pvs_search, the Day 9 search plus one upgrade.
//! think() runs it one depth deeper at a time until the clock runs out.

use std::time::Instant;

use niram_rules::attacks::in_check;
use niram_rules::game_state::State;
use niram_rules::legal_moves::legal_moves;
use niram_rules::make_move::{make_move, undo_move};
use niram_rules::move_ordering::order_moves;
use niram_rules::moves::Move;
use niram_rules::search_tools::{
    MATE_SCORE, SearchInfo, SearchResult, SearchTimeout, capture_moves, check_time, format_info, new_search_info,
    with_first_move,
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

/// Search a move after the first one, which is made already, the PVS way. `depth`
/// and `ply` belong to the position after the move, and alpha and beta are the
/// window of the position before it. First a null window (alpha, alpha + 1) asks
/// only "is this move better than alpha?". Only a surprise, a score between alpha
/// and beta, gets a second search with the full window to find the exact score.
/// Returns the move's score for the side that moved, and its line.
fn search_later_move(
    state: &mut State,
    depth: i32,
    ply: i32,
    alpha: i32,
    beta: i32,
    info: &mut SearchInfo,
) -> SearchResult {
    let (mut score, mut line) = pvs_search(state, depth, ply, -alpha - 1, -alpha, info, None)?;
    score = -score;
    if alpha < score && score < beta {
        // A surprise: search it again with the full window
        (score, line) = pvs_search(state, depth, ply, -beta, -alpha, info, None)?;
        score = -score;
    }
    Ok((score, line))
}

/// The Remus-PINK search: the Day 9 search plus principal variation search. The
/// first move, the best one by the move ordering, gets the full window, and every
/// later move first gets a cheap null window.
///
/// `depth` counts the plies left before quiescence takes over, `ply` how many moves
/// from the root this position is, and alpha and beta the search window. `first` is
/// a move to try first, such as the best move of the last iteration. Returns the
/// score for the side to move, and the principal variation.
pub fn pvs_search(
    state: &mut State,
    mut depth: i32,
    ply: i32,
    mut alpha: i32,
    beta: i32,
    info: &mut SearchInfo,
    first: Option<Move>,
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
    let moves = legal_moves(state);
    if moves.is_empty() {
        let score = if in_check_now { -(MATE_SCORE - ply) } else { 0 };
        return Ok((score, Vec::new()));
    }
    let mut best_line: Vec<Move> = Vec::new();
    let ordered = order_moves(&moves, &state.board, first, &[]);
    for (index, &mv) in ordered.iter().enumerate() {
        let undo = make_move(state, mv);
        let result = if index == 0 {
            match pvs_search(state, depth - 1, ply + 1, -beta, -alpha, info, None) {
                Ok((score, line)) => Ok((-score, line)),
                Err(timeout) => Err(timeout),
            }
        } else {
            search_later_move(state, depth - 1, ply + 1, alpha, beta, info)
        };
        undo_move(state, undo);
        let (score, line) = result?;
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
        let Ok((score, pv)) = pvs_search(state, depth, 0, -MATE_SCORE - 1, MATE_SCORE + 1, &mut info, Some(best))
        else {
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
