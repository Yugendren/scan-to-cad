# 11 — Scan-to-parametric-CAD technical landscape (2026-09-02)

Method: ~13 direct fetches (GitHub, CGAL docs, arXiv API, project
pages) — the agent's search quota was exhausted; 2026 arXiv IDs from
live API queries (~95% reliable).

## 1. Primitive fitting & segmentation
- Efficient RANSAC (Schnabel 2007); production implementation CGAL
  Shape_detection (RANSAC + Region Growing, noise knobs epsilon/
  normal_threshold/cluster_epsilon). CGAL package is GPL — research
  OK, product-contaminating; alternatives pyransac3d (MIT, crude) or
  reimplementation. Region growing more stable than RANSAC on dense
  structured-light meshes.
- Learned: ParSeNet (ECCV'20), HPNet (ICCV'21, open), SED-Net (2023);
  trained on ABC with mild noise — degrade on real scans. Point2CAD
  (CVPR'24, prs-eth): most complete open pipeline (ParSeNet seg →
  analytic + INR fitting → clipping) but CC-BY-NC 4.0 + PyMesh
  dependency (build pain, Docker). Split-and-Fit (SIGGRAPH'24,
  2406.05261), BPNet (2307.04013). Nothing 2025–26 displaced these.
  Verdict: CGAL region-growing + RANSAC baseline; Point2CAD eval-only.

## 2. CAD program synthesis
- CAD-Recode (github filaPro/cad-recode; 2412.14042; ICCV'25): point
  projector (one linear layer) on Qwen2-1.5B → executable CadQuery;
  1M procedurally generated sequences released; weights v1/v1.5 (Mar
  2025) on HuggingFace; SOTA on DeepCAD/Fusion360/CC3D. Successor
  cadrille (2505.22914): multimodal + RL.
- Lineage: DeepCAD → Text2CAD → 2026: CADReasoner (≈2603.29847,
  kernel-in-the-loop: emit → render → discrepancy → iterate, with a
  scan-sim track), CADFit (≈2605.01171, editable construction
  sequences from meshes), MIRAGE-CAD (Aug'26), extrusion-decomposition
  paper (≈2605.08971) — per-extrusion segmentation improves
  generalization. Direct B-rep: BrepGen (GPL-3.0, generative not
  reconstruction), HiFi-BRep, BrepARG, ParaCAD (point-cloud-conditioned
  autoregressive B-rep — closest 2026 competitor). Scan-to-BRep /
  BRepDetNet (2409.14087) edge prior.
- No published system combines RANSAC evidence + LLM code synthesis +
  constraint solving.

## 3. Intent recovery / beautification (dormant classical lane)
Langbein, Marshall, Martin et al., "Choosing consistent constraints for
beautification of reverse engineered geometric models," CAD 36(3),
2004: hypothesize regularities (equal radii, angles near 0/30/45/90°,
symmetries) → maximal consistent subset via priority greedy/backtracking
→ numerical solve. Companions: Benkő/Várady/Martin constrained fitting
(2001–02), Werghi (1999), Mitra partial symmetry (SIGGRAPH'06), PRS-Net
(2020). Modern revivals attack SKETCHES (Vitruvion 2109.14124,
SketchGraphs, DAVINCI 2410.22857). Discrete-continuous recipe:
hypothesis generation → discrete selection (greedy-with-rollback beats
MILP; consistency = constrained least-squares converges within
tolerance) → simultaneous constrained optimization (LM with hard
constraints or penalty homotopy). Nobody has published a learned/LLM-era
Langbein for solids; nobody rounds dimensions to standard series.

## 4. Datasets & benchmarks
ABC (1M B-reps), Fusion 360 Gallery, DeepCAD (~178k), MCB. CC3D (Uni
Luxembourg): 50k+ virtual-scanner scan–CAD pairs (academic access);
CC3D-PSE (sharp edges), CC3D-Ops (37k B-reps with op labels). 2026
benchmarks UniCAD (2606.05058), OmniMech, CADEngBench — all synthetic
input. Metrics: Chamfer, F-score@1%, Invalidity Ratio, face IoU, edge
Chamfer. No public benchmark of real prosumer scans with ground-truth
parametric CAD and dimension-level metrics; nobody reports dimension
error or constraint-recovery accuracy.

## 5. Virtual scanner simulation
BlenSor (2011) abandoned. Practical stack: Open3D RaycastingScene +
analytic noise + ScalableTSDFVolume (reproduces edge rounding,
thin-feature loss). Noise model (Khoshelham & Elberink 2012; Nguyen–
Izadi–Lovell 2012): axial σ ~quadratic in depth, lateral σ in pixels,
grazing-angle dropout, quantization. No canonical published model for
fringe-projection prosumer scanners; vendor 0.02–0.05mm claims vs
0.1–0.3mm independent real-world accuracy dominated by registration
drift, reflectance bias, fusion smoothing. Characterize own scanner
against gauge blocks — publishable, feeds the certificate.

## 6. Tooling
build123d (Apache 2.0, active, OCP/OCCT, STEP) — synthesis target;
CAD-Recode emits CadQuery (same kernel; trivial interop). FreeCAD 1.0+
scripting heavyweight for headless. trimesh (MIT) glue; Open3D (arm64
wheels); PyMeshLab fallback; avoid PyMesh. Apple Silicon: classical
pipeline fine; ParSeNet/HPNet need CUDA; CAD-Recode 1.5B CPU inference
feasible.

## Three biggest risks
1. Segmentation on real noise (fillets, worn edges, fusion smoothing)
   → region growing + multi-hypothesis until the solver disambiguates.
2. Wrong snapping (89.7°→90° on a true 89.5° part) → certificate-gated:
   accept only if post-solve deviation ≤ characterized noise envelope.
3. B-rep validity / OCCT boolean fragility; LLM lane hallucinates OOD →
   kernel-in-the-loop repair from day one.

## Where a small team wins
(a) real-noise robustness + a real benchmark (20–50 parts with CAD +
gauge measurements on Revopoint-class hardware) — no such benchmark
exists; (b) intent solving (lane dead since ~2005); (c) honesty/
certificates (no system reports per-face deviation guarantees or
refuse-to-snap decisions).

Sources: arXiv 2412.14042, github filaPro/cad-recode, prs-eth/point2cad,
CGAL Shape_detection docs, cvi2.uni.lu/cc3d, samxuxiang/BrepGen,
gumyr/build123d, arXiv 2606.05058, 2409.14087, 2410.22857, 2109.14124,
2406.05261, arXiv API listings Aug 2026 (CADReasoner, CADFit,
MIRAGE-CAD, ParaCAD, HiFi-BRep, OmniMech, CADEngBench).
