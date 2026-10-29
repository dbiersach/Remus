#!/usr/bin/env -S uv run
"""python_fen_fields_instructor.py

Day 6, period 4, Python lab 9: split(), int(), and exceptions with try and
ValueError. The chess drill cuts a FEN string into its six fields, the first step
of reading FEN in fen.py later this period.
The student file python_fen_fields.py leaves one # line for each line the student pair types.
"""

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FIELD_NAMES = [
    "piece placement",
    "side to move",
    "castling rights",
    "en passant square",
    "halfmove clock",
    "fullmove number",
]


def main():
    print("Part #1 - split() Cuts Text at Every Space")
    # split("/") cuts at every slash instead, the way fen.py cuts the placement into rows
    fields = START_FEN.split()
    print(f"Fields: {len(fields)}  (expected 6)")

    print("Part #2 - Name the Six Fields")
    for i in range(6):
        print(f"  {FIELD_NAMES[i]}: {fields[i]}")
    print("  (expected the placement, w, KQkq, -, 0, and 1)")

    print("Part #3 - int() and ValueError")
    # Try "12" here too: int() turns digits into a number and raises ValueError otherwise
    text = "x"
    try:
        print(f"  {text} is the number {int(text)}")
    except ValueError:
        print(f"  {text} is not a number, so int() raised ValueError")
    print("  (expected x is not a number)")


if __name__ == "__main__":
    main()
