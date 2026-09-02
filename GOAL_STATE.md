# Goal State — drafted 2026-09-02 (awaiting founder freeze)

## The Mericanii thesis test

The harness, scorer, and rails are human-built lab equipment. The
**solutions** are machine-produced: the pipeline recovers design intent
(plane/bore/fillet structure, snapped dimensions, symmetry) from noisy
scans automatically, with zero human clicks, and every output carries a
deviation certificate against the raw scan. The customer-facing framing
is the P1 wedge from the Pain Ledger (MR-2026-09-02): "a bracket takes a
day" → minutes. The honest framing: this tests whether prior-driven
machine perception can beat the human reverse-engineering workflow on a
frozen public benchmark — a small, certificated instance of trusted
machine design (observe → model), not yet invention.

## The one-sentence goal

Build an automatic pipeline that turns noisy prosumer 3D scans of
prismatic mechanical parts into **editable parametric CAD** (executable
code-CAD + STEP) with a **per-part deviation certificate**, measured
continuously on a frozen 20-part real-scan benchmark (GAUNTLET-20), and
iterated one failure-class at a time.

## Scorecard — every gauntlet part is judged on all five

1. **Fidelity** — every caliper-measured key dimension within tolerance
   (default ±0.2 mm; per-part overrides fixed in the gauntlet manifest
   at freeze).
2. **Editability** — output is executable build123d/CadQuery that
   rebuilds the solid and exports valid STEP, with named features.
3. **Honesty** — every region deviating from the scan beyond threshold
   is flagged in the report. One silent hallucination = part fails.
4. **Autonomy** — zero human clicks between scan file in and artifact out.
5. **Runtime** — ≤10 min/part on the M4 (soft; logged, not gating at v0).

## In scope (and nothing else)

1. Part class: prismatic/rotational mechanical parts (brackets, mounts,
   adapters, knobs) — the dominant real use case. Organic/freeform
   surfaces are explicitly out for v0–v2.
2. v0: no learned models. Open3D conditioning → efficient-RANSAC
   primitive fitting → **intent solver** (discrete-continuous
   optimization: snap angles to 0/90/45°, dimensions to round numbers
   and standard series, enforce parallel/coaxial/symmetric within
   measurement tolerance) → templated code-CAD synthesis → deviation
   certificate.
3. v1 (only for failure classes v0 provably cannot fix): small learned
   segmentation trained on virtual-scanner corruption of ABC-dataset
   CAD — simulate the target scanner's noise; ground truth for free.
4. v2: LLM writes/repairs the CAD program from the structured
   primitive+constraint graph (never raw points); the kernel executes;
   the deviation report drives the repair loop. The LLM is never a
   scored oracle — geometry claims come only from the kernel + scorer.
5. Dev/holdout: unlimited DEV parts, iterate freely; GAUNTLET-20 frozen
   at Gate 0, never tuned or trained on, scored at most weekly,
   append-only ledger with commit hashes.
6. Failure taxonomy on every failed part:
   SEG (segmentation) · FIT (primitive fit) · SNAP (intent solver) ·
   SYNTH (program synthesis) · DEV (deviation) · HON (unflagged
   hallucination). One iteration = one intervention aimed at the
   highest-frequency class.

## Explicitly out of scope (later or never)

- Product, UI, pricing, marketing, or competitor feature-chasing before
  Gate 1 passes.
- Training any model before the Gate 0 harness exists.
- Tuning anything against GAUNTLET-20, ever (leakage = re-freeze with
  replacement parts and a logged incident).
- Freeform/organic surface reconstruction; assemblies; threads beyond
  recognizing standard bores (v3+ territory).
- RL / tree-search over intent hypotheses before Gate 1 (v3, needs the
  experience data the loop generates first).
- Claiming "solved scan-to-CAD" — the claim is scoped to the part class
  and the benchmark, always with the score attached.

## Current state

- [DONE 2026-09-02] Market/pain research complete (Pain Ledger artifact);
  P1 selected; technical landscape mapped (Point2CAD, CAD-Recode,
  Scan-to-BRep open-source; Backflip = funded pro-tier competitor;
  hobbyist tier unserved).
- [NEXT] Founder freezes this goal (edits welcome), then Gate 0
  execution: acquire 20 real parts + scans + caliper ground truth,
  build the scorer, score v0.
- [PLANNED 2026-09-02] Scan acquisition path resolved on paper — see
  DATA_PLAN.md (four part tiers with known geometry + one scanning
  session on the friend's scanner; ~$150 parts + $25 calipers).
  Remaining unknown: confirming the friend's scanner session.
