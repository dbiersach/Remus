//! uci_engine.rs
//!
//! Talk to a chess GUI such as Lucas Chess through the Universal Chess Interface
//! (UCI). The GUI sends one command per line on standard input, and Niram answers on
//! standard output. Debug text goes to standard error, where the GUI ignores it.
//!
//! The search runs in a thread, so Niram can still answer "isready" and obey "stop"
//! while it thinks. Niram plays a move from the opening book first, while the
//! position is in the book.

use std::io::{BufRead, Write};
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread::JoinHandle;

use crate::fen::{START_FEN, state_from_fen};
use crate::game_state::{State, WHITE};
use crate::legal_moves::legal_moves;
use crate::make_move::make_move;
use crate::moves::{move_from_uci, move_to_uci};
use crate::opening_book::{book_move, book_path, load_book};
use crate::search::think;

const DEFAULT_SECONDS: f64 = 2.0; // Thinking time when the GUI gives no clock

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
/// otherwise DEFAULT_SECONDS.
fn thinking_time(words: &[&str], white_to_move: bool) -> f64 {
    let value = |name: &str| -> Option<f64> {
        let index = words.iter().position(|&word| word == name)?;
        let milliseconds: f64 = words.get(index + 1)?.parse().ok()?;
        Some(milliseconds / 1000.0) // Milliseconds to seconds
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
        return (remaining / 30.0 + value(increment).unwrap_or(0.0) / 2.0).max(0.05);
    }
    DEFAULT_SECONDS
}

/// Read UCI commands until "quit" or the end of input.
pub fn run() {
    let mut state = state_from_fen(START_FEN).expect("START_FEN is valid");
    let book = load_book(&book_path());
    let stop = Arc::new(AtomicBool::new(false));
    let mut worker: Option<JoinHandle<()>> = None;
    for line in std::io::stdin().lock().lines() {
        let Ok(line) = line else { break };
        let words: Vec<&str> = line.split_whitespace().collect();
        let Some(&command) = words.first() else { continue };
        if matches!(command, "position" | "ucinewgame" | "go")
            && let Some(handle) = worker.take()
        {
            let _ = handle.join(); // Finish the last search before changing the position
        }
        match command {
            "uci" => {
                send("id name Niram");
                send("id author Turning a Chess Engine into Science AI");
                send("uciok");
            }
            "isready" => send("readyok"),
            "ucinewgame" => state = state_from_fen(START_FEN).expect("START_FEN is valid"),
            "position" => match set_position(&words) {
                Ok(new_state) => state = new_state,
                Err(message) => eprintln!("Niram cannot read the position: {message}"),
            },
            "go" => {
                if legal_moves(&mut state).is_empty() {
                    send("bestmove 0000");
                } else if let Some(opening) = book_move(&book, &state) {
                    send(&format!("bestmove {}", move_to_uci(opening)));
                } else {
                    stop.store(false, Ordering::Relaxed);
                    let seconds = thinking_time(&words, state.turn == WHITE);
                    let mut search_state = state.clone();
                    let search_stop = Arc::clone(&stop);
                    worker = Some(std::thread::spawn(move || {
                        let (best, _) = think(&mut search_state, Some(seconds), 64, Some(search_stop), &mut |line| {
                            send(line)
                        });
                        send(&format!("bestmove {}", move_to_uci(best)));
                    }));
                }
            }
            "stop" => stop.store(true, Ordering::Relaxed),
            "quit" => {
                stop.store(true, Ordering::Relaxed);
                break;
            }
            _ => eprintln!("Niram ignores: {line}"),
        }
    }
    if let Some(handle) = worker {
        let _ = handle.join(); // Input ended: let the last search send its move
    }
}
