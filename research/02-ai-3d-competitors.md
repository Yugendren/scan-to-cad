# 02 — AI 3D asset generation competitors (2026-09-01)

Method: 21 searches by a research agent. Purpose: is anything as good
as or better than Meshy?

## Market frame
Generative-AI 3D asset market ≈$3.23B (2026) → $9.4B (2030, ~31% CAGR).
Meshy: ~$400M Series B at $1.5B, 12M+ users, 100M+ models, ARR ~12x YoY.

## Commercial rivals
- Tripo AI (VAST, Beijing): Tripo 3.0 (Sept 2025) ~20x params, Ultra
  mode 2M polys; H3.1 + Smart Mesh P1.0 (Mar 2026) — clean quad
  low-poly in ~2s vs 5–8 min Meshy retopo, ~15 min Rodin. Funding $50M
  A (Mar 2026, Alibaba/Baidu Ventures) + ~$150M (Jun–Jul 2026) ≈ $200M,
  unicorn. 10M users, 90K studio/API clients, NetEase, Sony; ~$7M ARR
  Sept 2025. Pro $19.90/mo (3,000 credits).
- Rodin / Hyper3D (Deemos, Shanghai): Gen-2 (SIGGRAPH 2025 Best Paper;
  full launch Oct 1, 2025): 10B params, 4x geometric quality, part-based
  generation; Gen-2 Edit (Mar 31, 2026) first dedicated 3D editing
  platform. Funding: Angel+ (Nov 2025) + hundreds of millions RMB.
  Tens of $M ARR, ~80% overseas. Slowest (~15 min), best photorealism.
- Hitem3D / Hi3D (Sparc3D paper, May 2025; 1536³; Chamfer ~0.002 on
  ShapeNet/Objaverse): launched Jun–Jul 2025 amid open-source-promise
  controversy; $19.90–129.90/mo.
- ByteDance Seed3D 2.0 (Apr 2026): blind tests (60 raters with 3D
  background) beat Hunyuan3D-2.5/3.1, Tripo 3.0, Rodin Gen2 v1.9,
  HiTem v2.0 at 69.0–89.9% win rates. API on Volcano Engine.
- Exits/pivots: Luma Genie dead (video pivot); CSM shut Cube Jan 5,
  2026, acquired by Google; Kaedim = human-in-the-loop services;
  Sloyd ($3.26M, 2024) parametric/print niche; Alpha3D minor; 3D AI
  Studio/Neural4D wrappers; Spline AI, Krea 3D convenience plays.

## Big-tech / open
- Tencent Hunyuan3D: 2.6M+ HF downloads; 2.0 (Jan 2025), 2.1 (Jun
  2025, open weights+training), Omni (Sept 2025, ControlNet-of-3D),
  3.0 (Sept 2025, 1536³) and 3.1 (Nov 2025) proprietary; Hunyuan3D
  Studio paper (Sept 2025) end-to-end game-ready pipeline.
- Microsoft TRELLIS.2 (late 2025, MIT, 4B params): O-Voxel, full PBR,
  512³ in ~3s / 1536³ ~60s on H100. Best open model per 2026 roundups.
- Stability SF3D / SPAR3D (CES 2025): fast, below quality bar.
- Meta AssetGen 2.0 (May 2025): inside Horizon editor only.
- NVIDIA Edify 3D: licensing play, quiet. Hi3DGen, Direct3D-S2 threads.

## Head-to-head (2026 consensus)
Geometry SOTA: Seed3D 2.0 > Rodin Gen-2 ≈ Hunyuan3D 3.1 (closest chaser).
Topology for games: Tripo Smart Mesh, Meshy-6 (1,331-artist preference:
Meshy-6 over Tripo 3.1 at 63.8%, per Meshy). Textures/PBR: Meshy,
Hunyuan; TRELLIS.2 best open. No single winner.

## Category shortfalls
Animation topology (edge loops at joints fail; auto-rigs miss joints);
printability (~55% watertight out of the box; non-manifold, thin walls,
no units); hard-surface parts softened — dimensioned parts remain CAD
territory; UVs/LODs/style consistency weak; part-level editing nascent.

## Ranking vs Meshy
Better quality: Seed3D 2.0. Peer/better in niches: Rodin Gen-2, Tripo
H3.1, Hunyuan3D 3.x. Close/self-hostable: TRELLIS.2, Hitem3D. Behind:
wrappers, Kaedim, Sloyd, Spline, Krea, Stability. Meshy = best-funded,
most complete workflow, no longer clearly best raw model.

Sources: PRNewswire (Meshy B), GlobeNewswire (Tripo), Yahoo Finance,
Barchart/Deemos, Yicai, arXiv 2605.13862 (Seed3D 2.0), VoxelMatters,
Hunyuan3D GitHub/papers, TRELLIS.2 pages, arXiv 2505.14521 (Sparc3D),
Vset3D, Stability, UploadVR, Cinevva, 3D AI Studio, Tripo blog, Meshy
blog, 3dprinting.com, Vectorealism, Neural4D, Crunchbase, CB Insights,
aibase, Scenario, Medium 2026 comparisons.
