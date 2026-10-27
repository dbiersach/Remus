//! main.rs
//!
//! Niram-GOLD: Remus-GOLD rewritten in Rust, with the same rules, evaluation, and
//! search, so both engines visit the same positions and choose the same moves.
//!
//! Niram is the grandson of Sargon of Akkad (Naram-Sin), after Remus (Rimush), his son.
//!
//! With no argument, Niram talks to a chess GUI such as Lucas Chess over UCI. Two
//! other commands help check and time it:
//!
//!     niram bench [depth]        Time the search on ten positions
//!     niram perft [depth] [fen]  Count the leaf positions of the legal move tree

// Niram keeps Remus's plain loops over row and column numbers, the way the course
// teaches them, so it turns off the lints that ask for iterators instead.
#![allow(
    clippy::needless_range_loop,
    clippy::manual_ignore_case_cmp,
    clippy::manual_is_multiple_of
)]

mod attacks;
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
mod transposition_table;
mod uci_engine;

use std::time::Instant;

use crate::fen::{START_FEN, state_from_fen};
use crate::game_state::State;
use crate::legal_moves::legal_moves;
use crate::make_move::{make_move, undo_move};
use crate::moves::move_to_uci;
use crate::search::think;

const BENCH_POSITIONS: [&str; 10] = [
    // The ten positions of Remus's compare_search.py and niram/remus_benchmark.py
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    "rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5",
    "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2PP1N2/PP3PPP/RNBQ1RK1 w - - 0 7",
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "2r3k1/pp3ppp/8/3p4/3P4/8/PP3PPP/2R3K1 w - - 0 1",
    "8/5k2/8/3K4/8/8/4P3/8 w - - 0 1",
    "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1",
    "4k3/8/4p3/3p4/8/8/3Q4/4K3 w - - 0 1",
    "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
];
const BENCH_DEPTH: i32 = 4; // The deepest iteration, the same as remus_benchmark.py

/// Search each bench position one depth at a time, with no clock, and print the
/// positions visited and the speed next to Remus-GOLD's numbers.
fn bench(max_depth: i32) {
    println!("Niram-GOLD (Rust), iterative deepening to depth {max_depth}");
    let mut total_nodes = 0;
    let mut total_seconds = 0.0;
    for (number, fen) in BENCH_POSITIONS.iter().enumerate() {
        let mut state = state_from_fen(fen).expect("bench positions are valid FEN");
        let start = Instant::now();
        let mut last_info = String::new();
        let (best, info) = think(&mut state, None, max_depth, None, &mut |line| {
            last_info = line.to_string();
        });
        let seconds = start.elapsed().as_secs_f64();
        let score = score_from_info(&last_info);
        total_nodes += info.nodes;
        total_seconds += seconds;
        println!(
            "{:2}. {:6} score {:>7}  nodes {:>10}  {:8.3} s  {:>12} nodes/s",
            number + 1,
            move_to_uci(best),
            score,
            with_commas(info.nodes),
            seconds,
            with_commas((info.nodes as f64 / seconds) as u64)
        );
    }
    println!("Total nodes: {}", with_commas(total_nodes));
    println!("Total run time (sec): {total_seconds:.3}");
    println!(
        "Nodes per second: {}",
        with_commas((total_nodes as f64 / total_seconds) as u64)
    );
}

/// Return the score in an info line in Remus's units ("cp 35" gives 35, "mate 1" gives 99999).
fn score_from_info(line: &str) -> i32 {
    let words: Vec<&str> = line.split_whitespace().collect();
    for index in 0..words.len().saturating_sub(2) {
        if words[index] == "score" {
            let value: i32 = words[index + 2].parse().unwrap_or(0);
            if words[index + 1] == "mate" {
                let plies = 2 * value.abs() - 1;
                return if value > 0 {
                    search::MATE_SCORE - plies
                } else {
                    -(search::MATE_SCORE - plies)
                };
            }
            return value;
        }
    }
    0
}

/// Write a count with thousands separators, such as 197,281.
fn with_commas(count: u64) -> String {
    let digits = count.to_string();
    let mut text = String::new();
    for (index, digit) in digits.chars().enumerate() {
        if index > 0 && (digits.len() - index) % 3 == 0 {
            text.push(',');
        }
        text.push(digit);
    }
    text
}

/// Count the leaf positions of the legal move tree to a fixed depth.
fn perft(state: &mut State, depth: i32) -> u64 {
    if depth == 0 {
        return 1;
    }
    let mut count = 0;
    for mv in legal_moves(state) {
        let undo = make_move(state, mv);
        count += perft(state, depth - 1);
        undo_move(state, undo);
    }
    count
}

fn main() {
    let arguments: Vec<String> = std::env::args().collect();
    let command = arguments.get(1).map(|text| text.as_str()).unwrap_or("uci");
    match command {
        "bench" => {
            let depth = arguments
                .get(2)
                .and_then(|text| text.parse().ok())
                .unwrap_or(BENCH_DEPTH);
            bench(depth);
        }
        "perft" => {
            let depth = arguments.get(2).and_then(|text| text.parse().ok()).unwrap_or(4);
            let fen = if arguments.len() > 3 {
                arguments[3..].join(" ")
            } else {
                START_FEN.to_string()
            };
            let mut state = state_from_fen(&fen).expect("perft needs a valid FEN");
            let start = Instant::now();
            let count = perft(&mut state, depth);
            let seconds = start.elapsed().as_secs_f64();
            println!("perft({depth}) = {}", with_commas(count));
            println!("Total run time (sec): {seconds:.3}");
        }
        _ => uci_engine::run(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// perft from the start: 20, 400, 8,902 (the standard reference counts).
    #[test]
    fn perft_start_position() {
        let mut state = state_from_fen(START_FEN).unwrap();
        assert_eq!(perft(&mut state, 3), 8_902);
    }

    /// "Kiwipete", the castling, en passant, and promotion test: 2,039 at depth 2.
    #[test]
    fn perft_kiwipete() {
        let fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1";
        let mut state = state_from_fen(fen).unwrap();
        assert_eq!(perft(&mut state, 2), 2_039);
    }

    /// Remus-GOLD visits 22,001 positions on the bench positions at depth 3
    /// (uv run niram/remus_benchmark.py 3), so Niram-GOLD must visit the same.
    #[test]
    fn same_node_count_as_remus() {
        let mut total_nodes = 0;
        for fen in BENCH_POSITIONS {
            let mut state = state_from_fen(fen).unwrap();
            let (_, info) = think(&mut state, None, 3, None, &mut |_| {});
            total_nodes += info.nodes;
        }
        assert_eq!(total_nodes, 22_001);
    }

    /// Back-rank mate: Ra8 mates at once.
    #[test]
    fn finds_back_rank_mate() {
        let mut state = state_from_fen("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1").unwrap();
        let (best, _) = think(&mut state, None, 3, None, &mut |_| {});
        assert_eq!(move_to_uci(best), "a1a8");
    }
}
