//! uci_engine.rs
//!
//! Talk to a chess GUI such as Lucas Chess, or to a match script, through the
//! Universal Chess Interface (UCI). The GUI sends one command per line on standard
//! input, and Niram answers on standard output. Debug text goes to standard error,
//! where the GUI ignores it.
//!
//! Niram reads one command, answers it, and only then reads the next, so a search
//! always ends with a "bestmove" before Niram listens again. The versions with an
//! opening book (GREEN and GOLD) play a book move first, while the position is in
//! the book.

use std::io::{BufRead, Write};

use crate::fen::{START_FEN, state_from_fen};
use crate::game_state::{State, WHITE};
use crate::legal_moves::legal_moves;
use crate::make_move::make_move;
use crate::moves::{move_from_uci, move_to_uci};
use crate::opening_book::{Book, book_move, book_path, load_book};
use crate::search_tools::ThinkFn;

const DEFAULT_SECONDS: f64 = 2.0; // Thinking time when the GUI gives no clock
const RESERVE_SECONDS: f64 = 3.0; // Clock time Niram never plans to spend, to pay for sending moves
const MIN_SECONDS: f64 = 0.01; // The shortest think, for when the clock is nearly empty

/// Send one line to the GUI and flush it, so it leaves at once.
fn send(text: &str) {
    let mut out = std::io::stdout().lock();
    let _ = writeln!(out, "{text}");
    let _ = out.flush();
}

/// Build the state that a "position" command describes, such as
/// "position startpos moves e2e4 e7e5".
fn set_position(words: &[&str]) -> Result<State, String> {
    let moves_at = words.iter().position(|&word| word == "moves");
    let mut state = if words.get(1) == Some(&"startpos") {
        state_from_fen(START_FEN)?
    } else {
        let fen_end = moves_at.unwrap_or(words.len());
        state_from_fen(&words[2..fen_end].join(" "))?
    };
    if let Some(moves_at) = moves_at {
        for text in &words[moves_at + 1..] {
            let mv = move_from_uci(text, state.turn == WHITE)?;
            make_move(&mut state, mv);
        }
    }
    Ok(state)
}

/// Decide how many seconds to think from a "go" command: "movetime" if the GUI gives
/// one; otherwise a thirtieth of the remaining time plus half the increment;
/// otherwise DEFAULT_SECONDS. The remaining time leaves out RESERVE_SECONDS, because
/// every move also costs time the search does not see, and one move never takes
/// more than half of the spare time.
fn thinking_time(words: &[&str], white_to_move: bool) -> f64 {
    let value = |name: &str| -> Option<f64> {
        let index = words.iter().position(|&word| word == name)?;
        let milliseconds: f64 = words.get(index + 1)?.parse().ok()?;
        Some(milliseconds / 1000.0) // The GUI counts milliseconds, and Niram seconds
    };
    if let Some(movetime) = value("movetime") {
        return movetime;
    }
    let (clock, increment) = if white_to_move {
        ("wtime", "winc")
    } else {
        ("btime", "binc")
    };
    if let Some(remaining) = value(clock) {
        let spare = remaining - RESERVE_SECONDS;
        let seconds = spare / 30.0 + value(increment).unwrap_or(0.0) / 2.0;
        return seconds.min(spare / 2.0).max(MIN_SECONDS);
    }
    DEFAULT_SECONDS
}

/// Read UCI commands until "quit" or the end of input. `name` is the engine's name,
/// such as "Niram-RED", `think` is its search, and `use_book` says whether it plays
/// from the opening book.
pub fn run(name: &str, think: ThinkFn, use_book: bool) {
    let mut state = state_from_fen(START_FEN).expect("START_FEN is valid");
    let book = if use_book { load_book(&book_path()) } else { Book::new() };
    for line in std::io::stdin().lock().lines() {
        let Ok(line) = line else { break };
        let words: Vec<&str> = line.split_whitespace().collect();
        let Some(&command) = words.first() else { continue };
        match command {
            "uci" => {
                send(&format!("id name {name}"));
                send("id author Turning a Chess Engine into Science AI");
                send("uciok");
            }
            "isready" => send("readyok"),
            "ucinewgame" => state = state_from_fen(START_FEN).expect("START_FEN is valid"),
            "position" => match set_position(&words) {
                Ok(new_state) => state = new_state,
                Err(message) => eprintln!("{name} cannot read the position: {message}"),
            },
            "go" => {
                if legal_moves(&mut state).is_empty() {
                    send("bestmove 0000");
                } else if let Some(opening) = book_move(&book, &state) {
                    send(&format!("bestmove {}", move_to_uci(opening)));
                } else {
                    let seconds = thinking_time(&words, state.turn == WHITE);
                    let (best, _) = think(&mut state, Some(seconds), 64, &mut |line| send(line));
                    send(&format!("bestmove {}", move_to_uci(best)));
                }
            }
            "stop" => {} // Each search ends on its own clock before Niram reads "stop"
            "quit" => break,
            _ => eprintln!("{name} ignores: {line}"),
        }
    }
}
