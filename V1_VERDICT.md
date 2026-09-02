# V1 VERDICT — scanfix v1 (2026-09-02)

Goal (from V1_GOAL_PROMPT.md): a local, deterministic pipeline that takes a
scan or any mesh and returns a RESTORED model, a PRINT-READY file, and an
HONEST REPORT, evaluated on a DEV set. Branch `goal/v1`.

## What was built
`tool/scanfix/` — load (USDZ/STL/OBJ/PLY/3MF/glTF) → analyze (stats, noise
envelope, CAD-like detection) → repair (floaters, clean, close holes,
orient, budget-gated Taubin smoothing, VERIFIED decimation) → idealize
(prismatic class only; planar regions flattened only if p95 deviation ≤
budget; every accept/refusal logged) → printability (inward-ray wall
thickness with corner-hit rejection, thin-region locations, orientation
suggestion, explicit --thicken) → deviation certificate (original→restored
distortion, restored→original added-surface fraction with flagged regions)
→ JSON + HTML report → CLI `run` / `batch` (ledger).
Plus: minimal virtual scanner (raycast + noise + dropout + jitter + Poisson
refusion + trim), three known-CAD parts with recorded truth, `eval_dev.py`.

## DEV scorecard (final run; evidence/dev_eval.md, evidence/dev_ledger.md)

| file | class | watertight | printable | dev p95 mm | thin % | idealized | s |
|---|---|---|---|---|---|---|---|
| MINI-fan-spacer.stl | prismatic | yes | yes | 0.000 | 0.0 | 1/40 | 0.46 |
| MINI-fsenzor-cover.stl | prismatic | yes | yes | 0.000 | 0.0 | 0/14 | 0.43 |
| MINI-inspection-door.stl | prismatic | yes | yes | 0.017 | 0.5 | 9/32 | 0.44 |
| MINI-knob.stl | prismatic | yes | yes | 0.004 | 0.4 | 29/45 | 0.71 |
| MINI-rail-spoolholder.stl | prismatic | yes | yes | 0.000 | 0.0 | 2/29 | 0.29 |
| MINI-x-carriage.stl | prismatic | yes | yes | 0.000 | 3.4 | 5/37 | 0.74 |
| MINI-y-belt-holder.stl | prismatic | yes | yes | 0.000 | 0.4 | 2/34 | 0.89 |
| MINI-y-idler.stl | prismatic | yes | yes | 0.000 | 0.1 | 2/29 | 0.97 |
| MINI-z-top.stl | prismatic | yes | yes | 0.000 | 0.1 | 6/27 | 0.65 |
| dualsense_controller.usdz | organic | yes | yes | 0.000 | 0.0 | 0/0 (never snapped) | 1.75 |
| numpad.usdz | organic* | yes | yes | 0.131 | 0.0 | 0/0 | 1.26 |
| synth_flange.stl | mixed | yes | yes | 0.000 | 0.3 | 0/0 | 3.01 |
| synth_l_bracket.stl | prismatic | yes | yes | 0.011 | 2.7 | 6/10 | 2.50 |
| synth_pocket_block.stl | mixed | yes | yes | 0.001 | 0.9 | 0/0 | 2.46 |

Totals: 14/14 watertight, 14/14 printable by the verdict rule, 14/14 within
the 0.15 mm deviation budget, mean 1.18 s/file on the M4 (single runs).
Batch of 14: 17.5 s on the Mac (within the ~2-minute rule; it was run here
because it is shorter than a coffee — larger sweeps go to the 3060).
3060 batch runtime: NOT MEASURED — no access to the box from this session;
the `batch` command is machine-agnostic and ready to run there.

*numpad exam (devset/exam/numpad_auto, `--snap-budget auto --mesh-class
prismatic`): 23 planar candidates, 2 accepted, 21 refused. The key surface
(3,140 mm²) was REFUSED with p95 deviation 0.98 mm from a plane — correct:
keycaps are not a plane. The gate did its job on a real scan.

## What "good" was achieved
- Both scans and every STL come out watertight, oriented, in mm, with a
  print file that slices, and a report that discloses every action.
- The deviation certificate is honest in both directions: distortion of
  existing surface (budgeted) is separated from added surface (closed
  holes), which is listed as flagged regions with locations.
- Idealization is conservative and evidence-gated: on CAD STLs it flattens
  faces at ~0.00 mm deviation; on the numpad it refuses the keys; on the
  controller it does nothing and says so.
- Verified decimation: when quadric collapse broke manifoldness (pocket
  block), the repair pass fixed it; if repair fails it reverts and logs.

## What was NOT achieved
- The Apple Object Capture scans arrive already closed and clean, so the
  hole-closing and floater logic was exercised only by the synthetic scans
  and one 6-face floater. Raw Revopoint/Creality meshes remain untested.
- Class thresholds are heuristic. The numpad (11% truly planar area at the
  noise-widened tolerance) classifies as organic in default mode; the
  flange and pocket block (35–36%) as mixed and therefore are not
  idealized. A prismatic object scanned noisily can miss the prismatic
  gate; the user override exists but the auto-classifier is not yet a
  product-grade decision.
- Dimensional accuracy vs CAD truth on synthetic scans is 0.9–2.1 mm off —
  and the corrupted INPUT was already off by exactly that much (Poisson
  refusion inflates/rounds). scanfix reproduces the scan faithfully; it
  does not recover true dimensions. That is the v2/M3 intent lane, not v1.
- The DualSense "dimension check" (9.5 mm vs an approximate public spec)
  is inconclusive: the spec includes stick tops and trigger travel the
  scan does not, so this reference is not a valid ground truth.
- No web drag-drop page (stretch); STEP export intentionally out of scope.

## Top-3 failure modes (with example files)
1. THIN flags from repair slivers at unscanned undersides — synth_l_bracket
   (2.7% below 0.8 mm; the thin cluster sits at z = −0.7 mm, below the
   base, i.e., the cap over the missing bottom nearly coincides with
   residual surface). Real artifact of hole closing; correctly reported,
   not yet fixed. Also seen at 0.9% on synth_pocket_block.
2. Prismatic scans classified mixed/organic → no idealization —
   numpad.usdz, synth_flange, synth_pocket_block. Cause: Poisson-rounded
   edges and noise fragment planar regions; the truly-planar-area test is
   safe but conservative.
3. Possible genuine thin features flagged on CAD parts — MINI-x-carriage
   3.4% below 0.8 mm (largest cluster at [63.1, 19.7, 18.2] mm, min
   0.53 mm). Not verified by eye; could be real design detail (Prusa parts
   have thin lips/embossing) or residual corner-hit artifacts two hops away.

## Single highest-leverage next intervention
Sliver-aware hole closing: before capping a boundary loop, remove thin
flap faces within ~2× sample spacing of the loop, then cap and re-check
thickness locally. It attacks failure mode 1 directly and would also
reduce mode 3's ambiguity by removing double-surface artifacts. Second in
line: replace the class threshold with "idealize any region that passes
the gate, regardless of class, but never on organic-classified meshes" —
which turns failure mode 2 into a non-issue while keeping the controller
protected.

## Would a hobbyist pay for this output today?
Honestly: not for the two Apple scans as they are — those files were
already watertight and sliceable when they arrived, so v1 mainly told the
truth about them (useful, not worth money). The payable moments in this
DEV set are narrower: a raw scan with holes and floaters that becomes a
sliceable, oriented, mm-correct file with a thin-wall map in one command
(the synthetic cases show this works, real raw scans are untested), and
the deviation certificate itself, which no free tool produces in this
form. Against free alternatives (Meshmixer, Blender's toolbox, slicer
auto-repair) v1's edge is disclosure and the deviation-gated flattening,
not repair quality. That is a $0–$10 "nice tool" today, not a $29 license;
the price case depends on v2 recovering dimensions and true flat faces on
real scanner output — which is exactly what the failure modes above point
at. No claim of novelty is made (see NOVELTY.md); this is known methods
with a disclosure discipline.
