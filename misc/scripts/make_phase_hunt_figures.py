#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = ["matplotlib"]
# ///
"""make_phase_hunt_figures.py

Draw the pictures in the Day 10 READMEs that explain phase_hunt.py.

A course designer tool, like the other make_*.py scripts. It reads the phase library and the
benchmark from the finished Day 10 phase_hunt.py and saves PNG files in
misc/docs/images/phase_hunt/. The inline script block above names matplotlib, so
`uv run misc/scripts/make_phase_hunt_figures.py` installs it for this script alone; Remus itself
and the class laptops never need it.
"""

import math
import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Draw straight to files, with no window

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).parent.parent.parent  # The top Remus folder, above misc/scripts/
DAY10 = next(ROOT.glob("Day 10 - *")) / "period4" / "instructor"
sys.path.insert(0, str(DAY10))

import phase_hunt as hunt

OUT = ROOT / "misc" / "docs" / "images" / "phase_hunt"
MYSTERY_POWDER = 23  # A benchmark powder of table salt (halite) and silicon
LOW_ANGLE, HIGH_ANGLE = 18, 92  # The 2-theta range every pattern shows

# One bright color per phase, the same color in every picture
COLORS = {
    "silicon": "#3b82f6",
    "halite": "#06b6d4",
    "quartz": "#a855f7",
    "rutile": "#ef4444",
    "anatase": "#f97316",
    "corundum": "#db2777",
    "zincite": "#84cc16",
    "gold": "#eab308",
    "silver": "#94a3b8",
    "copper": "#b45309",
}
# Where a student meets each phase in everyday life
EVERYDAY = {
    "silicon": "computer chips",
    "halite": "table salt",
    "quartz": "sand",
    "rutile": "white paint",
    "anatase": "sunscreen",
    "corundum": "rubies and sapphires",
    "zincite": "zinc cream",
    "gold": "jewelry",
    "silver": "coins and mirrors",
    "copper": "wires and pennies",
}
GREEN, ORANGE, RED = "#16a34a", "#f59e0b", "#dc2626"
NAVY, INK, PAPER = "#0b1f33", "#1f2937", "#fffdf7"

plt.rcParams.update(
    {
        "font.size": 13,
        "font.weight": "bold",
        "axes.titlesize": 17,
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
    }
)


def pattern_curve(peaks, rng, noise=0.6):
    """Return (angles, counts): a detector trace with a bump at every peak."""
    angles = []
    counts = []
    steps = 1500
    for i in range(steps):
        angle = LOW_ANGLE + (HIGH_ANGLE - LOW_ANGLE) * i / (steps - 1)
        value = 4 + rng.uniform(0, noise)
        for peak in peaks:
            value += 100 * math.exp(-(((angle - peak) / 0.22) ** 2))
        angles.append(angle)
        counts.append(value)
    return angles, counts


def save(fig, name):
    """Save one figure into misc/docs/images/phase_hunt and report the path."""
    file_path = OUT / name
    fig.savefig(file_path, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {file_path}")


def draw_experiment():
    """The beamline: X-rays, a powder, rings on a detector, and the pattern."""
    fig, ax = plt.subplots(figsize=(13, 4.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    # The light source
    ax.add_patch(
        FancyBboxPatch((0.2, 1.6), 2.2, 1.4, boxstyle="round,pad=0.1", color=NAVY)
    )
    ax.text(1.3, 2.45, "NSLS-II", color="white", ha="center", fontsize=16)
    ax.text(1.3, 1.95, "X-ray beam", color="#fde68a", ha="center", fontsize=11)
    ax.add_patch(
        FancyArrowPatch(
            (2.5, 2.3),
            (4.6, 2.3),
            arrowstyle="-|>",
            mutation_scale=30,
            lw=6,
            color="#facc15",
        )
    )
    # The powder: many tiny crystals pointing every which way
    rng = random.Random(4)
    for _ in range(60):
        x = 5.0 + rng.uniform(-0.38, 0.38)
        y = 2.3 + rng.uniform(-0.38, 0.38)
        size = rng.uniform(0.06, 0.12)
        ax.add_patch(
            plt.Rectangle(
                (x, y),
                size,
                size,
                angle=rng.uniform(0, 90),
                color=rng.choice(["#3b82f6", "#06b6d4"]),
            )
        )
    ax.text(5.05, 1.4, "powder\n(salt + silicon)", ha="center", fontsize=11)
    # Cones of scattered X-rays and the rings they make on the detector
    for spread in (0.55, 0.95, 1.3, 1.6):
        ax.plot([5.2, 8.0], [2.3, 2.3 + spread], color="#facc15", lw=1.5, alpha=0.7)
        ax.plot([5.2, 8.0], [2.3, 2.3 - spread], color="#facc15", lw=1.5, alpha=0.7)
    ax.add_patch(
        FancyBboxPatch(
            (7.9, 0.45), 0.25, 3.7, boxstyle="round,pad=0.02", color="#334155"
        )
    )
    for spread, color in zip(
        (0.55, 0.95, 1.3, 1.6), ("#3b82f6", "#06b6d4") * 2, strict=True
    ):
        ax.add_patch(Circle((8.02, 2.3), spread, fill=False, lw=3, color=color))
    ax.text(8.05, 0.05, "detector: one ring\nfor every peak", ha="center", fontsize=11)
    ax.add_patch(
        FancyArrowPatch(
            (9.75, 2.3),
            (10.45, 2.3),
            arrowstyle="-|>",
            mutation_scale=25,
            lw=3,
            color=INK,
        )
    )
    # The pattern the rings turn into
    inset = fig.add_axes((0.80, 0.22, 0.19, 0.55))
    measured, _ = hunt.make_pattern(MYSTERY_POWDER)
    angles, counts = pattern_curve(measured, random.Random(1))
    inset.plot(angles, counts, color=NAVY, lw=1.6)
    inset.set_yticks([])
    inset.set_xlabel("angle 2θ", fontsize=11)
    inset.set_title("the pattern", fontsize=13)
    fig.suptitle(
        "The experiment: shine X-rays through a powder and catch the rings",
        fontsize=18,
        color=NAVY,
    )
    save(fig, "experiment.png")


def draw_fingerprints():
    """The library: every phase as a barcode of four peaks."""
    fig, ax = plt.subplots(figsize=(13, 7.5))
    names = list(hunt.LIBRARY)
    for row, name in enumerate(names):
        y = len(names) - row
        ax.axhspan(y - 0.42, y + 0.42, color=COLORS[name], alpha=0.10)
        for peak in hunt.LIBRARY[name]:
            ax.plot(
                [peak, peak],
                [y - 0.38, y + 0.38],
                color=COLORS[name],
                lw=6,
                solid_capstyle="butt",
            )
        ax.text(
            LOW_ANGLE - 1,
            y,
            f"{name}  ",
            ha="right",
            va="center",
            color=COLORS[name],
            fontsize=15,
        )
        ax.text(
            HIGH_ANGLE + 1,
            y,
            EVERYDAY[name],
            ha="left",
            va="center",
            fontsize=12,
            color=INK,
            style="italic",
        )
    ax.set_xlim(LOW_ANGLE, HIGH_ANGLE)
    ax.set_ylim(0.4, len(names) + 0.6)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("angle 2θ (degrees)")
    ax.set_title(
        "Every crystal has its own fingerprint: four peaks at its own angles",
        color=NAVY,
        pad=14,
    )
    save(fig, "fingerprints.png")


def draw_mystery():
    """The mystery powder: the pattern the class has to explain."""
    measured, _ = hunt.make_pattern(MYSTERY_POWDER)
    angles, counts = pattern_curve(measured, random.Random(1))
    fig, ax = plt.subplots(figsize=(13, 4.3))
    ax.fill_between(angles, counts, color="#cbd5e1", alpha=0.6)
    ax.plot(angles, counts, color=NAVY, lw=2)
    for peak in measured:
        ax.annotate(f"{peak:.1f}", (peak, 108), ha="center", fontsize=11, color=NAVY)
    ax.set_xlim(LOW_ANGLE, HIGH_ANGLE)
    ax.set_ylim(0, 125)
    ax.set_yticks([])
    ax.set_xlabel("angle 2θ (degrees)")
    ax.set_ylabel("brightness")
    ax.set_title(
        f"Mystery powder {MYSTERY_POWDER}: eight peaks. Which crystals made them?",
        color=NAVY,
    )
    save(fig, "mystery_powder.png")


def draw_scoring():
    """Score three guesses about the mystery powder, peak by peak."""
    measured, _ = hunt.make_pattern(MYSTERY_POWDER)
    guesses = [["silicon"], ["silicon", "halite"], ["silicon", "halite", "zincite"]]
    fig, axes = plt.subplots(len(guesses), 1, figsize=(13, 9.5), sharex=True)
    for ax, guess in zip(axes, guesses, strict=True):
        predicted = hunt.predicted_peaks(guess)
        explained = left_over = missing = 0
        height = 1.0
        previous = -100.0
        for peak in measured:
            # Lift a dot that would sit on top of its neighbor
            height = 1.45 if peak - previous < 1.5 and height == 1.0 else 1.0
            previous = peak
            if hunt.matches(peak, predicted):
                explained += 1
                color, mark = GREEN, "✓"
            else:
                left_over += 1
                color, mark = ORANGE, "?"
            ax.plot([peak, peak], [0.6, height], color=color, lw=1.5)
            ax.plot(peak, height, "o", ms=22, color=color)
            ax.text(
                peak, height, mark, ha="center", va="center", color="white", fontsize=15
            )
        for name in guess:
            for peak in hunt.LIBRARY[name]:
                ax.plot([peak, peak], [-0.1, 0.55], color=COLORS[name], lw=5)
                if not hunt.matches(peak, measured):
                    missing += 1
                    ax.text(
                        peak,
                        -0.45,
                        "✗",
                        ha="center",
                        va="center",
                        color=RED,
                        fontsize=24,
                    )
        total = hunt.score(guess, measured)
        label = " + ".join(guess) if guess else "nothing"
        ax.set_title(f"Guess: {label}", loc="left", color=NAVY)
        ax.text(
            HIGH_ANGLE + 1,
            0.4,
            f"+{explained} explained\n-{left_over} left over\n-{missing} missing\n"
            f"-{len(guess)} phases used\n= {total} points",
            va="center",
            fontsize=13,
            color=GREEN if total == max(6, total) else INK,
        )
        ax.set_ylim(-0.8, 1.8)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    axes[-1].set_xlim(LOW_ANGLE, HIGH_ANGLE)
    axes[-1].set_xlabel("angle 2θ (degrees)")
    fig.suptitle(
        "score(): dots are measured peaks, sticks are the guess's peaks\n"
        "green ✓ explained, orange ? left over, red ✗ missing",
        fontsize=16,
        color=NAVY,
    )
    fig.tight_layout()
    save(fig, "scoring.png")


def draw_greedy():
    """Greedy, step by step: try every phase, keep the one that scores best."""
    measured, _ = hunt.make_pattern(MYSTERY_POWDER)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), sharey=True)
    chosen = []
    for step, ax in enumerate(axes, start=1):
        now = hunt.score(chosen, measured)
        names = []
        scores = []
        for name in hunt.PHASE_NAMES:
            if name not in chosen:
                names.append(name)
                scores.append(hunt.score(chosen + [name], measured))
        best = max(scores)
        bars = ax.bar(
            range(len(names)),
            [s + 15 for s in scores],
            bottom=-15,
            color=[COLORS[n] for n in names],
            edgecolor=INK,
        )
        ax.axhline(now, color=INK, ls="--", lw=2)
        ax.text(
            len(names) - 0.5, now + 0.6, f"score now: {now}", ha="right", fontsize=11
        )
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=60, ha="right", fontsize=11)
        ax.set_ylim(-15, 9)
        if best > now:
            winner = names[scores.index(best)]
            bars[scores.index(best)].set_linewidth(4)
            ax.set_title(f"Step {step}: add {winner}", color=GREEN)
            chosen.append(winner)
        else:
            ax.set_title(f"Step {step}: nothing helps, stop", color=RED)
    axes[0].set_ylabel("score after adding the phase")
    fig.suptitle(
        "greedy_phases(): try each phase, take the best, repeat",
        fontsize=18,
        color=NAVY,
    )
    fig.tight_layout()
    save(fig, "greedy_steps.png")


def draw_tree():
    """The tree of phase sets that search() walks, with scores at each node."""
    measured, _ = hunt.make_pattern(MYSTERY_POWDER)
    names = ["silicon", "halite", "quartz", "zincite"]  # A small part of the library
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.axis("off")
    root = (0.5, 0.92)
    level1 = []
    for i, name in enumerate(names):
        level1.append(((i + 0.5) / len(names), 0.62, [name], i))
    level2 = []
    for x, _, phases, start in level1:
        for j in range(start + 1, len(names)):
            level2.append((phases + [names[j]], x))
    best_score = hunt.score(["silicon", "halite"], measured)

    def node(xy, phases):
        total = hunt.score(phases, measured)
        is_best = total == best_score
        label = "empty set" if not phases else "\n".join(phases)
        ax.text(
            xy[0],
            xy[1],
            f"{label}\n{total} pts",
            ha="center",
            va="center",
            zorder=3,
            fontsize=11 if len(phases) < 2 else 10,
            bbox={
                "boxstyle": "round,pad=0.4",
                "fc": "#bbf7d0" if is_best else "white",
                "ec": GREEN if is_best else INK,
                "lw": 3 if is_best else 1.2,
            },
        )

    for x, y, phases, _ in level1:
        ax.plot([root[0], x], [root[1], y], color="#64748b", lw=2, zorder=1)
        ax.text(
            (2 * x + root[0]) / 3,
            (2 * y + root[1]) / 3 + 0.02,
            f"+{phases[0]}",
            ha="center",
            fontsize=12,
            color=COLORS[phases[0]],
            zorder=4,
            bbox={"fc": PAPER, "ec": "none", "pad": 1},
        )
    count = len(level2)
    for k, (phases, parent_x) in enumerate(level2):
        x = (k + 0.5) / count
        ax.plot([parent_x, x], [0.62, 0.22], color="#94a3b8", lw=2, zorder=1)
        ax.text(
            (x + parent_x) / 2,
            0.42,
            f"+{phases[-1]}",
            ha="center",
            fontsize=10,
            color=COLORS[phases[-1]],
            zorder=4,
            bbox={"fc": PAPER, "ec": "none", "pad": 1},
        )
        node((x, 0.22), phases)
    for x, y, phases, _ in level1:
        node((x, y), phases)
    node(root, [])
    ax.text(
        0.5,
        0.0,
        "Each box is one set of phases, like one position in chess. Going down "
        "adds a phase (make); going back up takes it out (undo).\n"
        "Phases are added in library order, so silicon + halite is scored once, "
        "never again as halite + silicon.",
        ha="center",
        fontsize=12,
        color=INK,
    )
    ax.set_title(
        "search(): the tree of phase sets (4 of the 10 phases, 2 deep)", color=NAVY
    )
    save(fig, "search_tree.png")


def draw_lookalikes():
    """Gold and silver: two fingerprints closer together than the tolerance."""
    fig, axes = plt.subplots(1, 4, figsize=(14, 4.2), sharey=True)
    for ax, gold, silver in zip(
        axes, hunt.LIBRARY["gold"], hunt.LIBRARY["silver"], strict=True
    ):
        middle = (gold + silver) / 2
        ax.axvspan(middle - hunt.TOLERANCE, middle + hunt.TOLERANCE, color="#e2e8f0")
        ax.plot([gold, gold], [0, 1], color=COLORS["gold"], lw=8, label="gold")
        ax.plot(
            [silver, silver], [0, 0.85], color=COLORS["silver"], lw=8, label="silver"
        )
        ax.set_xlim(middle - 0.8, middle + 0.8)
        ax.set_title(f"near {middle:.1f}°", fontsize=14)
        ax.set_yticks([])
    axes[0].legend(loc="upper left", fontsize=11)
    fig.supxlabel(
        "angle 2θ (degrees); the gray band is the 0.3° tolerance", fontsize=13
    )
    fig.suptitle(
        "Gold and silver look almost the same to X-rays", fontsize=18, color=NAVY
    )
    fig.tight_layout()
    save(fig, "gold_and_silver.png")


def draw_verdicts():
    """The benchmark: right, can't tell, and wrong for greedy and for search."""
    greedy = hunt.benchmark(hunt.greedy_answer)
    search = hunt.benchmark(hunt.search_answer)
    fig, ax = plt.subplots(figsize=(13, 3.8))
    for row, (name, counts) in enumerate((("search", search), ("greedy", greedy))):
        left = 0
        for verdict, color in (
            ("right", GREEN),
            ("can't tell", ORANGE),
            ("wrong", RED),
        ):
            width = counts[verdict]
            ax.barh(row, width, left=left, color=color, edgecolor="white", lw=2)
            label = f"{width}\n{verdict}" if width >= 25 else f"{width}"
            if width > 0:
                ax.text(
                    left + width / 2,
                    row,
                    label,
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=12,
                )
            left += width
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["search()", "greedy"], fontsize=15)
    ax.set_xlim(0, hunt.TRIALS)
    ax.set_xlabel(f"{hunt.TRIALS} powders whose crystals are known")
    ax.set_title(
        "Greedy is wrong 34 times. The search is wrong 9 times and says "
        '"can\'t tell" instead of guessing.',
        color=NAVY,
    )
    save(fig, "verdicts.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    draw_experiment()
    draw_fingerprints()
    draw_mystery()
    draw_scoring()
    draw_greedy()
    draw_tree()
    draw_lookalikes()
    draw_verdicts()
    print("  (expected: 8 pictures)")


if __name__ == "__main__":
    main()
