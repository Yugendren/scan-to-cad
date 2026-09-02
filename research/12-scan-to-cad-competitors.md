# 12 — Scan-to-CAD competitive landscape (2026-09-02)

Method: ~25 search/fetch operations (Brave, DuckDuckGo via proxy,
pullpush, HN Algolia, vendor/press pages). Reddit blocks fetching; the
2026 r/3DScanning "Has anyone tried Backflip AI yet?" thread body was
unreachable.

## 1. Backflip AI — the reference threat
Aug 4, 2026 CAD Copilot: mesh/STL/scan → parametric CAD with feature
trees by chaining extrude/revolve/pattern/fillet. Fast Mode (~2 min, 4
variants, "results can vary wildly"), Thinking Mode (1 model, agentic
self-verification). Web app exports STEP; Fusion add-in Aug 19
(official Autodesk blog); Onshape "in a handful of weeks"; SOLIDWORKS
later 2026 — Dassault turned down the 2025 plugin and is building its
own. CEO Greg Mark on the 16-month delay: "The first model wasn't good,
so we didn't ship it."
Pricing: Free 60 credits; Builder $20/mo (100); Pro $50 (300);
Business $380 (2,500); Fast 10 cr, Thinking 50; credits don't roll
over; $1.52–$10/job (engineering.com). Claim "$1,500 → $10/part."
Accuracy: engineering.com hands-on — toaster-oven knob: all 5 outputs
"not without error" (missed notch; thin wall caught only by Thinking);
"any experienced CAD user could do it in a few minutes"; Adaptor Ring:
Fast failed 4/4, Thinking "flawless as far as I could tell BY EYE" — no
deviation metrics exist in the product. Mark: "We're at GPT-2 level
now. By the end of the year we expect GPT-4-level accuracy." Sweet
spot: moderate-complexity 3-axis milled/turned parts; an automotive
OEM digitizes "about half" of parts. Cloud-only; SOC 2 Type II
"targeted later in 2026"; no training opt-out for individual users.

## 2. Pro tools (verified 2026 prices)
- Geomagic Design X: Go $1,900/yr or $4,990 perpetual (promo $3,992);
  Plus +$2,090; Pro quote (~$20k class); "Design X without the price"
  threads endemic; ZEISS RE cited as cheaper alternative.
- QuickSurface: Lite €480/yr; Pro €1,700/yr or €5,250 perpetual (+10%
  maint.); QS for SOLIDWORKS €1,100/yr / €3,300; Personal €240/yr,
  non-commercial, STL export only. Trustpilot 4.7/5.
- Mesh2Surface: Rhino & SOLIDWORKS add-ins (same company).
- Shining3D EXModel: ~$495 Std/Pro; AI primitive detection,
  snap-to-mesh sketching, STEP/IGES.
All manual/semi-auto; none does automatic reconstruction.

## 3. Scanner-bundled software 2026
Revopoint: Revo Scan V1.0 (Feb 2026) mesh-out only; Revo Design $540 /
PRO $1,900 = white-labeled QuickSurface Lite (Mar 2025). Creality Scan:
AI mesh repair/denoise; Nov–Dec 2025 QuickSurface partnership (bundles,
~20% off). Shining3D: EXModel + Geomagic Essentials bundles (~$3,000).
No OEM app store/plugin ecosystem; integration via STL export or
white-label licensing.

## 4. Free/cheap workflows
Fusion mesh-to-BRep: prismatic simplified meshes only; decimate to
~0.1–0.2 or facet warnings; organic scans → unusable. Consensus: "use
the scan as reference and remodel on top." FreeCAD: Reverse
Engineering WB rudimentary; Curves WB, cross-section lofting,
Detessellate macro suite; active RE-challenge threads to Mar 2026.
r/3DScanning canonical answer: "There is no single software that can do
that… you use the scan data to create a model." PartMapper: not found.

## 5. Other entrants 2025–26
Direct scan-to-CAD AI competitors: none shipping. Adjacent open
research: Point2CAD, CAD-Recode (neither productized). Text-to-CAD:
Adam/CADAM (YC W25, open-source), Zoo Zookeeper, TexoCAD, Nurb — "Ask
HN: Is Text-to-CAD BS?" skepticism. 2D drawing-to-CAD: Ragnar, Prompt2CAD,
AI3DCAD (young). Dassault's own mesh-to-CAD AI looming (SOLIDWORKS
2026 ships Mistral-based Aura/Leo/Marie). Inspection (Control X, GOM,
Revo Measure) separate market.

## 6. Gap statement
Market splits into pro manual (€480–$20k), OEM mesh cleanup (free, stops
at STL), free manual remodeling (hours), and one AI player (cloud-only,
credit-metered, no accuracy guarantees, no training opt-out, plugins
only for paid CAD). Nobody offers: (1) local-first AI reconstruction
(CAD-Recode shows 1.5B suffices); (2) honest accuracy reporting /
per-feature deviation maps; (3) FreeCAD as first-class target; (4)
per-scanner noise models for hobby hardware; (5) flat hobbyist pricing
without QuickSurface Personal's STL-only trap.

Sources: backflip.ai/pricing, backflip.ai/blog, engineering.com
("Backflip's back: is the mesh-to-CAD AI real this time?"), Develop3D,
VoxelMatters, 3DPI, quicksurface.com/price, QS Personal page,
Creality×QS page, GoMeasure3D Design X shop, shining3d.com EXModel,
Trustpilot QS, Point2CAD, CAD-Recode, DesignWeaver3D/Detessellate,
Autodesk Fusion blog (Backflip add-in), r/3DScanning, r/FreeCAD,
r/Fusion360, r/Metrology snippets via search indexes.
