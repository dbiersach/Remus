# Real Science That Searches Like a Chess Engine

A survey of published science problems that use the same ideas as Remus (generate
moves, make and undo, evaluate, search a tree, prune), written to choose a real
problem for the Day 10 Science AI capstone.

## The short answer

No published BNL or NSLS-II paper found in this survey runs minimax, alpha-beta, or
Monte Carlo tree search on a beamline. Brookhaven's autonomous experiments use two
other tools: a Gaussian process that picks the next measurement (gpCAM, at the CMS
and SMI beamlines) and reinforcement learning that treats a beamline as a video game
(BadSeed, at the PDF beamline). Both are real and both appear below.

The closest match to a chess engine at a DOE light source is **X-ray phase
identification by tree search**. A powder diffraction pattern is a list of peaks.
The question is which crystal phases, mixed together, made those peaks. Two recent
papers solve it by searching a tree of phase combinations, and one of them ran on
real synchrotron data from SSRL (a DOE light source at SLAC) and CHESS (Cornell).
The same question is answered live at NSLS-II's PDF beamline by Brookhaven's
Crystallography Companion Agent, so the story leads back to Brookhaven.

**Recommendation 1:** replace `beam_time.py` (Day 10, periods 2 and 3) with a phase
identification search, `phase_hunt.py`. It is the most chess-like real problem found,
and the built lab fits the 40-line cap.

**Recommendation 2:** keep `hidden_peak.py` (Day 10, period 1), and anchor it in the
real gpCAM papers from the CMS beamline. If David prefers to keep `beam_time.py`
too, re-anchor it on the published NSLS-II BadSeed problem (stay on a sample or move
on), which it already resembles.

**Decision (David):** build `phase_hunt.py` and retire `beam_time.py`.
The built lab and its benchmark are described under Recommendation 1.

## How the candidates were judged

Each candidate is scored on four questions:

1. **Real:** is it a published, citable result on real data?
2. **Close to home:** BNL or NSLS-II first, other DOE light sources next, wider
   science last.
3. **Chess-like:** does it use the parts of Remus the students built (move
   generation, make and undo, evaluation, depth-limited search, pruning)?
4. **Teachable:** can a pair of 13-year-olds write the core in 20 to 40 minutes and
   at most about 40 typed lines per period, with the teacher writing the plumbing?

## The candidates

| # | Problem | Where | Search idea | Real data | Chess fit | Fits the cap |
| --- | --- | --- | --- | --- | --- | --- |
| A | Phase identification: CrystalShift | Cornell; data from CHESS ID3B and SSRL 1-5 | Best-first tree search, keep the best k nodes per level, depth limit from Gibbs' phase rule | Yes, synchrotron | Very close | Yes (prototype: about 30 lines) |
| B | Phase identification: Dara | UC Berkeley and LBNL (A-Lab) | Tree search over phase sets, fixed add order to skip repeats, threshold pruning, depth 5 | Yes, lab diffractometer | Very close | Yes (same lab as A) |
| C | Phase identification live at NSLS-II: XCA | NSLS-II PDF beamline | Neural network ensemble, no tree | Yes, NSLS-II | Story only | Not as code |
| D | BadSeed: stay or move on | NSLS-II PDF beamline | Reinforcement learning on a beamline "game" | Simulated, from PDF data | Close (a one-player game) | Yes, as an expectimax look-ahead |
| E | gpCAM autonomous X-ray scattering | NSLS-II CMS and SMI; CFN | Gaussian process, choose the most informative point | Yes, NSLS-II | Evaluation only, no tree | Already used by `hidden_peak.py` |
| F | Beamline alignment by Bayesian optimization | NSLS-II TES and ISS; ALS 5.3.1 | Gaussian process plus a route solver for motor travel | Yes | Weak | No |
| G | CASTING: materials design by Monte Carlo tree search | Argonne CNM, with ALS | MCTS with UCB selection, moves add or nudge atoms | Simulated materials | Close (MCTS) | Too heavy (needs a physics energy model) |
| H | Retrosynthesis planning (Segler, Preuss, Waller) | Univ. of Muenster | MCTS over chemical reactions | Yes, reaction database | Close (MCTS, the AlphaGo recipe) | Too heavy (chemistry) |
| I | HP protein folding on a grid | Wider science (Dill's HP model) | Depth-first tree search, nested Monte Carlo search | Benchmark sequences | Very close | Yes, but no beamline link |

### A. CrystalShift: phase labeling by best-first tree search

Chang, Ament, Amsler, Sutherland, Zhou, Gregoire, Gomes, van Dover, and Thompson,
"Probabilistic phase labeling and lattice refinement for autonomous materials
research," *npj Computational Materials* 11, 148 (2025).
[doi:10.1038/s41524-025-01627-0](https://doi.org/10.1038/s41524-025-01627-0),
preprint [arXiv:2308.07897](https://arxiv.org/abs/2308.07897).

Each node of the tree is a set of candidate phases. Expanding a node adds one more
phase. The program fits each node to the measured pattern and keeps only the k nodes
with the smallest leftover error at each level, so the tree stays small. The depth
limit, the largest number of phases that can coexist, comes from Gibbs' phase rule.
The Ta-Sn-O data came from the CHESS ID3B beamline and the Cr-Fe-V-O data from SSRL
beamline 1-5, a DOE light source.

Chess map: node = position, add a phase = make a move, remove it = undo, leftover
error = evaluation, keep the best k = pruning by move ordering, phase rule = depth
limit.

### B. Dara: multiple-hypothesis phase identification

Fei, McDermott, Rom, Wang, and Ceder, "Dara: Automated multiple-hypothesis phase
identification and refinement from powder X-ray diffraction" (2025),
[arXiv:2510.19667](https://arxiv.org/abs/2510.19667).

Dara searches the same kind of tree. A node is a set of phases and an edge adds one
phase. To avoid visiting the same set twice in a different order, each new phase
must have weaker peaks than every phase already in the node. That rule is the
chess idea of a transposition (two move orders, one position) handled by fixed move
ordering. A new phase stays only if it improves the fit by at least 2 percent, which
plays the role of a cutoff. The data came from lab diffractometers and the A-Lab
self-driving lab at Berkeley Lab, not a synchrotron.

### C. XCA: phase identification live at NSLS-II

Maffettone, Banko, Lysogorskiy, Olds, Ludwig, Cooper, and others,
"Crystallography companion agent for high-throughput materials discovery," *Nature
Computational Science* (2021), [arXiv:2008.00283](https://arxiv.org/abs/2008.00283);
Brookhaven story: [AI Agent Helps Identify Material Properties
Faster](https://www.bnl.gov/newsroom/news.php?a=218824).

Brookhaven's agent answers the same question as A and B while the data streams in
at the NSLS-II PDF beamline, but it uses an ensemble of neural networks instead of a
tree. It gives the capstone its Brookhaven connection: "the PDF beamline asks this
question every day; here is one published way to answer it by searching."

### D. BadSeed: a beamline turned into a game

Maffettone, Lynch, Caswell, Cook, Campbell, and Olds, "Gaming the beamlines:
employing reinforcement learning to maximize scientific outcomes at large-scale user
facilities," *Machine Learning: Science and Technology* 2, 025025 (2021).
[doi:10.1088/2632-2153/abc9fc](https://doi.org/10.1088/2632-2153/abc9fc); Brookhaven
story: [Game on: Science Edition](https://www.bnl.gov/newsroom/news.php?a=218774).

Ten samples sit on a holder. Some scatter strongly and some weakly, and a weak sample
needs about ten times more scans to give useful data. At each step the agent makes
one of two moves: stay on this sample or move to the next one. Each useful scan
earns a point, and the beam time runs out. The paper trains a reinforcement learning
agent, which beat a simple one-after-another sweep by up to a factor of two when
time was short. Daniel Olds: "for an AI agent to run our beamline, we needed to turn
our beamline into a video game."

The paper uses no tree search, but the problem is a one-player game with chance
(whether the next scan is useful), so a short expectimax look-ahead solves it the
way Remus solves a position. The current `beam_time.py` already asks a close
cousin of this question (which sample gets the next shot), so re-anchoring it on
BadSeed costs little.

### E. gpCAM: choosing the next measurement at CMS

Noack, Yager, Fukuto, and others, "A Kriging-based approach to
autonomous experimentation with applications to X-ray scattering," *Scientific
Reports* 9 (2019), [PMC6694190](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6694190/);
and "Advances in Kriging-based autonomous X-ray scattering experiments,"
*Scientific Reports* 10 (2020),
[PMC6987221](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6987221/). Brookhaven
story: [Automatically Steering Experiments Toward Scientific
Discovery](https://www.bnl.gov/newsroom/news.php?a=218852).

gpCAM picks the next spot on a sample where a measurement teaches the most, first at
the NSLS-II CMS beamline, then at SMI, the ALS, and the ILL. This is the real
problem behind `hidden_peak.py`. It has an evaluation (predicted value plus
uncertainty) but no tree.

### F. Beamline alignment by Bayesian optimization

Morris and 12 coauthors, "A general Bayesian algorithm for the autonomous alignment
of beamlines," *Journal of Synchrotron Radiation* (2024),
[gy5067](https://journals.iucr.org/s/issues/2024/06/00/gy5067/gy5067.pdf).

The agent aligns mirrors at the NSLS-II TES and ISS beamlines and ALS 5.3.1. It
chooses a batch of motor settings and then routes the motors between them to save
travel time. The paper names "making the agent take into account the traveling cost"
as future work: a look-ahead problem nobody has published yet, but too abstract for
this audience.

### G. CASTING: Monte Carlo tree search for new materials

Banik, Loeffler, Manna, Chan, Srinivasan, Darancet, Hexemer, Sankaranarayanan, and
others, "A continuous action space tree search for inverse design (CASTING)
framework for materials discovery," *npj Computational Materials* 9, 177 (2023),
[doi:10.1038/s41524-023-01128-y](https://doi.org/10.1038/s41524-023-01128-y).

Argonne's Center for Nanoscale Materials grows a Monte Carlo search tree whose moves
add, remove, or nudge atoms, and scores each structure by its energy. It found the
lowest-energy gold clusters of 13, 20, and 40 atoms and the polymorphs of carbon.
It is the clearest "AlphaGo for materials" example at a DOE lab, but the evaluation
needs a physics simulator (LAMMPS or VASP), which a 40-line lab cannot hold. Good
for the closing talk.

### H. Retrosynthesis by Monte Carlo tree search

Segler, Preuss, and Waller, "Planning chemical syntheses with deep neural networks
and symbolic AI," *Nature* 555, 604 to 610 (2018),
[doi:10.1038/nature25978](https://doi.org/10.1038/nature25978).

The program plans how to make a drug molecule by searching backward through
reactions, with the AlphaGo recipe of a neural network plus Monte Carlo tree search.
Famous and chess-like, but the chemistry is out of reach for 13-year-olds. Good for
the closing talk.

### I. HP protein folding on a grid

Roucairol and Cazenave, "Solving the HP model with Nested Monte Carlo Search"
(2023), [arXiv:2301.09533](https://arxiv.org/abs/2301.09533); an older exhaustive tree
search: "Fast tree search for enumeration of a lattice model of protein folding,"
[arXiv:cond-mat/0107554](https://arxiv.org/abs/cond-mat/0107554).

A protein is a string of H (water-fearing) and P (water-loving) beads, placed one at
a time on a square grid. The moves are up, down, left, right; the score counts H
beads that touch. This is the most chess-like problem of all and very teachable, but
it has no beamline story beyond "NSLS-II measures real protein shapes at its AMX and
FMX crystallography beamlines." It is a strong backup if phase identification feels
too far from the students' world.

### Searched and set aside

- **ALS 5.3.1 Osprey agent** (*Journal of Synchrotron Radiation*, 2026,
  [soo5005](https://journals.iucr.org/s/issues/2026/05/00/soo5005/index.html)): a
  language-model agent that plans beamline workflows; no tree search.
- **NSLS-II orbit feedback by reinforcement learning** (Dong, Tian, and Sun,
  [arXiv:2601.03486](https://arxiv.org/abs/2601.03486)): accelerator control, no
  search tree.
- **CAMEO** (Kusne and others, *Nature Communications* 2020, SSRL): autonomous
  phase mapping with Bayesian active learning; the same family as gpCAM, no tree.
- **Argonne AutoPhaseNN** (Yao and others, *npj Computational Materials* 2022, APS):
  a neural network for coherent diffraction imaging; no tree.

## Recommendation 1: `phase_hunt.py`, a phase identification search

### The problem, as the students meet it

A scientist at the NSLS-II PDF beamline shines X-rays through a powder made in a new
experiment. The detector records a pattern of peaks, each at an angle. Every crystal
phase (silicon, quartz, rutile, and so on) has its own fingerprint of peak angles. The
powder may hold one, two, or three phases. Which ones? Remus answers the question
the way it picks a move: try adding a phase, score how well the set explains the
peaks, look a few phases deeper, take the phase back, and keep the best set.

### The chess map for the board

| Chess engine | Phase hunt |
| --- | --- |
| Position | The set of phases chosen so far |
| Legal moves | Library phases not yet in the set |
| `make_move` and `undo_move` | `phases.append(name)` and `phases.pop()` |
| Evaluation | Peaks explained, minus unexplained peaks, minus predicted peaks that are missing |
| Depth limit | At most three phases (Gibbs' phase rule sets the real limit) |
| Transpositions | Quartz then rutile is the same set as rutile then quartz |
| Move ordering prunes repeats | Add phases only in library order (Dara's rule) |
| `greedy_move()` vs alpha-beta | Add the single best phase each time vs search three deep |
| Perft against python-chess | Known mixtures: does the search name the true phases? |

### What the benchmark shows

David chose Recommendation 1, and `phase_hunt.py` replaces
`beam_time.py` in Day 10, periods 2 and 3. The library holds ten real phases, each
with its four strongest peaks, computed with Bragg's law from published lattice sizes
for copper X-rays (1.5406 angstrom). Two of them, gold and silver, have lattice
sizes 0.2 percent apart, so their peaks land less than 0.3 degrees apart and no
peak list can tell them apart. Each benchmark powder mixes one to three phases; each
peak shows up 85 times in 100 and lands up to 0.15 degrees from its true angle.

The first throwaway prototype seemed to show look-ahead beating greedy (152 against
167 of 200 right). A closer check found that the gap came from ties: when two sets
scored the same, the search returned whichever it met first, and that set was
sometimes the true one. With ties counted as ties, a full search and greedy agree on
almost every powder of a clean library, because a phase that explains peaks of two
real phases at once almost never happens with four peaks per phase.

What the search does give, and greedy cannot, is every answer that ties for the best
score. That is the main point of Dara ("multiple-hypothesis") and CrystalShift (a
probability for each phase combination): a scientist needs to know when the pattern
alone cannot decide. The built lab therefore scores each answer with three verdicts:

| Agent (200 known powders) | Right | Can't tell | Wrong |
| --- | --- | --- | --- |
| Greedy: add the best phase, again and again | 166 | 0 | 34 |
| Search: every set of up to three phases, every tie kept | 139 | 52 | 9 |

Greedy names gold for every gold or silver powder, so it is right when the powder
holds gold and wrong when it holds silver, and it never knows which. The search is
wrong on 9 powders, almost all with missing peaks, and says "can't tell" on 52, most
of them gold or silver: the cue for a second measurement, such as X-ray
fluorescence, which tells the two metals apart at once. Adding phases in library
order scores 176 sets per powder instead of 821, the same lesson as move ordering.
Each phase also costs one point, so a simpler explanation wins a tie, the role that
Dara's "keep a phase only if it improves the fit by 2 percent" rule plays.

### Who writes what

- **Given code:** the phase library, `matches()`, `predicted_peaks()`,
  `make_pattern(seed)`, the `Hunt` record, `judge()`, and the benchmark.
- **Student pairs write, period 2 (28 lines):** `score(phases, measured)`, the evaluation
  (11 lines), and `greedy_phases(measured)`, the greedy agent with append and pop
  as make and undo (17 lines).
- **Student pairs write, period 3 (13 lines):** `search(phases, measured, depth, start,
  hunt)`, the recursive search that keeps every tied set. Then the class runs the
  benchmark and changes `PHASE_COST` and `MISSING` to watch the verdicts move.

### Still open

- Ask the NSLS-II PDF or XPD beamline staff for one real measured pattern of a
  two-phase powder, to use as the final test. The management brief now asks for it.

## Recommendation 2: keep `hidden_peak.py`, anchored on gpCAM

`hidden_peak.py` already teaches choosing the next measurement by exploit plus
explore, which is what gpCAM does at the CMS beamline. It needs no code change, only
the citations in section E on the teacher's closing slide, so students see that the
toy grid stands for a published Brookhaven method.

## Sources

- [Chang et al. 2025, CrystalShift, npj Comput. Mater. 11, 148](https://doi.org/10.1038/s41524-025-01627-0)
- [Fei et al. 2025, Dara, arXiv:2510.19667](https://arxiv.org/abs/2510.19667)
- [Maffettone et al. 2021, Crystallography companion agent, arXiv:2008.00283](https://arxiv.org/abs/2008.00283)
- [BNL: AI Agent Helps Identify Material Properties Faster](https://www.bnl.gov/newsroom/news.php?a=218824)
- [Maffettone et al. 2021, Gaming the beamlines, Mach. Learn.: Sci. Technol. 2, 025025](https://doi.org/10.1088/2632-2153/abc9fc)
- [BNL: Game on: Science Edition](https://www.bnl.gov/newsroom/news.php?a=218774)
- [Noack et al. 2019, Sci. Rep. 9](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6694190/)
- [Noack et al. 2020, Sci. Rep. 10](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6987221/)
- [BNL: Automatically Steering Experiments Toward Scientific Discovery](https://www.bnl.gov/newsroom/news.php?a=218852)
- [Morris et al. 2024, J. Synchrotron Rad.](https://journals.iucr.org/s/issues/2024/06/00/gy5067/gy5067.pdf)
- [Banik et al. 2023, CASTING, npj Comput. Mater. 9, 177](https://doi.org/10.1038/s41524-023-01128-y)
- [Segler, Preuss, and Waller 2018, Nature 555, 604](https://doi.org/10.1038/nature25978)
- [Roucairol and Cazenave 2023, HP model, arXiv:2301.09533](https://arxiv.org/abs/2301.09533)
- [Fast tree search for a lattice protein model, arXiv:cond-mat/0107554](https://arxiv.org/abs/cond-mat/0107554)
- [ALS 5.3.1 Osprey agent, J. Synchrotron Rad. 2026](https://journals.iucr.org/s/issues/2026/05/00/soo5005/index.html)
- [Dong, Tian, and Sun, NSLS-II orbit feedback, arXiv:2601.03486](https://arxiv.org/abs/2601.03486)
