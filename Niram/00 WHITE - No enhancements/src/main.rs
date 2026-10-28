//! main.rs
//!
//! Niram-WHITE: Remus-WHITE rewritten in Rust, no enhancements: the finished Day 9 Remus. It has the same
//! rules, evaluation, and search, so both engines visit the same positions and
//! choose the same moves.
//!
//! With no argument, Niram-WHITE talks UCI. "bench [depth]" times the search on
//! ten positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-WHITE", search::think, evaluation::evaluate, false);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-WHITE visits 72,747 positions on the bench positions at depth 3
    /// (uv run scripts/remus_benchmark.py WHITE 3), so Niram-WHITE must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 72_747);
    }
}
