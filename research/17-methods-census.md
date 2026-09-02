# 17 — Methods census: who already does each pipeline stage (2026-09-02)

Method: 70 search/fetch attempts by a research agent with an explicit
mandate to be brutally honest. Format per line: TOOL/PAPER — what it
does — closeness (Same / Partial / Adjacent) — source.

## 1. Mesh repair + printability
- Meshmixer — Inspector auto-fix, Make Solid, Analysis→Thickness — Same;
  free, unmaintained — meshmixers.com, Formlabs.
- Netfabb — repair scripts, wall-thickness reports — Same — 3dprinting.com.
- Microsoft 3D Builder — unmaintained; its Netfabb-licensed Windows
  repair API is what PrusaSlicer "Fix through Netfabb" and Bambu Studio
  "Fix Model" call — Windows-only — Prusa forum, PrusaSlicer #6454,
  Bambu wiki.
- Slicers — auto-repair small errors on import; NONE ships wall-thickness
  analysis (BambuStudio #1410 open since Mar 2023) — Partial.
- Materialise Magics — Fix Wizard + wall-thickness — Same (paid).
- Blender 3D Print Toolbox — non-manifold/intersections/thickness/
  overhang checks — Same (free).
- Formware — free online repair — Same.
- Rhino ShrinkWrap / Blender voxel remesh / MeshLab — watertight by
  rewrapping, loses sharp intent — Adjacent.
- Academic robust repair: MeshFix, ManifoldPlus, fTetWild, CelloCut
  (2026; arXiv 2605.17853) — Same.
- Learned: DiffComplete (NeurIPS 2023), SC-Diff (2024), DL hole
  inpainting (2024); Tripo/Meshy "AI auto-repair" = watertight remesh
  marketing — nothing learned integrated into printability tools.
VERDICT: REUSED. Commodity; any implementation is a wrapper.

## 2. Primitive segmentation
- Efficient RANSAC (Schnabel 2007) / Region Growing in CGAL — gated by
  epsilon/normal_threshold/min_points — Same; PCL SACSegmentation,
  Open3D segment_plane same idea.
- Learned: SPFN, ParSeNet, HPNet, PrimitiveNet, SED-Net (SIGGRAPH 2023),
  BPNet (IJCAI 2023), Point2Primitive (2025), Segment Any Primitive
  (CVPRW 2025); Adobe patent US11682166 — Same.
- Fusion — "Generate Face Groups" (planar/cylindrical/radial/fillet)
  then "Convert Mesh → Prismatic" merges groups into faces and infers
  prismatic features; no feature tree, no deviation report — Same.
- SolidWorks — Segment Imported Mesh Body; ScanTo3D Surface Wizard
  auto-region + analytic assignment + Deviation Analysis — Same.
- Geomagic Design X — Auto Segment, "Automatically Extract Shapes" — Same.
- Shining3D EXModel — auto primitives + perpendicular/parallel/
  coincident relations — Same.
- QuickSurface/Mesh2Surface, PolyWorks Modeler, Artec Studio — Same.
- Onshape (no mesh→BRep), Rhino QuadRemesh — Adjacent.
VERDICT: REUSED. Free code and 4+ commercial packages.

## 3. Intent / beautification
- Langbein lineage — thesis 2003; "Choosing consistent constraints"
  (CAD 2004); regularity feature trees (2006); Li/Langbein/Martin
  symmetry-based design intent (CAD 2010) — Same, 20 years old.
- Benko/Várady constrained fitting (CAGD 2002); Kovács/Várady/Salvi
  (Graphical Models 2015): constraints "only up to a certain tolerance"
  — Same.
- INUS/3D Systems patent US7814441 (filed 2006; now Hexagon):
  "identifying original design intents from 3D scan data" — extrusion
  direction, revolve axis, mirror planes, draft, fillet radii, shell
  thickness by error minimization with outlier removal. This IS Design
  X's Redesign Assistant — Same, shipped since ~2006–2010.
- Design X Auto Sketch — lines/arcs/circles/slots with constraints,
  explicit Fitting Tolerance, Equal Constraints (2024.3) — Same.
- QuickSurface, Artec Studio, EXModel — auto-constrain + refit — Same.
- Dimension snapping to standard series — Verisurf describes manual
  "normalizing" (0.3721″→0.3750″); NO tool found that automatically
  snaps to ISO preferred numbers or drill/thread tables. CAD-Recode's
  round numbers are a quantization artifact — Not found.
- Recent: Autodesk "Aligning Constraint Generation with Design Intent"
  (ICCV 2025, sketches); Lambourne prismatic CAD from rounded voxels
  (2022); symmetry-plane detection papers — Partial.
VERDICT: ADAPTED. Constraint inference + consistent-subset selection is
textbook and patented in product since 2006. Automatic snap-to-standard
under a deviation budget is unshipped — a policy layer on existing
machinery: product novelty, not method novelty.

## 4. Parametric CAD export
- Backflip (Aug 2026) — foundation model → feature tree with sketch
  constraints; agent self-check loop; Fusion add-in + web; from $20/mo;
  ADVERTISES deviation heatmaps — Same, and cheap.
- Point2CAD — per-segment plane/sphere/cylinder/cone/INR, lowest-error
  model selection, surfaces+topology, no feature tree — Partial.
- CAD-Recode, cadrille, CADReasoner (CVPR 2026), CADFit (2026),
  Point2Primitive, TransCAD, CAD-SIGNet, SOV-CAD — Same in research.
- Scan2CAD — retrieval+alignment — Adjacent.
- Commercial: Fusion prismatic BRep (no tree); Design X LiveTransfer
  (history to SW/NX/Creo/Inventor); QuickSurface; Mesh2Surface;
  PolyWorks Modeler; EXModel Pro; FreeCAD Detessellate (only OSS route).
VERDICT: REUSED. Only thin gap: open-source, fully automatic,
feature-tree output.

## 5. Deviation reports / certificates
- Free: CloudCompare C2M/C2C, MeshLab Hausdorff — Same. Metrology:
  Control X, ZEISS INSPECT, PolyWorks Inspector, VXinspect — Same.
  Prosumer: Revo Measure (color map, PDF report) — Same.
- In-reconstruction deviation: Design X Accuracy Analyzer (patents
  US7821513 / RE48498), Mesh2Surface/QuickSurface real-time maps,
  ScanTo3D Deviation Analysis, Backflip heatmaps — Same.
- Fusion: no mesh-vs-body deviation map (requested 2018, absent);
  Blender toolbox none — Gap.
- GATING (the key check): RANSAC/RG gate per point; Point2CAD by lowest
  residual; Design X 2024.3 Fitting Tolerance + Remove Outlier N·Sigma
  + fitting-deviation colors on preview (user accepts); PolyWorks
  0.25 mm/20° filters; US7814441 outlier removal + user accept;
  CADFit/CADReasoner iterate on IoU/Chamfer; Backflip self-checks.
  NO tool found that automatically rejects/downgrades a SNAPPED feature
  against a stated tolerance and emits a pass/fail certificate.
VERDICT: REUSED for the report; ADAPTED for gating. Certificate
packaging is product, not method.

## 6. Ensembles / uncertainty
- Deep ensembles / MC-dropout for point-cloud segmentation (2020),
  Bayesian point-cloud segmentation (2024), GURecon (2024), RANSAAC,
  STAPLE (2004) — Partial.
- Embodied Intelligence patent US12183011 (priority 2020): hundreds of
  sampled segmentation hypotheses; agreement ≥x% = x% confidence;
  threshold-gated acceptance — the exact mechanism, in 2D robot picking.
- Cross-method disagreement as per-face confidence for CAD primitive
  segmentation — not found (absence of evidence is weak; disagreement
  ≠ error; value unproven).
VERDICT: ADAPTED.

## Bottom line (agent's words)
Design X has shipped stages 2–5 with a patented deviation analyzer and
patented design-intent extraction since ~2006–2010; Backflip now
automates 2–5 with a self-checking agent and heatmaps for $20/month.
Nothing in this pipeline is methodologically new. The only defensible
claims are integration-level: (a) automatic snap-to-standard-series
with an explicit deviation budget and pass/fail certificate, (b)
multi-method disagreement maps for primitive segmentation, (c) all of
it open-source and unattended. Those are product bets, and (a)/(b) must
be validated against Backflip and Design X on real scans before being
called contributions.

Sources (selection): meshmixers.com, Formlabs, 3dprinting.com, 3DPI,
Prusa forum, PrusaSlicer #6454, Bambu wiki, BambuStudio #1410,
Materialise, Blender manual, McNeel, arXiv 2605.17853, DiffComplete,
Meshy tutorials, CGAL docs, BPNet/HPNet/SED-Net/SAP papers, US11682166,
Autodesk blog + Fusion help, SolidWorks help, Hawk Ridge, GoEngineer,
Design X 2024.3 release notes, Shining3D, QuickSurface, PolyWorks,
Artec docs, Onshape blog, langbein.org, CAD 2004, GM 2015, US7814441,
Verisurf, ICCV 2025 (2504.13178), 2209.01161, DEVELOP3D, backflip.ai/
mesh-to-cad, ar5iv Point2CAD, CADReasoner GitHub, CADFit 2605.01171,
CAD-Recode, Scan2CAD, Detessellate, Leo AI, Revopoint (Revo Measure),
Novedge, RE48498, Autodesk forum (deviation map request), 2007.01787,
GURecon 2412.14939, US12183011.
