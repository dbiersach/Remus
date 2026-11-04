# misc

The pages people read during the workshop, beside the plan of the course in `docs/`.
Students, teachers, and parents open these pages in VS Code or on GitHub. None of them
holds code to type or run.

| Folder | What it holds | Who reads it |
| --- | --- | --- |
| [`engines/`](engines/) | One folder per engine, `Remus1` to `Remus4`, each with a `README.md` (its files, their code lines, and what the version adds) and `call_tree.svg`, a picture of which function calls which. [`remus_versions.md`](engines/remus_versions.md) lists every enhancement and the version that adds it. | Student pairs, before and while they type a version |
| [`lucas_chess/`](lucas_chess/) | The [Lucas Chess guide](lucas_chess/lucas_chess_guide.md) and its 18 screenshots: how to add a Remus engine, play against it, and run it against Stockfish 1500. | Student pairs and teachers |
| [`chess_tutor/`](chess_tutor/) | [`learn_chess.md`](chess_tutor/learn_chess.md), the rarer rules (castling, en passant, promotion, the draws) and how moves are written, with its board pictures in `images/`; [`uci.md`](chess_tutor/uci.md), the conversation between Lucas Chess and Remus; and [videos](chess_tutor/minimax_negamax_alpha_beta_video_resources.md) on minimax, negamax, and alpha-beta. | Student pairs, right before the code that needs each idea |
| [`briefs/`](briefs/) | Two one-page PDFs: the [management brief](briefs/Turning_a_Chess_Engine_into_Science_AI_Management_Brief.pdf) and the [student and parent brief](briefs/Turning_a_Chess_Engine_into_Science_AI_Student_and_Parent_Brief.pdf). | School leaders, students, and parents, before the workshop |

The engine code itself lives in the top `engines_instructor/` folder, the student
pairs' own engines in `engines/`, and the Day 5 programs in `science/`.
