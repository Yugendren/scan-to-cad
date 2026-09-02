# Prototype experiment 1 — phone scan vs reference scans of the DualSense (2026-09-03)

Inputs: Apple Object Capture scan (dualsense_controller.usdz, 19k faces) vs three
independent community 3D scans of the same product (Kabliga, V3Design, Printables
#1508424; see SOURCES.md). All decimated to ~150k faces. Script:
tool/compare_reference.py (+ ad-hoc section analysis). Runtime 108 s on the Mac.

## Result 1 — the references agree with each other (a usable consensus exists)
| pair | median | p95 | max | >0.5 mm |
|---|---|---|---|---|
| kabliga vs v3design | 0.150 mm | 0.569 mm | 3.58 mm | 8% |
| kabliga vs printables1508424 | 0.177 mm | 0.589 mm | 7.31 mm | 7% |
Three scans made by different people on different scanners agree to ~0.15 mm over
>90% of the surface. Disagreement (>0.5 mm) is confined to ~8% of the surface —
the known weak zones (button wells, stick undersides). Volumes: 369 / 364 / 361 cm³.

## Result 2 — the phone scan is NOT a scaled copy; it is shape-distorted
| alignment | median | p95 | max | >1 mm |
|---|---|---|---|---|
| rigid ICP | 3.05 mm | 7.02 mm | 13.2 mm | 84% |
| ICP with free scale (best fit 0.923) | 2.52 mm | 5.63 mm | 10.4 mm | 79% |
Letting the scale float only removes 0.5 mm of the error, so this is not a
global scale problem. Phone-scan volume 260 cm³ vs ~365 cm³ (−29%).

## Result 3 — where the phone scan is wrong (cross-sections, sections_phone_vs_kabliga.png)
- Mid-thickness slice: phone footprint matches the reference to ~1–3 mm — overall
  length and width are essentially right.
- Center slice through the thickness: the phone body is compressed ~2–3 mm on
  BOTH the front and the back face (total thickness 56.5 mm vs ~61–66 mm).
- Near-back slice: the grips are badly distorted/shrunken — the underside, where
  the controller met the table and where glossy black plastic defeats
  photogrammetry, is the worst region.
- Front-face slice: the phone captured the stick tops but its front face sits
  ~5 mm lower than the reference's.

## Interpretation
The phone scan has the right silhouette and the wrong depth: front and back
surfaces pulled inward and the underside reconstructed poorly. A cradle designed
from this phone scan would be ~5–9 mm too tight in thickness and would not fit.
A cradle designed from the consensus reference would (the references agree to
0.15 mm — comfortably inside snap-fit tolerance).

This is the product gap in one experiment: cheap scans are convenient and
wrong in a STRUCTURED way (depth compression, unscanned underside), references
are right and expensive. For mass-produced objects the winning path is
recognize → retrieve the consensus reference → align it to the phone scan →
trust the reference where the phone is unreliable → export mating features.
For one-off objects the same machinery needs priors (symmetry, primitives) and a
scale/depth correction model instead of a retrieved reference.

## Caveats
- Bounding-box comparisons (axis-aligned or oriented) are unreliable for this
  shape because of the sticks/triggers; volumes and cross-sections were used.
- The stick-top spacing check was inconclusive (the "highest points" differ in
  meaning between meshes) and is not used as evidence.
- One phone scan, one object. Repeat with 3–5 phone scans of the same
  controller (different lighting/placement) to separate systematic from
  random error, and with a matte object to isolate the glossy-black effect.
