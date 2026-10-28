//! search_tools.rs
//!
//! The pieces of search.py that every Niram version shares: the search counters,
//! the clock, the capture list for quiescence, killer moves, the null move, late
//! move reductions, draw sense, and the UCI "info" line. Each color's search.rs
//! puts the pieces its version uses together.
//!
//! Python's Remus stops a search that runs out of time by raising SearchTimeout.
//! Rust has no exceptions, so each search function returns a Result: Ok with the
//! score, or Err(SearchTimeout). The `?` after a call passes the timeout up to the
//! caller, always after undo_move has put the position back.

use std::collections::HashMap;
use std::time::Instant;

use crate::board::{Board, EMPTY, Square, piece_at};
use crate::game_state::{State, opponent, position_key};
use crate::legal_moves::legal_moves;
use crate::moves::{Move, move_to_uci};
use crate::transposition_table::Table;

pub const MATE_SCORE: i32 = 100_000; // Larger than any material count; a mate n plies away scores MATE_SCORE - n
pub const NULL_MOVE_REDUCTION: i32 = 2; // How many plies shallower the null-move search looks
pub const LATE_MOVE_INDEX: usize = 3; // Moves after the first three in the ordered list count as late

/// What a search counts while it runs.
#[derive(Default)]
pub struct SearchInfo {
    pub nodes: u64,                       // Positions visited
    pub deadline: Option<Instant>,        // When the search must stop
    pub table: Table,                     // Transposition table: position_key -> entry
    pub killers: HashMap<i32, Vec<Move>>, // Ply -> up to two killer moves
}

/// The search ran out of time.
#[derive(Debug)]
pub struct SearchTimeout;

/// A score and the principal variation, or a timeout.
pub type SearchResult = Result<(i32, Vec<Move>), SearchTimeout>;

/// The think() of one Niram version: search the state up to max_depth plies, or
/// until `seconds` run out, and return the best move and the search counters.
pub type ThinkFn = fn(&mut State, Option<f64>, i32, &mut dyn FnMut(&str)) -> (Move, SearchInfo);

/// Return Err(SearchTimeout) if the deadline has passed.
pub fn check_time(info: &SearchInfo) -> Result<(), SearchTimeout> {
    if let Some(deadline) = info.deadline
        && Instant::now() > deadline
    {
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

/// Keep a quiet move that caused a cutoff as one of two killers for this ply.
pub fn remember_killer(info: &mut SearchInfo, ply: i32, mv: Move, board: &Board) {
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
pub fn make_null_move(state: &mut State) -> Option<Square> {
    let en_passant = state.en_passant;
    state.turn = opponent(state.turn);
    state.en_passant = None;
    let key = position_key(state);
    state.history.push(key);
    en_passant
}

/// Take back a null move, restoring the side to move and the en passant target.
pub fn undo_null_move(state: &mut State, en_passant: Option<Square>) {
    state.history.pop();
    state.turn = opponent(state.turn);
    state.en_passant = en_passant;
}

/// Return true if the color has a knight, bishop, rook, or queen.
pub fn has_pieces(board: &Board, color: char) -> bool {
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
pub fn reduction(depth: i32, index: usize, mv: Move, captured: char, gives_check: bool) -> i32 {
    let late = index >= LATE_MOVE_INDEX && depth >= 3;
    let quiet = captured == EMPTY && mv.promotion.is_none();
    if late && quiet && !gives_check { 1 } else { 0 }
}

/// Return true if the search has reached a draw it can claim right away: the
/// position has already appeared earlier in the game or the search, or the
/// fifty-move limit (100 plies with no capture or pawn move) is reached.
pub fn is_draw_in_search(state: &State) -> bool {
    let key = state.history.last().expect("history holds the current position");
    let mut count = 0;
    for old_key in &state.history {
        if old_key == key {
            count += 1;
        }
    }
    count >= 2 || state.halfmove_clock >= 100
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

/// Return the search counters for a think() that stops after `seconds`, or never.
pub fn new_search_info(start: Instant, seconds: Option<f64>) -> SearchInfo {
    SearchInfo {
        deadline: seconds.map(|seconds| start + std::time::Duration::from_secs_f64(seconds)),
        ..SearchInfo::default()
    }
}

/// Return the line that starts with a move and goes on with the line after it,
/// the Rust form of Python's [move] + line.
pub fn with_first_move(mv: Move, line: Vec<Move>) -> Vec<Move> {
    let mut whole = Vec::with_capacity(line.len() + 1);
    whole.push(mv);
    whole.extend(line);
    whole
}
