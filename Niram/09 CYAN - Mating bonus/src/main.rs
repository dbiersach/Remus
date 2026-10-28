//! main.rs
//!
//! Niram-CYAN: Remus-CYAN rewritten in Rust, Remus-WHITE plus the mating bonus. It has the same
//! rules, evaluation, and search, so both engines visit the same positions and
//! choose the same moves.
//!
//! With no argument, Niram-CYAN talks UCI. "bench [depth]" times the search on
//! ten positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-CYAN", search::think, false);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-CYAN visits 72,692 positions on the bench positions at depth 3
    /// (uv run scripts/remus_benchmark.py CYAN 3), so Niram-CYAN must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 72_692);
    }
}
