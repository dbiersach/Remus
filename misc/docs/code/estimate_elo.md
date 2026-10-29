# estimate_elo.py: How strong is Remus?

*Lives in Remus-GOLD, in the teacher's `engines/instructor/11 GOLD - All enhancements`, the engine of Day 10.*

## The big picture

Chess players get an Elo rating: a number that predicts who wins. A player rated
200 points higher is expected to score about 76 percent.

This file measures the finished Remus. Remus plays Stockfish, the strongest free
engine, with Stockfish turned down to a fixed rating such as 1320 or 1500. The results
give Remus a rating of its own.

## Where this piece fits

estimate_elo.py starts uci_engine.py and Stockfish. It uses python-chess as the referee, the way version_match.py does.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

## Words to know

- **Elo rating:** a number for playing strength. Bigger gaps mean more lopsided results.
- **UCI_Elo:** a Stockfish setting that makes it play at a chosen rating.
- **expected score:** the points per game the Elo formula predicts, from 0 to 1.
- **confidence interval:** the range the true rating most likely sits in. More games make it narrower.

## What it stores

Each level plays 10 games by default, with Remus taking White and Black in turn.
The clock gives 1 minute plus 0.6 seconds a move, the clock Stockfish uses to set
UCI_Elo. Every game is added to misc/games/remus_games.pgn, at the top of the Remus
folder, the moment it ends, and the file is never erased.

## How it works

1. `find_stockfish()` finds the Stockfish program.
2. `play_game()` plays one game on the clock against Stockfish at one rating.
3. `main()` adds each game to the PGN file and keeps Remus's points.
4. `estimate_rating()` finds the rating whose expected score matches Remus's real score.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    estimate_rating()
        expected_score()
    find_stockfish()
    remus_points()
    play_game()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `find_stockfish` | Finds Stockfish on the PATH or in Lucas Chess's engine folder. | Remus-GOLD |
| `expected_score` | Gives the points per game the Elo formula expects. | Remus-GOLD |
| `estimate_rating` | Finds the rating that best fits all the results, and its error margin. | Remus-GOLD |
| `play_game` | Plays Remus against Stockfish at one rating and returns the game as PGN. | Remus-GOLD |
| `remus_points` | Reads Remus's points (1, 0.5, or 0) from one game. | Remus-GOLD |

## Try it

Open `estimate_elo.py` from the `11 GOLD - All enhancements` folder in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: The result of every game, the score at each level, and the estimated Elo with its error margin.

## Puzzle questions

1. Remus scores 5 out of 10 against Stockfish 1500. What rating does that suggest?
2. Why does a 10 out of 10 score give only a lower bound for the rating?
