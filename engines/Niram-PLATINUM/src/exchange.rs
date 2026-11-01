//! exchange.rs
//!
//! Remus-PLATINUM's exchange.py, line for line. Static exchange evaluation (SEE):
//! add up a capture and every recapture on the same square, each side always
//! taking with its least valuable piece, without searching. Quiescence search skips
//! a capture whose exchange loses material.

use crate::board::{Board, EMPTY, Square, piece_at};
use crate::evaluation::piece_value;
use crate::moves::Move;

const KING_VALUE: i32 = 10_000; // The king can take last, but no exchange may win the king
const KNIGHT_JUMPS: [(i32, i32); 8] = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)];

/// Return a piece's value in an exchange: its centipawns, or KING_VALUE.
fn exchange_value(piece: char) -> i32 {
    let kind = piece.to_ascii_uppercase();
    if kind == 'K' { KING_VALUE } else { piece_value(kind) }
}

/// Return true if the piece on `start` attacks `target`. A rook, bishop, or queen
/// needs every square between the two to be empty.
fn attacks_square(board: &Board, start: Square, target: Square) -> bool {
    let piece = piece_at(board, start);
    let kind = piece.to_ascii_uppercase();
    let row_gap = target.0 - start.0;
    let col_gap = target.1 - start.1;
    match kind {
        'P' => {
            let forward = if piece == 'P' { -1 } else { 1 }; // White pawns move toward row 0
            return row_gap == forward && col_gap.abs() == 1;
        }
        'N' => return KNIGHT_JUMPS.contains(&(row_gap, col_gap)),
        'K' => return row_gap.abs().max(col_gap.abs()) == 1,
        _ => {}
    }
    let straight = row_gap == 0 || col_gap == 0;
    let diagonal = row_gap.abs() == col_gap.abs();
    if row_gap == 0 && col_gap == 0 {
        return false;
    }
    if kind == 'R' && !straight {
        return false;
    }
    if kind == 'B' && !diagonal {
        return false;
    }
    if kind == 'Q' && !(straight || diagonal) {
        return false;
    }
    let row_step = row_gap.signum();
    let col_step = col_gap.signum();
    let (mut row, mut col) = (start.0 + row_step, start.1 + col_step);
    while (row, col) != target {
        if board[row as usize][col as usize] != EMPTY {
            return false; // A piece in between blocks the line
        }
        row += row_step;
        col += col_step;
    }
    true
}

/// Return the square of the cheapest piece of one side attacking `target`, or None.
fn least_valuable_attacker(board: &Board, target: Square, white: bool) -> Option<Square> {
    let mut best: Option<Square> = None;
    let mut best_value = 0;
    for row in 0..8 {
        for col in 0..8 {
            let piece = board[row as usize][col as usize];
            if piece == EMPTY || piece.is_ascii_uppercase() != white {
                continue;
            }
            let value = exchange_value(piece);
            if best.is_some() && value >= best_value {
                continue;
            }
            if attacks_square(board, (row, col), target) {
                best = Some((row, col));
                best_value = value;
            }
        }
    }
    best
}

/// Return the centipawns a capture wins or loses once every recapture is made,
/// each side recapturing with its cheapest piece and stopping when one more
/// recapture would lose. A queen taking a pawn defended by a knight returns -800.
pub fn static_exchange(board: &Board, mv: Move) -> i32 {
    let mut work = *board; // A copy, so pieces can leave and x-rays open
    let target = mv.to_square;
    let mut gains = vec![exchange_value(piece_at(&work, target))];
    let mover = piece_at(&work, mv.from_square);
    let mut on_square = exchange_value(mover);
    work[mv.from_square.0 as usize][mv.from_square.1 as usize] = EMPTY;
    work[target.0 as usize][target.1 as usize] = mover;
    let mut white = !mover.is_ascii_uppercase(); // The side that recaptures next
    while let Some(attacker) = least_valuable_attacker(&work, target, white) {
        let last = *gains.last().expect("gains starts with the victim");
        gains.push(on_square - last);
        let piece = piece_at(&work, attacker);
        on_square = exchange_value(piece);
        work[attacker.0 as usize][attacker.1 as usize] = EMPTY;
        work[target.0 as usize][target.1 as usize] = piece;
        white = !white;
    }
    let mut index = gains.len() - 1;
    while index > 0 {
        gains[index - 1] = -(-gains[index - 1]).max(gains[index]);
        index -= 1;
    }
    gains[0]
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::fen::state_from_fen;

    #[test]
    fn queen_takes_defended_pawn() {
        let state = state_from_fen("4k3/8/5n2/3p4/8/8/8/3QK3 w - - 0 1").unwrap();
        let mv = Move {
            from_square: (7, 3),
            to_square: (3, 3),
            promotion: None,
        };
        assert_eq!(static_exchange(&state.board, mv), -800);
    }

    #[test]
    fn rook_with_backup_wins_the_pawn() {
        let state = state_from_fen("3rk3/8/8/3p4/8/8/3R4/3RK3 w - - 0 1").unwrap();
        let mv = Move {
            from_square: (6, 3),
            to_square: (3, 3),
            promotion: None,
        };
        assert_eq!(static_exchange(&state.board, mv), 100);
    }
}
