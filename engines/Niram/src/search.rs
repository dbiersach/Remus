//! search.rs
//!
//! Remus-GOLD's search, line for line. upgraded_search is alpha-beta with
//! quiescence at the leaves, ordered moves, and a check extension, plus the six
//! search upgrades: a transposition table, killer moves, principal variation search,
//! draw sense, null-move pruning, and late move reductions. think() runs it one
//! depth deeper at a time until the clock runs out.

use std::time::Instant;

use crate::attacks::in_check;
use crate::game_state::State;
use crate::legal_moves::legal_moves;
use crate::make_move::{make_move, undo_move};
use crate::move_ordering::order_moves;
use crate::moves::Move;
use crate::search_tools::{
    MATE_SCORE, NULL_MOVE_REDUCTION, SearchInfo, SearchResult, SearchTimeout, capture_moves, check_time, format_info,
    has_pieces, is_draw_in_search, make_null_move, new_search_info, reduction, remember_killer, undo_null_move,
};
use crate::transposition_table::{Bound, best_stored_move, probe, store};

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

/// Pass the turn, search shallower, and say whether passing still holds beta. A
/// real move is almost always better than passing, so the position is cut off.
fn null_move_cutoff(
    state: &mut State,
    depth: i32,
    ply: i32,
    beta: i32,
    info: &mut SearchInfo,
) -> Result<bool, SearchTimeout> {
    let en_passant = make_null_move(state);
    let result = upgraded_search(
        state,
        depth - 1 - NULL_MOVE_REDUCTION,
        ply + 1,
        -beta,
        -beta + 1,
        info,
        false,
    );
    undo_null_move(state, en_passant);
    let (score, _) = result?;
    Ok(-score >= beta)
}

/// Search a move after the first one, already made: a cheap test first, a full
/// search only if needed. `depth` and `ply` belong to the position after the move,
/// and `cut` is 1 for a late, quiet move (late move reductions), otherwise 0.
/// Returns the move's score for the side that made it, and the line that follows it.
#[allow(clippy::too_many_arguments)]
fn search_later_move(
    state: &mut State,
    depth: i32,
    ply: i32,
    alpha: i32,
    beta: i32,
    info: &mut SearchInfo,
    cut: i32,
) -> SearchResult {
    // The null window (alpha, alpha + 1) only asks "is this move better than alpha?"
    let (mut score, mut line) = upgraded_search(state, depth - cut, ply, -alpha - 1, -alpha, info, true)?;
    score = -score;
    if cut > 0 && score > alpha {
        // A late move surprised: test it at full depth
        (score, line) = upgraded_search(state, depth, ply, -alpha - 1, -alpha, info, true)?;
        score = -score;
    }
    if alpha < score && score < beta {
        // Better than alpha: find its exact score
        (score, line) = upgraded_search(state, depth, ply, -beta, -alpha, info, true)?;
        score = -score;
    }
    Ok((score, line))
}

/// The final search: alpha-beta with quiescence plus the six upgrades.
///
/// - Draw sense: a position that repeats inside the search, or that reaches the
///   fifty-move limit, scores 0.
/// - Transposition table: a position already searched deeply enough is not searched
///   again, and its stored best move is tried first.
/// - Killer moves: quiet moves that caused cutoffs at this ply are tried early.
/// - Principal variation search: the first move gets the full window; every other
///   move first gets a null window (alpha, alpha + 1) that only asks "is this move
///   better?", and is searched again in full only when the answer is yes.
/// - Null-move pruning: Niram passes, so the opponent moves twice, and runs a
///   shallower search. If Niram still scores at least beta, the position is cut off.
/// - Late move reductions: late, quiet moves get a search one ply shallower, and a
///   full-depth search only if they turn out better than alpha.
///
/// Returns the score for the side to move and the principal variation. allow_null
/// is false right after a null move, so that two passes never follow each other.
pub fn upgraded_search(
    state: &mut State,
    mut depth: i32,
    ply: i32,
    mut alpha: i32,
    beta: i32,
    info: &mut SearchInfo,
    allow_null: bool,
) -> SearchResult {
    info.nodes += 1;
    check_time(info)?;
    if ply > 0 && is_draw_in_search(state) {
        return Ok((0, Vec::new())); // Draw sense: a repeated position is a draw, not a gain
    }
    let in_check_now = in_check(state, state.turn);
    if in_check_now {
        depth += 1; // Check extension: never stop the search while in check
    }
    if depth <= 0 {
        return Ok((quiescence(state, alpha, beta, info)?, Vec::new()));
    }
    let key = state
        .history
        .last()
        .expect("history holds the current position")
        .clone();
    let stored = probe(&info.table, &key, depth, alpha, beta);
    if ply > 0
        && let Some(score) = stored
    {
        return Ok((score, Vec::new()));
    }
    // Null-move pruning, skipped in check (passing would be illegal) and with only
    // pawns left, where passing can be better than any move (zugzwang)
    let can_pass = allow_null
        && ply > 0
        && !in_check_now
        && depth >= 3
        && beta.abs() < MATE_SCORE - 1000
        && has_pieces(&state.board, state.turn);
    if can_pass && null_move_cutoff(state, depth, ply, beta, info)? {
        return Ok((beta, Vec::new()));
    }
    let moves = legal_moves(state);
    if moves.is_empty() {
        let score = if in_check_now { -(MATE_SCORE - ply) } else { 0 };
        return Ok((score, Vec::new()));
    }

    let original_alpha = alpha;
    let mut best_line: Vec<Move> = Vec::new();
    let killers = info.killers.get(&ply).cloned().unwrap_or_default();
    let ordered = order_moves(&moves, &state.board, best_stored_move(&info.table, &key), &killers);
    for (index, &mv) in ordered.iter().enumerate() {
        let undo = make_move(state, mv);
        let result = if index == 0 {
            // The first move gets the full window
            match upgraded_search(state, depth - 1, ply + 1, -beta, -alpha, info, true) {
                Ok((score, line)) => Ok((-score, line)),
                Err(timeout) => Err(timeout),
            }
        } else {
            let gives_check = in_check(state, state.turn);
            let cut = reduction(depth, index, mv, undo.captured, gives_check);
            search_later_move(state, depth - 1, ply + 1, alpha, beta, info, cut)
        };
        undo_move(state, undo);
        let (score, line) = result?;
        if score >= beta {
            remember_killer(info, ply, mv, &state.board);
            if score.abs() < MATE_SCORE - 1000 {
                store(&mut info.table, &key, depth, score, Bound::Lower, Some(mv));
            }
            let mut pv = vec![mv];
            pv.extend(line);
            return Ok((score, pv));
        }
        if score > alpha {
            alpha = score;
            best_line = vec![mv];
            best_line.extend(line);
        }
    }
    if alpha.abs() < MATE_SCORE - 1000 {
        // Mate scores depend on ply, so they are not stored
        let bound = if alpha > original_alpha {
            Bound::Exact
        } else {
            Bound::Upper
        };
        store(&mut info.table, &key, depth, alpha, bound, best_line.first().copied());
    }
    Ok((alpha, best_line))
}

/// Search one move deeper at a time until time runs out, and return the best move
/// of the deepest search that finished. `report` gets each finished depth's info
/// line. Each depth runs upgraded_search; its transposition table carries the best
/// move of one depth into the next.
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
        let Ok((score, pv)) = upgraded_search(state, depth, 0, -MATE_SCORE - 1, MATE_SCORE + 1, &mut info, true) else {
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
