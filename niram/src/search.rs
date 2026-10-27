//! search.rs
//!
//! Choose a move: the search of Remus-GOLD, line for line. upgraded_search is
//! alpha-beta with quiescence at the leaves, ordered moves, a check extension, and
//! the six search upgrades: a transposition table, killer moves, principal
//! variation search, draw sense, null-move pruning, and late move reductions.
//! think() runs it one depth deeper at a time until the clock runs out.
//!
//! Python's Remus stops a search that runs out of time by raising SearchTimeout.
//! Rust has no exceptions, so each search function returns a Result: Ok with the
//! score, or Err(SearchTimeout). The `?` after a call passes the timeout up to the
//! caller, always after undo_move has put the position back.

use std::collections::HashMap;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::Instant;

use crate::attacks::in_check;
use crate::board::{Board, EMPTY, piece_at};
use crate::evaluation::evaluate;
use crate::game_state::{State, opponent, position_key};
use crate::legal_moves::legal_moves;
use crate::make_move::{make_move, undo_move};
use crate::move_ordering::order_moves;
use crate::moves::{Move, move_to_uci};
use crate::transposition_table::{Bound, Table, best_stored_move, probe, store};

pub const MATE_SCORE: i32 = 100_000; // Larger than any material count; a mate n plies away scores MATE_SCORE - n
const NULL_MOVE_REDUCTION: i32 = 2; // How many plies shallower the null-move search looks
const LATE_MOVE_INDEX: usize = 3; // Moves after the first three in the ordered list count as late

/// What a search counts while it runs.
#[derive(Default)]
pub struct SearchInfo {
    pub nodes: u64,                       // Positions visited
    pub deadline: Option<Instant>,        // When the search must stop
    pub stop: Option<Arc<AtomicBool>>,    // Set by the GUI's "stop" command
    pub table: Table,                     // Transposition table: position_key -> entry
    pub killers: HashMap<i32, Vec<Move>>, // Ply -> up to two killer moves
}

/// The search ran out of time, or the GUI said stop.
#[derive(Debug)]
pub struct SearchTimeout;

/// A score and the principal variation, or a timeout.
type SearchResult = Result<(i32, Vec<Move>), SearchTimeout>;

/// Return Err(SearchTimeout) if the deadline has passed or the GUI said stop.
fn check_time(info: &SearchInfo) -> Result<(), SearchTimeout> {
    let out_of_time = match info.deadline {
        Some(deadline) => Instant::now() > deadline,
        None => false,
    };
    let stopped = match &info.stop {
        Some(stop) => stop.load(Ordering::Relaxed),
        None => false,
    };
    if out_of_time || stopped {
        return Err(SearchTimeout);
    }
    Ok(())
}

/// Return the legal moves that capture a piece or promote a pawn: the moves
/// quiescence search keeps playing until the position is quiet.
pub fn capture_moves(state: &mut State) -> Vec<Move> {
    let mut captures = Vec::new();
    for mv in legal_moves(state) {
        let is_en_passant = Some(mv.to_square) == state.en_passant
            && piece_at(&state.board, mv.from_square).to_ascii_uppercase() == 'P';
        if piece_at(&state.board, mv.to_square) != EMPTY || is_en_passant || mv.promotion.is_some() {
            captures.push(mv);
        }
    }
    captures
}

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

/// Keep a quiet move that caused a cutoff as one of two killers for this ply.
fn remember_killer(info: &mut SearchInfo, ply: i32, mv: Move, board: &Board) {
    if piece_at(board, mv.to_square) != EMPTY || mv.promotion.is_some() {
        return; // Captures are already ordered first
    }
    let killers = info.killers.entry(ply).or_default();
    if !killers.contains(&mv) {
        killers.insert(0, mv);
        killers.truncate(2);
    }
}

/// Pass the turn without moving a piece: the null move. Chess has no such move, but
/// the search uses it to ask "is my position so good that even passing wins?"
/// Returns the en passant target before the null move, which undo_null_move restores.
fn make_null_move(state: &mut State) -> Option<(i32, i32)> {
    let en_passant = state.en_passant;
    state.turn = opponent(state.turn);
    state.en_passant = None;
    let key = position_key(state);
    state.history.push(key);
    en_passant
}

/// Take back a null move, restoring the side to move and the en passant target.
fn undo_null_move(state: &mut State, en_passant: Option<(i32, i32)>) {
    state.history.pop();
    state.turn = opponent(state.turn);
    state.en_passant = en_passant;
}

/// Return true if the color has a knight, bishop, rook, or queen.
fn has_pieces(board: &Board, color: char) -> bool {
    let pieces = if color == 'w' { "NBRQ" } else { "nbrq" };
    for row in board {
        for &piece in row {
            if pieces.contains(piece) {
                return true;
            }
        }
    }
    false
}

/// Return how many plies to cut from the search of one move: late move reductions.
/// 1 for a late, quiet move (no capture, no promotion, no check) with at least 3
/// plies to go, because move ordering puts the best moves first and a late quiet
/// move rarely turns out best. Otherwise 0.
fn reduction(depth: i32, index: usize, mv: Move, captured: char, gives_check: bool) -> i32 {
    let late = index >= LATE_MOVE_INDEX && depth >= 3;
    let quiet = captured == EMPTY && mv.promotion.is_none();
    if late && quiet && !gives_check { 1 } else { 0 }
}

/// Return the number of times a key appears in the game history.
fn count_in_history(history: &[String], key: &str) -> usize {
    let mut count = 0;
    for old_key in history {
        if old_key == key {
            count += 1;
        }
    }
    count
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
/// - Null-move pruning: if passing the turn still scores at least beta in a
///   shallower search, a real move will too, so the position is cut off early.
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
    let key = state
        .history
        .last()
        .expect("history holds the current position")
        .clone();
    if ply > 0 && (count_in_history(&state.history, &key) >= 2 || state.halfmove_clock >= 100) {
        return Ok((0, Vec::new())); // Draw sense: a repeated position is a draw, not a gain
    }
    let in_check_now = in_check(state, state.turn);
    if in_check_now {
        depth += 1; // Check extension: never stop the search while in check
    }
    if depth <= 0 {
        return Ok((quiescence(state, alpha, beta, info)?, Vec::new()));
    }
    let stored = probe(&info.table, &key, depth, alpha, beta);
    if ply > 0
        && let Some(score) = stored
    {
        return Ok((score, Vec::new()));
    }
    // Null-move pruning, skipped in check (passing would be illegal) and with only
    // pawns left, where passing can be better than any move (zugzwang)
    let can_pass = allow_null && ply > 0 && !in_check_now && depth >= 3;
    if can_pass && beta.abs() < MATE_SCORE - 1000 && has_pieces(&state.board, state.turn) {
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

    let original_alpha = alpha;
    let mut best_line: Vec<Move> = Vec::new();
    let killers = info.killers.get(&ply).cloned().unwrap_or_default();
    let ordered = order_moves(&moves, &state.board, best_stored_move(&info.table, &key), &killers);
    for (index, &mv) in ordered.iter().enumerate() {
        let undo = make_move(state, mv);
        let captured = undo.captured;
        let result = search_one_move(state, depth, ply, alpha, beta, info, index, mv, captured);
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

/// Search the reply to one move, already made, the way principal variation search
/// and late move reductions say. Returns the score from the mover's side.
#[allow(clippy::too_many_arguments)]
fn search_one_move(
    state: &mut State,
    depth: i32,
    ply: i32,
    alpha: i32,
    beta: i32,
    info: &mut SearchInfo,
    index: usize,
    mv: Move,
    captured: char,
) -> SearchResult {
    if index == 0 {
        let (score, line) = upgraded_search(state, depth - 1, ply + 1, -beta, -alpha, info, true)?;
        return Ok((-score, line));
    }
    let gives_check = in_check(state, state.turn);
    let cut = reduction(depth, index, mv, captured, gives_check);
    let (mut score, mut line) = upgraded_search(state, depth - 1 - cut, ply + 1, -alpha - 1, -alpha, info, true)?;
    score = -score;
    if cut > 0 && score > alpha {
        // A late move surprised: search full depth
        (score, line) = upgraded_search(state, depth - 1, ply + 1, -alpha - 1, -alpha, info, true)?;
        score = -score;
    }
    if alpha < score && score < beta {
        // A surprise: search it again with the full window
        (score, line) = upgraded_search(state, depth - 1, ply + 1, -beta, -alpha, info, true)?;
        score = -score;
    }
    Ok((score, line))
}

/// Return a UCI "info" line, such as "info depth 3 score cp 35 nodes 4120 pv e2e4
/// e7e5 g1f3". A mate score is written as "score mate 2", counted in moves.
pub fn format_info(depth: i32, score: i32, nodes: u64, seconds: f64, pv: &[Move]) -> String {
    let score_text = if score.abs() > MATE_SCORE - 1000 {
        let plies = MATE_SCORE - score.abs();
        let moves_to_mate = (plies + 1) / 2;
        format!("mate {}", if score > 0 { moves_to_mate } else { -moves_to_mate })
    } else {
        format!("cp {score}")
    };
    let mut line = String::new();
    for &mv in pv {
        line.push(' ');
        line += &move_to_uci(mv);
    }
    let milliseconds = (seconds * 1000.0) as u64;
    let nps = if seconds > 0.0 {
        (nodes as f64 / seconds) as u64
    } else {
        0
    };
    format!("info depth {depth} score {score_text} nodes {nodes} nps {nps} time {milliseconds} pv{line}")
}

/// Search one move deeper at a time until time runs out, and return the best move
/// of the deepest search that finished. `report` gets each finished depth's info line.
pub fn think(
    state: &mut State,
    seconds: Option<f64>,
    max_depth: i32,
    stop: Option<Arc<AtomicBool>>,
    report: &mut dyn FnMut(&str),
) -> (Move, SearchInfo) {
    let start = Instant::now();
    let mut info = SearchInfo {
        deadline: seconds.map(|seconds| start + std::time::Duration::from_secs_f64(seconds)),
        stop,
        ..SearchInfo::default()
    };
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
