# Day 10, Period 4: Science results, take-home, and wrap-up

Each pair reports its science results: the hidden-peak benchmark and the phase hunt's right, wrong, and can't-tell counts. Then each student takes the pair's repository home on a USB drive.

## Learning objectives

By the end of this period, each pair can:

- Report a science result the way a scientist does. **Measured by:** The pair's results table gives the hidden-peak benchmark against random guessing and the phase hunt's right, wrong, and can't-tell counts for greedy and for search, from the pair's own runs.
- Explain one decision the science AI made. **Measured by:** Each pair presents one powder its search named and one it answered with can't tell, and says which measurement would settle the second.
- Take the code home. **Measured by:** Each student's USB copy opens and runs `uv run pytest`.

## The files

The engine for Day 10 is Remus-GOLD, the finished Remus with all ten enhancements, in the teacher's `Day 09 .../period2/engines/Remus-GOLD` folder. Lucas Chess runs its `remus.bat`, and its `estimate_elo.py` rates it against Stockfish. This folder holds only the science files, which never import the engine.

The code here is the same as at the end of the period before.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `hidden_peak.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
