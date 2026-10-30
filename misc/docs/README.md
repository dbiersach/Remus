# Remus documentation

The pages fall into seven folders. Pick the folder by the question you have.

| Folder | Read it to learn | Pages |
| --- | --- | --- |
| [`chess_instruction/`](chess_instruction/) | How to read and play chess itself, apart from Remus and Python | [`chess_notation.md`](chess_instruction/chess_notation.md) |
| [`class_demos/`](class_demos/) | The class demos and experiments that live only in their period folders, never in an engine folder | [`demo_promotion.md`](class_demos/demo_promotion.md), [`compare_search.md`](class_demos/compare_search.md), [`show_board.md`](class_demos/show_board.md) |
| [`course/`](course/) | How the two weeks run: the teaching principles and lessons, what each day and period teaches, which slides go with it, and how to run Remus in Lucas Chess, plus the workshop in a few pages for managers and for students and parents | [`remus_course_plan.md`](course/remus_course_plan.md), [`student_guide.md`](course/student_guide.md), [`slide_plan.md`](course/slide_plan.md), [`lucas_chess_guide.md`](course/lucas_chess_guide.md), [`student_edit_plan.md`](course/student_edit_plan.md), [`file_versions.md`](course/file_versions.md), [`science_tree_search_survey.md`](course/science_tree_search_survey.md), and the two briefing PDFs |
| [`engine_code/`](engine_code/) | What each `.py` file of the Remus engine does: one page per file, named after it. Every engine folder holds these files | [`board.md`](engine_code/board.md) for `board.py`, [`notation.md`](engine_code/notation.md) for `notation.py` |
| [`engine_comparison/`](engine_comparison/) | How the whole program fits together and how its tests check it, and the twelve Remus engines (Remus-WHITE, the ten enhanced engines, and Remus-GOLD), how strong each one plays, whether Niram runs the same algorithms as Remus-GOLD, and the match tools `play_match.py` and `estimate_elo.py` | [`remus_program_overview.md`](engine_comparison/remus_program_overview.md), [`tests.md`](engine_comparison/tests.md), [`remus_versions.md`](engine_comparison/remus_versions.md), [`engines_elo.md`](engine_comparison/engines_elo.md), [`remus-niram same algorithms.md`](engine_comparison/remus-niram%20same%20algorithms.md), [`play_match.md`](engine_comparison/play_match.md), [`estimate_elo.md`](engine_comparison/estimate_elo.md) |
| [`learning_python/`](learning_python/) | The Python skills labs: one page per lab, named after its file | [`python_lists.md`](learning_python/python_lists.md) for `python_lists.py` |
| [`science/`](science/) | The Day 10 Science AI files | [`hidden_peak.md`](science/hidden_peak.md), [`phase_hunt.md`](science/phase_hunt.md) |

The pictures for these pages live in [`images/`](images/): the chess board
diagrams of the enhanced engine READMEs, goals files, and code pages in `images/boards/`, the Lucas Chess
screenshots in `images/lucas_chess/`, the phase hunt figures in
`images/phase_hunt/`, and the Remus-WHITE import diagram of the program overview in
`images/code/`.

Two pages come from scripts, so edit the script, not the page.
`misc/scripts/make_student_folders.py` writes `course/student_edit_plan.md`, and
`misc/scripts/engine_parity.py` writes `engine_comparison/remus-niram same algorithms.md`.
`misc/scripts/version_elo.py` prints the Stockfish tables that
`engine_comparison/engines_elo.md` reports.
