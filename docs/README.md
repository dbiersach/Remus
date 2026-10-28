# Remus documentation

The pages fall into four folders. Pick the folder by the question you have.

| Folder | Read it to learn | Pages |
| --- | --- | --- |
| [`course/`](course/) | How the two weeks run: what each day and period teaches, which slides go with it, and how to run Remus in Lucas Chess | [`workshop_roadmap.md`](course/workshop_roadmap.md), [`remus_course_plan.md`](course/remus_course_plan.md), [`slide_plan.md`](course/slide_plan.md), [`lucas_chess_guide.md`](course/lucas_chess_guide.md), [`student_edit_plan.md`](course/student_edit_plan.md), [`science_tree_search_survey.md`](course/science_tree_search_survey.md) |
| [`code/`](code/) | How the program fits together, and what each `.py` file does | [`remus_program_overview.md`](code/remus_program_overview.md), [`file_versions.md`](code/file_versions.md), and one page per file, such as [`board.md`](code/board.md) for `board.py` |
| [`engines/`](engines/) | The twelve Remus engines (Remus-WHITE, the ten color versions, and Remus-GOLD), how strong each one plays, and whether each Niram twin matches it | [`remus_versions.md`](engines/remus_versions.md), [`remus_elo.md`](engines/remus_elo.md), [`engine_parity.md`](engines/engine_parity.md) |
| [`briefs/`](briefs/) | The workshop in a few pages, for managers and for students and parents | The two briefing PDFs |

The pictures for these pages live in [`images/`](images/): the Lucas Chess
screenshots in `images/lucas_chess/` and the phase hunt figures in
`images/phase_hunt/`.

Three pages come from scripts, so edit the script, not the page.
`scripts/make_student_folders.py` writes `course/student_edit_plan.md`,
`scripts/version_elo.py` writes `engines/remus_elo.md`, and
`scripts/engine_parity.py` writes `engines/engine_parity.md`.
