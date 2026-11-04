# science

The two programs of Day 5, the science project. Each one aims an idea from the Remus
engines at a problem from a synchrotron beamline, such as NSLS-II at Brookhaven. Both
use common Python modules and import no engine: they reuse the engine's ideas,
not its code.

| Program | The question | The chess idea | Day 5 periods |
| --- | --- | --- | --- |
| `hidden_peak.py` | A 10 by 10 sample hides a hot spot. Where should the next measurement go? | The squares not yet measured are the legal moves, a score for each square is the evaluation, and the best-scoring square is the move. | Period 1 |
| `phase_hunt.py` | Which crystal phases are in a powder, judged from its X-ray peaks? | A set of phases is a position, adding a phase is a move, and a search scores every set of up to three phases. | Periods 2 and 3 |

## The two folders

| Folder | What it holds |
| --- | --- |
| `science/`, this folder | The programs the student pairs work in. Every line is there except the bodies of the functions the student pair writes: `candidate_squares()`, `score_candidate()`, and `choose_next_measurement()` in `hidden_peak.py`, then `score()`, `greedy_phases()`, and `search()` in `phase_hunt.py`. Each empty function keeps its docstring, which says what the function must do, and a comment names its period. |
| [`science_instructor/`](../science_instructor/) | The same programs, complete and correct. A student pair that is stuck compares its function with the one there. |

## Running a program

Open the file in VS Code and click Run Python File. `main()` prints each result next
to the result it expects, and matplotlib opens each graph in its own window. Close the
window and the program continues. In this folder, a function not written yet stops the
run with `NotImplementedError` and its name, such as "Write score()".

Expected results of the finished programs:

- `hidden_peak.py`: random guessing needs 54.3 measurements on average over 100 hidden
  samples, and the program's AI with explore weight 8 needs 9.4.
- `phase_hunt.py`: on 200 known powders the greedy answer gets 166 right and 34 wrong,
  and the search gets 139 right, 52 "can't tell", and 9 wrong.
