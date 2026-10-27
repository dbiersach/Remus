# Bug hunt

The Remus files in this folder are a copy of the Day 6, period 3 code, with three bugs planted in them. Each bug breaks one chess rule. Run `uv run hunt.py` from inside this folder: it uses `divide()` to count the positions under every root move of four standard positions, and prints each root move where Remus and python-chess disagree.

A root move that disagrees points at a rule that its position needs. Ask what is special about that move or about the replies to it, find the rule in the code, fix the line, and run the hunt again. The hunt is over when it prints 0 root moves that disagree.
