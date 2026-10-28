//! opening_book.rs
//!
//! Play the first few moves from a list of well-known openings instead of searching.
//! Each line of opening_book.txt is one opening written in SAN. Niram replays every
//! line from the starting position and records, for each position along the way,
//! the moves the book suggests there. The book is a hash map:
//!
//! ```text
//! position_key -> list of book moves
//! ```
//!
//! A line that starts with "White:" or "Black:" shows how that side defends against
//! a trap. Niram records only the defender's moves from such a line, so it answers
//! the trap at once but never sets the trap itself.
//!
//! Every book move is read with parse_san, which accepts only legal moves, so a
//! typo in the file is reported and skipped. A missing file gives an empty book,
//! and an empty book never stops play: Niram simply searches instead. Reports go to
//! standard error, because standard output carries the UCI conversation.

use std::collections::HashMap;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use crate::fen::{START_FEN, state_from_fen};
use crate::game_state::{State, position_key};
use crate::make_move::make_move;
use crate::moves::Move;
use crate::notation::parse_san;

pub type Book = HashMap<String, Vec<Move>>;

/// Return the path of opening_book.txt, in the Niram folder above rules/.
pub fn book_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("opening_book.txt")
}

/// Split a book line into its defender ('w', 'b', or None for both sides) and its moves.
pub fn read_defender(line: &str) -> (Option<char>, Vec<&str>) {
    let words: Vec<&str> = line.split_whitespace().collect();
    match words[0] {
        "White:" => (Some('w'), words[1..].to_vec()),
        "Black:" => (Some('b'), words[1..].to_vec()),
        _ => (None, words),
    }
}

/// Read an opening book file into a map from position key to book moves.
pub fn load_book(file_path: &PathBuf) -> Book {
    let mut book = Book::new();
    let Ok(text) = std::fs::read_to_string(file_path) else {
        eprintln!("No opening book at {}; Niram searches every move", file_path.display());
        return book;
    };
    for line in text.lines() {
        if line.trim().is_empty() || line.starts_with('#') {
            continue;
        }
        let (defender, words) = read_defender(line);
        let mut state = state_from_fen(START_FEN).expect("START_FEN is valid");
        for word in words {
            let Ok(mv) = parse_san(&mut state, word) else {
                eprintln!("Book line skipped at {word:?}: {line}");
                break;
            };
            // A trap line teaches the defense, so the attacker's moves stay out
            if defender.is_none() || defender == Some(state.turn) {
                let moves_here = book.entry(position_key(&state)).or_default();
                if !moves_here.contains(&mv) {
                    moves_here.push(mv);
                }
            }
            make_move(&mut state, mv);
        }
    }
    book
}

/// Return a random book move for this position, or None when out of book.
pub fn book_move(book: &Book, state: &State) -> Option<Move> {
    let choices = book.get(&position_key(state))?;
    if choices.is_empty() {
        return None;
    }
    // The clock's nanoseconds are random enough to pick among a few book moves
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|time| time.subsec_nanos())
        .unwrap_or(0);
    Some(choices[nanos as usize % choices.len()])
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Remus's load_book() reads 285 positions holding 328 book moves from
    /// opening_book.txt, so Niram's must read the same.
    #[test]
    fn same_book_as_remus() {
        let book = load_book(&book_path());
        let mut moves = 0;
        for choices in book.values() {
            moves += choices.len();
        }
        assert_eq!((book.len(), moves), (285, 328));
    }
}
