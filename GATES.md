# Decision gates — scan-to-CAD (drafted 2026-09-02)

Purpose: kill wasted effort early; make failure cheap and informative.
Checked against partial results — the scorer writes after every part.
Standing rule: no new experiment starts before the previous gate is
evaluated and its verdict written here.

## GATE 0a — synthetic harness (first; zero cost; target ~1–2 weeks)
- Build a **virtual scanner** over online CAD (ABC dataset, GrabCAD /
  manufacturer STEP files): multi-view raycast depth rendering from
  realistic poses → distance-dependent depth noise → self-occlusion
  holes + dropped steep/shiny faces → per-view SE(3) registration
  jitter → TSDF/Poisson fusion (this is what rounds sharp edges) →
  outlier speckle. NOT vertex-jitter Gaussian — structured corruption
  only, applied as a pipeline of layers each of which can be toggled.
- Freeze SYNTH-GAUNTLET-20 (20 held-out CAD models run through the
  frozen simulator; same dev/holdout rules as the real gauntlet).
- COMPLETE when the scorer runs end-to-end and v0 is scored on
  SYNTH-GAUNTLET-20 — regardless of score.
- Standing rule: **a synthetic score is an upper bound, never a thesis
  claim.** Ground truth here includes full reference CAD, so intent
  recovery is checkable exactly.

## GATE 0b — real-scan harness (the actual exam; parallel track)
- 20 real parts scanned + caliper ground truth per DATA_PLAN.md
  (friend's scanner session is the only blocking dependency; tiers 1–3
  are an AliExpress order).
- First use of real scans: **calibrate the virtual scanner** — scan a
  few tier-1 parts with known STEP, fit the simulator's noise
  parameters to the measured residual distribution. This converts the
  Gate 0a simulator from guessed to calibrated, and quantifies the
  sim-to-real gap (itself a publishable number).
- COMPLETE when v0 is scored on the real GAUNTLET-20 — regardless of
  score. The synthetic-vs-real score drop is a first-class finding: if
  v0 drops sharply, the noise model is wrong or the thesis is harder
  than it looks — either way, that is the information Gate 1 needs.
- KILL condition (the only one): real scan data cannot be acquired at
  all. Synthetic-only results never advance past Gate 0a.

## GATE 1 — signal (after v0 + intent solver complete to spec)
Scored on the REAL gauntlet (Gate 0b). Synthetic scores inform
iteration but never adjudicate this gate.
- ≥ 8/20 → CONTINUE. Unlock: show the tool to external users; begin v1
  only for failure classes v0 provably cannot fix.
- 4–7/20 → ITERATE. One intervention per iteration, aimed at the
  highest-frequency failure class. Re-evaluate this gate after every 5
  interventions; the ledger's slope is the health metric.
- < 4/20 AND failure analysis attributes blockers to information
  genuinely absent from the scans (sensor physics), not algorithm
  quality → thesis falsified for this scanner class. STOP, write the
  negative result (it is a publishable finding about consumer scan
  entropy), decide pivot (better scanner tier vs different wedge).
- < 4/20 with failures attributable to fixable algorithm classes →
  not a kill; iterate. Frustration is not a stop rule; verdicts are
  written here, in writing, against these criteria only.

## GATE 2 — credibility
- ≥ 14/20 AND ≥3 external users' own scans processed and accepted by
  those users → productization decision unlocked (business gate,
  separate doc; local-first + FreeCAD/Fusion integration + published
  accuracy benchmarks is the standing differentiation hypothesis).
- 8–13/20 sustained with flat ledger slope over 10+ interventions →
  scope check: narrow the part class (e.g., flat brackets only) and
  re-freeze a class-scoped gauntlet rather than grinding.

## Branch kill rule (technique level)
A technique branch (e.g., RANSAC vs learned segmentation; template
synthesis vs LLM synthesis) is killed only when BOTH hold:
(a) dominated by another branch on every failure class, AND
(b) two distinct, logged improvement attempts did not change the
ranking. Killed branches are archived with evidence, never deleted —
"failed without much iteration" is data, not disproof; only
dominated-and-twice-defended is disproof.

## Verdicts
(none yet — Gate 0 not started)
