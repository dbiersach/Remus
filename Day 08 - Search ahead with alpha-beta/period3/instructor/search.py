#!/usr/bin/env -S uv run
"""search.py

Choose a move. Remus's first two "brains" are simple: a random legal move, and a
greedy move that grabs the most valuable piece it can capture. Then Remus looks
ahead: minimax tries every move and every reply, and negamax does the same work
with one function instead of two mirror-image halves.

Day 8 makes the search smarter without changing its answer: alpha-beta skips
moves that cannot change the result, and quiescence keeps looking until the
captures stop.
"""

import random
from dataclasses import dataclass

from attacks import in_check
from board import EMPTY, piece_at
from evaluation import PIECE_VALUES, evaluate
from fen import state_from_fen
from legal_moves import legal_moves
from make_move import make_move, state_snapshot, undo_move
from moves import Move, move_to_uci

# Larger than any material count; a mate n plies away scores MATE_SCORE - n
MATE_SCORE = 100_000


@dataclass
class SearchInfo:
    """What a search counts while it runs."""

    nodes: int = 0  # Positions visited


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
            scores.append(minimax(state, depth - 1, info))  # Recursive call to itself
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
            # Recursive call to itself
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
            # Recursive call to itself
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
        Counts the positions visited.

    Returns
    -------
    int
        The score for the side to move.
    """
    info.nodes += 1
    stand_pat = evaluate(state)
    if stand_pat >= beta:
        return stand_pat
    alpha = max(alpha, stand_pat)
    for move in capture_moves(state):
        undo = make_move(state, move)
        try:
            score = -quiescence(state, -beta, -alpha, info)  # Recursive call to itself
        finally:
            undo_move(state, undo)
        if score >= beta:
            return score
        alpha = max(alpha, score)
    return alpha


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


if __name__ == "__main__":
    main()
