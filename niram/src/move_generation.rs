//! move_generation.rs
//!
//! Generate pseudo-legal moves: every move the pieces can make by their movement
//! rules, before checking whether the move leaves the mover's own king in check.
//!
//! Directions are (row change, col change) pairs. Row 0 is rank 8, so White pawns
//! move toward row 0 (a row change of -1) and Black pawns toward row 7 (+1).

use crate::board::{Board, EMPTY, Square, piece_at};
use crate::game_state::{BLACK, State, WHITE, color_of};
use crate::moves::Move;

pub const KNIGHT_JUMPS: [Square; 8] = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)];
pub const KING_STEPS: [Square; 8] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)];
pub const ROOK_DIRECTIONS: [Square; 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)]; // Along ranks and files
pub const BISHOP_DIRECTIONS: [Square; 4] = [(-1, -1), (-1, 1), (1, -1), (1, 1)]; // Along diagonals
pub const QUEEN_DIRECTIONS: [Square; 8] = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)];
const PROMOTION_PIECES: [char; 4] = ['Q', 'R', 'B', 'N']; // A pawn on the last rank may become any of these

/// Return true if (row, col) is one of the 64 squares.
pub fn on_board(row: i32, col: i32) -> bool {
    (0..8).contains(&row) && (0..8).contains(&col)
}

/// Add the moves of a piece that jumps by fixed offsets (a knight or a king): a move
/// to every target on the board that does not hold a piece of the same color.
fn jump_moves(board: &Board, square: Square, color: char, offsets: &[Square], moves: &mut Vec<Move>) {
    let (row, col) = square;
    for (row_change, col_change) in offsets {
        let target = (row + row_change, col + col_change);
        if on_board(target.0, target.1) && color_of(piece_at(board, target)) != Some(color) {
            moves.push(Move::new(square, target));
        }
    }
}

/// Walk from a square in one direction and add the moves along the way, until the
/// walk reaches the edge or a piece. If that piece is an enemy, the capture is the
/// last move added.
fn slide(board: &Board, square: Square, direction: Square, color: char, moves: &mut Vec<Move>) {
    let (row_change, col_change) = direction;
    let (mut row, mut col) = (square.0 + row_change, square.1 + col_change);
    while on_board(row, col) {
        let target_piece = piece_at(board, (row, col));
        if target_piece == EMPTY {
            moves.push(Move::new(square, (row, col)));
        } else {
            if color_of(target_piece) != Some(color) {
                moves.push(Move::new(square, (row, col)));
            }
            break;
        }
        row += row_change;
        col += col_change;
    }
}

/// Add the moves of a rook, bishop, or queen, one direction at a time.
fn slider_moves(board: &Board, square: Square, color: char, directions: &[Square], moves: &mut Vec<Move>) {
    for direction in directions {
        slide(board, square, *direction, color, moves);
    }
}

/// Add a pawn move, or the four promotion moves if it reaches the last rank.
fn pawn_moves_to(square: Square, target: Square, color: char, moves: &mut Vec<Move>) {
    let last_row = if color == WHITE { 0 } else { 7 };
    if target.0 != last_row {
        moves.push(Move::new(square, target));
        return;
    }
    for piece in PROMOTION_PIECES {
        let promotion = if color == WHITE {
            piece
        } else {
            piece.to_ascii_lowercase()
        };
        moves.push(Move {
            from_square: square,
            to_square: target,
            promotion: Some(promotion),
        });
    }
}

/// Add a pawn's forward moves onto empty squares: one step, or two steps from its
/// starting rank. A pawn never captures straight ahead.
fn pawn_pushes(board: &Board, square: Square, color: char, moves: &mut Vec<Move>) {
    let (row, col) = square;
    let forward = if color == WHITE { -1 } else { 1 };
    let start_row = if color == WHITE { 6 } else { 1 };
    let one_step = (row + forward, col);
    if on_board(one_step.0, one_step.1) && piece_at(board, one_step) == EMPTY {
        pawn_moves_to(square, one_step, color, moves);
        let two_steps = (row + 2 * forward, col);
        if row == start_row && piece_at(board, two_steps) == EMPTY {
            moves.push(Move::new(square, two_steps));
        }
    }
}

/// Add a pawn's diagonal captures of enemy pieces.
fn pawn_captures(board: &Board, square: Square, color: char, moves: &mut Vec<Move>) {
    let (row, col) = square;
    let forward = if color == WHITE { -1 } else { 1 };
    for col_change in [-1, 1] {
        let target = (row + forward, col + col_change);
        if on_board(target.0, target.1) {
            let target_color = color_of(piece_at(board, target));
            if target_color.is_some() && target_color != Some(color) {
                pawn_moves_to(square, target, color, moves);
            }
        }
    }
}

/// Add the pseudo-legal moves of whatever piece stands on the square.
pub fn piece_moves(board: &Board, square: Square, moves: &mut Vec<Move>) {
    let piece = piece_at(board, square);
    let color = if piece.is_ascii_uppercase() { WHITE } else { BLACK };
    match piece.to_ascii_uppercase() {
        'N' => jump_moves(board, square, color, &KNIGHT_JUMPS, moves),
        'K' => jump_moves(board, square, color, &KING_STEPS, moves),
        'R' => slider_moves(board, square, color, &ROOK_DIRECTIONS, moves),
        'B' => slider_moves(board, square, color, &BISHOP_DIRECTIONS, moves),
        'Q' => slider_moves(board, square, color, &QUEEN_DIRECTIONS, moves),
        'P' => {
            pawn_pushes(board, square, color, moves);
            pawn_captures(board, square, color, moves);
        }
        _ => {}
    }
}

/// Add the en passant captures for the side to move: a capture onto the en passant
/// square by each pawn standing diagonally behind it.
fn en_passant_captures(state: &State, moves: &mut Vec<Move>) {
    let Some(target) = state.en_passant else {
        return;
    };
    let pawn = if state.turn == WHITE { 'P' } else { 'p' };
    let behind = if state.turn == WHITE { 1 } else { -1 };
    for col_change in [-1, 1] {
        let square = (target.0 + behind, target.1 + col_change);
        if on_board(square.0, square.1) && piece_at(&state.board, square) == pawn {
            moves.push(Move::new(square, target));
        }
    }
}

/// Return every pseudo-legal move for the side to move, including en passant.
/// Castling needs attack tests, so legal_moves adds it.
pub fn pseudo_legal_moves(state: &State) -> Vec<Move> {
    let mut moves = Vec::with_capacity(64);
    for row in 0..8 {
        for col in 0..8 {
            if color_of(state.board[row as usize][col as usize]) == Some(state.turn) {
                piece_moves(&state.board, (row, col), &mut moves);
            }
        }
    }
    en_passant_captures(state, &mut moves);
    moves
}
