//! main.rs
//!
//! Niram-BROWN: Remus-BROWN rewritten in Rust, Remus-WHITE plus late move reductions. It has the same
//! rules, evaluation, and search, so both engines visit the same positions and
//! choose the same moves.
//!
//! With no argument, Niram-BROWN talks UCI. "bench [depth]" times the search on
//! ten positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-BROWN", search::think, false);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-BROWN visits 38,545 positions on the bench positions at depth 3
    /// (uv run Niram/remus_benchmark.py BROWN 3), so Niram-BROWN must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 38_545);
    }
}
