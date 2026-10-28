//! main.rs
//!
//! Niram-GRAY: Remus-GRAY rewritten in Rust, Remus-WHITE plus the king safety term. It has the same
//! rules, evaluation, and search, so both engines visit the same positions and
//! choose the same moves.
//!
//! With no argument, Niram-GRAY talks UCI. "bench [depth]" times the search on
//! ten positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-GRAY", search::think, evaluation::evaluate, false);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-GRAY visits 75,525 positions on the bench positions at depth 3
    /// (uv run scripts/remus_benchmark.py GRAY 3), so Niram-GRAY must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 75_525);
    }
}
