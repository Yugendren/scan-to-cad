# NOVELTY — honest verdict against prior work (2026-09-02)

Source: research/17-methods-census.md (70 search/fetch operations,
adversarial mandate). This file states plainly what is reused,
adapted, or new, and corrects earlier over-claims made in this
project's own documents.

## Stage-by-stage

| Stage | Verdict | Who already does it |
|---|---|---|
| Repair + printability | REUSED | Meshmixer, Netfabb, Magics, Blender 3D Print Toolbox, MeshFix/ManifoldPlus; slicers auto-repair (but none ships wall-thickness analysis) |
| Primitive segmentation | REUSED | CGAL RANSAC/region growing, PCL, Open3D; ParSeNet/HPNet/SED-Net/BPNet; Fusion Face Groups → Prismatic; SolidWorks Segment Mesh; Design X Auto Segment; EXModel; QuickSurface; PolyWorks; Artec |
| Intent / beautification | ADAPTED | Langbein 2004, Várady 2002/2015 (textbook); Design X Redesign Assistant = patent US7814441 (2006); Auto Sketch with Fitting Tolerance; QuickSurface/Artec auto-constraints. NOT FOUND anywhere: automatic snap to standard series (ISO preferred numbers, drill/thread tables) under a stated deviation budget |
| Parametric export | REUSED | Backflip (self-checking agent, $20/mo), Design X LiveTransfer, QuickSurface, PolyWorks Modeler, EXModel Pro; research: CAD-Recode, CADReasoner, CADFit. Only thin gap: open-source, unattended, feature-tree output |
| Deviation report | REUSED | CloudCompare (free), Control X, ZEISS INSPECT, PolyWorks, Revo Measure (PDF report); IN-reconstruction: Design X Accuracy Analyzer (patented), Mesh2Surface/QuickSurface live maps, ScanTo3D, Backflip heatmaps. Gap: Fusion has none |
| Deviation GATING | ADAPTED | Per-point residual gates are universal; Design X exposes fitting tolerance + outlier removal with user acceptance. NOT FOUND: automatic reject/downgrade of a SNAPPED feature against a tolerance with a pass/fail certificate |
| Ensemble disagreement → confidence | ADAPTED | Textbook (deep ensembles, STAPLE) and patented in 2D robot picking (US12183011). Unreported for CAD primitive segmentation; value unproven (disagreement ≠ error) |

## Corrections to this project's earlier claims

1. "Nobody reports deviation guarantees / the competitor is judged by
   eye" — WRONG as a market claim. Design X has a patented Accuracy
   Analyzer; QuickSurface/Mesh2Surface show live deviation maps;
   Backflip advertises heatmaps. What is true: one independent
   reviewer judged Backflip's output by eye, and Fusion has no
   deviation map. The defensible remainder is automatic
   accept/reject of snapped features + a pass/fail certificate.
2. "Intent solving is an empty lane since 2005" — WRONG commercially.
   The academic lane went quiet, but Design X shipped patented
   design-intent extraction (extrusion axes, mirror planes, fillets,
   draft, shell) from 2006 and Auto Sketch constraint fitting with
   explicit tolerance. The only unshipped piece is snap-to-standard-
   series under a deviation budget — a policy layer, not a method.
3. "No public real-scan benchmark with dimension metrics" — still
   stands (not contradicted), and remains the most genuinely useful
   contribution available.

## Plain-English verdict

We are NOT doing something super unique. Methodologically this is an
ADAPTATION: every stage exists in free code or in commercial tools
that have shipped for 15–20 years, and a funded competitor automates
the whole chain for $20/month. What we would be doing differently is
integration and policy:

(a) automatic snap-to-standard-series with an explicit deviation budget
    and a pass/fail certificate (unshipped; small, checkable idea);
(b) multi-method disagreement as a per-face confidence map (unreported
    for this use; must prove disagreement predicts error);
(c) all of it open-source, unattended, local-first, and priced for
    hobbyists (product/distribution, not science);
(d) a public real-scan benchmark with dimension-error metrics (the one
    thing that would be a genuine contribution if published).

(a) and (b) must be validated head-to-head against Backflip and Design
X on real scans before being called contributions.

## What this means for the Mericanii thesis

This product does NOT test Bet 3 ("machine-created systems surpass
the best human designs"). It is an engineering wedge that reuses
human-designed methods well. Its honest value to the company is (i)
revenue and users in the physical domain, (ii) the messy-mesh corpus
and per-scanner noise data, and (iii) the certificate/benchmark
discipline practiced on a real market. Anyone presenting it as
frontier machine discovery would be over-claiming.
