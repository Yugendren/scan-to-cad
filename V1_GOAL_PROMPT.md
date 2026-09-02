# Copy-paste prompt: build scanfix v1 — scan in, good output out

(GOAL_PROMPT.md remains the separate benchmark-track prompt. This one
builds the product function.)

```text
/goal Build scanfix v1: a local, deterministic pipeline that takes a
3D scan or any mesh file and returns a RESTORED model, a PRINT-READY
file, and an HONEST REPORT — evaluated on a DEV set and closed with a
written v1 verdict. No training, no cloud, no hallucination.

WORKING DIRECTORY AND AUTHORITY

Run only inside /Users/yugendren/experiments/scan_to_cad.
Read, in order: PLAN.md, METHOD.md, NOVELTY.md, GATES.md, then
tool/scanfix.py (the working skeleton). Init Git if absent (main =
baseline, work on goal/v1). Never touch sibling folders. Use the
existing .venv in tool/ (python 3.12; trimesh, pymeshlab, usd-core,
scipy installed) — add packages with uv only.

COMPUTE RULES (non-negotiable)
- The Mac is for editing and single-file runs (seconds). Any batch
  evaluation, parameter sweep, or job over ~2 minutes runs on the
  RTX 3060 box or AWS. Write scripts so the same command runs on
  either; do not launch sweeps on the Mac.
- Nothing in v1 requires a GPU. Do not add training.

INPUT
- tool must accept: .usdz (Apple Object Capture — already supported),
  .stl, .obj, .ply, .3mf, .glb.
- DEV set (never call it a benchmark): the two scans in
  /Users/yugendren/3d/test_scans/ (DualSense controller = organic
  shell class; numpad = prismatic class) PLUS at least 8 more meshes
  you obtain: mechanical-part STLs from Printables/Thingiverse
  (brackets, mounts, knobs), any raw scanner meshes available, and
  2–3 synthetic corruptions of known CAD (a MINIMAL virtual scanner:
  raycast depth + noise + hole dropout + Poisson/TSDF refusion; no
  need for full calibration in v1). Record each file's source, class
  (organic / prismatic / mixed), and any known true dimensions.

OUTPUT — the definition of "good" (all three per input)
1. <name>_restored.(stl|ply): floaters removed; large holes closed
   (open bottoms included); noise reduced with edge-preserving
   smoothing (Taubin or bilateral — sharp edges must survive);
   decimated to a sane face budget while keeping ≤0.05 mm geometric
   error; correct mm scale (flag if bbox suggests wrong units).
   IDEALIZATION (the one smart step, prismatic class only): detect
   near-planar regions (region growing / RANSAC), and flatten a region
   ONLY IF the post-flatten deviation of its vertices stays within the
   measured noise envelope of the mesh (estimate it from local residual
   statistics; default budget 0.15 mm, configurable). Log every accept
   and every refusal with the numbers. Organic surfaces (controller)
   are never snapped — say so in the report.
2. <name>_print.(stl|3mf): watertight, unified outward normals,
   single body (or explicitly listed multiple bodies), mm scale.
   Wall-thickness analysis (ray/SDF sampling): report minimum and
   distribution, flag regions below 2× nozzle width (default 0.8 mm
   for a 0.4 mm nozzle) and below a user-set minimum. Suggest a print
   orientation (minimize overhang area / maximize flat base) and state
   the reasoning. Never thicken or alter geometry silently — offer
   --shell/--thicken as explicit options that are logged.
3. <name>_report.(json+html): before/after stats; every action taken
   with parameters; deviation of restored-vs-original (signed distance:
   max, 95th percentile, per-region flags); idealization accept/refuse
   log; thickness stats and flagged regions; scale sanity; a final
   verdict line per artifact (printable: yes/no + why). The HTML must
   be readable by a hobbyist with no jargon in the summary block.
   HON rule: any change not disclosed in the report is a defect.

INTERFACE
- CLI: `scanfix run <file> [-o outdir] [--nozzle 0.4] [--min-wall 0.8]
  [--snap-budget 0.15] [--no-idealize] [--shell <mm>]` and
  `scanfix batch <dir>` (batch is the thing that runs on the 3060).
- Stretch, only after everything above works: a single-file local web
  page (drag-drop → runs locally → shows the report) — no uploads to
  any server.

EVALUATION (DEV, honest, written down)
- Score every DEV file on the scorecard: watertight? min-wall met?
  restored-vs-original deviation within budget? idealization
  accept/refuse decisions correct on inspection? known dimensions
  preserved (DualSense ≈160×66×106 mm; any STL with a declared size)?
  runtime? Write evidence/dev_ledger.md: one row per file per run,
  with commit hash and failure class (SEG/FIT/SNAP/SYNTH/DEV/HON —
  for v1 mostly DEV/HON/thickness).
- Iterate one intervention at a time on the most frequent failure.
  Do not tune to a single file; a change must not regress the others.

DO NOT
- Train or fine-tune any model. No LLM in the geometry path (LLMs may
  help you write code; the code, the kernel, and the scorer decide
  geometry).
- Upload user files anywhere. Everything local.
- Snap, flatten, or "beautify" anything outside the deviation budget,
  or without logging it. Silent cleanup = failure.
- Claim novelty. NOVELTY.md is explicit: this is an integration of
  known methods with a certificate discipline. Report it that way.
- Spend time on parametric/STEP export, scanner noise calibration, or
  UI polish before the three outputs are good on the DEV set.

STOP CONDITION
Write V1_VERDICT.md: per-file scorecard table; what "good" was
achieved and what wasn't; the three most common failure modes with
example files; runtime on Mac (single) and 3060 (batch); the single
highest-leverage next intervention; and an honest one-paragraph
answer to "would a hobbyist pay for this output today, and why/why
not?" Commit everything. Then stop.
```
