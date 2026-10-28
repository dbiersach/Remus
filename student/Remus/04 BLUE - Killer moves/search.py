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

The BLUE color version adds killer_search, and think uses it.
"""

import random
import time
from dataclasses import dataclass, field

from attacks import in_check
from board import EMPTY, Board, piece_at
from evaluation import PIECE_VALUES, evaluate
from fen import state_from_fen
from legal_moves import legal_moves
from make_move import make_move, state_snapshot, undo_move
from move_ordering import order_moves
from moves import Move, move_to_uci

# Larger than any material count; a mate n plies away scores MATE_SCORE - n
MATE_SCORE = 100_000


@dataclass
class SearchInfo:
    """What a search counts while it runs."""

    nodes: int = 0  # Positions visited
    deadline: float | None = None  # time.perf_counter() value when the search must stop
    killers: dict = field(default_factory=dict)  # Ply -> up to two killer moves


class SearchTimeout(Exception):
    """Raised inside the search when time is up, to unwind back to the root."""


def check_time(info: SearchInfo) -> None:
    """Raise SearchTimeout if the deadline has passed."""
    if info.deadline is not None and time.perf_counter() > info.deadline:
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
    best_move = moves[0]
    best_value = capture_value(state, best_move)
    for move in moves:
        value = capture_value(state, move)
        if value > best_value:
            best_move = move
            best_value = value
    return best_move


def white_score(state: dict) -> int:
    """Return the evaluation from White's side, as minimax uses it."""
    return evaluate(state) if state["turn"] == "w" else -evaluate(state)


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


def remember_killer(info: SearchInfo, ply: int, move: Move, board: Board) -> None:
    """Keep a quiet move that caused a cutoff as one of two killers for this ply."""
    # Day 9, period 2: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 9 P2: write remember_killer()")


def killer_search(
    state: dict,
    depth: int,
    ply: int,
    alpha: int,
    beta: int,
    info: SearchInfo,
    first: Move | None = None,
) -> tuple[int, list[Move]]:
    """
    The Remus-BLUE search: the Day 9 search plus killer moves. A quiet move
    that caused a cutoff at this ply is tried right after the captures in the
    next position at the same ply.

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
    killers = info.killers.get(ply)
    for move in order_moves(moves, state["board"], first, killers):
        undo = make_move(state, move)
        try:
            score, line = killer_search(state, depth - 1, ply + 1, -beta, -alpha, info)
            score = -score
        finally:
            undo_move(state, undo)
        if score >= beta:
            remember_killer(info, ply, move, state["board"])
            return score, [move] + line  # Cutoff: the opponent will not allow this
        if score > alpha:
            alpha = score
            best_line = [move] + line
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
    line = ""
    for move in pv:
        line += " " + move_to_uci(move)
    return f"info depth {depth} score {score_text} nodes {nodes} pv{line}"


def think(state: dict, seconds: float = 2.0, max_depth: int = 64, report=None) -> Move:
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
    report : callable | None
        Called with each finished depth's info line, such as the UCI send().

    Returns
    -------
    Move
        The best move of the deepest search that finished.
    """
    info = SearchInfo(deadline=time.perf_counter() + seconds)
    moves = legal_moves(state)
    best = order_moves(moves, state["board"])[0]
    for depth in range(1, max_depth + 1):
        try:
            score, pv = killer_search(
                state, depth, 0, -MATE_SCORE - 1, MATE_SCORE + 1, info, best
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
