//! evaluation.rs
//!
//! The terms that score a position in centipawns (hundredths of a pawn) without
//! looking ahead. A positive term is good for White. evaluate() at the end adds all
//! five, the way Remus-GOLD's evaluation.py does:
//!
//! 1. Material: the value of every piece on the board.
//! 2. Placement: a bonus or penalty from a piece-square table, such as a knight in
//!    the center (it attacks eight squares) against a knight in the corner (two).
//! 3. Pawn structure (PURPLE): penalties for doubled and isolated pawns, a bonus for passed pawns.
//! 4. Mating (CYAN): with a big material lead, drive the losing king to the edge and bring
//!    the winning king close, so Niram can finish off a won endgame.
//! 5. King safety (GRAY): while the enemy queen is on the board, a bonus for each pawn that
//!    shelters the king from in front.
//!
//! Niram-PLATINUM adds five more, the same as Remus-PLATINUM:
//!
//! 6. Tapered king placement and passed pawns, blended by the game phase.
//! 7. Pawn race: the rule of the square in a pawn ending.
//! 8. Mobility: a bonus for each square a knight, bishop, rook, or queen reaches.
//! 9. Bishop pair.
//! 10. Rooks on open and half-open files.
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
const KING_ENDGAME_TABLE: Table = [
    // With few pieces left, the king walks to the center
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50],
];
const TOTAL_PHASE: i32 = 24; // The phase with every piece on the board: 4 + 4 + 8 + 8
const UNSTOPPABLE_PAWN: i32 = 400; // Bonus for a passed pawn the defending king cannot catch
const BISHOP_PAIR: i32 = 30; // Bonus for a side that still has two bishops
const ROOK_OPEN_FILE: i32 = 20; // Bonus for a rook on a file with no pawns at all
const ROOK_HALF_OPEN_FILE: i32 = 10; // Bonus for a rook on a file with no friendly pawn
const KNIGHT_JUMPS: [(i32, i32); 8] = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)];
const ROOK_DIRECTIONS: [(i32, i32); 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)];
const BISHOP_DIRECTIONS: [(i32, i32); 4] = [(-1, -1), (-1, 1), (1, -1), (1, 1)];

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
            if piece == EMPTY || piece.to_ascii_uppercase() == 'K' {
                continue; // The king's tables are blended by the game phase in tapered_terms()
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

/// What each piece adds to the game phase.
fn phase_weight(kind: char) -> i32 {
    match kind {
        'N' | 'B' => 1,
        'R' => 2,
        'Q' => 4,
        _ => 0,
    }
}

/// Mobility bonus for each square a piece reaches.
fn mobility_weight(kind: char) -> i32 {
    match kind {
        'N' | 'B' => 4,
        'R' => 2,
        'Q' => 1,
        _ => 0,
    }
}

/// Return how much of the middlegame is left, from TOTAL_PHASE down to 0.
pub fn game_phase(board: &Board) -> i32 {
    let mut phase = 0;
    for row in board {
        for &piece in row {
            if piece != EMPTY {
                phase += phase_weight(piece.to_ascii_uppercase());
            }
        }
    }
    phase.min(TOTAL_PHASE)
}

/// Blend a middlegame and an endgame score by the phase. div_euclid rounds down,
/// the way Python's // does, so negative scores match Remus-PLATINUM.
pub fn taper(middlegame: i32, endgame: i32, phase: i32) -> i32 {
    (middlegame * phase + endgame * (TOTAL_PHASE - phase)).div_euclid(TOTAL_PHASE)
}

/// Return true if no enemy pawn stands ahead of this pawn on its file or a neighbor.
fn is_passed(board: &Board, row: usize, col: usize) -> bool {
    let pawn = board[row][col];
    let enemy = if pawn == 'P' { 'p' } else { 'P' };
    let ahead = if pawn == 'P' { 0..row } else { row + 1..8 };
    for ahead_row in ahead {
        for ahead_col in [col as i32 - 1, col as i32, col as i32 + 1] {
            if (0..8).contains(&ahead_col) && board[ahead_row][ahead_col as usize] == enemy {
                return false;
            }
        }
    }
    true
}

/// Score the king's square and the passed pawns by the game phase, positive when
/// it favors White: the king blends KING_TABLE and KING_ENDGAME_TABLE, and a passed
/// pawn earns its PASSED_PAWN bonus once more in the endgame.
pub fn tapered_terms(board: &Board) -> i32 {
    let mut middlegame = 0;
    let mut endgame = 0;
    for row in 0..8 {
        for col in 0..8 {
            let piece = board[row][col];
            if piece == 'K' {
                middlegame += KING_TABLE[row][col];
                endgame += KING_ENDGAME_TABLE[row][col];
            } else if piece == 'k' {
                middlegame -= KING_TABLE[7 - row][col];
                endgame -= KING_ENDGAME_TABLE[7 - row][col];
            } else if piece == 'P' && is_passed(board, row, col) {
                endgame += PASSED_PAWN[6 - row];
            } else if piece == 'p' && is_passed(board, row, col) {
                endgame -= PASSED_PAWN[row - 1];
            }
        }
    }
    taper(middlegame, endgame, game_phase(board))
}

/// Score passed pawns the defending king cannot catch (the rule of the square), in
/// a pawn ending, positive when it favors White. A defending king that moves first
/// gains a step.
pub fn pawn_race(board: &Board, turn: char) -> i32 {
    let mut white_king: Option<(i32, i32)> = None;
    let mut black_king: Option<(i32, i32)> = None;
    for row in 0..8 {
        for col in 0..8 {
            if board[row][col] == 'K' {
                white_king = Some((row as i32, col as i32));
            } else if board[row][col] == 'k' {
                black_king = Some((row as i32, col as i32));
            }
        }
    }
    let mut score = 0;
    for (pawn, defender_king, defender_color, sign) in [('P', black_king, 'b', 1), ('p', white_king, 'w', -1)] {
        let Some((king_row, king_col)) = defender_king else {
            continue;
        };
        let defender_pieces = if defender_color == 'b' { "nbrq" } else { "NBRQ" };
        let mut has_defender_piece = false;
        for row in board {
            for &piece in row {
                if defender_pieces.contains(piece) {
                    has_defender_piece = true;
                }
            }
        }
        if has_defender_piece {
            continue;
        }
        let mut unstoppable = false;
        for row in 0..8 {
            for col in 0..8 {
                if board[row][col] != pawn || !is_passed(board, row, col) {
                    continue;
                }
                let (promote_row, moves_to_go) = if pawn == 'P' {
                    (0, if row == 6 { 5 } else { row as i32 })
                } else {
                    (7, if row == 1 { 5 } else { 7 - row as i32 })
                };
                let mut king_steps = (king_row - promote_row).abs().max((king_col - col as i32).abs());
                if turn == defender_color {
                    king_steps -= 1; // The defending king moves first
                }
                if king_steps > moves_to_go {
                    unstoppable = true;
                }
            }
        }
        if unstoppable {
            score += sign * UNSTOPPABLE_PAWN;
        }
    }
    score
}

/// Return how many squares a knight, bishop, rook, or queen can move to.
fn reachable_squares(board: &Board, row: i32, col: i32) -> i32 {
    let piece = board[row as usize][col as usize];
    let kind = piece.to_ascii_uppercase();
    let white = piece.is_ascii_uppercase();
    let mut count = 0;
    if kind == 'N' {
        for (row_step, col_step) in KNIGHT_JUMPS {
            let (to_row, to_col) = (row + row_step, col + col_step);
            if (0..8).contains(&to_row) && (0..8).contains(&to_col) {
                let target = board[to_row as usize][to_col as usize];
                if target == EMPTY || target.is_ascii_uppercase() != white {
                    count += 1;
                }
            }
        }
        return count;
    }
    let mut directions: Vec<(i32, i32)> = Vec::with_capacity(8);
    if kind == 'R' || kind == 'Q' {
        directions.extend(ROOK_DIRECTIONS);
    }
    if kind == 'B' || kind == 'Q' {
        directions.extend(BISHOP_DIRECTIONS);
    }
    for (row_step, col_step) in directions {
        let (mut to_row, mut to_col) = (row + row_step, col + col_step);
        while (0..8).contains(&to_row) && (0..8).contains(&to_col) {
            let target = board[to_row as usize][to_col as usize];
            if target != EMPTY {
                if target.is_ascii_uppercase() != white {
                    count += 1; // A capture counts; the slide stops at any piece
                }
                break;
            }
            count += 1;
            to_row += row_step;
            to_col += col_step;
        }
    }
    count
}

/// Score how freely the knights, bishops, rooks, and queens move, positive when it
/// favors White: mobility_weight() for each square each one reaches.
pub fn mobility(board: &Board) -> i32 {
    let mut score = 0;
    for row in 0..8 {
        for col in 0..8 {
            let piece = board[row][col];
            if piece == EMPTY {
                continue;
            }
            let weight = mobility_weight(piece.to_ascii_uppercase());
            if weight == 0 {
                continue;
            }
            let bonus = weight * reachable_squares(board, row as i32, col as i32);
            if piece.is_ascii_uppercase() {
                score += bonus;
            } else {
                score -= bonus;
            }
        }
    }
    score
}

/// Score the bishop pair and rooks on open and half-open files, positive when it
/// favors White.
pub fn piece_terms(board: &Board) -> i32 {
    let mut white_pawns = [0; 8];
    let mut black_pawns = [0; 8];
    let mut white_bishops = 0;
    let mut black_bishops = 0;
    for row in 0..8 {
        for col in 0..8 {
            match board[row][col] {
                'P' => white_pawns[col] += 1,
                'p' => black_pawns[col] += 1,
                'B' => white_bishops += 1,
                'b' => black_bishops += 1,
                _ => {}
            }
        }
    }
    let mut score = 0;
    if white_bishops >= 2 {
        score += BISHOP_PAIR;
    }
    if black_bishops >= 2 {
        score -= BISHOP_PAIR;
    }
    for row in 0..8 {
        for col in 0..8 {
            let (own, enemy, sign) = match board[row][col] {
                'R' => (white_pawns[col], black_pawns[col], 1),
                'r' => (black_pawns[col], white_pawns[col], -1),
                _ => continue,
            };
            if own == 0 && enemy == 0 {
                score += sign * ROOK_OPEN_FILE;
            } else if own == 0 {
                score += sign * ROOK_HALF_OPEN_FILE;
            }
        }
    }
    score
}

/// Score the position for the side to move: material, placement, pawn structure,
/// the mating bonus, and king safety, positive when the side to move stands better.
/// Negamax search needs the score from the mover's side.
pub fn evaluate(state: &State) -> i32 {
    let board = &state.board;
    let white_score = material(board)
        + placement(board)
        + pawn_structure(board)
        + mating_bonus(board)
        + king_safety(board)
        + tapered_terms(board)
        + pawn_race(board, state.turn)
        + mobility(board)
        + piece_terms(board);
    if state.turn == WHITE { white_score } else { -white_score }
}
