#!/usr/bin/env -S uv run
"""search.py

Choose a move. Remus's first two "brains" are simple: a random legal move, and a
greedy move that grabs the most valuable piece it can capture. Then Remus looks
ahead: minimax tries every move and every reply, and negamax does the same work
with one function instead of two mirror-image halves.

Day 8 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result, quiescence keeps looking until the captures
stop, and move ordering tries strong moves first. Day 9 adds iterative
deepening, which searches one move deeper at a time until the clock runs out.

Day 10 adds the upgrade stations to one final search, upgraded_search: a
transposition table, killer moves, principal variation search, draw sense,
null-move pruning, and late move reductions.
"""

import random
import threading
import time
from dataclasses import dataclass, field

from attacks import in_check
from board import EMPTY, piece_at
from evaluation import PIECE_VALUES, evaluate, material, placement
from fen import state_from_fen
from game_state import opponent, position_key
from legal_moves import legal_moves
from make_move import make_move, state_snapshot, undo_move
from move_ordering import order_moves
from moves import Move, move_to_uci
from transposition_table import EXACT, LOWER, UPPER, best_stored_move, probe, store

MATE_SCORE = (
    100_000  # Larger than any material count; a mate n plies away scores MATE_SCORE - n
)
NULL_MOVE_REDUCTION = 2  # How many plies shallower the null-move search looks
LATE_MOVE_INDEX = 3  # Moves after the first three in the ordered list count as late


@dataclass
class SearchInfo:
    """What a search counts while it runs."""

    nodes: int = 0  # Positions visited
    deadline: float | None = None  # time.perf_counter() value when the search must stop
    stop: threading.Event | None = None  # Set by the GUI's "stop" command
    table: dict = field(
        default_factory=dict
    )  # Transposition table: position_key -> entry
    killers: dict = field(default_factory=dict)  # Ply -> up to two killer moves


class SearchTimeout(Exception):
    """Raised inside the search when time is up, to unwind back to the root."""


def check_time(info: SearchInfo) -> None:
    """Raise SearchTimeout if the deadline has passed or the GUI said stop."""
    out_of_time = info.deadline is not None and time.perf_counter() > info.deadline
    if out_of_time or (info.stop is not None and info.stop.is_set()):
        raise SearchTimeout


def random_move(state: dict) -> Move:
    """Return a random legal move."""
    return random.choice(legal_moves(state))


def capture_value(state: dict, move: Move) -> int:
    """Return the value of the piece a move captures, or 0 for a quiet move."""
    captured = piece_at(state["board"], move.to_square)
    if captured == EMPTY:
        return 0
    return PIECE_VALUES[captured.upper()]


def greedy_move(state: dict) -> Move:
    """
    Return the move that captures the most valuable piece.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    Move
        The capture of the most valuable piece. When no move captures anything,
        a random legal move.
    """
    moves = legal_moves(state)
    random.shuffle(moves)  # Break ties between equal captures at random
    return max(moves, key=lambda move: capture_value(state, move))


def white_score(state: dict) -> int:
    """Return the evaluation from White's side, as minimax uses it."""
    return material(state["board"]) + placement(state["board"])


def minimax(state: dict, depth: int, info: SearchInfo) -> int:
    """
    Score a position by looking `depth` moves ahead. White picks the highest
    score, Black the lowest.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when minimax returns.
    depth : int
        How many more moves (plies) to look ahead.
    info : SearchInfo
        Counts the positions visited.

    Returns
    -------
    int
        The score from White's side, assuming both sides play their best.
    """
    info.nodes += 1
    if depth == 0:
        return white_score(state)
    moves = legal_moves(state)
    if not moves:
        if in_check(state, state["turn"]):
            return -MATE_SCORE if state["turn"] == "w" else MATE_SCORE
        return 0  # Stalemate
    scores = []
    for move in moves:
        undo = make_move(state, move)
        try:
            scores.append(minimax(state, depth - 1, info))
        finally:
            undo_move(state, undo)
    return max(scores) if state["turn"] == "w" else min(scores)


def negamax(state: dict, depth: int, ply: int, info: SearchInfo) -> int:
    """
    Score a position by looking `depth` moves ahead, from the side to move.

    A score that is good for one side is bad for the other by the same amount, so
    the side to move takes the best of the negated scores of its replies. One
    function does the work of minimax's two halves.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when negamax returns.
    depth : int
        How many more moves (plies) to look ahead.
    ply : int
        How many moves from the root this position is, so a faster mate scores
        higher than a slower one.
    info : SearchInfo
        Counts the positions visited.

    Returns
    -------
    int
        The score for the side to move.
    """
    info.nodes += 1
    if depth == 0:
        return evaluate(state)
    moves = legal_moves(state)
    if not moves:
        if in_check(state, state["turn"]):
            return -(MATE_SCORE - ply)  # Checkmated: worse the sooner it happens
        return 0  # Stalemate
    best = -MATE_SCORE - 1
    for move in moves:
        undo = make_move(state, move)
        try:
            score = -negamax(state, depth - 1, ply + 1, info)
        finally:
            undo_move(state, undo)
        best = max(best, score)
    return best


def best_move(state: dict, depth: int) -> tuple[Move, int, SearchInfo]:
    """
    Search every root move with negamax and return the best one.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when the search returns.
    depth : int
        How many moves (plies) to look ahead, counting the root move.

    Returns
    -------
    tuple[Move, int, SearchInfo]
        The best move, its score for the side to move, and the search counts.
    """
    info = SearchInfo()
    moves = legal_moves(state)
    random.shuffle(moves)  # Choose at random between moves with equal scores
    best, best_score = moves[0], -MATE_SCORE - 1
    for move in moves:
        undo = make_move(state, move)
        try:
            score = -negamax(state, depth - 1, 1, info)
        finally:
            undo_move(state, undo)
        if score > best_score:
            best, best_score = move, score
    return best, best_score, info


def negamax_move(state: dict) -> Move:
    """Return the negamax move at depth 2, the brain the UCI engine uses."""
    return best_move(state, 2)[0]


def alpha_beta(
    state: dict, depth: int, ply: int, alpha: int, beta: int, info: SearchInfo
) -> int:
    """
    Negamax with alpha-beta pruning: the same score, far fewer positions.

    Once one reply shows that a move is worse than a move already found, the
    other replies to it cannot help, so the search skips them (a cutoff).

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when alpha_beta returns.
    depth : int
        How many more moves (plies) to look ahead.
    ply : int
        How many moves from the root this position is.
    alpha : int
        The score the side to move is already sure of.
    beta : int
        The score above which the opponent will avoid this position.
    info : SearchInfo
        Counts the positions visited.

    Returns
    -------
    int
        The same score negamax returns at this depth.
    """
    info.nodes += 1
    if depth == 0:
        return evaluate(state)
    moves = legal_moves(state)
    if not moves:
        return -(MATE_SCORE - ply) if in_check(state, state["turn"]) else 0
    for move in moves:
        undo = make_move(state, move)
        try:
            score = -alpha_beta(state, depth - 1, ply + 1, -beta, -alpha, info)
        finally:
            undo_move(state, undo)
        if score >= beta:
            return score  # Cutoff: the opponent will not allow this
        alpha = max(alpha, score)
    return alpha


def capture_moves(state: dict) -> list[Move]:
    """
    Return the legal moves that capture a piece or promote a pawn.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    list[Move]
        The captures (including en passant) and promotions, the moves quiescence
        search keeps playing until the position is quiet.
    """
    board = state["board"]
    captures = []
    for move in legal_moves(state):
        is_en_passant = move.to_square == state["en_passant"] and (
            piece_at(board, move.from_square).upper() == "P"
        )
        if piece_at(board, move.to_square) != EMPTY or is_en_passant or move.promotion:
            captures.append(move)
    return captures


def quiescence(state: dict, alpha: int, beta: int, info: SearchInfo) -> int:
    """
    Keep searching captures until the position is quiet, then evaluate it.

    A search that stops in the middle of an exchange sees a queen take a pawn but
    not the pawn that takes the queen back (the horizon effect). Quiescence lets
    the side to move "stand pat" with the current score, or try a capture that
    might do better.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when quiescence returns.
    alpha : int
        The score the side to move is already sure of.
    beta : int
        The score the opponent will not allow the side to move to exceed.
    info : SearchInfo
        Counts positions and holds the deadline.

    Returns
    -------
    int
        The score for the side to move.
    """
    info.nodes += 1
    check_time(info)
    stand_pat = evaluate(state)
    if stand_pat >= beta:
        return stand_pat
    alpha = max(alpha, stand_pat)
    for move in order_moves(capture_moves(state), state["board"]):
        undo = make_move(state, move)
        try:
            score = -quiescence(state, -beta, -alpha, info)
        finally:
            undo_move(state, undo)
        if score >= beta:
            return score
        alpha = max(alpha, score)
    return alpha


def alpha_beta_with_quiescence(
    state: dict,
    depth: int,
    ply: int,
    alpha: int,
    beta: int,
    info: SearchInfo,
    first: Move | None = None,
) -> tuple[int, list[Move]]:
    """
    The full Day 8 search: alpha-beta with quiescence at the leaves, ordered
    moves, a check extension, a clock, and the line of best play.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when alpha_beta returns.
    depth : int
        How many more moves (plies) to look ahead before quiescence takes over.
    ply : int
        How many moves from the root this position is.
    alpha : int
        The score the side to move is already sure of.
    beta : int
        The score above which the opponent will avoid this position.
    info : SearchInfo
        Counts positions and holds the deadline.
    first : Move | None
        A move to try first, such as the best move of the last iteration.

    Returns
    -------
    tuple[int, list[Move]]
        The score for the side to move, and the principal variation: the line
        of best play that leads to that score.
    """
    info.nodes += 1
    check_time(info)
    in_check_now = in_check(state, state["turn"])
    if in_check_now:
        depth += 1  # Check extension: never stop the search while in check
    if depth <= 0:
        return quiescence(state, alpha, beta, info), []
    moves = legal_moves(state)
    if not moves:
        if in_check_now:
            return -(MATE_SCORE - ply), []
        return 0, []
    best_line = []
    for move in order_moves(moves, state["board"], first):
        undo = make_move(state, move)
        try:
            score, line = alpha_beta_with_quiescence(
                state, depth - 1, ply + 1, -beta, -alpha, info
            )
            score = -score
        finally:
            undo_move(state, undo)
        if score >= beta:
            return score, [move] + line  # Cutoff: the opponent will not allow this
        if score > alpha:
            alpha = score
            best_line = [move] + line
    return alpha, best_line


def remember_killer(
    info: SearchInfo, ply: int, move: Move, board: list[list[str]]
) -> None:
    """Keep a quiet move that caused a cutoff as one of two killers for this ply."""
    if piece_at(board, move.to_square) != EMPTY or move.promotion is not None:
        return  # Captures are already ordered first
    killers = info.killers.setdefault(ply, [])
    if move not in killers:
        killers.insert(0, move)
        del killers[2:]


def make_null_move(state: dict) -> tuple[int, int] | None:
    """
    Pass the turn without moving a piece: the null move. Chess has no such move,
    but the search uses it to ask "is my position so good that even passing wins?"

    Parameters
    ----------
    state : dict
        The game state. The side to move changes and the en passant target clears.

    Returns
    -------
    tuple[int, int] | None
        The en passant target before the null move, which undo_null_move restores.
    """
    en_passant = state["en_passant"]
    state["turn"] = opponent(state["turn"])
    state["en_passant"] = None
    state["history"].append(position_key(state))
    return en_passant


def undo_null_move(state: dict, en_passant: tuple[int, int] | None) -> None:
    """Take back a null move, restoring the side to move and the en passant target."""
    state["history"].pop()
    state["turn"] = opponent(state["turn"])
    state["en_passant"] = en_passant


def has_pieces(board: list[list[str]], color: str) -> bool:
    """Return True if the color has a knight, bishop, rook, or queen."""
    pieces = "NBRQ" if color == "w" else "nbrq"
    return any(piece in pieces for row in board for piece in row)


def reduction(
    depth: int, index: int, move: Move, captured: str, gives_check: bool
) -> int:
    """
    Return how many plies to cut from the search of one move: late move reductions.

    Parameters
    ----------
    depth : int
        How many plies the search still looks ahead.
    index : int
        The move's place in the ordered list, counting from 0.
    move : Move
        The move.
    captured : str
        The piece the move captured, or EMPTY.
    gives_check : bool
        True if the move puts the opponent in check.

    Returns
    -------
    int
        1 for a late, quiet move (no capture, no promotion, no check) with at least
        3 plies to go, because move ordering puts the best moves first and a late
        quiet move rarely turns out best. Otherwise 0.
    """
    late = index >= LATE_MOVE_INDEX and depth >= 3
    quiet = captured == EMPTY and move.promotion is None
    return 1 if late and quiet and not gives_check else 0


def upgraded_search(
    state: dict,
    depth: int,
    ply: int,
    alpha: int,
    beta: int,
    info: SearchInfo,
    allow_null: bool = True,
) -> tuple[int, list[Move]]:
    """
    The final Day 10 search: alpha_beta_with_quiescence plus the upgrade stations.

    - Draw sense: a position that repeats inside the search, or that reaches the
      fifty-move limit, scores 0.
    - Transposition table: a position already searched deeply enough is not
      searched again, and its stored best move is tried first.
    - Killer moves: quiet moves that caused cutoffs at this ply are tried early.
    - Principal variation search: the first move gets the full window; every other
      move first gets a null window (alpha, alpha + 1) that only asks "is this
      move better?", and is searched again in full only when the answer is yes.
    - Null-move pruning: if passing the turn still scores at least beta in a
      shallower search, a real move will too, so the position is cut off early.
    - Late move reductions: late, quiet moves get a search one ply shallower,
      and a full-depth search only if they turn out better than alpha.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when the search returns.
    depth : int
        How many more moves (plies) to look ahead before quiescence takes over.
    ply : int
        How many moves from the root this position is.
    alpha : int
        The score the side to move is already sure of.
    beta : int
        The score above which the opponent will avoid this position.
    info : SearchInfo
        Counts positions and holds the deadline, table, and killers.
    allow_null : bool
        False right after a null move, so that two passes never follow each other.

    Returns
    -------
    tuple[int, list[Move]]
        The score for the side to move, and the principal variation.
    """
    info.nodes += 1
    check_time(info)
    key = state["history"][-1]
    if ply > 0 and (state["history"].count(key) >= 2 or state["halfmove_clock"] >= 100):
        return 0, []  # Draw sense: a repeated position is a draw, not a gain
    in_check_now = in_check(state, state["turn"])
    if in_check_now:
        depth += 1
    if depth <= 0:
        return quiescence(state, alpha, beta, info), []
    stored = probe(info.table, key, depth, alpha, beta)
    if ply > 0 and stored is not None:
        return stored, []
    # Null-move pruning, skipped in check (passing would be illegal) and with only
    # pawns left, where passing can be better than any move (zugzwang)
    can_pass = allow_null and ply > 0 and not in_check_now and depth >= 3
    if (
        can_pass
        and abs(beta) < MATE_SCORE - 1000
        and has_pieces(state["board"], state["turn"])
    ):
        en_passant = make_null_move(state)
        try:
            score, _ = upgraded_search(
                state,
                depth - 1 - NULL_MOVE_REDUCTION,
                ply + 1,
                -beta,
                -beta + 1,
                info,
                allow_null=False,
            )
            score = -score
        finally:
            undo_null_move(state, en_passant)
        if score >= beta:
            return beta, []
    moves = legal_moves(state)
    if not moves:
        return (-(MATE_SCORE - ply) if in_check_now else 0), []

    original_alpha = alpha
    best_line = []
    ordered = order_moves(
        moves, state["board"], best_stored_move(info.table, key), info.killers.get(ply)
    )
    for index, move in enumerate(ordered):
        cut = 0
        undo = make_move(state, move)
        try:
            if index == 0:
                score, line = upgraded_search(
                    state, depth - 1, ply + 1, -beta, -alpha, info
                )
                score = -score
            else:
                gives_check = in_check(state, state["turn"])
                cut = reduction(depth, index, move, undo["captured"], gives_check)
                score, line = upgraded_search(
                    state, depth - 1 - cut, ply + 1, -alpha - 1, -alpha, info
                )
                score = -score
                if cut and score > alpha:  # A late move surprised: search full depth
                    score, line = upgraded_search(
                        state, depth - 1, ply + 1, -alpha - 1, -alpha, info
                    )
                    score = -score
                if (
                    alpha < score < beta
                ):  # A surprise: search it again with the full window
                    score, line = upgraded_search(
                        state, depth - 1, ply + 1, -beta, -alpha, info
                    )
                    score = -score
        finally:
            undo_move(state, undo)
        if score >= beta:
            remember_killer(info, ply, move, state["board"])
            if abs(score) < MATE_SCORE - 1000:
                store(info.table, key, depth, score, LOWER, move)
            return score, [move] + line
        if score > alpha:
            alpha = score
            best_line = [move] + line
    if (
        abs(alpha) < MATE_SCORE - 1000
    ):  # Mate scores depend on ply, so they are not stored
        bound = EXACT if alpha > original_alpha else UPPER
        store(info.table, key, depth, alpha, bound, best_line[0] if best_line else None)
    return alpha, best_line


def format_info(depth: int, score: int, nodes: int, pv: list[Move]) -> str:
    """
    Return a UCI "info" line so the GUI can show what Remus is thinking.

    Parameters
    ----------
    depth : int
        The depth just finished.
    score : int
        The score in centipawns for the side to move.
    nodes : int
        Positions visited so far.
    pv : list[Move]
        The principal variation.

    Returns
    -------
    str
        Text such as "info depth 3 score cp 35 nodes 4120 pv e2e4 e7e5 g1f3". A
        mate score is written as "score mate 2", counted in moves, not plies.
    """
    if abs(score) > MATE_SCORE - 1000:
        plies = MATE_SCORE - abs(score)
        moves_to_mate = (plies + 1) // 2
        score_text = f"mate {moves_to_mate if score > 0 else -moves_to_mate}"
    else:
        score_text = f"cp {score}"
    line = " ".join(move_to_uci(move) for move in pv)
    return f"info depth {depth} score {score_text} nodes {nodes} pv {line}"


def think(
    state: dict,
    seconds: float = 2.0,
    max_depth: int = 64,
    stop: threading.Event | None = None,
    report=None,
) -> Move:
    """
    Search one move deeper at a time until time runs out, and return the best move.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when the search returns.
    seconds : float
        How long to think.
    max_depth : int
        The deepest search to try.
    stop : threading.Event | None
        An event the GUI sets to stop the search early.
    report : callable | None
        Called with each finished depth's info line, such as the UCI send().
        Each depth runs upgraded_search; its transposition table carries the best
        move of one depth into the next.

    Returns
    -------
    Move
        The best move of the deepest search that finished.
    """
    info = SearchInfo(deadline=time.perf_counter() + seconds, stop=stop)
    moves = legal_moves(state)
    best = order_moves(moves, state["board"])[0]
    for depth in range(1, max_depth + 1):
        try:
            score, pv = upgraded_search(
                state, depth, 0, -MATE_SCORE - 1, MATE_SCORE + 1, info
            )
        except SearchTimeout:
            break  # Keep the best move of the last depth that finished
        if pv:
            best = pv[0]
        if report is not None:
            report(format_info(depth, score, info.nodes, pv))
        if abs(score) > MATE_SCORE - 1000 or len(moves) == 1:
            break  # A forced mate or a single legal move needs no deeper search
    return best


def think_move(state: dict) -> Move:
    """Return the iterative-deepening move with two seconds to think."""
    return think(state, 2.0)


def main():
    state = state_from_fen("4k3/8/8/3q4/8/2N1p3/8/4K3 w - - 0 1")
    print(
        f"Greedy move: {move_to_uci(greedy_move(state))}  (expected c3d5, taking the queen)"
    )
    print(f"Random move: {move_to_uci(random_move(state))}  (any legal move)")

    state = state_from_fen("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1")
    before = state_snapshot(state)
    move, score, info = best_move(state, 2)
    print(
        f"Back-rank mate: {move_to_uci(move)} scores {score}  (expected a1a8 and {MATE_SCORE - 1})"
    )
    print(
        f"Positions visited: {info.nodes:,}; root unchanged: {state_snapshot(state) == before}"
    )
    minimax_info = SearchInfo()
    print(
        f"Minimax agrees: {minimax(state, 2, minimax_info) == MATE_SCORE}  (expected True)"
    )

    state = state_from_fen(
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    )
    plain = SearchInfo()
    plain_score = negamax(state, 3, 0, plain)
    pruned = SearchInfo()
    pruned_score = alpha_beta(state, 3, 0, -MATE_SCORE - 1, MATE_SCORE + 1, pruned)
    print(f"Negamax depth 3: score {plain_score}, {plain.nodes:,} positions")
    print(
        f"Alpha-beta depth 3: score {pruned_score}, {pruned.nodes:,} positions"
        "  (expected the same score, fewer positions)"
    )
    print("Thinking for 2 seconds from that position:")
    think(state, 2.0, report=print)


if __name__ == "__main__":
    main()
