//! legal_moves.rs
//!
//! Keep only the legal moves: a move is legal if, after it is made, the mover's own
//! king is not attacked. Testing after the move catches pins, discovered checks, and
//! a king stepping into check, all with one rule. Castling has extra conditions,
//! so castling_moves checks them before the move joins the list.

use crate::attacks::{in_check, is_square_attacked};
use crate::board::{EMPTY, Square, piece_at};
use crate::game_state::{State, WHITE, opponent};
use crate::make_move::{make_move, undo_move};
use crate::move_generation::pseudo_legal_moves;
use crate::moves::Move;

/// One castling move: the right it needs, the king's start and landing squares,
/// the squares that must be empty, and the square the king crosses.
struct Castle {
    right: char,
    king_from: Square,
    king_to: Square,
    must_be_empty: &'static [Square],
    crossed: Square,
}

const CASTLES: [Castle; 4] = [
    Castle {
        right: 'K',
        king_from: (7, 4),
        king_to: (7, 6),
        must_be_empty: &[(7, 5), (7, 6)],
        crossed: (7, 5),
    },
    Castle {
        right: 'Q',
        king_from: (7, 4),
        king_to: (7, 2),
        must_be_empty: &[(7, 3), (7, 2), (7, 1)],
        crossed: (7, 3),
    },
    Castle {
        right: 'k',
        king_from: (0, 4),
        king_to: (0, 6),
        must_be_empty: &[(0, 5), (0, 6)],
        crossed: (0, 5),
    },
    Castle {
        right: 'q',
        king_from: (0, 4),
        king_to: (0, 2),
        must_be_empty: &[(0, 3), (0, 2), (0, 1)],
        crossed: (0, 3),
    },
];

/// Return the castling moves the side to move may make: the right remains, the
/// squares between king and rook are empty, the king is not in check, and the
/// square the king crosses is not attacked. The legal filter checks the landing square.
pub fn castling_moves(state: &State) -> Vec<Move> {
    let color = state.turn;
    let enemy = opponent(color);
    let mut moves = Vec::new();
    for castle in &CASTLES {
        if !state.castling.contains(castle.right) || castle.right.is_ascii_uppercase() != (color == WHITE) {
            continue;
        }
        let mut path_is_empty = true;
        for square in castle.must_be_empty {
            if piece_at(&state.board, *square) != EMPTY {
                path_is_empty = false;
            }
        }
        if !path_is_empty {
            continue;
        }
        if in_check(state, color) || is_square_attacked(&state.board, castle.crossed, enemy) {
            continue;
        }
        moves.push(Move::new(castle.king_from, castle.king_to));
    }
    moves
}

/// Return every legal move for the side to move: the pseudo-legal moves that do not
/// leave the mover's king in check. Each move is made and undone, so the state ends
/// unchanged.
pub fn legal_moves(state: &mut State) -> Vec<Move> {
    let mover = state.turn;
    let mut candidates = pseudo_legal_moves(state);
    candidates.extend(castling_moves(state));
    let mut moves = Vec::with_capacity(candidates.len());
    for mv in candidates {
        let undo = make_move(state, mv);
        if !in_check(state, mover) {
            moves.push(mv);
        }
        undo_move(state, undo);
    }
    moves
}
