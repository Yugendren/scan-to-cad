# Research digest — scan-to-CAD (compiled 2026-09-02)

Dense summary of three research sweeps (technical, competitive, GTM).
Full narrative: the "Scan-to-CAD Dossier" artifact. Evidence caveat:
two sweeps hit search-quota limits and used direct fetches + prior
knowledge; YouTube sub counts and Kickstarter figures are
order-of-magnitude; hobbyist sentiment on Backflip's Aug-2026 release
is the thinnest area (one unindexed r/3DScanning thread — read manually).

## Technical: what to reuse, what to build, what to avoid

REUSE:
- CAD-Recode (github filaPro/cad-recode, ICCV'25): Qwen2-1.5B + point
  projector → executable CadQuery; weights v1/v1.5 on HuggingFace;
  trained on 1M procedural sequences (released); evaluated on CC3D
  scan-like data; CPU inference feasible. The v2 LLM lane starts here.
- build123d (Apache-2.0, active, OCP/OCCT, STEP export) — synthesis
  target. CadQuery↔build123d interop is trivial (same kernel).
- Open3D RaycastingScene + analytic depth noise + ScalableTSDFVolume =
  the virtual scanner (TSDF fusion reproduces the edge-rounding that
  kills reverse engineering). BlenSor is abandoned; don't use.
- trimesh (MIT) as glue; PyMeshLab fallback; avoid PyMesh entirely.
- CC3D / CC3D-PSE / CC3D-Ops (uni.lu, academic access): 50k virtual
  scan–CAD pairs — DEV data, not a substitute for our real gauntlet.
- Kernel-in-the-loop repair is literature-validated (CADReasoner:
  emit → execute → render → compare → fix). Build it from day one.

LICENSE LANDMINES:
- CGAL Shape_detection (efficient RANSAC + region growing) is GPL —
  fine for Gate 0 research, contaminating for a shipped product. Plan:
  research with CGAL, ship pyransac3d (MIT) or own implementation.
- Point2CAD is CC-BY-NC (research only) + PyMesh dependency; use as
  eval reference only.

BUILD (the empty lanes — our moat):
1. Intent solver: Langbein et al. 2004 ("consistent constraints for
   beautification") is the blueprint — hypothesize regularities, select
   maximal consistent subset (greedy-with-rollback beats MILP), then
   constrained least-squares. NOBODY has published a modern/learned
   version for solids; nobody rounds dimensions to standard series.
2. Real-scan benchmark with dimension-error metrics: does not exist
   publicly. Whoever ships it defines the leaderboard. (Academic
   metrics stop at Chamfer/F-score/validity — no dimension error, no
   constraint-recovery accuracy.)
3. Certificates: no academic or commercial system reports per-face
   deviation guarantees or refuses-to-snap decisions.

RISKS (mitigations already in GATES/GOAL_STATE):
- Segmentation under real noise (fillets, worn edges, fusion smoothing)
  → region growing over RANSAC; multi-hypothesis kept alive until the
  constraint solver disambiguates.
- Wrong snapping is worse than no snapping (89.7°→90° on a true 89.5°
  part) → constraint accepted only if post-solve deviation stays inside
  the characterized scanner noise envelope.
- OCCT boolean fragility on near-tangent intersections → repair loop.
- Prosumer scanner noise has NO canonical published model; vendor
  "0.02–0.05mm" claims vs 0.1–0.3mm real-world (registration drift,
  shiny-surface bias, fusion smoothing dominate). Characterizing our
  own scanner against gauge blocks is publishable AND feeds the
  certificate. Apple Silicon: classical pipeline fine; learned lanes
  need CUDA (3060/cloud) or CPU inference.

## Competitive: the gap, verified

- Backflip (only AI player): Aug 2026 CAD Copilot; $20–380/mo, credits
  expire, ~$1.5–10/job; cloud-only; no training opt-out for individual
  users; SOC2 only "targeted later in 2026". Independent hands-on
  (engineering.com): all five attempts on a knob "not without error";
  verified "by eye" — NO deviation metrics exist in the product. CEO:
  "We're at GPT-2 level now." Dassault refused their plugin and is
  building its own (SOLIDWORKS 2026 ships AI agents) — incumbent
  response is coming, aimed at pros.
- Pro tools are manual: Design X $1,900/yr–$20k-class; QuickSurface
  Lite €480/yr, Personal €240/yr but STL-export-only (defeats the
  purpose); Shining3D EXModel ~$495.
- OEMs don't build: Revopoint AND Creality both white-label/bundle
  QuickSurface. Proves OEMs license rather than build → our endgame
  partnership/exit path. No OEM app store; no gatekeeper either.
- Free workflows (Fusion mesh-to-BRep, FreeCAD Curves/Detessellate)
  break on real scans; canonical community answer is still "remodel by
  hand on top of the scan."
- Our five ownable gaps: (1) local-first (CAD-Recode proves 1.5B
  suffices — kills IP objection + credit anxiety), (2) honest accuracy
  reporting/deviation maps, (3) FreeCAD as first-class target (zero
  commercial tools serve it), (4) per-scanner noise models for
  Revopoint/Creality-class hardware, (5) flat hobbyist pricing in the
  empty band between free-manual and €480/yr.

## Competitive refresh (verified 2026-09-02, second sweep)

- Backflip: Fusion add-in shipped Aug 19 with official Autodesk
  co-marketing (Autodesk PARTNERS, doesn't build native — telling);
  Onshape add-in NOT shipped ("coming soon"); original SOLIDWORKS
  partnership abandoned entirely; headline economics now "$10/part,
  1–5 min"; free tier ≈ 6 fast jobs/mo is their funnel; "deployed with
  a top automotive manufacturer"; no funding news since launch.
- NEW ENTRANTS: none. Zero 2026 HN/press hits for scan-to-CAD AI
  startups. CAD-Recode/Point2CAD teams show no commercialization
  signals. The lane is still one-player.
- Text-to-CAD wave drifting to in-CAD agents: Adam shipped an AI agent
  that edits feature trees inside Fusion/Onshape (May 2026, open-
  sourced CADAM June 2026) — no mesh/scan input, but they normalize
  free AI-CAD tooling; an OSS mesh-to-parametric follower of that
  playbook is the plausible next threat. None exists today.
- Incumbents: Geomagic now belongs to HEXAGON (acquisition completed
  Apr 2025; Design X 2026.1 tiered Go/Plus/Pro) — drifting upmarket to
  metrology, not down. Dassault's only 2026 AI activity is token-based
  cloud AI billing docs; nothing shipped on mesh-to-CAD; no SW2027
  news. PTC/Onshape quiet. QuickSurface is the liveliest manual
  incumbent (Parasolid, 2026 subscription option, Personal edition,
  Creality/Revopoint OEM deals, "AI" marketing with no actual AI).
- Adjacent: Polycam no parametric export; Matter and Form THREE mesh-
  only; no slicer-ecosystem scan moves.
- Standing evidence gap: fresh Reddit/YouTube reaction to Backflip's
  CAD Copilot is unretrievable from agent environments — check
  manually before launch decisions.

## GTM: pricing, channels, sequencing

PRICING (three rails):
- Personal: $29–49 ONE-TIME local-first license (HueForge precedent:
  $24 lifetime works; maker communities are subscription-fatigued).
- Commercial: ~$20/mo or ~$200/yr (undercuts Shapr3D/Polycam; gates
  commercial use, batch, accuracy reports).
- Metered credits only for heavy cloud compute (Backflip's 10/50
  fast/thinking split is proven); Zoo-style API rail later; never
  charge failed jobs.

CHANNELS (ranked):
1. YouTube scanner reviewers — the #1 question in every scanner review
   is "can I get a usable model?"; accuracy-obsessed channels (My Tech
   Fun, CNC Kitchen, Uncle Jessy, Teaching Tech, Maker's Muse) are
   made for a deviation-report demo.
2. r/3DScanning (~60–80k) + weekly free "fix my scan" thread;
   r/functionalprint, r/Machinists, r/hobbycnc; scanner FB groups and
   Discords (post-purchase frustration lives there).
3. OEM Kickstarter bundle (Revopoint/3DMakerpro campaigns: 5–10k
   perfect-fit buyers per campaign; OEMs love launch differentiators).
4. Open-source FreeCAD companion plugin as funnel (FreeCAD addon
   manager has no payment rails and the community resents paywalled
   cores — free companion, paid app).
5. PH/HN: one-day amplifier only.

SEQUENCING: service-first — $79–199/part semi-automated reverse
engineering from day one (bureaus: $250–2,000). Validates payment,
funds development, and builds the messy-real-scan corpus (the
flywheel). Cap at ~20% time post-launch; convert repeat customers to
Commercial tier.

LAUNCH PLAYS:
1. "Accuracy Gauntlet" reviewer kit: free lifetime Pro + known-geometry
   part + the deviation report as the shareable artifact; embargoed
   simultaneous reviews; $29 launch price.
2. OEM Kickstarter piggyback (3 months free Pro for backers).
3. Open companion + paid core, launched with the story: "your noisy
   $500 scan, editable, locally, no subscription."

## The convergence

One asset serves three purposes: the real-scan benchmark + deviation
certificate is simultaneously (a) the scientific contribution (no such
benchmark exists), (b) the product differentiator (Backflip is judged
"by eye"), and (c) the marketing artifact (reviewer gauntlet kits).
Build it once, spend it three times.
