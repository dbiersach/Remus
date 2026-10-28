//! lib.rs
//!
//! The parts every Niram engine shares. Each module matches the Remus Python file
//! of the same name, and every Remus version uses the same copy of these files:
//! the board, the rules of chess, FEN, SAN, and the opening book. The evaluation
//! terms, move ordering, transposition table, and search helpers are here too, so
//! that each color folder needs only the code that makes its version different.

// Niram keeps Remus's plain loops over row and column numbers, the way the course
// teaches them, so it turns off the lints that ask for iterators instead.
#![allow(
    clippy::needless_range_loop,
    clippy::manual_ignore_case_cmp,
    clippy::manual_is_multiple_of
)]

pub mod attacks;
pub mod bench;
pub mod board;
pub mod evaluation;
pub mod fen;
pub mod game_state;
pub mod legal_moves;
pub mod make_move;
pub mod move_generation;
pub mod move_ordering;
pub mod moves;
pub mod notation;
pub mod opening_book;
pub mod search_tools;
pub mod transposition_table;
pub mod uci_engine;
