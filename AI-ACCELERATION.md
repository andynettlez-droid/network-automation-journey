# AI-ACCELERATION.md

The meta-portfolio piece. One running record of how AI was used across the whole climb — and, more importantly, the track record of catching what it got wrong. This file is the proof of the exact skill the roadmap argues is durable: not "AI knows it so I don't have to," but "I know it well enough to wield AI safely and fast."

## Where AI compressed time

_(rough before/after estimates per task)_

| Date | Task | Without AI (est.) | With AI (actual) | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## The verification track record (the important part)

_(running list of things the AI got wrong that I caught — the single most hireable evidence in this repo)_

| Date | What the AI produced | What was wrong | How I caught it (ground truth) |
| --- | --- | --- | --- |
| 2026-06-23 | SETUP.md said to deploy the validation lab from the repo path on `/mnt/c` | drvfs can't set Linux file perms → SR Linux config commit failed (`config.tmp … Operation not permitted`); nodes ran but config didn't commit | Re-deployed from `~/netlab/phase0` (Linux-native fs) — commit succeeded cleanly, both nodes `running`. Established the source-on-Windows / labs-on-Linux rule (now in CONVENTIONS.md + SETUP.md). |

## Concepts AI explained faster than traditional resources

-

## Honest take — what AI could and couldn't do for the learning

-
