# PLAN — the mesh perfection layer (drafted 2026-09-02)

Style: q27b idiom. Companion to GOAL_STATE.md / GATES.md / RESEARCH.md.
Test data: /Users/yugendren/3d/test_scans/ (DualSense controller USDZ,
numpad USDZ). Working skeleton: tool/scanfix.py (load → analyze →
repair → export → report; runs on both scans).

## The exact goal, one sentence

Take any hobbyist mesh — a phone/scanner scan or a downloaded STL —
and return two VERIFIED artifacts: (1) a RESTORED model (clean,
complete, correctly scaled, surfaces idealized toward design intent)
and (2) a PRINT-CERTIFIED file (watertight, thickness-checked,
sliceable), each with an honest report of what changed and how far the
result deviates from the input.

## Input

- Now (DEV items): the two test scans.
  - DualSense: 19k faces, watertight, 158×56×109 mm. Class: curved
    organic shell. Ground truth exists (real device ≈160×66×106 mm).
  - Numpad: 25k faces, floater removed, 91×49×133 mm. Class:
    prismatic — the class the intent lane is built for.
- Soon: any STL/OBJ/PLY/3MF, because the verified paid market is
  mostly DOWNLOADED meshes, not scans (see Evidence).

## Output (three artifacts per job)

1. `*_restored` — "the proper scan": floaters gone, large holes
   closed, noise smoothed without melting edges, correct mm scale,
   and — the differentiator — flat faces made truly flat / cylinders
   truly round WHERE THE EVIDENCE SUPPORTS IT, every idealization
   logged with its confidence.
2. `*_print.stl/3mf` — watertight, unified normals, minimum-wall
   report, suggested orientation; optional shell/solidify for thin
   scans.
3. `*_report` — the certificate: before/after stats, actions taken,
   restored-vs-original deviation summary (max / 95th percentile),
   flagged uncertain regions, dimension checks. One silent
   hallucination = failed part (HON rule).

## How — milestones on top of the skeleton

- M1 REPAIR THAT EARNS ITS KEEP (pymeshlab lane): large-hole closing
  (open bottoms), adaptive decimation + Taubin edge-preserving
  smoothing, wall-thickness measurement (ray/SDF sampling), scale
  sanity checks. Exit: both scans pass a slicer + thickness map in the
  report. (The Apple scans arrive pre-closed; raw scanner meshes are
  the real test — acquire a few for DEV.)
- M2 IDEALIZE (the moat; numpad is the exam): region-growing/RANSAC
  segmentation → intent solver (snap coplanar/perpendicular faces,
  cylinder axes, standard dimensions — accepted only when post-snap
  deviation stays inside the measured noise envelope) → re-mesh the
  idealized regions. Exit: numpad's top and sides become true planes
  with certificate proof; controller passes through untouched except
  repair (organic class = no snapping, honestly reported).
- M3 PARAMETRIC LANE (premium): build123d/STEP feature tree for
  prismatic parts; CAD-Recode fine-tune + small segmentation net
  (the mini-model ensemble) only after classical v0 plateaus — models
  propose, kernel + scorer judge, ensemble disagreement = confidence
  heatmap.
- INTERFACE: CLI now → local-first drag-drop app later. Free
  analysis/report as the funnel; paid restore/export (one-time
  personal license per GTM research); dogfood by fulfilling
  Fiverr-style per-part jobs for revenue + messy real meshes.

## Evidence this output is desired (from the session's market research)

1. PAID DEMAND, VERIFIED: Fiverr "stl to step" ≈13,000 gigs; top
   sellers 887/817/446 reviews at $25–264/job — thousands of real,
   repeated transactions for exactly "turn my mesh into a usable
   model." Mostly downloaded meshes → input-agnostic core.
2. PAIN LEDGER: r/functionalprint (~0.5M) top content = solution
   requests ("can print, can't design"); "will it hold?" has zero
   consumer tools; tolerance/fit is universal. Print-certification +
   honest reports target these directly.
3. SCANS ARE REAL BUT EPISODIC: 14/19 top r/3DScanning posts are
   mechanical RE, but a few parts/year/person, community ~1% the size
   of printing → scans = premium tier, not the core market.
4. COMMODITY FLOOR: free converters (imagetostl, 500MB) already do
   naive tessellated conversion → only idealization + certificates
   are defensible. Incumbent Backflip: cloud-only, judged "by eye,"
   ~3K declining monthly visits despite $30M → the honest-accuracy,
   local-first lane is open.
5. ANTI-SLOP POSITIONING: the MakerWorld AI backlash means "verified,
   honest output" is free brand equity in this community.

## Discipline

Gates and kill rules per GATES.md. The two test scans are DEV items,
never gauntlet. M2's exam is certificate-gated: no snap without
evidence. A negative reproducible result at any gate is completion,
not failure.
