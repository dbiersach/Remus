# Remus for teachers

This folder holds what a teacher needs to run the two-week workshop as it stands.
Every step of the workshop runs from VS Code's Run Python File button or from a
Markdown page; after the Day 1 setup, no student or teacher types a git or `uv`
command.

| Page | What it holds |
| --- | --- |
| [`remus_course_plan.md`](remus_course_plan.md) | The teaching principles, the thirteen lessons and their gates, the day-by-day plan with every period, the rules to refresh, the verification exercises, and the teacher preparation list |
| `unplugged_activities.md` | The run sheet for each of the nine unplugged warm-ups and its handout. This page is still to be written; until then the "Unplugged warm-ups" table in the course plan names each one, its period, its idea, and its materials |
| [`slide_plan.md`](slide_plan.md) | The PowerPoint slides the workshop needs, numbered by day, with what each one shows |
| [`student_edit_plan.md`](student_edit_plan.md) | Who writes what, period by period, with the lines to type. `make_student_folders.py` writes it from the code, so it always matches the folders |
| [`briefs/`](briefs/) | The management brief and the student and parent brief, as PDFs |

## Where the course lives

The course itself is in the Day folders at the top of Remus, `Day 01 - Draw the
board` to `Day 10 - Solve a science problem using chess AI`:

- Each Day folder opens with its syllabus, such as `Day 04 Syllabus.md`: the day's
  objectives, a table of the four periods, a timed sequence of activities for each
  period, and the checkpoint at 4:30. Read it the evening before.
- Each period folder, `period1` to `period4`, holds one goals file, such as
  `Day 04 Period 03 Goals.md`: the learning objectives and how each one is measured,
  the files that are new or growing, a paragraph on every change, the timed steps,
  and "The code you type", the exact lines the student pairs write with their line
  numbers. Beside it sit `instructor/`, the finished code of that period, and
  `student/`, the same code with the period's functions left as stubs.
- `run_tests.py` in any folder runs that folder's tests with the Run button. A dot is
  a pass, an `F` a failure with a report below.
- The enhanced engines of Day 9 live in `engines/instructor` and `engines/student` at
  the top of Remus. Each engine folder has its own README with the idea, a worked
  example, what it costs, and the code the student pair writes.

The student pages in [`misc/students/`](../students/) explain every file the student
pairs read or write, and the [Lucas Chess guide](../students/lucas_chess_guide.md)
shows, with screenshots, how to add Remus to Lucas Chess and watch it play Stockfish.

## Before Day 1

The "Teacher preparation" section of the course plan lists the steps: the laptop
image with VS Code and Lucas Chess, the Day 1 install of git and `uv` that each
student does with the teacher, the handouts to print, the unplugged materials per
student pair (a printed board, sticky-note pieces, index cards, and the worksheets),
20 USB drives plus one class stick for the Day 9 battles, and a first full game of
the finished Remus in Lucas Chess on one laptop.

## Day 9 and Day 10

On Day 9, period 4, the student pairs battle their enhanced engines: a visitor copies
its engine folder from the USB stick over the host's folder of the same engine color,
and the host runs `play_battle.py`. The course plan's Day 9 section and
[`remus_versions.md`](../students/remus_versions.md) give the steps, and the league
table the teacher shows at the end of the period is on that page. Day 10 is the
science: `hidden_peak.py` and `phase_hunt.py` in the Day 10 folder, explained in
[`science_ai.md`](../students/science_ai.md).
