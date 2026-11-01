# The unplugged activities

Nine of the hardest ideas in the course get a 10 to 15 minute warm-up away from the
screen first. The student pairs close the laptop, slide it aside, and work on the
desk with a printed board, sticky notes, index cards, and a one-page worksheet. The
warm-up replaces part of the teacher's explanation at the board; it never takes time
from the block in which the student pairs type code.

This page is the teacher's run sheet: for each warm-up, when it runs, what to hand
out, the steps, and the answers. The answer key for the concept check, which the
students take on Day 1 and again on Day 10, is the last section. The worksheets the student pairs hold are in
[`handouts.md`](handouts.md), one section per warm-up, with no answers on them. Print
the handouts before the day; the "Teacher preparation" list in the
[course plan](remus_course_plan.md) says how many copies.

| Warm-up | When | Idea it prepares | Materials per student pair |
| --- | --- | --- | --- |
| [Call the square](#call-the-square) | Day 1, period 3, 1:00 to 1:15 | Row 0 is rank 8 | The board labeled both ways, one token (a coin or a sticky note) |
| [Undo from the card](#undo-from-the-card) | Day 2, period 4, 3:00 to 3:15 | Undo records and exact undo | A printed board, sticky-note pieces, three index cards, the undo card worksheet |
| [Shade the reach](#shade-the-reach) | Day 3, period 2, 10:30 to 10:45 | Jump lists and sliding | The three-board worksheet, a pencil |
| [Pin hunt](#pin-hunt) | Day 4, period 3, 1:00 to 1:15 | The legal-move filter | The four-position worksheet |
| [Count by hand](#count-by-hand) | Day 6, period 2, 10:30 to 10:45 | Perft and recursion | The position worksheet, six index cards |
| [Paper minimax](#paper-minimax) | Day 8, period 1, 8:30 to 8:45 | Minimax | The tree worksheet |
| [Fewest flips](#fewest-flips) | Day 8, period 2, 10:30 to 10:45 | Alpha-beta cutoffs | Nine index cards with the tree's leaf scores, face down |
| [Find the hidden peak](#find-the-hidden-peak) | Day 10, period 1, 8:30 to 8:45 | How a beamline AI chooses the next measurement | The 10x10 grid worksheet; the teacher holds the answer grid |
| [Name the powder](#name-the-powder) | Day 10, period 2, 10:45 to 11:00 | Scoring a guess, and why a fingerprint that fits half the peaks is a trap | Five fingerprint strips and the mystery pattern sheet |

Every warm-up runs the same way. The teacher states the task in one sentence, the
student pairs work for most of the time, and the last three minutes compare answers
across the room before the code that uses the idea comes up on the projector. The
driver and the navigator both take part: in most warm-ups one partner does and the
other checks, then they swap.

## Call the square

**Day 1, period 3, 1:00 to 1:15.** Prepares "row 0 is rank 8" before the
`python_lists.py` lab builds the board as a list of rows.

Hand out the board labeled both ways (handout 1): the files `a` to `h` and the ranks
`1` to `8` on the usual edges, and Remus's column numbers 0 to 7 along the top and
row numbers 0 to 7 down the right side.

1. The teacher calls a `(row, col)` pair, such as `(6, 4)`. The navigator puts the
   token on that square, counting rows from the top. The driver names the square:
   `e2`.
2. After three `(row, col)` pairs, swap roles and go the other way: the teacher
   calls a square name, such as `c5`, the navigator puts the token on it, and the
   driver says the `(row, col)` pair.
3. Last two minutes: the teacher asks the room why `(0, 0)` is `a8` and not `a1`.
   The answer to draw out: Remus prints the board the way a chess book shows it, with
   Black's side at the top, so the first row it prints is rank 8.

Pairs to call, with the answers:

| Called | Answer |
| --- | --- |
| `(6, 4)` | `e2` |
| `(0, 0)` | `a8` |
| `(7, 7)` | `h1` |
| `(4, 4)` | `e4` |
| `c5` | `(3, 2)` |
| `d7` | `(1, 3)` |
| `h8` | `(0, 7)` |

The rule to leave on the board: `row = 8 - rank` and `col = "abcdefgh".index(file)`.

## Undo from the card

**Day 2, period 4, 3:00 to 3:15.** Prepares the undo record that `make_move()`
returns and `undo_move()` reads, right before the student pairs write both.

Hand out a printed board, sticky-note pieces for the start position (or the pieces
of a pocket set), and the undo card worksheet (handout 2), three blank cards per
student pair. Each card has the fields of the Day 2 undo record: the move, the piece
that moved, the piece it captured (a dot for none), the old en passant square, the
old halfmove clock, and the old fullmove number.

1. The navigator plays three moves on the board and fills in one card for each move
   as it is made: 1. e4, then d5, then exd5. The driver looks away.
2. The driver takes the three cards, and only the cards, and restores the start
   position in reverse order: card 3 first. For each card the driver moves the piece
   back from the destination to the start square and puts the captured piece back on
   the destination square.
3. The navigator checks the board against a start position on the next desk. Then
   the partners swap and play three different moves.
4. Last three minutes: ask what would go wrong with no "captured piece" field. The
   pawn taken on d5 would be lost for good, which is exactly the bug the Day 2 tests
   catch.

The three cards for 1. e4 d5 2. exd5, as the state keeps them:

| Card | Move | Piece moved | Captured | Old en passant | Old halfmove clock | Old fullmove number |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | e2 to e4 | `P` | `.` | none | 0 | 1 |
| 2 | d7 to d5 | `p` | `.` | e3 | 0 | 1 |
| 3 | e4 to d5 | `P` | `p` | d6 | 0 | 2 |

A pawn move resets the halfmove clock to 0 and sets the en passant square behind it,
and the fullmove number goes up after Black's move, so card 3 reads 2.

## Shade the reach

**Day 3, period 2, 10:30 to 10:45.** Prepares the knight's jump list and the
sliding loop before the student pairs write `king_moves()` and, in the next period,
`slide()`.

Hand out the three-board worksheet (handout 3): three empty boards, one marked with a
knight on d4, one with a knight on a1, and one with a bishop on c1.

1. Each student pair shades every square each piece can reach on an empty board.
2. They write the count under each board and compare it with the next student pair.
3. Last three minutes: the teacher asks why the a1 knight keeps so few of its jumps,
   and what the bishop would do if a piece stood on e3.

The answers: the knight on d4 reaches 8 squares (b3, b5, c2, c6, e2, e6, f3, f5); the
knight on a1 reaches 2 (b3, c2), because the other six jumps leave the board; the
bishop on c1 reaches 7 (b2, a3, d2, e3, f4, g5, h6). With a piece on e3 the bishop
stops at e3: it reaches e3 (a capture if the piece is Black, nothing if it is White)
and never f4, g5, or h6. That stop is the `break` in `slide()`.

## Pin hunt

**Day 4, period 3, 1:00 to 1:15.** Prepares the legal-move filter: make the move,
ask whether the mover's own king is attacked, undo the move.

Hand out the four-position worksheet (handout 4). Each position lists every move the
Day 3 generator would offer the piece or the king named; the student pairs cross out
each move that leaves White's king attacked.

1. Work through position 1 together: the knight on e2 stands between the Black rook
   on e8 and the White king on e1. Every knight move uncovers the rook's line, so
   every knight move is crossed out.
2. The student pairs do positions 2 to 4 on their own.
3. Last three minutes: compare answers, then ask which single question settles all
   four worksheets. The answer is "after the move, is my king attacked?", and that
   one question is `legal_moves()`.

The positions and their answers (White to move in each):

| Position | Pieces | Moves offered | Cross out | Why |
| --- | --- | --- | --- | --- |
| 1 | White Ke1, Ne2; Black Ka8, Re8 | Knight to c1, c3, d4, f4, g1, g3 | All six | The knight is pinned: it shields the king from the rook |
| 2 | White Kd1, Bc2; Black Ke8, Ba4 | Bishop to b1, b3, d3, e4, f5, g6, h7, and the capture on a4 | b1, d3, e4, f5, g6, h7 | The bishop is pinned along the a4 to d1 diagonal. Bb3 stays on the diagonal, and Bxa4 removes the pinning piece, so those two stay |
| 3 | White Ke1; Black Ke8, Rf2 | King to d1, d2, e2, f1, and the capture on f2 | d2, e2, f1 | The rook on f2 guards the whole second rank and the f-file. Kd1 and Kxf2 stay |
| 4 | White Ka5, Pd5; Black Ke8, pawn c5 (just moved two squares), Rh5 | King to a4, a6, b4, b5, b6; pawn to d6; pawn captures c6 en passant | b4, and the capture on c6 | b4 is attacked by the pawn on c5. The en passant capture removes the c5 pawn and leaves d5, which opens the fifth rank from the rook to the king |

Position 4 is the rare trap the course plan names: the only way to see that the
capture is illegal is to make it and look, which is what the filter does.

## Count by hand

**Day 6, period 2, 10:30 to 10:45.** Prepares `perft()`: count the positions two
plies deep by hand, then run the code on the same position and see the same number.

Hand out the position worksheet (handout 5) and six index cards. The position is
White king e1 and pawn e2 against the Black king on e8, White to move.

1. The student pair lists every White move, one per card: Kd1, Kd2, Kf1, Kf2, e3,
   e4. Six cards.
2. On each card, under the move, they list Black's replies and write the count. In
   every case the Black king has the same five squares: d7, d8, e7, f7, f8.
3. They add the counts across the six cards: 30 positions two plies deep.
4. At 10:55 the student pairs write `perft()` and run it on this position. It prints
   6 at depth 1 and 30 at depth 2, matching the cards.
5. Last three minutes: ask how many cards depth 3 would need. The answer is one per
   depth 2 position, 30 of them, and `perft()` does that counting for them: at depth
   3 it prints 210.

The point to draw out: each card is one call of `perft()` one level down, and
adding the cards is the `total += perft(state, depth - 1)` line.

## Paper minimax

**Day 8, period 1, 8:30 to 8:45.** Prepares `minimax()` and the sign flip of
`negamax()`.

Hand out the tree worksheet (handout 6): a root marked "White to move" with three
moves A, B, and C, each with three Black replies, and nine scores on the bottom row.

1. The student pairs fill in each Black node with the smallest score below it, because
   Black picks the reply that is worst for White.
2. They fill in the root with the largest of the three Black nodes and circle the
   move White should play.
3. Compare across the room, then run the given `minimax()` on the same tree on the
   projector.

The tree and its answers:

| White's move | Black's replies score | Black's node (minimum) |
| --- | --- | --- |
| A | 4, 6, 5 | 4 |
| B | 2, 9, 7 | 2 |
| C | 3, 8, 8 | 3 |

The root takes the maximum of 4, 2, and 3: White plays A for a score of 4. The trap
on the worksheet is the 9 under B: a student pair that picks B for its best case has
forgotten that Black chooses, not White.

The optional human tree: seven students stand at the front, one as the root, two as
Black nodes, four as leaves holding score cards. The leaves show their cards, each
Black node calls out its minimum, the root calls out its maximum, and the rest of the
room predicts each call on paper before it is made.

## Fewest flips

**Day 8, period 2, 10:30 to 10:45.** Prepares alpha-beta: a branch can be abandoned
as soon as one reply shows it is worse than a move already found.

Hand out nine index cards with the leaf scores of the paper minimax tree written on
their faces, laid face down on the desk in three groups of three, in the order of the
worksheet: A (4, 6, 5), B (2, 9, 7), C (3, 8, 8).

1. The student pairs turn cards over one at a time, left to right, and may stop a group
   as soon as the group can no longer change White's choice. They count their flips.
2. The student pair with the fewest flips and the right move (A, scoring 4) explains
   its stopping rule to the room.
3. Last three minutes: the teacher names the rule. After group A, White is sure of
   4. In group B the first card shows 2: Black can hold White to 2 or less here, so B
   can never beat A and the other two cards stay face down. The same for group C,
   whose first card shows 3.

The best play is 5 flips of 9: all three cards of A, then one card each of B and C.
The 9 and the 7 under B, and the two 8s under C, never need to be seen. That is the
cutoff `alpha_beta()` writes as `if score >= beta: break`, and `compare_search.py`
counts the same saving in positions later in the period.

## Find the hidden peak

**Day 10, period 1, 8:30 to 8:45.** Prepares `hidden_peak.py`: with a few readings
in hand, where should the next measurement go?

Hand out the blank 10x10 grid worksheet (handout 7), rows 0 to 9 down the side and
columns 0 to 9 across the top, as `hidden_peak.py` numbers them. The teacher keeps
the answer grid below, which is `make_grid(7)` from the Day 10 folder, and reads
values from it.

1. Each student pair picks a square and calls it out as `(row, col)`. The teacher
   reads the value at that square from the answer grid, and the student pair writes
   the value on its worksheet. Five rounds.
2. After five readings each student pair marks its guess for the hottest square.
3. Reveal the peak, `(5, 2)`, and ask the student pairs who found it how they chose
   their fifth square. The two habits to name are exploring (measure far from every
   reading so far) and exploiting (measure next to the highest reading so far). The
   `explore_weight` the student pairs tune later in the period trades one against
   the other.

The answer grid, `make_grid(7)`, with the peak of 100 at row 5, column 2:

| row | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 1 | 2 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 4 | 14 | 21 | 14 | 4 | 1 | 0 | 0 | 0 | 0 |
| 4 | 14 | 45 | 67 | 45 | 14 | 2 | 0 | 0 | 0 | 0 |
| 5 | 21 | 67 | **100** | 67 | 21 | 3 | 0 | 0 | 0 | 0 |
| 6 | 14 | 45 | 67 | 45 | 14 | 2 | 0 | 0 | 0 | 0 |
| 7 | 4 | 14 | 21 | 14 | 4 | 1 | 0 | 0 | 0 | 0 |
| 8 | 1 | 2 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Most first guesses land on the right half of the grid and read 0, which is the
lesson: a reading of 0 still says where the peak is not, and the next measurement
should go far from it. To run the warm-up again with a fresh grid, print
`make_grid(seed)` for another seed from the Day 10 folder.

## Name the powder

**Day 10, period 2, 10:45 to 11:00.** Prepares `score()`: a guess earns a point for
each measured peak it explains and loses a point for each peak it leaves over, each
peak it predicts that is missing, and each phase it uses.

Hand out the mystery pattern sheet and the five fingerprint strips (handout 8). The
pattern is `make_pattern(7)` from the Day 10 folder, eight peaks between 20 and 57
degrees. The five strips are quartz, zincite, rutile, halite, and silicon, each
with its four strongest peaks from the `LIBRARY` in `phase_hunt.py`.

1. The student pairs lay each strip under the pattern and count how many of the
   pattern's peaks line up with a mark on the strip, within about a third of a degree.
2. They choose the two phases that together explain the most peaks, and count the
   peaks their choice leaves over and the marks on their strips that the pattern does
   not show.
3. Last three minutes: ask which strip fooled them. Halite lines up with two of the
   eight peaks and looks promising, but its other two marks, at 45.4 and 66.2
   degrees, point at nothing in the pattern. Rutile lines up with one peak only. The
   scoring function the student pairs write next charges for exactly those missing
   peaks, which is why a fingerprint that fits half the peaks loses.

The measured pattern and the answer:

| Measured peaks (degrees) | 20.77, 26.56, 31.68, 34.50, 36.22, 36.50, 50.08, 56.73 |
| --- | --- |
| Quartz strip | 20.9, 26.6, 36.5, 50.1: explains four peaks, misses none |
| Zincite strip | 31.8, 34.4, 36.3, 56.6: explains the other four, misses none |
| Halite strip | 31.7, 45.4, 56.5, 66.2: lines up with two peaks, two marks missing |
| Rutile strip | 27.4, 36.1, 41.2, 54.3: lines up with one peak, three marks missing |
| Silicon strip | 28.4, 47.3, 56.1, 69.1: lines up with nothing |

The powder is quartz and zincite. Every measured peak is explained and no predicted
peak is missing, so the pair scores 8 points for the explained peaks less 2 for the
two phases: 6, the best score any set can reach on this pattern.

## The concept check: answer key and scoring

**Day 1, period 1, 8:30 to 8:50, and Day 10, period 4, 4:00 to 4:20.** Handout 13
asks the same ten questions both days, before the first word about Remus and after
the science work. Each student works alone on paper. Score one point per question,
so a sheet scores 0 to 10, and keep each student's two sheets together: the gain
from Day 1 to Day 10 is the result, and the Day 1 sheet also shows the teacher what
the class already knows. Give the point for the idea, not the wording.

| Question | Answer | The point goes for |
| --- | --- | --- |
| 1 | Board: holds where every piece stands. Moves: lists where each piece could go. Rules: keeps only the legal moves and says when the game ends. Search: looks ahead through replies to replies. Evaluation: scores a position with a number | Three or more parts with a sensible job each |
| 2 | Row 6, column 4 is e2; h1 is (7, 7) | Both answers |
| 3 | The moves that leave the mover's own king attacked: moving a pinned piece off its line, walking the king into check, or ignoring a check | Naming the king's safety |
| 4 | Move A, expecting +3. After A Black picks +3; after B Black picks +1; White takes the larger of the two worst cases | A with +3, or B ruled out because Black would pick +1 |
| 5 | The counts check that the move generator obeys every rule, because the right numbers are known; 401 means one move too many, so some rule is wrong | Counting as a check against known numbers |
| 6 | No. B already leads to +1 at best, which is worse than A's +3, so B's other reply cannot make B the better choice | No, with the comparison against +3 |
| 7 | White has 11, Black has 13: Black is ahead by 2 | Black by 2 |
| 8 | A square next to the 40, such as c2, b3, d3, or c4, because the hot spot is near the highest reading; a far corner such as a5 is also a point if the reason is that nothing there has been measured yet | Any square with a reason that names the readings |
| 9 | A and B together explain all four peaks with none left over. The second powder is "can't tell": A with its 20 missing, or C with its 60 missing, so measure again or look for the 20 or 60 peak | A and B; then "can't tell" or a second measurement |
| 10 | The same: list the choices, look ahead, score each one, pick the best. Different: in chess an opponent answers, and in the lab nature answers with a reading, so the program averages instead of expecting the worst | One sentence on each |

On Day 1 most sheets score 1 to 3 points, from questions 2, 7, and 8, which need
only arithmetic and common sense. Questions 4, 6, 9, and 10 are the ones the course
teaches, and a Day 10 sheet should score 7 or more. Hand the sheets, with the two
interest surveys (handout 15) and the rubrics (handout 14), to the Brookhaven
education staff who support the evaluation.
