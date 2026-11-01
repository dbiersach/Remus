#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = ["matplotlib", "imageio-ffmpeg"]
# ///
"""make_game_tree_video.py

Make the game tree video: minimax, negamax, and alpha-beta searching one small tree.

A course designer tool, like the other make_*.py scripts. It searches a three-ply
tree with eight leaves five times (minimax, negamax, alpha-beta with White's alpha
and beta, alpha_beta as Remus writes it, and alpha-beta with the best move first),
draws every step with matplotlib, and writes misc/teachers/videos/game_tree_search.mp4.
Each step shows the tree, the score or window beside every node on the search path,
a narration panel that says why the step happens, and the lines of search.py it
runs. The inline script block above names matplotlib and imageio-ffmpeg (which
carries its own ffmpeg), so `uv run misc/designer/make_game_tree_video.py` installs
them for this script alone; Remus itself and the class laptops never need them.
Pass --stills to also save one PNG per step in the git-ignored tmp/game_tree_stills/
folder, for checking.
"""

import copy
import math
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Draw straight to memory, with no window

import imageio_ffmpeg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder, above misc/designer/
OUT = ROOT / "misc" / "teachers" / "videos"
VIDEO = OUT / "game_tree_search.mp4"

WIDTH, HEIGHT = 1920, 1080  # Full HD frames
FPS = 15  # Frames per second: every step is a still picture, so 15 is plenty
FADE_FRAMES = 5  # A short cross-fade between steps (a third of a second)
SECONDS_PER_WORD = 0.27  # Hold each step long enough to read its narration
MIN_HOLD, MAX_HOLD = 3.0, 13.0  # Shortest and longest hold of one step, in seconds

INF = math.inf
ROOT_NODE = "Start"

# Each position is named by the move that reaches it. White moves first (A or B),
# Black replies (A1, A2, B1, B2), White moves again (C to J), and the eight leaves
# are scored from White's side: bigger is better for White.
CHILDREN = {
    "Start": ["A", "B"],
    "A": ["A1", "A2"],
    "B": ["B1", "B2"],
    "A1": ["C", "D"],
    "A2": ["E", "F"],
    "B1": ["G", "H"],
    "B2": ["I", "J"],
}
LEAF_SCORES = {"C": 2, "D": 6, "E": 1, "F": -3, "G": -1, "H": 1, "I": 3, "J": 2}
LEAVES = list(LEAF_SCORES)
LEVEL = {"Start": 0, "A": 1, "B": 1, "A1": 2, "A2": 2, "B1": 2, "B2": 2}
for leaf in LEAVES:
    LEVEL[leaf] = 3
PARENT = {child: node for node, kids in CHILDREN.items() for child in kids}

# Where each node sits in the frame, in pixels from the top left corner
TREE_LEFT, TREE_RIGHT = 400, 1150
PANEL_LEFT, PANEL_WIDTH = 1250, 640  # The narration and code panels on the right
LEVEL_Y = [250, 435, 620, 805]
NODE_RADIUS = 36

# Colors
PAPER = "#fbfaf6"
INK = "#1f2328"
FAINT = "#c9ccd1"
WHITE_PIECE = "#ffffff"
BLACK_PIECE = "#2b2b2b"
HIGHLIGHT = "#f08c00"  # The node the search is looking at
PATH = "#f08c00"  # Edges on the current search path
VISITED = "#5c6470"  # Edges the search has walked
CUT = "#d6336c"  # Cutoffs and skipped branches
BEST = "#2f9e44"  # The best line at the end
TAG_FILL = "#fff4d6"  # Score and window labels
MUTED = "#6b7280"  # Quiet labels
PANEL = "#ffffff"
CODE_FILL = "#f3f4f6"
CODE_LIT = "#ffe8a3"


def node_xy(node: str) -> tuple[float, float]:
    """Return the pixel position of a node: each parent sits above the middle of its leaves."""
    if node in LEAF_SCORES:
        step = (TREE_RIGHT - TREE_LEFT) / (len(LEAVES) - 1)
        return TREE_LEFT + LEAVES.index(node) * step, LEVEL_Y[3]
    xs = [node_xy(child)[0] for child in CHILDREN[node]]
    return sum(xs) / len(xs), LEVEL_Y[LEVEL[node]]


def side(node: str) -> str:
    """Return the side to move at a node: White at levels 0 and 2, Black at 1 and 3."""
    return "White" if LEVEL[node] % 2 == 0 else "Black"


def other(color: str) -> str:
    return "Black" if color == "White" else "White"


def fmt(value: float) -> str:
    """Write a score, with infinity as a symbol and a plain hyphen for minus."""
    if value == INF:
        return "+∞"
    if value == -INF:
        return "-∞"
    return str(int(value))


def below(node: str) -> list[str]:
    """Return every node under a node, children first."""
    found = []
    for child in CHILDREN.get(node, []):
        found.append(child)
        found += below(child)
    return found


def skipped_words(nodes: list[str]) -> str:
    """Name the branches a cutoff skips, such as "B2 and its leaves I and J"."""
    parts = []
    for node in nodes:
        if node in LEAF_SCORES:
            parts.append(f"leaf {node}")
        else:
            parts.append(f"{node} and its leaves {' and '.join(CHILDREN[node])}")
    return " and ".join(parts)


class Scene:
    """Everything one frame shows."""

    def __init__(self, title: str, panel: str, code: list[str] | None):
        self.title = title
        self.panel = panel  # The heading of the box under the narration
        self.code = code  # Lines of search.py, or None to show the rules instead
        self.rules: list[str] = []
        self.lit: set[int] = set()  # Code lines to highlight
        self.text = ""
        self.current: str | None = None
        self.path: list[str] = []  # Nodes from the root to the node being searched
        self.values: dict[str, str] = {}  # The score written inside a node
        self.tags: dict[str, str] = {}  # The score or window of each node on the path
        self.walked: set[str] = set()  # Nodes reached so far (named by their edge)
        self.cut: set[str] = set()  # Nodes skipped by a cutoff
        self.cut_marks: set[str] = set()  # Edges that carry the cutoff mark
        self.best: set[str] = set()  # Nodes on the best line, drawn in green
        self.leaf_view = "White"  # Whose side the leaf scores are written from
        self.leaves_scored = 0
        self.last_path: list[str] = []  # The path at the last step shown


class Movie:
    """Collect the steps of the whole video, each a copy of the scene."""

    def __init__(self):
        self.steps: list[tuple[str, object]] = []

    def card(self, heading: str, lines: list[str]):
        self.steps.append(("card", (heading, lines)))

    def snap(self, scene: Scene, text: str, lit: set[int] | None = None):
        scene.text = text
        scene.lit = lit or set()
        self.steps.append(("scene", copy.deepcopy(scene)))
        scene.last_path = list(scene.path)
        if scene.current in LEAF_SCORES and scene.current in scene.path:
            scene.path.remove(scene.current)  # A leaf is done once it is shown


def enter(scene: Scene, node: str):
    """Walk one edge down the tree."""
    scene.current = node
    scene.path.append(node)
    scene.walked.add(node)


def leave(scene: Scene, node: str):
    scene.path.remove(node)
    scene.tags.pop(node, None)
    scene.current = PARENT.get(node, ROOT_NODE)


def descent_words(path_before: list[str], node: str) -> str:
    """Say which new nodes the search walks down to reach a leaf, such as "Go down A, A1 to leaf C."."""
    new_nodes = []
    walk = node
    while walk not in path_before and walk != ROOT_NODE:
        new_nodes.insert(0, walk)
        walk = PARENT[walk]
    if len(new_nodes) <= 1:
        return ""
    return "Go down " + ", ".join(new_nodes[:-1]) + f" to leaf {new_nodes[-1]}. "


# The lines of search.py each pass shows, shortened: the position counter and the
# checks for mate and stalemate are left out so the search itself stands out.
MINIMAX_CODE = [
    "def minimax(state, depth):",
    "    if depth == 0:",
    "        return white_score(state)",
    "    scores = []",
    "    for move in legal_moves(state):",
    "        undo = make_move(state, move)",
    "        scores.append(minimax(state, depth - 1))",
    "        undo_move(state, undo)",
    '    if state["turn"] == "w":',
    "        return max(scores)",
    "    return min(scores)",
]
NEGAMAX_CODE = [
    "def negamax(state, depth):",
    "    if depth == 0:",
    "        return evaluate(state)",
    "    best = -infinity",
    "    for move in legal_moves(state):",
    "        undo = make_move(state, move)",
    "        score = -negamax(state, depth - 1)",
    "        undo_move(state, undo)",
    "        best = max(best, score)",
    "    return best",
]
ALPHA_BETA_CODE = [
    "def alpha_beta(state, depth, alpha, beta):",
    "    if depth == 0:",
    "        return evaluate(state)",
    "    for move in legal_moves(state):",
    "        undo = make_move(state, move)",
    "        score = -alpha_beta(state, depth - 1,",
    "                            -beta, -alpha)",
    "        undo_move(state, undo)",
    "        if score >= beta:",
    "            return score  # Cutoff",
    "        alpha = max(alpha, score)",
    "    return alpha",
]
WINDOW_RULES = [
    "α (alpha): the score White is already",
    "sure of. White to move raises α.",
    "",
    "β (beta): the score Black is already",
    "sure of. Black to move lowers β.",
    "",
    "Both are written from White's side.",
    "A child starts with its parent's α and β.",
    "",
    "Cutoff when α ≥ β: the side that moved",
    "into this position already has something",
    "at least as good elsewhere, so the game",
    "never gets here. Skip the other moves.",
]


def run_minimax(movie: Movie):
    scene = Scene("Pass 1: Minimax", "search.py: minimax (shortened)", MINIMAX_CODE)
    movie.card(
        "Pass 1: Minimax",
        [
            "White moves at Start, Black replies, White moves again.",
            "The eight leaves are scored from White's side:",
            "bigger is better for White, smaller is better for Black.",
            "",
            "White picks the largest score. Black picks the smallest.",
        ],
    )
    movie.snap(
        scene,
        "This is the tree. Each position is named by the move that reaches it. "
        "White circles are positions with White to move, black circles with Black "
        "to move. The numbers under the leaves are their scores for White.",
    )
    movie.snap(
        scene,
        "Minimax walks the tree from left to right. At each position it remembers "
        "the best score it has seen so far: the largest one when White is to move, "
        "the smallest one when Black is to move.",
        {3, 4},
    )

    def minimax(node: str) -> int:
        enter(scene, node)
        if node in LEAF_SCORES:
            scene.leaves_scored += 1
            scene.values[node] = fmt(LEAF_SCORES[node])
            return LEAF_SCORES[node]
        best = None
        for child in CHILDREN[node]:
            value = minimax(child)
            scene.current = child
            if child in LEAF_SCORES:
                said = descent_words(scene.last_path, child)
                said += f"Leaf {child} scores {value} for White. "
                lit = {1, 2, 6}
            else:
                said = f"{child} has tried all its moves, so {child} is worth {value}. "
                lit = {6, 9} if side(child) == "White" else {6, 10}
            mover = side(node)
            want = "largest" if mover == "White" else "smallest"
            name = "max" if mover == "White" else "min"
            if best is None:
                said += (
                    f"It is the first score {node} has seen, so {node}'s {name} so "
                    f"far is {value}."
                )
                best = value
            elif (mover == "White" and value > best) or (
                mover == "Black" and value < best
            ):
                said += (
                    f"{mover} wants the {want} score, and {value} beats {best}, so "
                    f"{node}'s {name} so far becomes {value}."
                )
                best = value
            else:
                said += (
                    f"{mover} wants the {want} score, and {value} does not beat "
                    f"{best}, so {node} keeps {best}."
                )
            scene.tags[node] = f"{name} so far: {fmt(best)}"
            movie.snap(scene, said, lit)
            scene.current = node
        scene.values[node] = fmt(best)
        leave(scene, node)
        return best

    value = minimax(ROOT_NODE)
    scene.current = ROOT_NODE
    scene.values[ROOT_NODE] = fmt(value)
    scene.best = {ROOT_NODE, "A", "A2", "E"}
    movie.snap(
        scene,
        f"Start has tried both moves. A and B are both worth {value}, and A came "
        "first, so White plays A. The green line is the game minimax expects: "
        "White A, Black A2, White E, worth 1 for White. Minimax scored all 8 leaves.",
        {9},
    )


def run_negamax(movie: Movie):
    scene = Scene("Pass 2: Negamax", "search.py: negamax (shortened)", NEGAMAX_CODE)
    scene.leaf_view = "mover"
    movie.card(
        "Pass 2: Negamax",
        [
            "The same tree, searched with one rule instead of two.",
            "",
            "Every score is from the side to move.",
            "A score that is good for one side is bad for the other",
            "by the same amount, so a child's score changes sign",
            "on its way up: my score is minus my opponent's.",
        ],
    )
    movie.snap(
        scene,
        "Negamax writes every score from the side to move. Black is to move at "
        "the leaves, so evaluate() gives each leaf the opposite of its White score: "
        "leaf C, worth 2 for White, is worth -2 for Black.",
    )

    def negamax(node: str) -> int:
        enter(scene, node)
        if node in LEAF_SCORES:
            scene.leaves_scored += 1
            value = -LEAF_SCORES[node]  # Black is to move at every leaf
            scene.values[node] = fmt(value)
            return value
        best = -INF
        for child in CHILDREN[node]:
            value = negamax(child)
            scene.current = child
            if child in LEAF_SCORES:
                said = (
                    descent_words(scene.last_path, child)
                    + f"Leaf {child}: evaluate() gives {value} for Black, who is to "
                    "move there. "
                )
            else:
                said = f"{child} returns {value}, its best for {side(child)}. "
            score = -value
            old = best
            best = max(best, score)
            said += (
                f"At {node}, {side(node)} flips the sign: score = -({value}) = "
                f"{score}. best = max({fmt(old)}, {score}) = {fmt(best)}."
            )
            scene.tags[node] = f"best so far: {fmt(best)}"
            movie.snap(scene, said, {6, 8} if child not in LEAF_SCORES else {2, 6, 8})
            scene.current = node
        scene.values[node] = fmt(best)
        leave(scene, node)
        return int(best)

    value = negamax(ROOT_NODE)
    scene.current = ROOT_NODE
    scene.values[ROOT_NODE] = fmt(value)
    scene.best = {ROOT_NODE, "A", "A2", "E"}
    movie.snap(
        scene,
        f"Start returns {value} for White, the same answer as minimax, and the same "
        "move A. Look at A and B: they say -1 because Black is to move there, and "
        "-1 for Black is +1 for White. Negamax also scored all 8 leaves.",
        {9},
    )


def run_window_alpha_beta(movie: Movie, best_first: bool):
    """Alpha-beta with alpha and beta both written from White's side."""
    if best_first:
        title = "Pass 5: Alpha-beta, best move first"
        order = {**CHILDREN, "A": ["A2", "A1"]}
        movie.card(
            title,
            [
                "Alpha-beta cuts the most when the best move comes first.",
                "",
                "Search the same tree again, but at A let Black try",
                "its best reply, A2, before A1. Remus's order_moves",
                "sorts moves so that the likely best ones come first.",
            ],
        )
    else:
        title = "Pass 3: Alpha-beta"
        order = CHILDREN
        movie.card(
            title,
            [
                "The same tree. Alpha-beta gets the same answer as minimax,",
                "but it skips moves that cannot change the answer.",
                "",
                "α (alpha) is the score White is already sure of.",
                "β (beta) is the score Black is already sure of.",
                "Both are written from White's side.",
            ],
        )
    scene = Scene(title, "The rules", None)
    scene.rules = WINDOW_RULES
    if best_first:
        intro = (
            "At Start nothing is known yet: α = -∞ and β = +∞. This time the "
            "search tries A2 before A1 at position A. Watch for two cutoffs."
        )
    else:
        intro = (
            "At Start nothing is known yet, so α = -∞ (White is sure of nothing) "
            "and β = +∞ (Black is sure of nothing). Each child starts with the α "
            "and β of its parent, the window passed down the tree."
        )
    enter(scene, ROOT_NODE)
    scene.tags[ROOT_NODE] = "α = -∞    β = +∞"
    movie.snap(scene, intro)

    def search(node: str, alpha: float, beta: float) -> tuple[int, str]:
        """Return a node's score for White and how it is written (2, ≤ 1, or ≥ 2)."""
        if node in LEAF_SCORES:
            scene.leaves_scored += 1
            scene.values[node] = fmt(LEAF_SCORES[node])
            return LEAF_SCORES[node], fmt(LEAF_SCORES[node])
        mover = side(node)
        best = -INF if mover == "White" else INF
        kids = order[node]
        for index, child in enumerate(kids):
            enter(scene, child)
            if child not in LEAF_SCORES:
                scene.tags[child] = f"α = {fmt(alpha)}    β = {fmt(beta)}"
                movie.snap(
                    scene,
                    f"Go down to {child}, with {side(child)} to move. {child} starts "
                    f"with the window of {node}: α = {fmt(alpha)}, β = {fmt(beta)}.",
                )
            value, written = search(child, alpha, beta)
            scene.current = child
            if child in LEAF_SCORES:
                said = descent_words(scene.last_path, child)
                said += f"Leaf {child} scores {value} for White. "
            elif written.startswith(("≤", "≥")):
                said = f"{child} was cut off, so {child} is worth {written} for White. "
            else:
                said = f"{child} is finished: worth {value} for White. "
            if mover == "White":
                best = max(best, value)
                if best > alpha:
                    said += f"White raises α at {node} to {fmt(best)}. "
                    alpha = best
                else:
                    said += f"That does not raise α = {fmt(alpha)}. "
            else:
                best = min(best, value)
                if best < beta:
                    said += f"Black lowers β at {node} to {fmt(best)}. "
                    beta = best
                else:
                    said += f"That does not lower β = {fmt(beta)}. "
            scene.tags[node] = f"α = {fmt(alpha)}    β = {fmt(beta)}"
            rest = kids[index + 1 :]
            if alpha >= beta and rest:
                parent = PARENT[node]
                if mover == "White":
                    said += (
                        f"Now α = {fmt(alpha)} ≥ β = {fmt(beta)}: CUTOFF. At {node} "
                        f"White can get {fmt(best)} or more, but at {parent} Black "
                        f"already has a move that holds White to {fmt(beta)}. Black "
                        f"will never play into {node}, so skip "
                        f"{skipped_words(rest)}."
                    )
                    written = f"≥ {fmt(best)}"
                else:
                    said += (
                        f"Now α = {fmt(alpha)} ≥ β = {fmt(beta)}: CUTOFF. At {node} "
                        f"Black can hold White to {fmt(best)} or less, but at "
                        f"{parent} White is already sure of {fmt(alpha)} from an "
                        f"earlier move. White will never play {node}, so skip "
                        f"{skipped_words(rest)}."
                    )
                    written = f"≤ {fmt(best)}"
                for skipped in rest:
                    scene.cut.add(skipped)
                    scene.cut.update(below(skipped))
                    scene.cut_marks.add(skipped)
                movie.snap(scene, said)
                scene.current = node
                scene.values[node] = written
                leave(scene, node)
                return int(best), written
            if rest and node == ROOT_NODE:
                said += f"Try the next move, {rest[0]}."
            elif rest:
                said += (
                    f"α = {fmt(alpha)} is still below β = {fmt(beta)}, so the game "
                    f"can still reach {node}: keep searching."
                )
            movie.snap(scene, said)
            scene.current = node
        scene.values[node] = fmt(best)
        if node != ROOT_NODE:
            leave(scene, node)
        return int(best), fmt(best)

    value, _ = search(ROOT_NODE, -INF, INF)
    scene.current = ROOT_NODE
    scene.values[ROOT_NODE] = fmt(value)
    scene.tags.pop(ROOT_NODE, None)
    scene.best = {ROOT_NODE, "A", "A2", "E"}
    count = scene.leaves_scored
    if best_first:
        said = (
            f"White plays A, worth {value}: the same answer again. With the best "
            f"reply first, alpha-beta scored only {count} of the 8 leaves and made "
            "two cutoffs. In a real chess tree the savings are far bigger."
        )
    else:
        said = (
            f"White plays A, worth {value}, the same answer as minimax. Alpha-beta "
            f"scored {count} of the 8 leaves: the cutoff at B skipped I and J, which "
            "could not change White's choice."
        )
    movie.snap(scene, said)


def run_remus_alpha_beta(movie: Movie):
    """alpha_beta as Remus writes it: negamax with the window flipped at each call."""
    title = "Pass 4: alpha_beta in Remus"
    movie.card(
        title,
        [
            "Remus's alpha_beta is negamax with a window.",
            "",
            "alpha: the score the side to move is already sure of.",
            "beta: the score above which the opponent avoids this position.",
            "",
            "Both are from the side to move, so each call",
            "flips the window: the child gets (-beta, -alpha).",
        ],
    )
    scene = Scene(title, "search.py: alpha_beta (shortened)", ALPHA_BETA_CODE)
    scene.leaf_view = "mover"
    enter(scene, ROOT_NODE)
    scene.tags[ROOT_NODE] = "alpha = -∞   beta = +∞"
    movie.snap(
        scene,
        "Remus calls alpha_beta(Start, 3, -∞, +∞). Every number in this pass is "
        "from the side to move, as in negamax, so a child's score changes sign on "
        "the way up and the window flips on the way down.",
        {0},
    )

    def search(node: str, alpha: float, beta: float) -> tuple[int, str]:
        if node in LEAF_SCORES:
            scene.leaves_scored += 1
            value = -LEAF_SCORES[node]  # Black is to move at every leaf
            scene.values[node] = fmt(value)
            return value, fmt(value)
        kids = CHILDREN[node]
        for index, child in enumerate(kids):
            enter(scene, child)
            if child not in LEAF_SCORES:
                scene.tags[child] = f"alpha = {fmt(-beta)}   beta = {fmt(-alpha)}"
                movie.snap(
                    scene,
                    f"Call alpha_beta for {child}, {side(child)} to move. The window "
                    f"flips: alpha = -beta = {fmt(-beta)}, beta = -alpha = "
                    f"{fmt(-alpha)}.",
                    {5, 6},
                )
            value, _ = search(child, -beta, -alpha)
            scene.current = child
            if child in LEAF_SCORES:
                said = descent_words(scene.last_path, child)
                said += f"Leaf {child}: evaluate() gives {value} for Black. "
                lit = {2, 5}
            else:
                said = f"{child} returns {value}. "
                lit = {5}
            score = -value
            said += f"At {node}: score = -({value}) = {score}. "
            rest = kids[index + 1 :]
            if score >= beta:
                parent = PARENT[node]
                said += (
                    f"Is score ≥ beta ({fmt(beta)})? Yes: CUTOFF, return {score}. "
                    f"At {parent}, {side(parent)} is already sure of {fmt(-beta)}. "
                    f"{node} gives {side(parent)} {-score} at best, no better, so "
                    f"{side(parent)} avoids {node}. Skip {skipped_words(rest)}."
                )
                for skipped in rest:
                    scene.cut.add(skipped)
                    scene.cut.update(below(skipped))
                    scene.cut_marks.add(skipped)
                movie.snap(scene, said, lit | {8, 9})
                scene.current = node
                scene.values[node] = fmt(score)
                leave(scene, node)
                return score, fmt(score)
            old = alpha
            alpha = max(alpha, score)
            said += (
                f"Is score ≥ beta ({fmt(beta)})? No. alpha = max({fmt(old)}, "
                f"{score}) = {fmt(alpha)}."
            )
            scene.tags[node] = f"alpha = {fmt(alpha)}   beta = {fmt(beta)}"
            movie.snap(scene, said, lit | {8, 10})
            scene.current = node
        scene.values[node] = fmt(alpha)
        if node != ROOT_NODE:
            leave(scene, node)
        return int(alpha), fmt(alpha)

    value, _ = search(ROOT_NODE, -INF, INF)
    scene.current = ROOT_NODE
    scene.tags.pop(ROOT_NODE, None)
    scene.best = {ROOT_NODE, "A", "A2", "E"}
    movie.snap(
        scene,
        f"alpha_beta returns {value} for White and Remus plays A. It made the same "
        f"cutoff as pass 3 and scored {scene.leaves_scored} of the 8 leaves. B shows "
        "-1: Black's score there, which is +1 for White.",
        {11},
    )


def build_movie() -> Movie:
    movie = Movie()
    movie.card(
        "How a chess engine searches a game tree",
        [
            "One small tree, searched five ways:",
            "",
            "1. Minimax",
            "2. Negamax",
            "3. Alpha-beta",
            "4. alpha_beta as Remus writes it",
            "5. Alpha-beta with the best move first",
        ],
    )
    run_minimax(movie)
    run_negamax(movie)
    run_window_alpha_beta(movie, best_first=False)
    run_remus_alpha_beta(movie)
    run_window_alpha_beta(movie, best_first=True)
    movie.card(
        "Same answer, less work",
        [
            "Minimax                        8 of 8 leaves   White plays A, worth 1",
            "Negamax                        8 of 8 leaves   White plays A, worth 1",
            "Alpha-beta                     6 of 8 leaves   White plays A, worth 1",
            "alpha_beta in Remus            6 of 8 leaves   White plays A, worth 1",
            "Alpha-beta, best move first    5 of 8 leaves   White plays A, worth 1",
            "",
            "A cutoff never changes the answer. It skips moves",
            "that one side would never let the game reach.",
        ],
    )
    return movie


def draw_card(ax, heading: str, lines: list[str]):
    ax.text(
        WIDTH / 2,
        330,
        heading,
        ha="center",
        va="center",
        fontsize=46,
        fontweight="bold",
        color=INK,
    )
    mono = any("   " in line for line in lines)
    for index, line in enumerate(lines):
        ax.text(
            WIDTH / 2,
            450 + index * 58,
            line,
            ha="center",
            va="center",
            fontsize=26 if not mono else 23,
            color=INK,
            family="DejaVu Sans Mono" if mono else "DejaVu Sans",
        )


def edge_points(parent: str, child: str) -> tuple[float, float, float, float]:
    """Return an edge from the bottom of one circle to the top of the other."""
    x1, y1 = node_xy(parent)
    x2, y2 = node_xy(child)
    length = math.hypot(x2 - x1, y2 - y1)
    dx, dy = (x2 - x1) / length, (y2 - y1) / length
    return (
        x1 + dx * NODE_RADIUS,
        y1 + dy * NODE_RADIUS,
        x2 - dx * NODE_RADIUS,
        y2 - dy * NODE_RADIUS,
    )


def wrap_to_width(ax, text: str, size: float, width: float) -> list[str]:
    """Break text into lines no wider than `width` pixels at this font size."""
    renderer = ax.figure.canvas.get_renderer()
    lines, line = [], ""
    for word in text.split():
        trial = word if not line else line + " " + word
        probe = ax.text(0, 0, trial, fontsize=size)
        too_wide = probe.get_window_extent(renderer).width > width
        probe.remove()
        if too_wide and line:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def draw_scene(ax, scene: Scene):
    ax.text(60, 70, scene.title, fontsize=34, fontweight="bold", color=INK, va="center")

    # The left column: the side to move at each level, and the score or window of
    # the node the search path passes through on that level
    level_words = ["White to move", "Black to move", "White to move", "Leaves"]
    on_level = {}
    for node, tag in scene.tags.items():
        on_level[LEVEL[node]] = (node, tag)
    for level, words in enumerate(level_words):
        y = LEVEL_Y[level]
        ax.text(50, y - 52, words, fontsize=16, color=MUTED, va="center")
        if level == 3:
            ax.text(
                50, y - 18, "(Black to move)", fontsize=16, color=MUTED, va="center"
            )
        if level in on_level:
            node, tag = on_level[level]
            ax.add_patch(
                FancyBboxPatch(
                    (44, y - 30),
                    290,
                    72,
                    boxstyle="round,pad=0,rounding_size=10",
                    facecolor=TAG_FILL,
                    edgecolor=HIGHLIGHT,
                    lw=2.5,
                    zorder=7,
                )
            )
            ax.text(
                58,
                y - 10,
                node,
                fontsize=17,
                fontweight="bold",
                color=INK,
                va="center",
                zorder=8,
            )
            ax.text(58, y + 20, tag, fontsize=16, color=INK, va="center", zorder=8)
    ax.text(
        50, LEVEL_Y[3] + 75, "Score for White:", fontsize=16, color=MUTED, va="center"
    )

    # Edges
    for parent, kids in CHILDREN.items():
        for child in kids:
            x1, y1, x2, y2 = edge_points(parent, child)
            if child in scene.best and parent in scene.best:
                color, width, style = BEST, 6, "-"
            elif child in scene.path and parent in scene.path:
                color, width, style = PATH, 6, "-"
            elif child in scene.cut:
                color, width, style = CUT, 2.5, (0, (5, 4))
            elif child in scene.walked:
                color, width, style = VISITED, 3, "-"
            else:
                color, width, style = FAINT, 2.5, "-"
            ax.plot(
                [x1, x2],
                [y1, y2],
                color=color,
                lw=width,
                ls=style,
                solid_capstyle="round",
                zorder=1,
            )
            if child in scene.cut_marks:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                for offset in (-7, 7):
                    ax.plot(
                        [mx - 18, mx + 18],
                        [my - 10 + offset, my + 10 + offset],
                        color=CUT,
                        lw=5,
                        solid_capstyle="round",
                        zorder=4,
                    )
                ax.text(
                    mx + 26,
                    my - 22,
                    "cut",
                    color=CUT,
                    fontsize=18,
                    fontweight="bold",
                    zorder=4,
                )

    # Nodes
    for node in list(CHILDREN) + LEAVES:
        x, y = node_xy(node)
        white = side(node) == "White"
        reached = node in scene.walked or node == ROOT_NODE
        fade = 1.0 if reached and node not in scene.cut else 0.35
        fill = WHITE_PIECE if white else BLACK_PIECE
        ax.add_patch(
            Circle(
                (x, y),
                NODE_RADIUS,
                facecolor=fill,
                edgecolor=INK,
                lw=2.5,
                alpha=fade,
                zorder=2,
            )
        )
        if node == scene.current:
            ax.add_patch(
                Circle(
                    (x, y),
                    NODE_RADIUS + 9,
                    facecolor="none",
                    edgecolor=HIGHLIGHT,
                    lw=6,
                    zorder=3,
                )
            )
        elif node in scene.best:
            ax.add_patch(
                Circle(
                    (x, y),
                    NODE_RADIUS + 9,
                    facecolor="none",
                    edgecolor=BEST,
                    lw=6,
                    zorder=3,
                )
            )
        if node in scene.values:
            text = scene.values[node]
            ax.text(
                x,
                y + 1,
                text,
                ha="center",
                va="center",
                fontsize=22 if len(text) < 4 else 17,
                fontweight="bold",
                color=INK if white else "#ffffff",
                zorder=5,
            )
        if node in scene.cut:
            ax.plot([x - 22, x + 22], [y - 22, y + 22], color=CUT, lw=4, zorder=6)
            ax.plot([x - 22, x + 22], [y + 22, y - 22], color=CUT, lw=4, zorder=6)
        # The node's name, beside it
        name_x = x - NODE_RADIUS - 8
        ax.text(
            name_x,
            y - NODE_RADIUS + 2,
            node,
            ha="right",
            va="center",
            fontsize=19,
            fontweight="bold",
            color="#374151",
            alpha=max(fade, 0.6),
        )
        if node in LEAF_SCORES:
            ax.text(
                x,
                y + 75,
                f"({LEAF_SCORES[node]})",
                ha="center",
                va="center",
                fontsize=19,
                color="#374151",
                alpha=max(fade, 0.6),
            )

    # Legend and counter under the tree
    ax.text(
        60,
        1005,
        f"Leaves scored: {scene.leaves_scored} of 8",
        fontsize=24,
        fontweight="bold",
        color=INK,
        va="center",
    )
    view = "White's side" if scene.leaf_view == "White" else "the side to move"
    ax.text(
        480,
        1005,
        f"Numbers inside the circles are from {view}.",
        fontsize=19,
        color="#4b5563",
        va="center",
    )

    # The narration panel
    panel_left, panel_width = PANEL_LEFT, PANEL_WIDTH
    ax.add_patch(
        FancyBboxPatch(
            (panel_left, 120),
            panel_width,
            440,
            boxstyle="round,pad=0,rounding_size=18",
            facecolor=PANEL,
            edgecolor="#d1d5db",
            lw=2,
            zorder=1,
        )
    )
    size, spacing = 21, 33
    wrapped = wrap_to_width(ax, scene.text, size, panel_width - 50)
    if len(wrapped) > 12:
        size, spacing = 19, 29
        wrapped = wrap_to_width(ax, scene.text, size, panel_width - 50)
    for index, line in enumerate(wrapped):
        ax.text(
            panel_left + 26,
            158 + index * spacing,
            line,
            fontsize=size,
            color=INK,
            va="center",
        )

    # The code or rules panel
    top = 585
    ax.add_patch(
        FancyBboxPatch(
            (panel_left, top),
            panel_width,
            455,
            boxstyle="round,pad=0,rounding_size=18",
            facecolor=CODE_FILL,
            edgecolor="#d1d5db",
            lw=2,
            zorder=1,
        )
    )
    ax.text(
        panel_left + 22,
        top + 32,
        scene.panel,
        fontsize=18,
        fontweight="bold",
        color="#374151",
        va="center",
    )
    if scene.code is not None:
        for index, line in enumerate(scene.code):
            y = top + 75 + index * 31
            if index in scene.lit:
                ax.add_patch(
                    FancyBboxPatch(
                        (panel_left + 12, y - 15),
                        panel_width - 24,
                        30,
                        boxstyle="round,pad=0,rounding_size=6",
                        facecolor=CODE_LIT,
                        edgecolor="none",
                        zorder=2,
                    )
                )
            ax.text(
                panel_left + 22,
                y,
                line,
                fontsize=14,
                family="DejaVu Sans Mono",
                color=INK,
                va="center",
                zorder=3,
            )
    else:
        for index, line in enumerate(scene.rules):
            ax.text(
                panel_left + 22,
                top + 75 + index * 29,
                line,
                fontsize=17,
                color=INK,
                va="center",
            )


def render(kind: str, data) -> np.ndarray:
    """Draw one step and return it as an array of RGB pixels."""
    fig = plt.figure(figsize=(WIDTH / 100, HEIGHT / 100), dpi=100)
    fig.patch.set_facecolor(PAPER)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(HEIGHT, 0)
    ax.axis("off")
    if kind == "card":
        draw_card(ax, *data)
    else:
        draw_scene(ax, data)
    fig.canvas.draw()
    pixels = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
    plt.close(fig)
    return pixels


def hold_seconds(kind: str, data) -> float:
    """Give each step time to read: about a quarter of a second per word."""
    if kind == "card":
        words = len((data[0] + " " + " ".join(data[1])).split())
    else:
        words = len(data.text.split())
    return min(MAX_HOLD, max(MIN_HOLD, 1.5 + SECONDS_PER_WORD * words))


def add_chapters(silent: Path, chapters: list[tuple[int, str]], frames: int):
    """Copy the video into VIDEO with one chapter per pass, so a player can jump to it."""
    metadata = silent.with_suffix(".txt")
    text = ";FFMETADATA1\n"
    for index, (start, heading) in enumerate(chapters):
        end = chapters[index + 1][0] if index + 1 < len(chapters) else frames
        text += f"[CHAPTER]\nTIMEBASE=1/{FPS}\nSTART={start}\nEND={end}\n"
        text += f"title={heading}\n"
    metadata.write_text(text, encoding="utf-8")
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(silent),
            "-i",
            str(metadata),
            "-map_metadata",
            "1",
            "-map_chapters",
            "1",
            "-codec",
            "copy",
            "-movflags",
            "+faststart",
            str(VIDEO),
        ],
        check=True,
    )
    metadata.unlink()
    silent.unlink()


def main():
    save_stills = "--stills" in sys.argv
    movie = build_movie()
    OUT.mkdir(parents=True, exist_ok=True)
    stills = (
        ROOT / "tmp" / "game_tree_stills"
    )  # /tmp/ in the Remus folder is git-ignored
    if save_stills:
        stills.mkdir(parents=True, exist_ok=True)
    silent = OUT / "game_tree_search_no_chapters.mp4"
    writer = imageio_ffmpeg.write_frames(
        str(silent),
        (WIDTH, HEIGHT),
        fps=FPS,
        codec="libx264",
        pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p",
        quality=None,
        macro_block_size=8,
        output_params=[
            "-crf",
            "26",
            "-preset",
            "slow",
            "-tune",
            "animation",
            "-g",
            "900",
        ],
    )
    writer.send(None)  # Start the encoder
    previous = None
    frames = 0
    chapters = []
    for number, (kind, data) in enumerate(movie.steps, start=1):
        frame = render(kind, data)
        if save_stills:
            plt.imsave(stills / f"step_{number:03d}.png", frame)
        if previous is not None:
            for index in range(1, FADE_FRAMES + 1):
                blend = index / (FADE_FRAMES + 1)
                mixed = previous * (1 - blend) + frame * blend
                writer.send(mixed.astype(np.uint8).tobytes())
                frames += 1
        if kind == "card":
            chapters.append((frames, data[0]))
        seconds = hold_seconds(kind, data)
        hold = round(seconds * FPS)
        if number == len(movie.steps):
            hold += 2 * FPS  # Two more seconds on the last step
        for _ in range(hold):
            writer.send(frame.tobytes())
        frames += hold
        previous = frame.astype(np.float32)
    writer.close()
    add_chapters(silent, chapters, frames)
    for start, heading in chapters:
        minutes, seconds = divmod(start // FPS, 60)
        print(f"{minutes:2d}:{seconds:02d}  {heading}")
    minutes, seconds = divmod(frames // FPS, 60)
    print(f"Saved {VIDEO}  ({len(movie.steps)} steps, {minutes} min {seconds} s)")
    if save_stills:
        print(f"Saved one picture per step in {stills}")


if __name__ == "__main__":
    main()
