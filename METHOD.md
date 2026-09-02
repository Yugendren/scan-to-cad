# METHOD — how the function is built, and on what compute (2026-09-02)

## The function

    f(mesh_file) -> (restored_mesh, print_mesh, certificate.json)

f is a PIPELINE, not a single model. Roughly 70% deterministic geometry +
optimization, 30% small learned components — and every stage's output
passes through a deterministic verifier before it can be emitted.
Reason: an end-to-end mesh→mesh network (a) has no real ground truth
for "restored" beyond synthetic data, (b) produces unverifiable output,
(c) needs data scale we don't have. The pipeline lets each model be
small and each output checkable.

## Stage map — what kind of "model" each stage is

| Stage | Method | Style | Trained? |
|---|---|---|---|
| Load / scale / floaters | geometry (trimesh) | none | no |
| M1 repair: hole closing, smoothing, decimation | geometry (pymeshlab) | none | no |
| M1 printability: wall thickness, orientation | ray/SDF sampling | none | no |
| M2 segmentation into regions | region-growing / RANSAC first; small supervised net when they fail | supervised (PointNet++/DGCNN-class, few M params) | yes, on virtual-scanner data |
| M2 intent solver: snap to planes/cylinders/standard dims | constrained optimization (Langbein-style hypothesis selection + least squares) | math, not ML | no |
| M2 verifier / certificate | signed-distance deviation, validity checks | none | no |
| M3 parametric export | LLM-style PROGRAM SYNTHESIS: emit build123d/CadQuery, kernel executes, compare, repair loop | LLM (CAD-Recode: Qwen2-1.5B + point projector) | fine-tune (LoRA) on synthetic programs |
| v3 intent search | tree search / RL over discrete snap hypotheses, reward = certificate score | RL | later, on accumulated experience |

Where each style genuinely fits:
- DIFFUSION: shape completion / hallucinating missing geometry. Plausible,
  not verifiable → NOT in the core. At most a gated option for large-hole
  filling, always flagged in the certificate.
- LLM (program synthesis): the right tool whenever the output is a
  PROGRAM the kernel can execute — editable, checkable by construction.
- RL: the right tool for the discrete search over intent hypotheses,
  because the certificate is a clean reward. Not before Gate 1.
- SUPERVISED small nets: segmentation, where labels are free (synthetic).

Ensemble principle: run several proposers (RANSAC + region-growing +
learned net); agreement = confidence, disagreement = flagged region.
Models propose; kernel + scorer judge. Never average geometry.

## Training data — the virtual scanner is the factory

Known CAD (ABC dataset, manufacturer STEP) → virtual scanner (raycast
views → depth noise → occlusion holes → registration jitter → TSDF
fusion edge-rounding → speckle) → corrupted mesh WITH perfect labels:
per-face primitive type, primitive parameters, the generating program.
Infinite, free, CPU-generated. Real DEV scans (the two test files +
raw scanner meshes to acquire) are used to CALIBRATE the noise model
and to EVALUATE — never as the only training source. Later: user
accept/reject of snaps = experience data for v3.

## Compute plan

[RULE — founder, 2026-09-02] The M4 Mac mini is a personal machine.
No training, no bulk data generation, no long batch jobs on it. All
heavy compute runs on the 3060 box (the one reliably available) or
AWS. Vault rule still applies: paid compute is never a foundation
dependency — everything must be runnable on the 3060 alone.

M4 Mac mini — development and light use only:
- Editing, unit tests, single-mesh runs of the classical pipeline
  (scanfix on one scan takes seconds — that's fine).
- Reading results, writing reports. Nothing that pins the CPU for
  more than a few minutes.

RTX 3060 (12 GB) — the primary compute box:
- Virtual-scanner data generation (CPU raycasting + GPU where useful).
- Eval harness / gauntlet scoring sweeps.
- Train segmentation nets: minutes–hours per run.
- LoRA / QLoRA fine-tune of CAD-Recode (1.5B) on 50–200k synthetic
  examples: ~1–2 days; fits in 12 GB with a 4-bit base.
- Inference of the 1.5B program-writer and batched evaluation.

AWS credits — burst and overflow:
- Parallel virtual-scanner generation on a CPU fleet (millions of
  samples in hours).
- A10G/L4/A100 for full (non-LoRA) fine-tunes or larger data scale.
- Long gauntlet sweeps when the 3060 is busy. Not needed before
  Gate 1.

## Order of work

v0 (M4 only): M1 repair + printability + certificate. Deterministic.
v1 (M4 + 3060): virtual scanner → train segmentation net → M2 intent
   solver on numpad-class parts.
v2 (3060, AWS optional): LoRA fine-tune program-writer → M3 parametric
   export with kernel-in-the-loop repair.
v3 (after Gate 1): RL/tree search over intent hypotheses using
   accumulated certificate scores and user feedback.
