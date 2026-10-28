//! bench.rs
//!
//! The command line every Niram engine shares. With no argument, an engine talks
//! UCI. Two other commands check and time it:
//!
//! ```text
//! niram-red bench [depth]        Time the search on ten positions
//! niram-red perft [depth] [fen]  Count the leaf positions of the legal move tree
//! niram-red parity FILE NODES    Print what the engine sees and chooses in each
//!                                position of FILE, for misc/scripts/engine_parity.py
//! niram-red book                 Print every position and move of the opening book
//! ```

use std::time::Instant;

use crate::fen::{START_FEN, state_from_fen};
use crate::game_state::{State, position_key};
use crate::legal_moves::legal_moves;
use crate::make_move::{make_move, undo_move};
use crate::move_ordering::order_moves;
use crate::moves::{Move, move_to_uci};
use crate::opening_book::{Book, book_path, load_book};
use crate::search_tools::{MATE_SCORE, ThinkFn};
use crate::uci_engine;
use crate::uci_engine::set_position;

/// A version's evaluate(): the score of a position for the side to move.
pub type EvalFn = fn(&State) -> i32;

pub const BENCH_POSITIONS: [&str; 10] = [
    // The ten positions of Remus's compare_search.py and misc/scripts/remus_benchmark.py
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
const PARITY_MAX_DEPTH: i32 = 12; // The deepest search the parity check ever asks for

/// One bench position's result: the best move, the score, and the positions visited.
pub struct BenchLine {
    pub best: String,
    pub score: i32,
    pub nodes: u64,
    pub seconds: f64,
}

/// Search one bench position one depth at a time with no clock, the way think() does.
pub fn bench_position(fen: &str, think: ThinkFn, max_depth: i32) -> BenchLine {
    let mut state = state_from_fen(fen).expect("bench positions are valid FEN");
    let start = Instant::now();
    let mut last_info = String::new();
    let (best, info) = think(&mut state, None, max_depth, &mut |line| {
        last_info = line.to_string();
    });
    BenchLine {
        best: move_to_uci(best),
        score: score_from_info(&last_info),
        nodes: info.nodes,
        seconds: start.elapsed().as_secs_f64(),
    }
}

/// Return the total positions visited on all ten bench positions at one depth.
pub fn bench_nodes(think: ThinkFn, max_depth: i32) -> u64 {
    let mut total_nodes = 0;
    for fen in BENCH_POSITIONS {
        total_nodes += bench_position(fen, think, max_depth).nodes;
    }
    total_nodes
}

/// Print each bench position's move, score, positions, and speed, then the totals,
/// in the same layout as remus_benchmark.py.
fn bench(name: &str, think: ThinkFn, max_depth: i32) {
    println!("{name} (Rust), iterative deepening to depth {max_depth}");
    let mut total_nodes = 0;
    let mut total_seconds = 0.0;
    for (number, fen) in BENCH_POSITIONS.iter().enumerate() {
        let line = bench_position(fen, think, max_depth);
        total_nodes += line.nodes;
        total_seconds += line.seconds;
        println!(
            "{:2}. {:6} score {:>7}  nodes {:>10}  {:8.3} s  {:>12} nodes/s",
            number + 1,
            line.best,
            line.score,
            with_commas(line.nodes),
            line.seconds,
            with_commas((line.nodes as f64 / line.seconds) as u64)
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
                    MATE_SCORE - plies
                } else {
                    -(MATE_SCORE - plies)
                };
            }
            return value;
        }
    }
    0
}

/// Write a count with thousands separators, such as 197,281.
pub fn with_commas(count: u64) -> String {
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

/// Return moves as UCI text separated by spaces, such as "e2e4 g1f3".
fn moves_text(moves: &[Move]) -> String {
    let mut words = Vec::with_capacity(moves.len());
    for &mv in moves {
        words.push(move_to_uci(mv));
    }
    words.join(" ")
}

/// Return an info line without its timing words ("nps" and "time"), which differ
/// from run to run and from Remus, whose info lines leave them out.
fn without_timing(line: &str) -> String {
    let words: Vec<&str> = line.split_whitespace().collect();
    let mut kept = Vec::with_capacity(words.len());
    let mut index = 0;
    while index < words.len() {
        if words[index] == "nps" || words[index] == "time" {
            index += 2;
        } else {
            kept.push(words[index]);
            index += 1;
        }
    }
    kept.join(" ")
}

/// Run think() on a fresh copy of the position, with no clock, to `depth`, and
/// return its info lines, its best move, and the positions it visited.
fn search_to_depth(command: &str, think: ThinkFn, depth: i32) -> (Vec<String>, Move, u64) {
    let words: Vec<&str> = command.split_whitespace().collect();
    let mut state = set_position(&words).expect("parity positions are valid");
    let mut lines = Vec::new();
    let (best, info) = think(&mut state, None, depth, &mut |line| {
        lines.push(without_timing(line));
    });
    (lines, best, info.nodes)
}

/// Print, for each position of the file, what misc/scripts/engine_parity.py compares
/// with Remus: the position key, the evaluation, the legal moves in generation
/// order and in search order, the book moves, and a search to a fixed depth.
///
/// Each line of the file is "name<TAB>position command", such as
/// "start<TAB>position startpos moves e2e4". The search depth is the deepest one
/// that visits at most `budget` positions, so Remus can repeat it in a few seconds;
/// a search that ends early on a forced mate or a single legal move stops there.
fn parity(file_path: &str, budget: u64, think: ThinkFn, evaluate: EvalFn, use_book: bool) {
    let text = std::fs::read_to_string(file_path).expect("parity needs a readable file");
    let book = if use_book { load_book(&book_path()) } else { Book::new() };
    for line in text.lines() {
        let Some((name, command)) = line.split_once('\t') else {
            continue;
        };
        let words: Vec<&str> = command.split_whitespace().collect();
        let mut state = set_position(&words).expect("parity positions are valid");
        let moves = legal_moves(&mut state);
        println!("case\t{name}");
        println!("key\t{}", position_key(&state));
        println!("eval\t{}", evaluate(&state));
        println!("legal\t{}", moves_text(&moves));
        println!("ordered\t{}", moves_text(&order_moves(&moves, &state.board, None, &[])));
        let book_moves = book.get(&position_key(&state)).cloned().unwrap_or_default();
        println!("book\t{}", moves_text(&book_moves));
        if moves.is_empty() {
            println!("depth\t0");
            println!("best\t0000");
            continue;
        }
        let mut chosen = search_to_depth(command, think, 1);
        let mut depth = 1;
        while depth < PARITY_MAX_DEPTH && chosen.0.len() == depth as usize {
            let deeper = search_to_depth(command, think, depth + 1);
            if deeper.2 > budget {
                break;
            }
            chosen = deeper;
            depth += 1;
        }
        println!("depth\t{depth}");
        for info in &chosen.0 {
            println!("info\t{info}");
        }
        println!("nodes\t{}", chosen.2);
        println!("best\t{}", move_to_uci(chosen.1));
    }
}

/// Print every position of the opening book with its moves, one position per line
/// in key order, for misc/scripts/engine_parity.py to compare with Remus's book.
fn print_book() {
    let book = load_book(&book_path());
    let mut keys: Vec<&String> = book.keys().collect();
    keys.sort();
    for key in keys {
        println!("{key}\t{}", moves_text(&book[key]));
    }
}

/// Count the leaf positions of the legal move tree to a fixed depth.
pub fn perft(state: &mut State, depth: i32) -> u64 {
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

/// Run the command line: "bench", "perft", "parity", "book", or, with no argument,
/// the UCI loop.
pub fn run_command_line(name: &str, think: ThinkFn, evaluate: EvalFn, use_book: bool) {
    let arguments: Vec<String> = std::env::args().collect();
    let command = arguments.get(1).map(|text| text.as_str()).unwrap_or("uci");
    match command {
        "bench" => {
            let depth = arguments
                .get(2)
                .and_then(|text| text.parse().ok())
                .unwrap_or(BENCH_DEPTH);
            bench(name, think, depth);
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
            println!("perft({depth}) = {}", with_commas(count));
            println!("Total run time (sec): {:.3}", start.elapsed().as_secs_f64());
        }
        "parity" => {
            let file_path = arguments.get(2).expect("parity needs a file of positions");
            let budget = arguments.get(3).and_then(|text| text.parse().ok()).unwrap_or(30_000);
            parity(file_path, budget, think, evaluate, use_book);
        }
        "book" => print_book(),
        _ => uci_engine::run(name, think, use_book),
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
}
