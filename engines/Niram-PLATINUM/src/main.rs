//! main.rs
//!
//! Niram-PLATINUM: Remus-PLATINUM rewritten in Rust, with the same rules,
//! evaluation, and search, so both engines visit the same positions and choose the
//! same moves. It is Niram-GOLD plus ten more enhancements: tapered evaluation, the
//! pawn race, mobility, the bishop pair, rooks on open files (evaluation.rs),
//! static exchange evaluation (exchange.rs), delta and futility pruning, aspiration
//! windows, and time management (search.rs).
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
mod exchange;
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
    crate::bench::run_command_line("Niram-PLATINUM", search::think, evaluation::evaluate, true);
}

#[cfg(test)]
mod tests {
    use crate::bench::bench_nodes;

    /// Remus-PLATINUM visits 10,038 positions on the bench positions at depth 3
    /// (the same think() to depth 3 on each position), so Niram-PLATINUM must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 10_038);
    }
}
