//! main.rs
//!
//! Niram: Remus-GOLD rewritten in Rust, with the same rules, evaluation, and
//! search, so both engines visit the same positions and choose the same moves.
//! It has all ten enhancements: the six search upgrades in search.rs, the three
//! evaluation terms in evaluation.rs, and the opening book.
//!
//! With no argument, Niram talks UCI. "bench [depth]" times the search on ten
//! positions, and "perft [depth] [fen]" counts the legal move tree.

// Niram keeps Remus's plain loops over row and column numbers, the way the course
// teaches them, so it turns off the lints that ask for iterators instead.
#![allow(
    clippy::needless_range_loop,
    clippy::manual_ignore_case_cmp,
    clippy::manual_is_multiple_of
)]

mod attacks;
mod bench;
mod board;
mod evaluation;
mod fen;
mod game_state;
mod legal_moves;
mod make_move;
mod move_generation;
mod move_ordering;
mod moves;
mod notation;
mod opening_book;
mod search;
mod search_tools;
mod transposition_table;
mod uci_engine;

fn main() {
    crate::bench::run_command_line("Niram", search::think, evaluation::evaluate, true);
}

#[cfg(test)]
mod tests {
    use crate::bench::bench_nodes;

    /// Remus-GOLD visits 22,001 positions on the bench positions at depth 3
    /// (uv run misc/scripts/remus_benchmark.py GOLD 3), so Niram must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 22_001);
    }
}
