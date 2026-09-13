# scan_to_cad (scanfix v1)

A local, deterministic pipeline that takes a 3D scan or any mesh and returns a restored model, a print-ready file, and an honest report.

Pipeline: load (USDZ, STL, OBJ, PLY, 3MF, glTF) → analyse → repair (floaters, holes, orientation, budget-gated smoothing, verified decimation) → idealise prismatic regions only where p95 deviation stays inside a stated budget → printability (wall thickness, thin regions, orientation) → deviation certificate → JSON and HTML report.

## Dev-set result (v1)

All seven recorded-truth parts came back watertight and printable, p95 deviation at or below 0.017 mm. Every idealisation accept or refusal is logged. See `V1_VERDICT.md`.

Read `METHOD.md` for the approach, `NOVELTY.md` for an adversarial comparison against existing tools (what is reused, adapted, or new), and `research/` for the survey notes. Work is on branch `goal/v1`.
