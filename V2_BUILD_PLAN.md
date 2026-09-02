# V2 BUILD PLAN — "scan it, fix it, design against it" (drafted 2026-09-02)

Goal: an app (Mac first; iPhone captures) that takes an Apple Object
Capture scan of an object you own, works out what it is, corrects the
scan in place using what real objects are like, and hands you a
reference accurate enough that a part designed around it fits on the
first print. Research basis: research/17–19; NOVELTY.md.

## Pipeline (eight stages) with difficulty and what exists

| # | Stage | What it does | Reuse | Difficulty |
|---|---|---|---|---|
| 1 | Capture + scale | Apple Object Capture (USDZ, LiDAR-metric). Add a SCALE REFERENCE protocol: a printed calibration tile / credit card in the scene; app detects it and corrects global scale. PLOS 2024: <1 mm with a scale bar, >1 mm without. This is how HEXR/DentalMonitoring get away with phones. | Apple API; AprilTag/ArUco detection (OpenCV) | EASY (weeks) — and the single biggest accuracy win |
| 2 | Recognize the object | From the capture photos: object class (controller, keyboard, bracket, bottle…) via an off-the-shelf vision model or a vision-LLM call; plus geometric class per region (planar / cylindrical / freeform) from v1's region growing | CLIP/YOLO/VLM; v1 idealize.py | EASY for class, MEDIUM for reliable region typing on noisy scans |
| 3 | Priors library | Per object class: symmetry planes, flat/cylindrical regions, grid regularity (keys, vents), standard hole sizes, "known reference CAD exists" flag. Start hand-written for 5–10 classes; grow from data | Langbein-style rules; MeshToFeatures-style snapping | MEDIUM (engineering + curation) |
| 4a | Prismatic correction | Fit planes/cylinders to regions → solve constraints (parallel, perpendicular, coaxial, round/standard dimensions) → REBUILD sharp geometry from fitted primitives (edges = plane intersections), not vertex nudging | CGAL/own RANSAC; v1 solver skeleton; OCCT/build123d for rebuild | MEDIUM–HARD (OCCT boolean fragility; known engineering — QuickSurface does it manually) |
| 4b | Organic correction | Detect symmetry plane robustly (Je et al., SIGGRAPH Asia 2024), mirror-average to cancel noise and fill one-sided gaps; smooth-surface fit preserving real creases | paper code; pymeshlab | MEDIUM |
| 4c | Retrieval (popular objects) | If a clean reference model of the recognized product exists (controllers, phones, consoles are all online), align and deform it to the scan (ROCA / CAD-Deform lineage) — best accuracy path for mass-produced objects | research code; public CAD | MEDIUM; licensing questions |
| 5 | Verification + confidence | Deviation vs scan (evidence, not truth), residual consistency, ensemble disagreement → per-region confidence; synthetic-truth harness (exists); caliper protocol | v1 deviation.py; virtual scanner | MEDIUM |
| 6 | Export for design | Mating features as CAD entities — planes, hole axes/diameters, symmetry plane, bounding dims — as STEP + the corrected mesh, into Fusion/FreeCAD/Shapr3D; confidence shown per feature | build123d/OCCT STEP | EASY–MEDIUM |
| 7 | Fit-aware design help | Turn confidence into CLEARANCE: low-confidence mating faces get more tolerance or compliant features (the DJI-mount trick: a 1.1× scaled scan as clearance, done properly). This is how the fit test passes even when accuracy is imperfect | design rules | MEDIUM — and strategically important |
| 8 | Fit test flywheel | Design a snap-fit part from the reference → print → does the real object click in? Log result + which faces were off → per-scanner error model + priors improve | v1 ledger discipline | EASY to define, SLOW to accumulate |

## The one hard problem
Everything above is known engineering EXCEPT the physics question: can
priors (scale bar + symmetry + primitives + retrieval) pull phone-scan
error from 1–3 mm down to the 0.1–0.3 mm a snap-fit needs? Evidence:
even a 0.037 mm scanner yields ±0.2 mm after primitive fitting (Turek
2025); no one has shown sub-mm from phones. Two ways to win it:
(a) accuracy — scale bar + symmetry + primitives on PRISMATIC objects
    plausibly reach ~0.3 mm (unproven); retrieval on known products
    reaches CAD accuracy by construction;
(b) tolerance — stage 7: design the mating part to absorb the remaining
    uncertainty (clearance from confidence, compliant clips). The
    customer buys "fits first time", not "0.1 mm".
Go/no-go experiment (2–3 weeks, Mac + one printer): scale-bar protocol +
symmetry + primitive rebuild on the synthetic truth set (target ≤0.3 mm
vs CAD truth, from ~1–2 mm today) and on the numpad/controller with
calipers; then ONE physical test — a snap-fit cradle for the DualSense
designed from the corrected reference. Fits → build; doesn't fit at any
clearance → stop.

## Order of work
1. Go/no-go experiment above (weeks 1–3). Uses v1 harness + new stages
   1, 4a/4b, 5. Mac for dev; batch/eval on the 3060.
2. Prototype (months 1–3): Mac CLI/app; prismatic + organic paths;
   scale bar; symmetry; CAD-entity export; confidence; two physical fit
   tests logged. No recognition model yet — class chosen by the user.
3. App (months 3–6): iPhone capture flow with scale tile; recognition
   via off-the-shelf vision; priors library for ~10 classes; retrieval
   for popular products; Fusion/FreeCAD import; fit-test logging.
4. Vertical proof (months 6–12): one paying segment first — restoration/
   RE shops (per-part pricing) or a handheld-device accessory niche —
   with published first-print fit rate. Body-fit verticals are the
   existence proof but are regulated and already served; keep as later
   option.

## Compute and cost
Stages 1–8 as listed need no training. Learned pieces (region typing on
noisy scans, class-conditioned completion) come later and train on the
3060 with virtual-scanner data. Off-the-shelf vision for recognition
(API or small local model). Physical costs: calibration tiles, filament,
calipers (~$100). The expensive input is time.

## Difficulty, honestly
- Engineering: medium. Every stage exists somewhere; integration into a
  one-button flow a non-expert can trust is the work (3–6 months solo
  with agents to a credible app).
- Science: one hard unknown (accuracy from phones), with a designed
  escape hatch (tolerance-aware design). Decided by a 3-week experiment.
- Market: proven per vertical (feet, teeth, heads), unproven in general;
  first buyers are shops paying per part, not hobbyists.
- Competition: Backflip could add most of this; speed and the fit-test
  data flywheel are the only durable edges.
