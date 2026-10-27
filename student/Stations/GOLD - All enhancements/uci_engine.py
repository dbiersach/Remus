#!/usr/bin/env -S uv run
"""uci_engine.py

Talk to a chess GUI such as Lucas Chess through the Universal Chess Interface (UCI).
The GUI sends one command per line on standard input, and Remus answers on standard
output. Debug text goes to standard error, where the GUI ignores it.

The first argument picks the brain: "random", "greedy", "negamax", or "think" (the
default), which searches deeper and deeper until its time is up. The search runs in a
thread, so Remus can still answer "isready" and obey "stop" while it thinks. The
"think" brain plays a move from the opening book first, while the position is in
the book.
"""

import sys
import threading

from fen import START_FEN, state_from_fen
from legal_moves import legal_moves
from make_move import make_move
from moves import move_from_uci, move_to_uci
from opening_book import book_move, load_book
from search import greedy_move, negamax_move, random_move, think

BRAINS = {
    "random": random_move,
    "greedy": greedy_move,
    "negamax": negamax_move,
}  # By name
DEFAULT_SECONDS = 2.0  # Thinking time when the GUI gives no clock
RESERVE_SECONDS = 3.0  # Clock time Remus never plans to spend, to pay for sending moves
MIN_SECONDS = 0.01  # The shortest think, for when the clock is nearly empty


def send(text: str) -> None:
    """Send one line to the GUI. flush=True makes it leave at once."""
    print(text, flush=True)


def set_position(words: list[str]) -> dict:
    """
    Build the state that a "position" command describes.

    Parameters
    ----------
    words : list[str]
        The command split into words, such as
        ["position", "startpos", "moves", "e2e4", "e7e5"].

    Returns
    -------
    dict
        The game state after the listed moves.
    """
    if words[1] == "startpos":
        state = state_from_fen(START_FEN)
    else:
        fen_end = words.index("moves") if "moves" in words else len(words)
        fen = ""
        for word in words[2:fen_end]:
            fen += word + " "
        state = state_from_fen(fen)
    if "moves" in words:
        for text in words[words.index("moves") + 1 :]:
            make_move(state, move_from_uci(text, state["turn"] == "w"))
    return state


def thinking_time(words: list[str], white_to_move: bool) -> float:
    """
    Decide how many seconds to think from a "go" command.

    Parameters
    ----------
    words : list[str]
        The command split into words, such as ["go", "wtime", "60000", "winc", "1000"].
    white_to_move : bool
        True if Remus plays White in this position.

    Returns
    -------
    float
        "movetime" if the GUI gives one; otherwise a thirtieth of the remaining
        time plus half the increment; otherwise DEFAULT_SECONDS. The remaining
        time leaves out RESERVE_SECONDS, because every move also costs time that
        the search does not see: starting the search, sending the move, and the
        GUI reading it. One move never takes more than half of the spare time.
    """
    values = {}
    for index in range(1, len(words) - 1):
        if words[index + 1].lstrip("-").isdigit():
            values[words[index]] = (
                int(words[index + 1]) / 1000
            )  # Milliseconds to seconds
    if "movetime" in values:
        return values["movetime"]
    clock, increment = ("wtime", "winc") if white_to_move else ("btime", "binc")
    if clock in values:
        spare = values[clock] - RESERVE_SECONDS
        seconds = spare / 30 + values.get(increment, 0) / 2
        return max(MIN_SECONDS, min(seconds, spare / 2))
    return DEFAULT_SECONDS


def search_and_send(state: dict, seconds: float, stop: threading.Event) -> None:
    """Think in the background, then send the best move to the GUI."""
    move = think(state, seconds, stop=stop, report=send)
    send(f"bestmove {move_to_uci(move)}")


def main():
    brain_name = sys.argv[1] if len(sys.argv) > 1 else "think"
    state = state_from_fen(START_FEN)
    book = load_book()
    stop = threading.Event()
    worker = None
    for line in sys.stdin:
        words = line.split()
        if not words:
            continue
        command = words[0]
        if worker is not None and command in ("position", "ucinewgame", "go"):
            worker.join()  # Finish the last search before changing the position
        if command == "uci":
            send("id name Remus")
            send("id author Turning a Chess Engine into Science AI")
            send("uciok")
        elif command == "isready":
            send("readyok")
        elif command == "ucinewgame":
            state = state_from_fen(START_FEN)
        elif command == "position":
            state = set_position(words)
        elif command == "go":
            opening = book_move(book, state)  # None once the game leaves the book
            if not legal_moves(state):
                send("bestmove 0000")
            elif brain_name in BRAINS:
                send(f"bestmove {move_to_uci(BRAINS[brain_name](state))}")
            elif opening is not None:
                send(f"bestmove {move_to_uci(opening)}")
            else:
                stop.clear()
                seconds = thinking_time(words, state["turn"] == "w")
                worker = threading.Thread(
                    target=search_and_send, args=(state, seconds, stop)
                )
                worker.start()
        elif command == "stop":
            stop.set()
        elif command == "quit":
            stop.set()
            break
        else:
            print(f"Remus ignores: {line.strip()}", file=sys.stderr)
    if worker is not None:
        worker.join()  # Input ended: let the last search send its move


if __name__ == "__main__":
    main()
