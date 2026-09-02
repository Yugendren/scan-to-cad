# 20 — DualSense 3D models online: provenance and truth-worthiness (2026-09-02)

Method: ~70 fetch/search attempts (GrabCAD JSON API, Printables GraphQL,
Cults3D, Thingiverse, Sketchfab, MakerWorld, CGTrader, BitBuilt, GitHub,
Sony manuals/blog/licensing pages, USPTO design patents, iFixit). No
files downloaded.

## Official dimensions / geometry
- Sony PlayStation Blog "PS5: The Ultimate FAQ" (2020-11-09): "approximately
  160mm x 66mm x 106mm (width x height x depth), excluding the largest
  projection… approximately 280g." Only first-party dimension statement.
  Manuals (CFI-ZCT1G 2021, CFI-ZCT2W 2025) list mass only.
- Design patents USD933750 / USD933751 (SIE, JP priority 2020-04-03):
  eight undimensioned stylised line drawings — the only official geometry.
- No official 2D/3D drawing exists publicly. iFixit teardown has no
  dimensional data. Shell geometry constant across BDM-010/020/030/040
  (eXtremeRate sells one back shell for all); DualSense Edge differs.

## Best models, ranked by provenance
1. Kabliga, "PS5 controller scan" — Printables #407609 (2023-02-24). OBJ
   59 MB + STL 37 MB; CC BY-NC-SA; 9,787 downloads, 233 likes. 3D scan,
   scanner unstated. Comments: "I found it dimensionally accurate"
   (2026-03); "exact measurements" for a holder; "some small artifacts";
   ".obj file is distorted, the stl works fine". Called "the only free
   dimensionally accurate PS5 controller scan" by a Thangs designer.
2. akaki, "DualSense controller 3D scan" — Cults3D (2023-02-10), also
   CGTrader $18. 5 STLs; €60; 12 dl. High-res scan, scanner unstated.
   Bounding box 159.0 × 105.7 × 65.7 mm vs spec 160 × 106 × 66 — within
   1 mm on all axes. Missing geometry in concave button wells; foam-tape
   artifact (corrected file supplied).
3. Benjamin Gonzalez, "PlayStation DualSense controller 3D scan" —
   GrabCAD (2025-12-29). 3MF; 234 dl. Creality Raptor X (laser,
   metrology-class spec). "Should be pretty dimensionally accurate (except
   for the backsides of joysticks) with correct units." Newest, best
   instrumented; no comments yet.
4. kentacles — Sketchfab (2024-10-01): 2.7M tris; CC BY 4.0; 836 dl;
   Revopoint Miraco; raw mesh, no accuracy claim.
5. Mister Red, "PS5 Controller Prop" — MakerWorld #1207667 (2025-03-14):
   STL halves; CC BY-SA; 517 dl, 51 prints; Creality scanner, cleaned;
   "accurate dimensions".
6. Referentiel/V3Design — Printables #678413 (2024-07-29): 2 STLs
   (119 MB); CC BY-NC-ND; 1,868 dl; scanner-based rework; holder comments
   "sits perfectly", "perfect negative shape".
7. Wesk (BitBuilt) — 2023-01-21: per-part meshes of a THIRD-PARTY shell;
   "reference only"; blobs where light couldn't reach.
8. Yuri Guerra — GrabCAD: SLDPRT + STL; 5,957 dl (most-downloaded CAD);
   created 2020-06-01, five months BEFORE retail → from reveal renders.
   Comments: "scale feels very off… boxy". Render model, not a reference.
Also: Douglas3D (Cults, "Creaform / high precision", 10 dl);
RottenSkinCollection "FIX SCAN" (claims 0.05–0.1 mm deviation, 3 dl);
CRE-8 raw OBJ; 3Dxyz "PS5 Joystick" (Sketchfab, Artec Spider, 983k tris);
Printables back-shell scan #1360636 (777 dl, public domain, foam
artifact); #1508424 (decimated 3MF); davec54 Thingiverse scan (stand
"fit like a glove", 725 dl, 11 makes). Artist models (AHarmlessPotato
38k dl — "no accurate blueprints or even an actual controller on hand";
Mstory-CG; CybearMiniatures dummy scaled to exactly 160×106×66) are not
dimensional references. GitHub: no controller geometry repos.

## How accessory makers get geometry
Sony's Official Licensing Program promises "technical documentation and
technical support"; nothing mentions CAD or drawings (unlike Valve, which
published Steam Controller CAD). No statements from Razer/Nacon/PowerA.
Observable practice at every level: scan a retail unit (Creaform, Raptor
X, Miraco, Artec), reverse-engineer, validate by trial prints (fteryda's
photo-designed dock: "dimensions are most probably wrong", multiple
revisions).

## Dummy/blank models and fit comments
Explicit dummies are rare; designers use the scans above as negatives.
No "had to scale 1.02" reports found; fit complaints cluster on
photo-derived designs, scan-derived docks/holders report exact fit.

## Metrology-grade truth
None public: no vendor dataset, university dataset, or CT of a DualSense.
Closest: Raptor X (Gonzalez), Creaform-tagged (Douglas3D), Artec Spider
(3Dxyz) — hobbyist captures with no deviation maps or calibration.

## Verdict
No online model is traceable ground truth. Kabliga (free, most used,
community-confirmed) + akaki (bbox within 1 mm of spec) + Gonzalez
(Raptor X) are strong PRIORS, best cross-checked against each other and
the 160/66/106 spec; known weak zones: concave button wells, stick
undersides, battery-foam region. Ground truth still requires measuring
or scanning a physical unit. Licensing: Kabliga CC BY-NC-SA and V3Design
CC BY-NC-ND are research-only; kentacles CC BY 4.0 and the public-domain
back-shell are product-usable.
