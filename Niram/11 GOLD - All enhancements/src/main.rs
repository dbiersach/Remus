//! main.rs
//!
//! Niram-GOLD: Remus-GOLD rewritten in Rust, with the same rules, evaluation, and
//! search, so both engines visit the same positions and choose the same moves.
//! It has all ten enhancements: the six search upgrades in search.rs, the three
//! evaluation terms in evaluation.rs, and the opening book.
//!
//! With no argument, Niram-GOLD talks UCI. "bench [depth]" times the search on ten
//! positions, and "perft [depth] [fen]" counts the legal move tree.

mod evaluation;
mod search;

fn main() {
    niram_rules::bench::run_command_line("Niram-GOLD", search::think, evaluation::evaluate, true);
}

#[cfg(test)]
mod tests {
    use niram_rules::bench::bench_nodes;

    /// Remus-GOLD visits 22,001 positions on the bench positions at depth 3
    /// (uv run scripts/remus_benchmark.py GOLD 3), so Niram-GOLD must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        assert_eq!(bench_nodes(crate::search::think, 3), 22_001);
    }
}
