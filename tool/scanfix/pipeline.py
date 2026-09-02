"""The v1 function: f(mesh_file) → restored, print, report."""

from __future__ import annotations

import datetime as dt
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import trimesh

from . import __version__
from .analyze import analyze
from .deviation import deviation
from .idealize import idealize
from .io import export_mesh, load_mesh
from .printability import suggest_orientation, thicken, wall_thickness
from .repair import clean, close_holes, decimate, orient, remove_floaters, smooth_taubin
from .report import write_html, write_json


@dataclass
class Options:
    nozzle: float = 0.4
    min_wall: float = 0.8
    snap_budget: float = 0.15
    idealize: bool = True
    thicken_mm: float = 0.0
    mesh_class: str | None = None  # None = auto
    target_faces: int = 60000
    smooth_steps: int = 0  # 0 = auto (only if noise envelope is above budget/3)
    max_hole_edges: int = 5000


def classify(mesh: trimesh.Trimesh) -> tuple[str, str]:
    """Heuristic class: prismatic if a large fraction of area lies in near-planar
    face groups; organic if almost none. Returned with its evidence string."""
    from .idealize import grow_planar_regions
    regions = grow_planar_regions(mesh, angle_deg=6.0, min_faces=30)
    if not regions:
        return "organic", "no planar regions of ≥30 faces"
    total = float(mesh.area)
    planar = sum(float(mesh.area_faces[r].sum()) for r in regions)
    frac = planar / total if total else 0.0
    if frac >= 0.45:
        return "prismatic", f"{frac*100:.0f}% of area in planar regions"
    if frac >= 0.15:
        return "mixed", f"{frac*100:.0f}% of area in planar regions"
    return "organic", f"{frac*100:.0f}% of area in planar regions"


def run(input_path: Path, outdir: Path, opt: Options) -> dict:
    t0 = time.time()
    outdir.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem.replace(" ", "_")
    actions: list[dict] = []

    original, load_notes = load_mesh(input_path)
    before = analyze(original)
    before.notes = load_notes + before.notes

    mesh_class, class_src = (opt.mesh_class, "user flag") if opt.mesh_class else classify(original)

    # --- repair -------------------------------------------------------------
    mesh, a = remove_floaters(original); actions.append(a.to_dict())
    mesh, a = clean(mesh); actions.append(a.to_dict())
    mesh, a = close_holes(mesh, opt.max_hole_edges); actions.append(a.to_dict())
    mesh, a = orient(mesh); actions.append(a.to_dict())

    # smoothing: only when the surface is noisier than a third of the budget, and only
    # if the smoothed result stays inside the budget (otherwise reverted and logged).
    noise = before.noise_envelope_mm
    steps = opt.smooth_steps if opt.smooth_steps > 0 else (10 if noise > opt.snap_budget / 3 else 0)
    if steps:
        cand, a = smooth_taubin(mesh, steps=steps)
        dv = deviation(mesh, cand, opt.snap_budget, samples=3000)
        if dv.p95_mm <= opt.snap_budget:
            mesh = cand
            a.result = {"applied": True, "p95_dev_mm": dv.p95_mm, "max_dev_mm": dv.max_mm}
        else:
            a.result = {"applied": False, "reverted": True, "p95_dev_mm": dv.p95_mm,
                        "reason": "smoothing would exceed the deviation budget"}
        actions.append(a.to_dict())
    else:
        actions.append({"step": "smooth_taubin", "params": {},
                        "result": {"skipped": True, "reason": f"noise envelope {noise} mm ≤ budget/3"}})

    mesh, a = decimate(mesh, opt.target_faces); actions.append(a.to_dict())

    # --- idealize (prismatic only, deviation-gated) --------------------------
    mesh, ide = idealize(mesh, mesh_class, opt.snap_budget, enabled=opt.idealize)
    actions.append({"step": "idealize_planar_regions",
                    "params": {"enabled": opt.idealize, "budget_mm": opt.snap_budget, "class": mesh_class},
                    "result": {"accepted": ide.accepted, "refused": ide.refused}})

    restored = mesh
    restored_path = export_mesh(restored, outdir / f"{stem}_restored.stl")

    # --- print file ----------------------------------------------------------
    print_mesh = restored.copy()
    if opt.thicken_mm > 0:
        print_mesh, info = thicken(print_mesh, opt.thicken_mm)
        actions.append({"step": "thicken", "params": {"offset_mm": opt.thicken_mm}, "result": info})
    print_mesh, a = orient(print_mesh); actions.append(a.to_dict())
    print_path = export_mesh(print_mesh, outdir / f"{stem}_print.stl")
    print_3mf = export_mesh(print_mesh, outdir / f"{stem}_print.3mf")

    # --- certificates --------------------------------------------------------
    after = analyze(print_mesh)
    dev = deviation(original, restored, opt.snap_budget)
    th = wall_thickness(print_mesh, opt.nozzle, opt.min_wall)
    ori = suggest_orientation(print_mesh)

    reasons = []
    printable = True
    if not after.watertight:
        printable = False; reasons.append(f"not watertight ({after.boundary_edges} boundary edges)")
    if after.components > 1:
        reasons.append(f"{after.components} separate bodies (will print as separate pieces)")
    if th.below_min_wall_frac > 0.02:
        reasons.append(f"{th.below_min_wall_frac*100:.1f}% of surface thinner than {opt.min_wall} mm")
        if th.below_min_wall_frac > 0.15:
            printable = False
    if any("units" in n for n in before.notes):
        reasons.append("units uncertain — verify size before printing")
    verdict = {"printable": printable,
               "printable_reason": "; ".join(reasons) if reasons else
               "watertight, single body, walls above minimum on sampled surface",
               "restored_within_budget": dev.within_budget,
               "dimensions_mm": after.bbox_mm}

    report = {
        "version": __version__, "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "input": str(input_path), "input_name": input_path.name, "runtime_s": round(time.time() - t0, 2),
        "mesh_class": mesh_class, "class_source": class_src,
        "options": opt.__dict__,
        "outputs": {"restored_stl": str(restored_path), "print_stl": str(print_path), "print_3mf": str(print_3mf)},
        "before": before.to_dict(), "after": after.to_dict(), "actions": actions,
        "idealize": ide.to_dict(), "deviation": dev.to_dict(), "thickness": th.to_dict(),
        "orientation": ori.to_dict(), "verdict": verdict,
    }
    write_json(report, outdir / f"{stem}_report.json")
    write_html(report, outdir / f"{stem}_report.html")
    report["outputs"]["report_json"] = str(outdir / f"{stem}_report.json")
    report["outputs"]["report_html"] = str(outdir / f"{stem}_report.html")
    return report
