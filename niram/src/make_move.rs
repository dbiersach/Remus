//! make_move.rs
//!
//! Make a move on the game state, and undo it exactly. make_move returns an undo
//! record that holds everything the move changed, so undo_move can put it all back.
//!
//! Three moves change more than two squares: castling also moves a rook, en passant
//! removes a pawn that is not on the landing square, and promotion swaps the pawn
//! for a new piece.

use crate::board::{EMPTY, Square, piece_at, set_piece};
use crate::game_state::{BLACK, State, opponent, position_key};
use crate::moves::Move;

const CASTLING_SQUARES: [(Square, &str); 6] = [
    // A move from or to one of these squares removes these rights
    ((7, 4), "KQ"), // e1, the White king
    ((7, 7), "K"),  // h1, White's kingside rook
    ((7, 0), "Q"),  // a1, White's queenside rook
    ((0, 4), "kq"), // e8, the Black king
    ((0, 7), "k"),  // h8, Black's kingside rook
    ((0, 0), "q"),  // a8, Black's queenside rook
];

/// Everything make_move changed, so undo_move can put it back.
#[derive(Clone, Debug)]
pub struct Undo {
    pub mv: Move,
    pub piece: char,    // The piece that moved
    pub captured: char, // The piece it captured, or EMPTY
    castling: String,
    en_passant: Option<Square>,
    halfmove_clock: u32,
    fullmove_number: u32,
    rook_move: Option<(Square, Square)>,
    en_passant_victim: Option<Square>,
}

/// Return the castling rights left after a move, such as "Qkq" after the h1 rook moves.
pub fn update_castling_rights(rights: &str, mv: Move) -> String {
    let mut rights = rights.to_string();
    for square in [mv.from_square, mv.to_square] {
        for (castling_square, letters) in CASTLING_SQUARES {
            if castling_square == square {
                for letter in letters.chars() {
                    rights = rights.replace(letter, "");
                }
            }
        }
    }
    rights
}

/// Return the square of the pawn an en passant capture removes: on the row the
/// capture starts from, in the column it lands in.
fn en_passant_victim_square(mv: Move) -> Square {
    (mv.from_square.0, mv.to_square.1)
}

/// Return the (from, to) squares of the rook in a castling move.
fn castling_rook_move(mv: Move) -> (Square, Square) {
    let row = mv.from_square.0;
    if mv.to_square.1 == 6 {
        return ((row, 7), (row, 5)); // Kingside: the rook goes from the h-file to the f-file
    }
    ((row, 0), (row, 3)) // Queenside: the rook goes from the a-file to the d-file
}

/// Make any move, including castling, en passant, and promotion, and return the
/// record needed to undo it.
pub fn make_move(state: &mut State, mv: Move) -> Undo {
    let piece = piece_at(&state.board, mv.from_square);
    let mut undo = Undo {
        mv,
        piece,
        captured: piece_at(&state.board, mv.to_square),
        castling: state.castling.clone(),
        en_passant: state.en_passant,
        halfmove_clock: state.halfmove_clock,
        fullmove_number: state.fullmove_number,
        rook_move: None,
        en_passant_victim: None,
    };

    // En passant: a pawn moves diagonally onto the empty en passant target square
    let is_pawn = piece.to_ascii_uppercase() == 'P';
    if is_pawn && Some(mv.to_square) == state.en_passant {
        let victim = en_passant_victim_square(mv);
        undo.en_passant_victim = Some(victim);
        undo.captured = piece_at(&state.board, victim);
        set_piece(&mut state.board, victim, EMPTY);
    }

    // Promotion: the pawn becomes the new piece on the last rank
    let landing_piece = mv.promotion.unwrap_or(piece);
    set_piece(&mut state.board, mv.to_square, landing_piece);
    set_piece(&mut state.board, mv.from_square, EMPTY);

    // Castling: a king moving two squares also moves its rook
    if piece.to_ascii_uppercase() == 'K' && (mv.to_square.1 - mv.from_square.1).abs() == 2 {
        let (rook_from, rook_to) = castling_rook_move(mv);
        let rook = piece_at(&state.board, rook_from);
        set_piece(&mut state.board, rook_to, rook);
        set_piece(&mut state.board, rook_from, EMPTY);
        undo.rook_move = Some((rook_from, rook_to));
    }

    // The fifty-move clock restarts after a capture or a pawn move
    if undo.captured != EMPTY || is_pawn {
        state.halfmove_clock = 0;
    } else {
        state.halfmove_clock += 1;
    }
    if state.turn == BLACK {
        state.fullmove_number += 1;
    }

    // A double step leaves an en passant target on the square the pawn skipped
    state.en_passant = None;
    if is_pawn && (mv.to_square.0 - mv.from_square.0).abs() == 2 {
        let skipped_row = (mv.from_square.0 + mv.to_square.0) / 2;
        state.en_passant = Some((skipped_row, mv.from_square.1));
    }
    state.castling = update_castling_rights(&state.castling, mv);
    state.turn = opponent(state.turn);
    let key = position_key(state);
    state.history.push(key);
    undo
}

/// Take back the move described by an undo record.
pub fn undo_move(state: &mut State, undo: Undo) {
    let mv = undo.mv;
    state.history.pop();
    set_piece(&mut state.board, mv.from_square, undo.piece);
    match undo.en_passant_victim {
        None => set_piece(&mut state.board, mv.to_square, undo.captured),
        Some(victim) => {
            set_piece(&mut state.board, mv.to_square, EMPTY);
            set_piece(&mut state.board, victim, undo.captured);
        }
    }
    if let Some((rook_from, rook_to)) = undo.rook_move {
        let rook = piece_at(&state.board, rook_to);
        set_piece(&mut state.board, rook_from, rook);
        set_piece(&mut state.board, rook_to, EMPTY);
    }
    state.turn = opponent(state.turn);
    state.castling = undo.castling;
    state.en_passant = undo.en_passant;
    state.halfmove_clock = undo.halfmove_clock;
    state.fullmove_number = undo.fullmove_number;
}
