#!/usr/bin/env -S uv run
"""python_functions_instructor.py

Day 2, period 1, Python lab 3: functions, type hints, tuples, assert, and pytest.
The chess drill writes is_white() and on_board(), two small questions Remus asks
all the time, and checks them with assert, first by hand and then with pytest.
The student file python_functions.py leaves one # line for each line the pair types.
"""


def is_white(piece: str) -> bool:
    """Return True if the piece is White. White pieces are uppercase letters."""
    return piece.isupper()


def on_board(row: int, col: int) -> bool:
    """
    Return True if (row, col) is one of the 64 squares of the board.

    Parameters
    ----------
    row : int
        Board row, where row 0 is rank 8.
    col : int
        Board column, where column 0 is file a.

    Returns
    -------
    bool
        True when both the row and the column are between 0 and 7.
    """
    return 0 <= row <= 7 and 0 <= col <= 7


# Write a whole function yourself: its def line, its docstring, and its body
def is_black(piece: str) -> bool:
    """Return True if the piece is Black. Black pieces are lowercase letters."""
    return piece.islower()


def test_is_white():
    """A White knight is White, and a Black knight is not."""
    assert is_white("N")
    assert not is_white("n")


def test_on_board():
    """The corner a1 is on the board, and row 8 is one row past rank 1."""
    # a1 is row 7, col 0
    assert on_board(7, 0)
    assert not on_board(8, 3)


def main():
    print("Part #1 - Call a Function")
    print(f'is_white("N") is {is_white("N")}  (expected True)')
    print(f'is_white("p") is {is_white("p")}  (expected False)')
    print(f"on_board(0, 7) is {on_board(0, 7)}  (expected True, the square h8)")
    print(f"on_board(3, -1) is {on_board(3, -1)}  (expected False)")

    print("Part #2 - Your Own Function")
    print(f'is_black("q") is {is_black("q")}  (expected True)')
    print(f'is_black("Q") is {is_black("Q")}  (expected False)')

    print("Part #3 - A Square Is a Tuple")
    # A tuple packs two numbers into one value: e4 is row 4, col 4
    square = (4, 4)
    # Unpacking gives each number its own name, in order
    row, col = square
    print(f"row {row}, col {col}  (expected row 4, col 4)")
    print(f"On the board: {on_board(row, col)}  (expected True)")

    print("Part #4 - Check the Functions with assert")
    # assert does nothing when its test is True and stops the program when it is False
    test_is_white()
    test_on_board()
    print("Every assert passed  (expected this line)")
    print("Now run the same tests with pytest: press Run on run_tests.py")
    print("Then change 8 to 7 in test_on_board and read the report of the failing test")


if __name__ == "__main__":
    main()
