//! main.rs
//!
//! Niram-GREEN: Remus-GREEN rewritten in Rust, Remus-WHITE plus the opening book. It has the same
//! rules, evaluation, and search, so both engines visit the same positions and
//! choose the same moves.
//!
//! With no argument, Niram-GREEN talks UCI. "bench [depth]" times the search on
//! ten positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-GREEN", search::think, true);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-GREEN visits 72,747 positions on the bench positions at depth 3
    /// (uv run Niram/remus_benchmark.py GREEN 3), so Niram-GREEN must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 72_747);
    }
}
