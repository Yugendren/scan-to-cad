# 09 — Scan → clean CAD: customer pain (2026-09-02)

Method: 26 searches by a research agent. Purpose: validate the
friend's pain ("scan gives dots; want it to know surfaces are flat").
This became P1 in the Pain Ledger.

## Customer base and size
Handheld scanners ~$1.8B (2025) → $3.4B (2035); broader 3D scanner
market ~$4.9B (2025), handheld ~39%. Hobbyist tier $300–1,500: Shining
Einstar (~$960), Revopoint POP/Mini/MIRACO ($600–1,000), Creality
Otter/Raptor ($700–3,700), 3DMakerpro Mole (~$634). Revopoint: five
~$2.6–3M Kickstarters, 26,000+ cumulative backers (POP 4: 3,373
backers/$2.64M; MIRACO $2.99M). Creality holds 7 of 10 top-selling
scanner slots. Segments: hobby machinists/CNC reverse-engineers;
automotive restoration/custom fab; makers/cosplayers; small job shops
without $20K Creaform gear.

## The pain in their words
Canadian Hobby Metal Workers: "Automatic surfacing creates a bunch of
shit surfaces that cannot be extended"; "Mesh data can only be used as
a guide to redraw the solid object"; "Even for $20K don't expect much
from a 3d scanner"; machining vs scanning success: "95% vs, well,
almost single digits." Autodesk forums: "I know how much of a
nightmare it can be to work with scan data"; "many people give up on
the idea once they see how much work is involved"; Fusion Prismatic
mesh-convert "freezes indefinitely." 1–2 hours post-processing minimum
for a simple part; standard advice: overlay the mesh and remodel by
hand.

## Software landscape and prices
Pro: Geomagic Design X Go $1,900/yr, Plus $3,990/yr, Pro quote; Go
perpetual ~$4,990. QuickSurface full ~$4,300 perpetual, Pro sub
~$1,900. Mesh2Surface for Rhino ~$1,700 incl. Rhino. All manual/
semi-automatic. Hobbyist: Fusion 360 personal mesh tools (crashy),
FreeCAD, Blender/Meshmixer. Vendor software (Revo Scan 6, Creality
Scan): "AI" one-click optimization, hole-filling, noise removal —
prettier meshes, never parametric CAD.
Backflip AI: Markforged founders, $30M NEA/a16z; SOLIDWORKS plugin
building native feature trees from meshes; web app; Aug 2026 "CAD
Copilot" that "checks its own work, then iterates" (Fast/Thinking
modes); Standard $20/mo, Pro $40, Business $200 (later verified as
$20/$50/$380). Pitch: hours and $1,500+/part → minutes and ~$10.
Independent hobbyist reviews scarce; marketing targets industrial
downtime and SOLIDWORKS seats.

## Technical state of the art
Point2CAD (CVPR 2024): segments point clouds, fits primitives + neural
freeform surfaces, SOTA on ABC. CAD-Recode (ICCV 2025): Qwen2-1.5B
emits executable CadQuery from point clouds, 10x lower Chamfer.
Scan-to-BRep (arXiv 2409.14087): detects B-rep boundaries. Gap: all
trained on synthetic CAD datasets; robustness to real scanner noise,
holes, partial coverage is the open problem — Backflip's claimed moat
(10x inference, 100x resolution vs academic).

## Willingness to pay
Bureaus $250–2,000+/part; "simple bracket with drawing" $2,000–3,000;
RE labor ~$145/hr; day rates $1,200–3,500. Hobbyists pay ~$0 for
software after $600–1,000 hardware; cliff to $1,900+; Backflip's
$20/mo first credible mid-point.

## Conclusion
Hobbyist/prosumer tier underserved: hardware got cheap 10x faster than
scan-to-CAD software. Between free-mesh-only and $1,900–5,000 manual
tools sits one funded player, pro-oriented, credit-metered,
cloud-only, unvalidated by hobbyists for dimensional accuracy. The
in-loop "this face is a plane, this bore is a cylinder" optimizer
integrated with free tools does not exist. Risks: OEMs bundling deeper
AI; Backflip downmarket.

Sources: GM Insights, Future Market Insights, MarketsandMarkets,
Revopoint news, Accio, IN3DTEC, canadianhobbymetalworkers.com thread
6039, Autodesk forums td-p/6795651, GoMeasure3D, Top3DShop, Novedge,
Rapid Scan 3D, Revopoint/Creality software pages, BusinessWire (Aug 3,
2026), 3DPrint.com, backflip.ai/pricing, arXiv 2312.04962 (Point2CAD),
2412.14042 (CAD-Recode), 2409.14087, Tangent, 3Blades.
