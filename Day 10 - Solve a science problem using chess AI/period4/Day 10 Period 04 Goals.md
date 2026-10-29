# Day 10, Period 4: Science results, take-home, and wrap-up

Each pair reports its science results: the hidden-peak benchmark and the phase hunt's right, wrong, and can't-tell counts. Then each student takes the pair's repository home on a USB drive.

## Learning objectives

By the end of this period, each pair can:

- Report a science result the way a scientist does. **Measured by:** The pair's results table gives the hidden-peak benchmark against random guessing and the phase hunt's right, wrong, and can't-tell counts for greedy and for search, from the pair's own runs.
- Explain one decision the science AI made. **Measured by:** Each pair presents one powder its search named and one it answered with can't tell, and says which measurement would settle the second.
- Take the code home. **Measured by:** Each student's USB copy opens and passes `run_tests.py`.

## The files

The engine for Day 10 is Remus-GOLD, the finished Remus with all ten enhancements, in the teacher's `Day 09 .../period2/instructor/engines/Remus-GOLD` folder. Lucas Chess runs its `remus.bat`, and its `estimate_elo.py` rates it against Stockfish. This folder holds only the science files, which never import the engine.

The code here is the same as at the end of the period before.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `hidden_peak.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Each student copies the pair's repository to a USB drive with `git clone --no-hardlinks` and checks that the copy opens and passes `run_tests.py`. |
| 3:15 to 3:40 | Each pair runs `hidden_peak.py` and `phase_hunt.py` once more and fills in its results table: measurements against random guessing, and right, wrong, and can't-tell counts for greedy and for search. The class collects every pair's numbers on the board. |
| 3:40 to 3:55 | Each pair picks one powder its search named and one it answered with can't tell, and works out which measurement would settle the second. |
| 3:55 to 4:20 | Each pair presents its results and its two powders in three minutes. |
| 4:20 to 4:30 | The class closes with what comes next: AI agents that steer real experiments at light sources such as NSLS-II. |
