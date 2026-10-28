//! main.rs
//!
//! Niram-BLUE: Remus-BLUE rewritten in Rust, Remus-WHITE plus killer moves. It has the same
//! rules, evaluation, and search, so both engines visit the same positions and
//! choose the same moves.
//!
//! With no argument, Niram-BLUE talks UCI. "bench [depth]" times the search on
//! ten positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-BLUE", search::think, false);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-BLUE visits 64,890 positions on the bench positions at depth 3
    /// (uv run scripts/remus_benchmark.py BLUE 3), so Niram-BLUE must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 64_890);
    }
}
