//! board.rs
//!
//! Hold the chessboard as an 8x8 grid of characters and convert between square
//! names, such as "e2", and (row, col) pairs, such as (6, 4).
//!
//! Row 0 is rank 8 and column 0 is file a, so the board prints in the same order a
//! player sees it from White's side: rank 8 at the top, rank 1 at the bottom.

pub const EMPTY: char = '.'; // An empty square
const BOARD_FILES: &str = "abcdefgh"; // File letters, indexed by column: column 0 is file a
const BOARD_RANKS: &str = "87654321"; // Rank digits, indexed by row: row 0 is rank 8

/// The board: 8 rows of 8 squares, row 0 (rank 8) first.
pub type Board = [[char; 8]; 8];

/// A square as (row, col). Signed numbers let a step walk off the board and be caught.
pub type Square = (i32, i32);

/// Return the letter of a file, such as 'e' for column 4.
pub fn file_letter(col: i32) -> char {
    BOARD_FILES.as_bytes()[col as usize] as char
}

/// Return the digit of a rank, such as '2' for row 6.
pub fn rank_digit(row: i32) -> char {
    BOARD_RANKS.as_bytes()[row as usize] as char
}

/// Convert board coordinates to an algebraic square name, such as "e2" for (6, 4).
pub fn square_name(row: i32, col: i32) -> String {
    let mut name = String::new();
    name.push(file_letter(col));
    name.push(rank_digit(row));
    name
}

/// Convert an algebraic square name, such as "e2", to (row, col), such as (6, 4).
pub fn parse_square(name: &str) -> Result<Square, String> {
    let letters: Vec<char> = name.chars().collect();
    if letters.len() != 2 {
        return Err(format!("Not a square: {name:?}"));
    }
    let col = BOARD_FILES.find(letters[0]);
    let row = BOARD_RANKS.find(letters[1]);
    match (row, col) {
        (Some(row), Some(col)) => Ok((row as i32, col as i32)),
        _ => Err(format!("Not a square: {name:?}")),
    }
}

/// Return the piece on a (row, col) square, or EMPTY.
pub fn piece_at(board: &Board, square: Square) -> char {
    board[square.0 as usize][square.1 as usize]
}

/// Put a piece (or EMPTY) on a (row, col) square.
pub fn set_piece(board: &mut Board, square: Square, piece: char) {
    board[square.0 as usize][square.1 as usize] = piece;
}
