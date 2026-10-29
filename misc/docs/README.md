# Remus documentation

The pages fall into three folders. Pick the folder by the question you have.

| Folder | Read it to learn | Pages |
| --- | --- | --- |
| [`course/`](course/) | How the two weeks run: what each day and period teaches, which slides go with it, and how to run Remus in Lucas Chess, plus the workshop in a few pages for managers and for students and parents | [`workshop_roadmap.md`](course/workshop_roadmap.md), [`remus_course_plan.md`](course/remus_course_plan.md), [`slide_plan.md`](course/slide_plan.md), [`lucas_chess_guide.md`](course/lucas_chess_guide.md), [`student_edit_plan.md`](course/student_edit_plan.md), [`science_tree_search_survey.md`](course/science_tree_search_survey.md), and the two briefing PDFs |
| [`code/`](code/) | How the program fits together, and what each `.py` file does | [`remus_program_overview.md`](code/remus_program_overview.md), [`file_versions.md`](code/file_versions.md), and one page per file, such as [`board.md`](code/board.md) for `board.py` |
| [`engines/`](engines/) | The twelve Remus engines (Remus-WHITE, the ten enhanced engines, and Remus-GOLD), how strong each one plays, and whether each Niram twin matches it | [`remus_versions.md`](engines/remus_versions.md), [`engines_elo.md`](engines/engines_elo.md), [`remus-niram parity.md`](engines/remus-niram%20parity.md) |

The pictures for these pages live in [`images/`](images/): the chess board
diagrams of the enhanced engine READMEs, goals files, and code pages in `images/boards/`, the Lucas Chess
screenshots in `images/lucas_chess/`, and the phase hunt figures in
`images/phase_hunt/`.

Two pages come from scripts, so edit the script, not the page.
`misc/scripts/make_student_folders.py` writes `course/student_edit_plan.md`, and
`misc/scripts/engine_parity.py` writes `engines/remus-niram parity.md`.
`misc/scripts/version_elo.py` prints the Stockfish tables that
`engines/engines_elo.md` reports.
