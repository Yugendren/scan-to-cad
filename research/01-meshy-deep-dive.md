# 01 — Meshy.ai deep dive (2026-09-01)

Method: 12 web searches + 2 page fetches by a research agent. Purpose:
understand the incumbent consumer AI-3D product and its customer
sentiment. Published in artifact "From Prompt to Matter".

## Product
Text-to-3D (prompts ≤800 chars) and image/multi-image-to-3D meshes with
PBR textures; standalone AI Texturing, Remesh (retopo), auto-rigging,
animation (600+ presets). Flagship Meshy-6 (GA Jan 18, 2026): meshes up
to ~600K faces, Low Poly Mode, quad retopo (~1M→5K faces), multi-color
3D-print output, industry-standard bone hierarchies. July 2026: Meshy
3D Agent (chat-driven modeling), Auto Split (printable parts), Smart
Topology, 8K textures. Formats: GLB, FBX, OBJ, STL, USDZ, 3MF. Print
path: watertightness/wall-thickness/non-manifold checks, Auto Repair,
base generation, vertex-color multicolor for Bambu AMS. REST API +
Python/Node SDKs, Blender/Unity/Unreal plugins.

Pricing (credits): Free 100/mo (CC-BY, low priority), Pro $20/mo
(1,000 credits, API), Premium $40, Studio $60, Ultra $100, Enterprise.
Full Meshy-6 generation ≈30 credits → free tier ≈3 generations/month.

## Company
Founded 2023 by Ethan (Yuanming) Hu (MIT graphics PhD, creator of
Taichi). ~128 employees. Series B announced Jul 21, 2026: ~$400M at
$1.5B valuation — largest AI-3D round to date (IDG, Matrix China,
Monolith; HongShan, GGV/Granite Asia, BAI, Source Code existing).
Prior funding ~$52M. Traction: 12M+ registered users, 100M+ models,
ARR ~12x YoY (one profile ≈$30M ARR).

## Customers
Games: Nexon, NetEase, 37 Interactive. 3D printing: Bambu Lab,
Creality, Elegoo, FlashForge, xTool. Also Hugo Boss, Sweden's national
museum of art and design. Mar 2026: engine embedded in Bambu's
MakerWorld (MakerLab). Dominant use: indie/mobile game prototyping,
3D-printing hobbyists (figurines/busts), XR/AR, e-commerce viz.

## Sentiment
G2 4.7/5 (400+); Trustpilot 4.7/5 (3,468) but an earlier snapshot was
~2.0/5 over ~120 — heavy solicitation likely.
Praise: speed, ease, remesh tool, Blender integration.
Complaints: topology "not clean or animation-friendly", triangle-heavy,
missing UVs; hands/fingers/faces merge; details "painted rather than
represented in geometry"; hard-surface failure ("couldn't do a cylinder
properly"); credit anger ("nickel and dime you for every single
change"; 90%→40% accuracy on change requests burning 3,000 credits;
failed generations still charged); refunds refused; expectation gap vs
promo videos. Consensus: most production-ready AI 3D tool, but all are
prototype/background-asset grade.

## Structural limits (why not engineering)
Outputs polygon meshes, not B-rep/parametric CAD: no dimensions,
tolerances, feature trees, GD&T, DFM. Statistical generation cannot
express "exactly 42mm bore". Printability is patched post-hoc. Competes
in aesthetic assets, not against SolidWorks/Fusion/Zoo.

Sources: prnewswire (Series B 7/21/26), techfundingnews, PitchBook
532823-68, meshy.ai/pricing, docs.meshy.ai, Trustpilot, G2, costbench,
Medium reviews (2026), 3dprintingindustry, rapiddirect, ResearchGate
385464484, itch.io forums.
