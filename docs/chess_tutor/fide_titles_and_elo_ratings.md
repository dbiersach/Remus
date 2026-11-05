# FIDE titles and typical Elo ratings

The Elo rating carries the name of Arpad Elo (1903 to 1992), a Hungarian-American
physics professor and chess master who designed it. Elo is his surname, not an
acronym, so it is written "Elo", not "ELO". US Chess adopted his system in 1960 and
FIDE in 1970. An Elo rating predicts results: two players with the same rating each
expect to score half the points between them, a player 200 points higher expects to
score about 76%, and a player 400 points higher about 91%. After each game, a rating
rises when the player scores more than that prediction and falls when the player
scores less, so beating a stronger opponent gains more points than beating a weaker
one. The scale has no maximum. The highest rating any person has held is 2882, set by
Magnus Carlsen in 2014, and the strongest chess engines rate above 3500 on engine
rating lists.

FIDE, the international chess federation, awards titles to players who reach a
minimum Elo rating. The class names below
the titles (Expert and Class A to Class D) come from national federations such as
US Chess, not from FIDE.

| Title | Minimum rating requirement | Typical rating range |
| --- | ---: | ---: |
| **Super Grandmaster** (unofficial) | 2700+ | 2700 to 2850 |
| **Grandmaster (GM)** | 2500 | 2500 to 2650 |
| **International Master (IM)** | 2400 | 2400 to 2500 |
| **FIDE Master (FM)** | 2300 | 2300 to 2400 |
| **Candidate Master (CM)** | 2200 | 2200 to 2300 |
| Expert (not a FIDE title) | None | 2000 to 2199 |
| Class A player | None | 1800 to 1999 |
| Class B player | None | 1600 to 1799 |
| Class C player | None | 1400 to 1599 |
| Class D player | None | 1200 to 1399 |

## Ratings of everyday players

Most chess players never earn a title. The table below places everyday players on the
same Elo scale, from someone who has just learned the moves to a FIDE Master. The
ranges are estimates: club ratings differ from one federation to another, and many
casual players have no rating at all.

| Player category | Typical Elo range | Representative rating |
| --- | ---: | ---: |
| Casual player who knows the rules | 400 to 900 | 650 |
| Beginning chess club member | 600 to 1200 | 900 |
| Strong chess club player | 1200 to 1700 | 1450 |
| First-board player on a club team | 1500 to 2000 | 1750 |
| Average city chess club member | 1200 to 1600 | 1400 |
| Strong city chess club competitor | 1600 to 2000 | 1800 |
| City club champion | 1800 to 2200+ | 2000 |
| FIDE Candidate Master | 2200+ | 2250 |
| FIDE Master | 2300+ | 2350 |

## Where the Remus engines would land

FIDE gives titles only to people, so no engine can earn one. The table below shows
the title or class a player with each engine's rating would hold. No rated games
have measured the Remus engines, so every number is an estimate: the Remus2 figure
comes from engines of the same design, and the later rows add the gains that
[`remus_versions.md`](../engines/remus_versions.md) expects for each version (about
+350 Elo for Remus3 and +195 for Remus4, less once the gains overlap). Expect each
estimate to be off by 150 Elo or more, and to change with the clock and the
computer.

| Engine | Estimated Elo | Likely title or class |
| --- | ---: | --- |
| Remus1 | 300 | None: a random mover sits far below Class D |
| Remus2 | 1300 | Class D player |
| Remus3 | 1600 | Class B player |
| Remus4 | 1750 | Class B player |
| Remus4-Rust | 2250 | Candidate Master (CM) |

Remus4-Rust plays the same moves as Remus4 but searches more than 100 times as many
positions per second, so it looks several moves deeper in the same time. That extra
depth alone lifts it about 500 Elo, from Class B to the edge of Candidate Master.
