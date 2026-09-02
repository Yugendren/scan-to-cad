# 19 — "AI scan edit for fit": does it exist, and who pays today? (2026-09-02)

Method: ~106 search/fetch attempts by a research agent. Idea under test:
an app that takes an Apple Object Capture scan, RECOGNIZES the object,
uses class knowledge to FIX the scan in place (sharpen edges, flatten
flats, enforce symmetry, fill holes, fix scale) — "AI image edit, but for
a 3D scan" — with dimensionally faithful output for designing mating
parts.

## Q1 — Does it exist?

(a) Generative-3D with scan conditioning — PARTIAL, not dimensionally
trustworthy. Hunyuan3D-Omni (Sept 2025): point-cloud/voxel/bbox control
encoder trained with noise "to simulate LiDAR/RGBD" — but an image is
always concatenated, output is a REGENERATED unit-normalized asset, and
no quantitative metrics are reported for point-cloud control. Rodin
Gen-2: PointCloud/Voxel/BBox ControlNet, Refine, Partial Edit, "3D Nano
Banana" (Mar 31 2026, box-select + text edit) — no scale/tolerance
statement; creative-asset tool. Meshy (Smart Remesh/auto-repair), Tripo
(Smart Mesh, retexture), TRELLIS.2 (image-only), Meta SAM 3D Objects
(single image, no metric claim), NVIDIA 3DObjectReconstruction (Jun 2026,
stereo→mesh, no priors): none object-aware. Closest research: MeshReGen
(Meta, Apr 2026, image + initial shape → regenerated geometry),
SpaceControl (mesh as spatial control with fidelity-vs-realism knob),
DetailGen3D, RecGen3D (SIGGRAPH Asia 2026) — all unit-cube normalized,
none evaluate mm error.

(b) Scanning apps — NONE object-aware. Polycam Object Mode (Jul 2026):
masking + chalk-spray advice, no AI cleanup claim; "Polycam AI" = separate
text/image-to-3D. KIRI Engine 4.2 (Apr 2026): 3DGS-to-Mesh 3.0 + a
measuring tool whose "AI-estimated distance won't be perfectly accurate"
→ manual rescale. Luma unmaintained; Scaniverse splats. Apple:
ObjectCaptureSession still "iOS 17.0+"; WWDC25/WWDC26 RealityKit contain
zero Object Capture changes (WWDC26 added splat rendering only). Android:
no LiDAR. Desktop suites: generic hole-fill/denoise.

(c) Research — PARTIAL; no metric evaluation of the exact idea.
Category-prior completion: DANCE (AAAI 2026, class head, preserves
observed geometry), GenPC (CVPR 2025, zero-shot real-scan completion via
image-to-3D priors with pose/scale-preserving fusion), Diffusion-Occ,
PoinTr/AdaPoinTr, SnowflakeNet, DiffComplete, SDFusion — all Chamfer in
normalized units on ShapeNet/PCN/MVP. CAD retrieve/align/deform:
Scan2CAD → Mask2CAD → ROCA → CAD-Deform → KP-RED/U-RED → FastCAD → OSCAR
(Jan 2026) → CAOA (3DV 2026) — indoor furniture, "a chair like this",
alignment-threshold scoring. Mesh-to-CAD half: CADFit (May 2026), BRep
boundary detection, MeshCone. The combination recognize → class prior →
in-place correction → mm evaluation: NO PAPER FOUND.

(d) Startups — NONE consumer; PARTIAL B2B. Backflip (Aug 3 2026 CAD
Copilot; $30M; "checks its own work to improve dimensional accuracy";
~$10/part; automaker deployment; $20/$50/$380 mo; no tolerance published,
no phone-scan claim; replaces the scan with prismatic CAD). Paramesh AI:
STL→STEP, "93% cross-section accuracy, <3% volume error", $2/part,
prismatic. Manual services: 2Soft3D, Fiverr from $15. "AI fix 3D scan"
searches: only generic cleanup and capture apps (RebuilderAI).

Dimensional trust: only Backflip/Paramesh claim it, on prismatic parts
from good scanners. Phone capture is the weak link: iPhone-vs-Revopoint
test (2025): "scale is not very accurate… scans need manual measuring
and resizing"; KIRI says the same.

## Q2 — Who pays today (ranked)

1. BODY-FIT FROM PHONE SCANS — real revenue, per-vertical anatomical
   priors. DentalMonitoring ($1B valuation, $100M Feb 2026, 500M+
   photos, FDA-cleared). Insoles/orthotics $4.5–4.8B market, custom = 63%:
   Groov (TrueDepth), MediScan (LiDAR), ReTiSense HEALIC, Materialise
   SAM/Phits, Volumental (3,000+ stores, 85M feet, mobile app summer
   2026). O&P: Össur acquired Standard Cyborg's tablet-scan socket
   design; SnugFit. Helmets: HEXR (calibration cap), KAV (TrueDepth, 108
   measurements). Eyewear: Fitz Frames, Topology. Ears: Snugs, SnugFit
   EarCam. These ARE "design around a scanned thing" — solved per
   vertical with a hard-coded anatomical template.
2. REVERSE-ENGINEERING / RESTORATION SHOPS — bureaus $2,000–3,000/part;
   BluMak3D $225 min / $150 hr; V3D crane restoration (May 2026);
   Restoric classic cars; Porsche 993 with SHINING 3D. Pay per part; use
   $1.5k–10k scanners, not phones.
3. MAKERWORLD/PRINTABLES FIT-ACCESSORY CREATORS — 2.6M models, 280k
   creators; "controller holder" 999+ models (top 29.4k downloads);
   Steam Deck 999+ (top 9.9k); $0.066/exclusive point, some creators
   >$1k/month, BOM commissions ~$20k/month. Real fit economy, but one
   accurate device scan serves thousands of downloads — tool spend small.
4. ETSY CUSTOM-FIT SELLERS — phone-accessory sellers est. $1k–5k/month
   at $8–40; replacement parts $8–50; scan/print-on-demand listings exist
   — workflow is "message photos or mail it in", not customer scans.
5. ACCESSORY BRANDS — cages designed per camera model; case makers use
   dummy units/leaked CAD "accurate to the millimeter"; no public
   evidence SmallRig/Tilta scan; indie photogrammetry grips only.
6. HOME APPLIANCE REPAIR — free files (happy3D, knob packs); near-zero
   willingness to pay.

## Verdict
"AI scan edit for fit" is NOT an existing product category. What exists:
(1) scan-conditioned generative REGENERATION for creative assets with no
metric guarantees; (2) B2B mesh→parametric CAD for prismatic parts from
pro scanners (the flatten/round half, no recognition, no in-place edit);
(3) vertical body-fit pipelines with hard-coded anatomical priors — the
only phone-scan-to-fit businesses with real revenue. Realistic 2026
buyers: reverse-engineering/restoration shops and O&P/insole clinics
(already paying $200–3,000/part and demanding accuracy), then
MakerWorld/Etsy accessory designers ($10–50/month ceiling). The
phone-scanning consumer is not yet a buyer because every phone app
disclaims scale — the bottleneck is METRIC CAPTURE + VERIFICATION, not
the edit.
