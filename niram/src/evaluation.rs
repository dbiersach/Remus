//! evaluation.rs
//!
//! Score a position in centipawns (hundredths of a pawn) without looking ahead.
//! A positive score is good for White. Five terms make up the score:
//!
//! 1. Material: the value of every piece on the board.
//! 2. Placement: a bonus or penalty from a piece-square table, such as a knight in
//!    the center (it attacks eight squares) against a knight in the corner (two).
//! 3. Pawn structure: penalties for doubled and isolated pawns, a bonus for passed pawns.
//! 4. Mating: with a big material lead, drive the losing king to the edge and bring
//!    the winning king close, so Niram can finish off a won endgame.
//! 5. King safety: while the enemy queen is on the board, a bonus for each pawn that
//!    shelters the king from in front.
//!
//! Each table is written from White's side, row 0 (rank 8) first. A Black piece
//! reads the table upside down, so its row 7 uses the table's row 0.

use crate::board::{Board, EMPTY};
use crate::game_state::{State, WHITE};

type Table = [[i32; 8]; 8];

const PAWN_TABLE: Table = [
    // Pawns gain as they advance, most in the center
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0],
];
const KNIGHT_TABLE: Table = [
    // Knights belong in the center, where they reach eight squares
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
];
const BISHOP_TABLE: Table = [
    // Bishops like long open diagonals, not corners
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20],
];
const ROOK_TABLE: Table = [
    // Rooks like the seventh rank and the center files
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0],
];
const KING_TABLE: Table = [
    // The king hides behind its pawns until the endgame
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20],
];
const QUEEN_TABLE: Table = [[0; 8]; 8]; // The queen is strong anywhere

const DOUBLED_PAWN: i32 = 8; // Penalty for each pawn that shares its file with another of its color
const ISOLATED_PAWN: i32 = 20; // Penalty for a pawn with no friendly pawn on either neighboring file
const PASSED_PAWN: [i32; 6] = [0, 10, 20, 40, 60, 70]; // Bonus for a passed pawn, by squares advanced
const CENTER_DISTANCE: [i32; 8] = [3, 2, 1, 0, 0, 1, 2, 3]; // How far a row or column is from the center
const MATING_MARGIN: i32 = 200; // A lead of at least a rook for a bishop starts the mating term
const WEAK_SIDE_LIMIT: i32 = 600; // ... when the losing side has at most two bishops' worth left
const SHIELD_PAWN: i32 = 15; // Bonus for each pawn on the king's file or a neighbor, 1 or 2 rows ahead

/// Return a piece's value in centipawns, from its uppercase letter.
pub fn piece_value(kind: char) -> i32 {
    match kind {
        'P' => 100,
        'N' => 300,
        'B' => 300,
        'R' => 500,
        'Q' => 900,
        _ => 0, // The king is never traded, so it counts 0
    }
}

/// Return the piece-square table for a piece, from its uppercase letter.
fn placement_table(kind: char) -> &'static Table {
    match kind {
        'P' => &PAWN_TABLE,
        'N' => &KNIGHT_TABLE,
        'B' => &BISHOP_TABLE,
        'R' => &ROOK_TABLE,
        'Q' => &QUEEN_TABLE,
        _ => &KING_TABLE,
    }
}

/// Return the material balance in centipawns: White's piece values minus Black's.
pub fn material(board: &Board) -> i32 {
    let mut score = 0;
    for row in board {
        for &piece in row {
            if piece == EMPTY {
                continue;
            }
            if piece.is_ascii_uppercase() {
                score += piece_value(piece);
            } else {
                score -= piece_value(piece.to_ascii_uppercase());
            }
        }
    }
    score
}

/// Return the piece-square bonus in centipawns, positive when it favors White.
pub fn placement(board: &Board) -> i32 {
    let mut score = 0;
    for row in 0..8 {
        for col in 0..8 {
            let piece = board[row][col];
            if piece == EMPTY {
                continue;
            }
            let table = placement_table(piece.to_ascii_uppercase());
            if piece.is_ascii_uppercase() {
                score += table[row][col];
            } else {
                score -= table[7 - row][col]; // Black reads the table upside down
            }
        }
    }
    score
}

/// Score the pawn structure, positive when it favors White: for each side, a
/// penalty for every doubled and every isolated pawn, and a bonus for every passed
/// pawn (no enemy pawn ahead of it on its own file or a neighboring file), bigger
/// the further it has advanced.
pub fn pawn_structure(board: &Board) -> i32 {
    let mut score = 0;
    for (pawn, enemy, sign) in [('P', 'p', 1), ('p', 'P', -1)] {
        let mut files = [0; 8];
        for row in 0..8 {
            for col in 0..8 {
                if board[row][col] == pawn {
                    files[col] += 1;
                }
            }
        }
        for row in 0..8 {
            for col in 0..8 {
                if board[row][col] != pawn {
                    continue;
                }
                if files[col] > 1 {
                    score -= sign * DOUBLED_PAWN;
                }
                let left = if col > 0 { files[col - 1] } else { 0 };
                let right = if col < 7 { files[col + 1] } else { 0 };
                if left == 0 && right == 0 {
                    score -= sign * ISOLATED_PAWN;
                }
                // White moves toward row 0, Black toward row 7
                let ahead = if pawn == 'P' { 0..row } else { row + 1..8 };
                let mut blocked = false;
                for ahead_row in ahead {
                    for ahead_col in [col as i32 - 1, col as i32, col as i32 + 1] {
                        if (0..8).contains(&ahead_col) && board[ahead_row][ahead_col as usize] == enemy {
                            blocked = true;
                        }
                    }
                }
                if !blocked {
                    let advanced = if pawn == 'P' { 6 - row } else { row - 1 };
                    score += sign * PASSED_PAWN[advanced];
                }
            }
        }
    }
    score
}

/// Return a bonus for cornering the losing king, positive when it favors White.
/// It is 0 unless one side leads by at least MATING_MARGIN and the other side has
/// at most WEAK_SIDE_LIMIT of material left. Then it is 10 points for each step the
/// losing king stands from the center, and 4 points for each step the winning king
/// has closed toward it.
pub fn mating_bonus(board: &Board) -> i32 {
    let mut white_material = 0;
    let mut black_material = 0;
    let mut white_king = (0, 0);
    let mut black_king = (0, 0);
    for row in 0..8 {
        for col in 0..8 {
            let piece = board[row][col];
            if piece == 'K' {
                white_king = (row as i32, col as i32);
            } else if piece == 'k' {
                black_king = (row as i32, col as i32);
            } else if piece != EMPTY {
                if piece.is_ascii_uppercase() {
                    white_material += piece_value(piece);
                } else {
                    black_material += piece_value(piece.to_ascii_uppercase());
                }
            }
        }
    }
    let lead = white_material - black_material;
    let weaker = white_material.min(black_material);
    if lead.abs() < MATING_MARGIN || weaker > WEAK_SIDE_LIMIT {
        return 0;
    }
    let (winner, loser) = if lead > 0 {
        (white_king, black_king)
    } else {
        (black_king, white_king)
    };
    let edge = CENTER_DISTANCE[loser.0 as usize] + CENTER_DISTANCE[loser.1 as usize];
    let kings_apart = (loser.0 - winner.0).abs().max((loser.1 - winner.1).abs());
    let bonus = 10 * edge + 4 * (7 - kings_apart);
    if lead > 0 { bonus } else { -bonus }
}

/// Score the pawn shields in front of both kings, positive when it favors White.
/// For each king facing an enemy queen: SHIELD_PAWN for every file (the king's own
/// and its two neighbors) with a friendly pawn one or two rows in front of the king.
pub fn king_safety(board: &Board) -> i32 {
    let mut score = 0;
    // White's pawns stand in front of its king at smaller rows, since row 0 is rank 8
    for (king, pawn, enemy_queen, forward, sign) in [('K', 'P', 'q', -1, 1), ('k', 'p', 'Q', 1, -1)] {
        let mut queen_on_board = false;
        for row in board {
            if row.contains(&enemy_queen) {
                queen_on_board = true;
            }
        }
        if !queen_on_board {
            continue;
        }
        for row in 0..8 {
            for col in 0..8 {
                if board[row as usize][col as usize] != king {
                    continue;
                }
                for file in [col - 1, col, col + 1] {
                    if !(0..8).contains(&file) {
                        continue;
                    }
                    for step in [1, 2] {
                        let ahead: i32 = row + forward * step;
                        if (0..8).contains(&ahead) && board[ahead as usize][file as usize] == pawn {
                            score += sign * SHIELD_PAWN;
                            break;
                        }
                    }
                }
            }
        }
    }
    score
}

/// Score the position for the side to move: all five terms, positive when the side
/// to move stands better. Negamax search needs the score from the mover's side.
pub fn evaluate(state: &State) -> i32 {
    let board = &state.board;
    let white_score =
        material(board) + placement(board) + pawn_structure(board) + mating_bonus(board) + king_safety(board);
    if state.turn == WHITE { white_score } else { -white_score }
}
