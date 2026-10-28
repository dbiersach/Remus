//! main.rs
//!
//! Niram-RED: Remus-RED rewritten in Rust, Remus-WHITE plus a transposition table. It has the same
//! rules, evaluation, and search, so both engines visit the same positions and
//! choose the same moves.
//!
//! With no argument, Niram-RED talks UCI. "bench [depth]" times the search on
//! ten positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-RED", search::think, false);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-RED visits 58,531 positions on the bench positions at depth 3
    /// (uv run scripts/remus_benchmark.py RED 3), so Niram-RED must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 58_531);
    }
}
