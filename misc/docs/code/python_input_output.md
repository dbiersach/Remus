# python_input_output.py: Read commands, answer at once

*Day 7, period 2. The lab file is `Day 07 - Play full games and score positions/period2/student/python_input_output.py`, and the answers are in `Day 07 - Play full games and score positions/period2/instructor/python_input_output_instructor.py`.*

## The big picture

A chess GUI talks to an engine through text: it writes a command on one line, and
the engine answers on its own line. This lab picks moves the way the first brains do,
then reads commands from the keyboard and answers `isready` with `readyok`, the first
exchange of the UCI protocol.

## Where this piece fits

The lab does not import Remus. In period 3, `random_move()` and `greedy_move()` in
`search.py` use `random.choice()` and the best-value idea of Part #2, and `uci_engine.py`
reads `sys.stdin` and answers with `flush=True` as Part #4 does.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`search.py`](search.md) and [`uci_engine.py`](uci_engine.md)

## Words to know

- **random.choice():** picks one item of a list at random.
- **best so far:** a variable that holds the best item seen yet. A loop swaps in any item that beats it.
- **stdin and stdout:** the text a program reads and the text it prints.
- **stderr:** a second output for notes, which a GUI does not read.
- **flush=True:** sends the printed line at once, so the GUI is not left waiting.

## How it works

1. Part #1: pick a random move.
2. Part #2: pick the most valuable capture with a loop that keeps the best piece so far.
3. Part #3: print a note to `sys.stderr`.
4. Part #4: read lines from `sys.stdin` until `quit`, answering `isready` and echoing the rest.

The pair types 16 lines.

## Try it

Open `python_input_output.py` in `Day 07 - Play full games and score positions/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: a random move, q, the note, and then readyok and echo hello for the lines you type.

## Puzzle questions

1. What would Lucas Chess do if the engine never flushed `readyok`?
2. Why do notes go to stderr and not to stdout?
