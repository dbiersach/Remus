# Remus documentation

The pages fall into four folders. Pick the folder by the question you have.

| Folder | Read it to learn | Pages |
| --- | --- | --- |
| [`course/`](course/) | How the two weeks run: what each day and period teaches, which slides go with it, and how to run Remus in Lucas Chess, plus the workshop in a few pages for managers and for students and parents | [`workshop_roadmap.md`](course/workshop_roadmap.md), [`remus_course_plan.md`](course/remus_course_plan.md), [`slide_plan.md`](course/slide_plan.md), [`lucas_chess_guide.md`](course/lucas_chess_guide.md), [`student_edit_plan.md`](course/student_edit_plan.md), [`file_versions.md`](course/file_versions.md), [`science_tree_search_survey.md`](course/science_tree_search_survey.md), and the two briefing PDFs |
| [`code/`](code/) | What each `.py` file of Remus does: one page per file, named after it | [`board.md`](code/board.md) for `board.py`, [`notation.md`](code/notation.md) for `notation.py` |
| [`learning_python/`](learning_python/) | The Python skills labs: one page per lab, named after its file | [`python_lists.md`](learning_python/python_lists.md) for `python_lists.py` |
| [`engines/`](engines/) | How the whole program fits together and how its tests check it, and the twelve Remus engines (Remus-WHITE, the ten enhanced engines, and Remus-GOLD), how strong each one plays, and whether Niram runs the same algorithms as Remus-GOLD | [`remus_program_overview.md`](engines/remus_program_overview.md), [`tests.md`](engines/tests.md), [`remus_versions.md`](engines/remus_versions.md), [`engines_elo.md`](engines/engines_elo.md), [`remus-niram same algorithms.md`](engines/remus-niram%20same%20algorithms.md) |

The pictures for these pages live in [`images/`](images/): the chess board
diagrams of the enhanced engine READMEs, goals files, and code pages in `images/boards/`, the Lucas Chess
screenshots in `images/lucas_chess/`, the phase hunt figures in
`images/phase_hunt/`, and the Remus-WHITE import diagram of the program overview in
`images/code/`.

Two pages come from scripts, so edit the script, not the page.
`misc/scripts/make_student_folders.py` writes `course/student_edit_plan.md`, and
`misc/scripts/engine_parity.py` writes `engines/remus-niram same algorithms.md`.
`misc/scripts/version_elo.py` prints the Stockfish tables that
`engines/engines_elo.md` reports.
