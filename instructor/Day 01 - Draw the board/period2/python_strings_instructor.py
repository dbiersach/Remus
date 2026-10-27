#!/usr/bin/env -S uv run
"""python_strings_instructor.py

Day 1, period 2, Python lab 1: strings, indexing, ord() and chr(), and f-strings.
The chess drill turns the square name "e2" into file number 4 and rank number 2,
the numbers board.py needs on Day 1, period 4.
The student file python_strings.py leaves one # line for each line the pair types.
"""


def main():
    print("Part #1 - Strings and Indexing")
    square = "e2"
    # Index 0 is the first character of a string, index 1 the second
    file_letter = square[0]
    rank_digit = square[1]
    print(f"{square}: file letter {file_letter}, rank digit {rank_digit}")
    print("  (expected file letter e, rank digit 2)")

    print("Part #2 - Letters Are Numbers: ord() and chr()")
    # ord() gives a character's code number, and chr() turns a number back
    print(f"ord('a') is {ord('a')}  (expected 97)")
    print(f"chr(98) is {chr(98)}  (expected b)")
    # Counting from file a = 0, file e is 4 letters after a
    file_number = ord(file_letter) - ord("a")
    rank_number = int(rank_digit)
    print(f"{square} is file number {file_number}, rank number {rank_number}")
    print("  (expected file number 4, rank number 2)")

    print("Part #3 - Numbers Back to a Square Name")
    # File number 6 is the g-file: start at "a" and count 6 letters on
    letter = chr(ord("a") + 6)
    name = f"{letter}{7}"
    print(f"File number 6, rank 7 is the square {name}  (expected g7)")

    print("Part #4 - Upper and Lower Case")
    # In Remus, uppercase letters are White pieces and lowercase are Black
    black_back_rank = "rnbqkbnr"
    white_back_rank = black_back_rank.upper()
    print(f"Black: {black_back_rank}  White: {white_back_rank}")
    print("  (expected Black: rnbqkbnr  White: RNBQKBNR)")
    is_white = "N".isupper()
    print(f"Is N a White piece? {is_white}  (expected True)")


if __name__ == "__main__":
    main()
