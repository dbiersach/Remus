# Chess notation: how people write down moves

Chess players write every move of a game so they can play it over later, send it to a
friend, or study it in a book. The usual way is called **SAN**, short for Standard
Algebraic Notation. Remus prints its moves in SAN, and Lucas Chess lists every move of a
game in SAN.

## Name every square

The board has eight **files**, the columns `a` to `h` from White's left to White's
right, and eight **ranks**, the rows `1` to `8` from White's side to Black's side.
A square's name is its file letter, then its rank number.

- White's king starts on `e1`, and Black's king starts on `e8`.
- The corner to White's left is `a1`. It is always a dark square.
- The square in front of White's king pawn is `e3`, and two squares ahead is `e4`.

## Name every piece

Each piece except the pawn has a capital letter:

| Piece | Letter |
| --- | --- |
| King | `K` |
| Queen | `Q` |
| Rook | `R` |
| Bishop | `B` |
| Knight | `N` (because `K` is the king) |
| Pawn | no letter |

## Write a move

A move is the piece letter, then the square it lands on.

- `Nf3`: a knight moves to f3.
- `Bc4`: a bishop moves to c4.
- `e4`: a pawn moves to e4. A pawn move is only the square.

## Captures

An `x` means the piece takes something on the square.

- `Bxf7`: a bishop captures on f7.
- `exd5`: a pawn captures on d5. A pawn capture starts with the file the pawn came
  from, here the e-file, because the pawn moves diagonally.

## Two pieces that could make the same move

When two of the same piece can reach a square, the move adds the file or the rank
the piece leaves from, so the reader knows which one moved.

- Knights on b1 and f3 can both reach d2. `Nbd2` moves the knight from the b-file.
- Rooks on a1 and a5 can both reach a3. `R1a3` moves the rook from rank 1.

## Castling, promotion, check, and checkmate

| Writing | Meaning |
| --- | --- |
| `O-O` | Castle on the king's side (the king moves two squares toward the h-file) |
| `O-O-O` | Castle on the queen's side (the king moves two squares toward the a-file) |
| `e8=Q` | A pawn reaches the last rank and becomes a queen |
| `e8=N` | The same pawn becomes a knight instead (an underpromotion) |
| `+` at the end | The move gives check, such as `Bb5+` |
| `#` at the end | The move gives checkmate, such as `Qxf7#` |

Castling uses the capital letter O, not the number zero.

## Read a whole move

```text
N  b  x  d2  +
|  |  |  |   gives check
|  |  |  square it lands on
|  |  captures
|  which knight (the one on the b-file)
piece letter (no letter for a pawn)
```

## A short game

A game is written as numbered moves, White's move first, then Black's.

```text
1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7#
```

On move 3 Black's knight on f6 attacks the queen, but only the king guards the pawn
on f7. On move 4 the queen captures that pawn with checkmate: the bishop on c4
protects the queen, so the king cannot take it, and every square the king could step
to is attacked or blocked.

## The notation chess programs use

Lucas Chess and Remus talk to each other in **UCI** notation instead. A UCI move is
only the square a piece leaves and the square it lands on, with no piece letter:
`e2e4`, `g1f3`, and `e1g1` for White castling on the king's side. A promotion adds
the new piece in a small letter: `e7e8q`. UCI is easy for a program to read but
harder for people, so Remus uses UCI only to talk to Lucas Chess and SAN everywhere a
person reads or types a move.

## Where Remus uses it

[`notation.py`](../engine_code/notation.md) writes Remus's moves in SAN and reads the
SAN you type. [`uci_engine.py`](../engine_code/uci_engine.md) reads and writes UCI
moves for Lucas Chess.

## Questions

1. What is the SAN of a pawn on g7 that captures on h8 and becomes a queen?
2. Rooks on a1 and h1 can both move to d1. How do you write each move?
3. The knight on g1 moves to f3. How does Lucas Chess write that move in UCI?
