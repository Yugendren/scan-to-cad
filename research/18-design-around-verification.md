# 18 — Does "phone scan → trustworthy reference to design around" exist? (verified 2026-09-02)

Method: ~115 search/fetch attempts by a research agent (Reddit via mirror;
Product Hunt CAPTCHA-blocked, unverified). Idea under test: consumer phone
scan (Apple Object Capture / Polycam class, 1–3 mm error) → object-class
inference → prismatic rebuild with sharp edges / organic smoothing →
symmetry enforcement → scale correction → mating features exported as CAD
entities → per-region confidence → validated by first-print fit.

## 1. Mainstream CAD
- SolidWorks ScanTo3D (Pro/Premium): Mesh Prep + Surface Wizard recognizes
  analytic shapes; manual; no noise model, symmetry, or fit validation —
  PARTIAL. Xtract3D, xShape/3D Sculptor — ADJACENT.
- Autodesk Fusion: Insert Mesh (OBJ has no units — Polycam's tutorial
  scales ×1000 by hand), Face Groups, Convert Mesh → Prismatic (locked out
  of Personal), Mesh Section Sketch; no native best-fit plane to a mesh
  face ("do the fitting in Blender") — PARTIAL. Fusion's scan-to-CAD answer
  is now the Backflip add-in (19 Aug 2026).
- Onshape: Constrained Surface (Apr 2025) BREP patches from mesh with
  deviation analysis; iPad LiDAR for large objects/areas — PARTIAL/ADJACENT.
- Shapr3D: mesh reference + booleans; no scan/LiDAR feature through
  v26.150 (17 Aug 2026) — NONE.
- Solid Edge Reverse Engineering: Identify Regions "Automatic" results
  "not quite as expected" per Siemens' own tutorial → manual painting;
  extracted surfaces "leave a large gap" — PARTIAL.
- Creo: via Design X LiveTransfer — ADJACENT.
- Rhino ShrinkWrap + Mesh2Surface/QuickSurface: primitives, auto-constrain,
  Live Deviation Analyzer; QuickSurface 2026 (Nov 2025) added a
  Selection-Based SYMMETRY PLANE "to compensate for real-world
  imperfections" — manual, pro; closest pro toolset — PARTIAL. Design X:
  Auto Segment, Accuracy Analyzer, ~$21k — PARTIAL.
- FreeCAD: Reverse Engineering WB; MeshToFeatures addon (v0.17.x, 23 Aug
  2026) does design-intent snapping (canonical axes, coaxial merge, equal
  radii, round values → PartDesign body) but "Organic / sculpted / scanned
  shapes will not reconstruct meaningfully"; no symmetry/scale/confidence —
  PARTIAL (clean STL only).
- Plasticity PolySplines — ADJACENT. SelfCAD — nothing. Blender symmetry
  tools are for authored meshes — ADJACENT.

## 2. Scanning apps
- Polycam: "Object Mode models are not dimensionally accurate unless you
  use the Rescale tool"; OBJ/STL only; "fixture that fits snugly" tutorial
  with no tolerances or test fits — PARTIAL (tutorial only).
- Scaniverse (Niantic Spatial, splats), KIRI Engine, Luma (dormant),
  Qlone, 3D Scanner App, MagiScan: mesh export at best — NONE.
- Apple Object Capture: PLOS One (Dec 2024) within 1 mm WITH a scale bar,
  >1 mm without; no design features — NONE.
- Revopoint Revo Design / Creality+QuickSurface bundle: hardware-bound
  pro RE — PARTIAL. Bambu MakerLab AI Scanner: "not professional-grade" —
  NONE. No app markets "design around your scan" — NONE.

## 3. Startups 2024–26
- Backflip AI — the real competitor: mesh (STL/OBJ/GLB/PLY) → feature
  tree, Fast/Thinking, self-check; targets 3-axis milled/turned parts;
  Fusion add-in use cases include "reconstruct an existing interface
  around which a new component must fit"; no mention of phone scans,
  symmetry, scale correction, confidence, or fit validation — PARTIAL,
  and one product decision from covering most of the idea.
- Spectral Labs SGS-1 (Sep 2025): image/mesh → STEP; HN tester: "Every
  dimension is wrong" — ADJACENT.
- Zoo, Adam, Kaedim: no scan path — NONE.
- ShapeScan / MyCaseBuilder Photo Tracer: 2D outline → holder — ADJACENT.
- Chinese: nothing beyond Revopoint/Creality. HN: zero scan-to-CAD
  stories besides SGS-1.

## 4. Open source
- CADFit (ICML 2026): mesh → CadQuery; watertight clean inputs; CC BY-NC —
  PARTIAL. dalidesign10-dev/scan-to-cad (0★): Poisson → primitives → STEP,
  "still scan-derived faceted geometry" — prototype.
- GitHub queries for symmetry-aware scan→CAD, primitive-fit-to-scan
  Blender addons, "case for scanned object" scripts: zero hits. Scan2CAD =
  CAD-to-room alignment (different problem) — NONE.

## 5. Community practice
Pro-scanner makers design-around routinely (Kindle bumper in
Einscan+QuickSurface "25 min"; IO shield "fit the first time"; DJI mount
via Miraco → Instant Meshes → Fusion using a 1.1×-scaled scan as
"clearance"). Phone-scan users are told not to bother: r/3DScanning (Oct
2024): "If dimensional accuracy is your goal then using an iPhone is not
the way… regardless which app" → calipers; "photo with a ruler" or
ShapeScan. Make: (Jan 2024) RealityScan → Blender → Fusion boolean with
zero tolerance/test-fit discussion. Autodesk forum: "Use the scan only as
reference." Nobody fit-tests systematically; no phone-scan → reference →
snap-fit tutorial exists.

## 6. Academic
- Symmetry: Mitra 2007 symmetrization; Je et al. SIGGRAPH Asia 2024
  (noise-robust symmetry detection/symmetrization, arXiv 2410.02786);
  E3Sym, PRS-Net; none coupled with B-rep/mating reconstruction — PARTIAL.
- Design intent: Langbein 2004, Gao 2015, Autodesk Research Oct 2025
  (sketches), Design X patent — PARTIAL (old, clean data).
- Scan→CAD learning: CC3D/SHARP, CAD-Recode, CADReasoner (scan-sim track),
  View2CAD (Apr 2025, single RGB-D, real data, encodes geometric
  uncertainty — closest to per-region confidence) — PARTIAL.
- Fit benchmarks: none. Turek et al. 2025 (Designs): even a 0.037 mm
  scanner gives ±0.2 mm after primitive fitting, ±0.9 mm autosurface,
  print ±0.2–0.3, total ±0.4–1.3 mm. MUSE (May 2026) assemblability
  rubric, no physical test — NONE for physical fit.

## Verdict
(a) Nothing does the whole idea.
(b) Pieces exist: primitive fitting + auto-constraints + deviation maps
(QuickSurface/Design X/ScanTo3D/Solid Edge — pro, manual, $1.8k–21k);
manual symmetry plane with compensation (QuickSurface 2026); intent
snapping on clean STLs (MeshToFeatures, free); AI whole-part rebuild with
"interface a component must fit" as a stated use case (Backflip, $20/mo,
accepts phone OBJ/PLY); noise-robust symmetrization and uncertainty-aware
B-rep in research code; scale by ruler (manual everywhere); 2D-outline
holders.
(c) Genuinely absent: a phone-scan error model used to CORRECT dimensions
rather than fit them; object-class inference driving strategy; automatic
symmetry enforcement on consumer scans; mating-feature export instead of
whole-part rebuild; per-region confidence for the designer;
fit-on-first-print as the validation loop; any product marketed to
non-pros as "design around your scan."

## Brutal caveats
1. Backflip already ingests phone-scan formats and owns the Fusion
   channel; the defensible wedge is the fit-validated reference +
   confidence, not "scan to CAD."
2. The physics is unproven: even a 0.037 mm scanner yields ±0.2 mm after
   primitive fitting; snap-fits need ~0.1–0.3 mm. Whether symmetry and
   primitive priors can pull sub-mm truth out of 1–3 mm phone scans is
   demonstrated nowhere.
3. Demand signal is weak: the communities that would use this currently
   route around it with calipers and "measure straight into CAD."
