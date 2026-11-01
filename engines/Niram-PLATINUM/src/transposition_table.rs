//! transposition_table.rs
//!
//! Remember positions the search has already scored. The same position can arise
//! in many orders (1. Nf3 Nf6 2. Nc3 and 1. Nc3 Nf6 2. Nf3), so a plain hash map
//! keyed by position_key saves the search from scoring it twice.
//!
//! Each entry stores the depth searched, the score, the kind of score, and the best
//! move. An alpha-beta score is not always exact:
//!
//! - Exact: the true score at that depth.
//! - Lower: a cutoff happened, so the true score is at least this much.
//! - Upper: no move beat alpha, so the true score is at most this much.

use std::collections::HashMap;

use crate::moves::Move;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Bound {
    Exact,
    Lower,
    Upper,
}

#[derive(Clone, Copy, Debug)]
pub struct Entry {
    depth: i32,
    score: i32,
    bound: Bound,
    best: Option<Move>,
}

/// The transposition table: position_key -> entry.
pub type Table = HashMap<String, Entry>;

/// Save a search result for a position, keeping the deeper of two results.
pub fn store(table: &mut Table, key: &str, depth: i32, score: i32, bound: Bound, best: Option<Move>) {
    let keep_old = match table.get(key) {
        Some(old) => depth < old.depth,
        None => false,
    };
    if !keep_old {
        table.insert(
            key.to_string(),
            Entry {
                depth,
                score,
                bound,
                best,
            },
        );
    }
}

/// Return a stored score that answers this search, or None: the stored score if it
/// was searched at least as deep and its bound settles the question (an exact score,
/// a lower bound at or above beta, or an upper bound at or below alpha).
pub fn probe(table: &Table, key: &str, depth: i32, alpha: i32, beta: i32) -> Option<i32> {
    let entry = table.get(key)?;
    if entry.depth < depth {
        return None;
    }
    let score = entry.score;
    match entry.bound {
        Bound::Exact => Some(score),
        Bound::Lower if score >= beta => Some(score),
        Bound::Upper if score <= alpha => Some(score),
        _ => None,
    }
}

/// Return the best move stored for a position, to try first.
pub fn best_stored_move(table: &Table, key: &str) -> Option<Move> {
    table.get(key).and_then(|entry| entry.best)
}
