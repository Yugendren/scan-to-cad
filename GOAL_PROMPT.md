# Copy-paste prompt: build the synthetic harness and v0 baseline (Gate 0a), then stop

```text
/goal Build and score Gate 0a of the Mericanii scan-to-CAD programme —
the virtual scanner, the SYNTH-GAUNTLET-20 benchmark, the deviation
scorer, and the v0 no-ML reconstruction baseline — write the Gate 0a
verdict, and stop before any real-scan, learned-model, or product work.

WORKING DIRECTORY AND AUTHORITY

Run only inside /Users/yugendren/experiments/scan_to_cad.
Read PROJECT_CONTRACT.md, GOAL_STATE.md, GATES.md, DATA_PLAN.md
completely; init Git with main stable, work on goal/gate0a-harness;
never touch sibling folders.

THE ONE-SENTENCE GOAL (context, not this run's scope)

An automatic pipeline turning noisy prosumer 3D scans of prismatic
mechanical parts into editable parametric CAD (build123d + STEP) with a
per-part deviation certificate, scored on frozen 20-part benchmarks
(synthetic now, real scans at Gate 0b).

THIS RUN'S SCOPE — GATE 0a ONLY

1. VIRTUAL SCANNER: structured corruption of known CAD, as a pipeline
   of toggleable layers — multi-view raycast depth rendering from
   realistic scanner poses; distance-dependent depth noise; holes from
   self-occlusion and steep/shiny-face dropout; per-view SE(3)
   registration jitter; TSDF/Poisson fusion (must visibly round sharp
   edges); outlier speckle clusters. Vertex-jitter Gaussian alone is
   forbidden as a scan mimic. Parameters in one config file so Gate 0b
   can later calibrate them against real scans.
2. DATA: source mechanical-part CAD online (ABC dataset; manufacturer /
   GrabCAD STEP of brackets, mounts, flanges, adapters). Freeze
   SYNTH-GAUNTLET-20: 20 held-out models + frozen simulator config,
   manifest with hashes and per-part key dimensions extracted from the
   reference CAD (tolerance default ±0.2mm). Unlimited separate DEV
   models for iteration. Holdout rules identical to the real gauntlet:
   never tuned on, scored at most weekly, append-only ledger.
3. SCORER: per-part pass/fail on the GOAL_STATE.md scorecard (fidelity,
   editability, honesty, autonomy, runtime) + deviation heatmap vs the
   corrupted scan + intent check vs reference CAD (recovered
   planes/bores/symmetry) + failure class per failed part
   (SEG/FIT/SNAP/SYNTH/DEV/HON). evidence/ledger.md entry per run with
   commit hash.
4. v0 PIPELINE, no learned models: Open3D conditioning → efficient
   RANSAC primitive fitting → intent solver (snap angles to 0/90/45°,
   dimensions to round numbers and standard metric series, enforce
   parallel/coaxial/symmetric within measurement tolerance; solved as
   constrained optimization; every snap logged with confidence) →
   templated build123d synthesis → STEP export → certificate.
5. Iterate on DEV; score SYNTH-GAUNTLET-20 once at the end; write the
   Gate 0a verdict in GATES.md with per-part results and failure
   taxonomy. 0/20 still completes the gate; the verdict must say where
   the entropy lives.

DO NOT

- Claim any thesis result from synthetic scores (upper bound only).
- Train or fine-tune any model (v1 territory).
- Use any LLM as a scored geometry oracle; LLM use is limited to
  writing code that the CAD kernel and scorer then judge.
- Tune anything against SYNTH-GAUNTLET-20; all iteration on DEV.
- Buy anything, build UI/product, or start Gate 0b/1 work; no new
  experiment before the Gate 0a verdict is written in GATES.md.

STOP CONDITION

Gate 0a verdict written, evidence committed, ledger entry complete.
Report: v0 SYNTH-GAUNTLET score, top-3 failure classes with counts,
which simulator layers hurt v0 most (ablation by toggling layers —
cheap and tells us what real-scan robustness will require), and the
single highest-leverage first intervention. Then stop.
```
