# 03 — Industrial / engineering-grade AI design layer (2026-09-01)

Method: 21 searches by a research agent. Purpose: who makes real CAD
with AI, and why mesh generators can't.

## Text-to-CAD / AI-native CAD startups
- Zoo (ex-KittyCAD, LA, $30M+, Sequoia): own geometry engine, KCL
  language, ML-ephant API, Design Studio. Text-to-CAD emits B-rep/STEP
  + editable KCL. Jan 2026 "Zookeeper" conversational CAD agent.
  Freemium (40 free min/mo, $0.50/min).
- Adam (adam.new, YC W25): $4.1M seed (TQ Ventures, Oct 31, 2025);
  1M+ models generated; parametric copilot, hobbyist/prototyping grade.
- Backflip AI: $30M Series A (a16z + NEA). Scan/mesh → editable
  parametric CAD with feature trees; claims $1,500 → $10 per part;
  SOLIDWORKS sidebar (later abandoned), Fusion add-in, web app; from
  $20/mo. Most credible mesh-to-B-rep productization.
- Leo AI: $9.7M seed; text/sketch/spec → DFMA-optimized assemblies;
  cites Scania, HP, Siemens.
- Spline (~$32M): design/web-visual, Meshy side of the divide.
- YC long tail: Camfer (S24), Draftaid, REV1 (2026, CAD → drawings).

## Incumbents — what shipped
Autodesk: Project Bernini research-only; Fusion shipped Assistant,
drawing automation, ConstraintGen, toolpath automation. PTC/Onshape:
AI Advisor GA Oct 14, 2025 (advisory). Siemens NX: Design Copilot +
DFM Advisor (2025). Dassault: SOLIDWORKS 2026 with AURA + agents
"Marie"/"Leo". Pattern: copilots around the model, no generative B-rep
in production.

## Simulation-driven computational engineering (most funded)
- PhysicsX: ~$155M through Series B (Atomico, Siemens, Temasek), then
  $300M Series C at $2.4B (Temasek, Jun 2026). LGM-Aero trained on
  25M+ geometries; Simcenter X integration.
- Neural Concept: ~$100M Series C (2025); 70+ OEMs (Airbus, GE, Bosch,
  Subaru, ESA), 4 of 10 F1 teams.
- nTop: ~$133M total; implicit modeling; acquired cloudfluid Feb 2025.
- Leap71 (Dubai): Noyron — deterministic physics-driven computational
  model (not an LLM) — designed a hot-fired 3D-printed rocket engine
  (2024); Dec 2025 hot-fired two orbital-class 20 kN methalox engines
  (bell + aerospike) designed autonomously, spec-to-ignition <3 weeks;
  200 kN / 2,000 kN targeted 2026.
- Divergent (Czinger): $290M Series E (Sept 2025) at $2.3B; DAPS =
  generative design + metal AM + automated assembly; defense pivot
  (Lockheed, Raytheon, Triumph), revenue up 5x in 2025.

## The mesh-vs-B-rep gap
Meshes: no exact surfaces, no topology guarantees, no dimensions/
tolerances/GD&T, no feature history, not editable. B-rep: parametric
NURBS faces/edges/vertices + feature tree. B-rep→mesh trivial;
mesh→B-rep "nearly impossible" in general (CADExchanger). Direct B-rep
generation must get topology AND geometry jointly right.
Research: BrepGen, SolidGen, DTGBrepGen, HoLa, ComplexGen, BrepLLM,
B-repLer; Text2CAD (NeurIPS 2024, ~170K models on DeepCAD), CAD-Coder,
TOOLCAD, Text2CAD-Bench, HistCAD, ICML 2026 B-rep-grounded program
generation. Pragmatic winner: CODE GENERATION (LLM emits CadQuery/
build123d/OpenSCAD/KCL executed by a real kernel). Bottlenecks: data
(ABC has no construction sequences; DeepCAD/Fusion360 only
sketch-extrude; nothing industrial with GD&T); no model handles
tolerances/manufacturability/assembly. Text-to-simple-part real;
text-to-production-part unsolved.

## Market signals
Generative design 2026 estimates scattered ($1.5B–5.5B); AI in product
design ~$17.7B. Better signal: ~$1B+ raised by simulation/physics-AI
startups; two unicorns in 12 months (PhysicsX, Divergent); text-to-CAD
rounds still seed-sized ($4–10M).

Sources: TechCrunch (Adam), 3DPI (Zoo, Backflip), zoo.dev/research,
getleo.ai, leap71.com (Dec 11, 2025), PRNewswire (Divergent), TamRadar
(PhysicsX C), Siemens news, Digital Engineering (Neural Concept), nTop
blog, PTC news, Siemens NX news, 3ds.com (SOLIDWORKS 2026), Autodesk
news, arXiv 2409.17106 (Text2CAD), arXiv 2401.15563 (BrepGen),
CADExchanger blog, Business Research Company, YC (REV1).
