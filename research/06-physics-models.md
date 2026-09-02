# 06 — Physics / simulation AI stacks usable in 2026 (2026-09-01)

Method: 24 searches by a research agent. Purpose: which open physics
models a 1–2 person team can adopt for design discovery.

## Universal MLIPs (Matbench Discovery, Sept 2026)
Leaders: TECE-OAM-RRA-1.0 (F1 0.929), EquFlashV2 (0.929), EquiformerV3
+DeNS-OAM (0.931), GRACE-3L-OAM-L, PET-OAM-XL, eSEN-30M-OAM (0.925).
~18–20 meV/atom MAE; nearly all trained on OMat24/OAM recipe.
- MACE-MP-0 / MPA-0 (MIT): F1 0.852; CPU-capable; best ASE/LAMMPS docs.
- Orb-v3 (Apache-2.0, Apr 2025): F1 0.905, 25.5M params, 3–6x faster;
  best open speed/accuracy on consumer GPUs. OrbMol for molecules.
- Meta UMA (May 2025, arXiv 2506.23971): MoE on ~30B atoms; gated
  "FAIR Chemistry License" (registration, geo-restricted).
- MatterSim (Microsoft, MIT): F1 0.862; 0–5000 K, up to 10⁷ atm.
- NVIDIA ALCHEMI: NIM/serving layer, not open weights.
Caveat: direct-force models don't conserve energy in long MD.

## Generative materials
- MatterGen (Nature Feb 2025, MIT code+weights): only model with
  experimental validation (TaCr₂O₆, 169 vs 200 GPa). Pairs with
  MatterSim for screening.
- CrystaLLM (MIT license, GPT-2 over CIF); FlowMM→FlowLLM (Meta);
  CrystalFlow (Nat. Commun. 2025); benchmarks AtomBench/PhononBench/
  LeMaterial GenBench (2025–26).

## Neural PDE surrogates
- NVIDIA PhysicsNeMo (Apache-2.0): DoMINO, Transolver/++, FNO/GNN zoo,
  uncertainty estimation (25.08+). Needs own FEA/CFD data.
- PhysicsX LGM-Aero, Neural Concept: proprietary SaaS.
- For structural FEA/topology optimization, differentiable solvers
  beat surrogates until >10³ evaluations/day are needed.

## Differentiable simulation
- JAX-FEM (open): differentiable 3D FEM; ~10x commercial on GPU; up to
  9.4x over 24-core Abaqus at 3M DOF on H100. Best fit for
  metamaterial/compliant-mechanism design.
- NVIDIA Warp (Apache-2.0): differentiable Python→CUDA kernels.
- MuJoCo-MJX + Brax (Apache-2.0): 10–50x throughput; thousands of
  parallel envs; sim-to-real via mujoco_playground.
- Genesis: broad (rigid/MPM/SPH/FEM), differentiable only in MPM/Tool
  solvers; generative engine unreleased; treat speed claims cautiously.
- Taichi/DiffTaichi: maintenance slowed; Warp safer long-term.

## RL/evolutionary design precedents
MatterGen TaCr₂O₆; Deep-DRAM (Adv. Mater. 2024, ~90% target accuracy
after fabrication on printed metamaterials); PENN inverse design of TPU
adaptive structures (2025); spinodal metamaterial inverse design;
RoboMorph/RoboMoRe (2024–25); sim2real non-monotonic in morphological
complexity (2026). Benchmarks: EvoGym, EvoGymCM (2026). No mature
benchmark for 3D metamaterial/mechanism design discovery — a gap.

## Bottom line
(a) Mechanisms/metamaterials: JAX-FEM + MuJoCo-MJX/Brax + Warp; add
PhysicsNeMo surrogates later; validate with OpenFOAM/CalculiX + prints.
(b) Materials: MatterGen → MatterSim/Orb-v3 → MACE, all on an RTX 3060
with cloud A100 for fine-tuning; DFT-verify before synthesis.

Sources: matbench-discovery.materialsproject.org, arXiv 2506.23971,
facebook/UMA (HF), orb-models GitHub, Nature s41586-025-08628-5,
microsoft/mattergen, microsoft/mattersim, ACEsuit/mace, NVIDIA ALCHEMI,
CrystaLLM, FlowLLM (OpenReview), Nat. Commun. (CrystalFlow),
nvidia/physicsnemo, DoMINO docs, thuml/Transolver, PhysicsX newsroom,
deepmodeling/jax-fem, NVIDIA Warp, mujoco_playground, Genesis docs,
Adv. Mater. (Deep-DRAM), Virtual & Physical Prototyping (PENN),
EvoGym, arXiv 2604.08258 (EvoGymCM), Sci. Data (Melt-Pool-Kinetics).
