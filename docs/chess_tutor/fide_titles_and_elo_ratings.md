# FIDE titles and typical Elo ratings

FIDE, the international chess federation, awards titles to players who reach a
minimum Elo rating. An Elo rating is a number that rises when a player beats
stronger opponents and falls after losses to weaker ones. The class names below
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
