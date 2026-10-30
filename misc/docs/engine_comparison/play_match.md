# play_match.py: Two Remus brains play each other

*First appears in `Day 07 - Play full games and score positions/period3/instructor`.*

## The big picture

Which brain is stronger? Let them play.

This file starts two copies of Remus and lets them play a match. python-chess acts as
the referee, so an illegal move is caught. Every game goes into the class games file,
misc/games/remus_games.pgn, so no game is lost.

## Where this piece fits

play_match.py starts uci_engine.py twice. It uses python-chess, which only the referees and tests outside the engine may use.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

## Words to know

- **referee:** a program that checks every move is legal.
- **match:** several games between the same two players, swapping piece colors.
- **PGN:** a text file format for saving chess games.

## What it stores

On Day 10, `think` beat `greedy` 4 to 0.

## How it works

1. `start_engine()` starts one copy of Remus with a chosen brain.
2. `play_game()` asks each side for a move until the game ends.
3. `save_game()` adds the game to misc/games/remus_games.pgn.
4. `main()` swaps piece colors each game and keeps the score.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    start_engine()
    play_game()
    save_game()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `start_engine` | Starts one copy of Remus with a chosen brain. | Day 7, period 3 |
| `play_game` | Plays one game and returns the board with every move on it. | Day 7, period 3 |
| `save_game` | Adds one game to the class games file and returns its result. | Day 7, period 3 |

## Try it

Open `play_match.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: Each game's result, then the final score.

## Puzzle questions

1. Why swap piece colors every game?
2. Set `FIRST_BRAIN` and `SECOND_BRAIN` to `"think"` and `GAMES` to `4` near the top of the file, then press Run. Why can Remus win against itself?

## Slides

Slides 7.6 in the [slide plan](../course/slide_plan.md).
