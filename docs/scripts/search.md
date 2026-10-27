# search.py: Choosing a move

*First appears in `instructor/Day 07 - Play full games in En Croissant/period4`.*

## The big picture

This is the brain of Remus. It looks ahead at moves and replies, then picks the best.

The file grows every day from Day 7 to Day 10. Each new, smarter search sits next to
the older one. That way you can run both and compare.

## Where this piece fits

search.py uses almost every engine file: legal_moves.py, make_move.py, evaluation.py, move_ordering.py, and transposition_table.py. uci_engine.py and console_game.py call it.

- **Uses:** [`attacks.py`](attacks.md), [`board.py`](board.md), [`evaluation.py`](evaluation.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`move_ordering.py`](move_ordering.md), [`moves.py`](moves.md), [`transposition_table.py`](transposition_table.md)
- **Uses only in its self-check:** [`fen.py`](fen.md)
- **Used by:** [`compare_search.py`](compare_search.md), [`console_game.py`](console_game.md), [`uci_engine.py`](uci_engine.md)

## Words to know

- **minimax:** you pick your best move, assuming your opponent picks their best reply.
- **negamax:** minimax with one rule: my score is minus my opponent's score.
- **alpha-beta:** skip moves that cannot change the answer. Same result, much less work.
- **quiescence:** keep looking at captures until the position is quiet, then score it.
- **iterative deepening:** search 1 move deep, then 2, then 3, until time runs out.
- **principal variation (PV):** the line of best moves the search expects.

## What it stores

The brains, from simplest to smartest:

| Day | Brain | Idea |
| --- | --- | --- |
| 7 | `random_move` | Any legal move |
| 7 | `greedy_move` | Grab the most valuable piece |
| 8 | `minimax`, `negamax` | Look ahead a few moves |
| 9 | `alpha_beta` | Look ahead, but skip useless branches |
| 9 | `alpha_beta_with_quiescence` | Also finish all the captures, and try good moves first |
| 9 | `think` | Go deeper and deeper until the clock runs out |
| 10 | `upgraded_search` | Adds memory, killer moves, and draw sense |

A checkmate scores `MATE_SCORE`, which is 100,000. A faster mate scores a little
more than a slower one.

## How it works

1. `think()` picks a backup move first, so it always has an answer.
2. It searches 1 move deep, then 2, then 3, and so on.
3. Each search tries every move, makes it, scores the replies, and undoes it.
4. At the end of the line, `quiescence()` finishes the captures and calls `evaluate()`.
5. If time runs out, `SearchTimeout` stops the search. Every `try/finally` undoes its move on the way out.
6. `think()` returns the best move from the deepest search that finished.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
random_move()
    legal_moves()  [legal_moves.py]

greedy_move()
    legal_moves()  [legal_moves.py]
    capture_value()
        piece_at()  [board.py]

minimax()
    legal_moves()  [legal_moves.py]
    white_score()
        material()  [evaluation.py]
        placement()  [evaluation.py]
    in_check()  [attacks.py]
    make_move()  [make_move.py]
    undo_move()  [make_move.py]
    minimax()  (calls itself again, one move deeper)

negamax_move()
    best_move()
        legal_moves()  [legal_moves.py]
        make_move()  [make_move.py]
        undo_move()  [make_move.py]
        negamax()
            legal_moves()  [legal_moves.py]
            evaluate()  [evaluation.py]
            in_check()  [attacks.py]
            make_move()  [make_move.py]
            undo_move()  [make_move.py]
            negamax()  (calls itself again, one move deeper)

alpha_beta()
    legal_moves()  [legal_moves.py]
    evaluate()  [evaluation.py]
    make_move()  [make_move.py]
    in_check()  [attacks.py]
    undo_move()  [make_move.py]
    alpha_beta()  (calls itself again, one move deeper)

alpha_beta_with_quiescence()
    check_time()
    in_check()  [attacks.py]
    legal_moves()  [legal_moves.py]
    order_moves()  [move_ordering.py]
    make_move()  [make_move.py]
    quiescence()
        check_time()
        evaluate()  [evaluation.py]
        order_moves()  [move_ordering.py]
        capture_moves()
            legal_moves()  [legal_moves.py]
            piece_at()  [board.py]
        make_move()  [make_move.py]
        undo_move()  [make_move.py]
        quiescence()  (calls itself again, one move deeper)
    alpha_beta_with_quiescence()  (calls itself again, one move deeper)
    undo_move()  [make_move.py]

think_move()
    think()
        legal_moves()  [legal_moves.py]
        order_moves()  [move_ordering.py]
        upgraded_search()
            check_time()
            in_check()  [attacks.py]
            probe()  [transposition_table.py]
            legal_moves()  [legal_moves.py]
            order_moves()  [move_ordering.py]
            best_stored_move()  [transposition_table.py]
            make_move()  [make_move.py]
            store()  [transposition_table.py]
            quiescence()
                check_time()
                evaluate()  [evaluation.py]
                order_moves()  [move_ordering.py]
                capture_moves()
                make_move()  [make_move.py]
                undo_move()  [make_move.py]
                quiescence()  (calls itself again, one move deeper)
            undo_move()  [make_move.py]
            remember_killer()
                piece_at()  [board.py]
            upgraded_search()  (calls itself again, one move deeper)
        format_info()
            move_to_uci()  [moves.py]
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `SearchInfo` | Holds what one search counts and needs: positions visited, the clock, and memory. | Day 8, period 3 |
| `SearchTimeout` | A signal that stops the search when time is up. | Day 9, period 3 |
| `check_time` | Raises SearchTimeout if time is up or the GUI said stop. | Day 9, period 3 |
| `random_move` | Picks any legal move at random. | Day 7, period 4 |
| `capture_value` | Says how much the captured piece is worth. | Day 7, period 4 |
| `greedy_move` | Picks the move that captures the most valuable piece. | Day 7, period 4 |
| `white_score` | Scores a position from White's side, for minimax. | Day 8, period 3 |
| `minimax` | Looks ahead. White picks the highest score, Black the lowest. | Day 8, period 3 |
| `negamax` | Does the same as minimax with one function and a minus sign. | Day 8, period 4 |
| `best_move` | Tries every first move with negamax and keeps the best. | Day 8, period 4 |
| `negamax_move` | The negamax brain: looks two moves ahead. | Day 8, period 4 |
| `alpha_beta` | Negamax that skips moves which cannot change the answer. | Day 9, period 1 |
| `capture_moves` | Lists only the captures and promotions. | Day 9, period 2 |
| `quiescence` | Keeps searching captures until the position is quiet. | Day 9, period 2 |
| `alpha_beta_with_quiescence` | The full Day 9 search: alpha-beta, quiescence, and good move order. | Day 9, period 3 |
| `remember_killer` | Remembers a quiet move that caused a cutoff, to try it early next time. | Day 10, period 1 |
| `upgraded_search` | The Day 10 search, with memory, killer moves, and draw sense. | Day 10, period 1 |
| `format_info` | Writes a line telling the GUI the depth, score, and best line. | Day 9, period 4 |
| `think` | Searches deeper and deeper until time runs out, then returns the best move. | Day 9, period 4 |
| `think_move` | The thinking brain, with two seconds per move. | Day 9, period 4 |

## How the file grows

- **Day 7, period 4:** `random_move`, `capture_value`, `greedy_move`
- **Day 8, period 3:** `SearchInfo`, `white_score`, `minimax`
- **Day 8, period 4:** `negamax`, `best_move`, `negamax_move`
- **Day 9, period 1:** `alpha_beta`
- **Day 9, period 2:** `capture_moves`, `quiescence`
- **Day 9, period 3:** `SearchTimeout`, `check_time`, `alpha_beta_with_quiescence`
- **Day 9, period 4:** `format_info`, `think`, `think_move`
- **Day 10, period 1:** `remember_killer`, `upgraded_search`

## Try it

From inside a period folder that has the file, run:

```bash
uv run search.py
```

You should see: A greedy capture, a back-rank mate found, negamax against alpha-beta node counts, and three `info depth` lines.

## Puzzle questions

1. Negamax visited 24,942 positions and alpha-beta 4,226 for the same score. Why is that allowed?
2. Why does `think()` keep the move from the last depth that finished?

## Slides

Slides 7.7, 8.3, 8.4, 8.5, 9.1, 9.3, 9.5, 9.6, 9.8, 10.4, 10.5 in the [slide plan](../slide_plan.md).
