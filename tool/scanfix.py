#!/usr/bin/env python3
"""scanfix — skeleton interface layer: scan in, print-ready mesh + honest report out.

Pipeline: load -> analyze -> repair -> export -> report
Each stage is deliberately minimal (v0 skeleton); the structure is the point.

Usage:
    python scanfix.py "scan.usdz" [-o outdir]
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np
import trimesh


# ---------------------------------------------------------------- load

def load_mesh(path: Path) -> trimesh.Trimesh:
    """Load a scan file. USDZ (Apple Object Capture) or anything trimesh reads."""
    if path.suffix.lower() == ".usdz":
        return _load_usdz(path)
    mesh = trimesh.load(path, force="mesh")
    return mesh


def _load_usdz(path: Path) -> trimesh.Trimesh:
    from pxr import Usd, UsdGeom  # usd-core

    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(path) as z:
            z.extractall(td)
        usdc = next(Path(td).rglob("*.usd*"))
        stage = Usd.Stage.Open(str(usdc))

        meters_per_unit = UsdGeom.GetStageMetersPerUnit(stage) or 1.0
        parts = []
        for prim in stage.Traverse():
            if prim.IsA(UsdGeom.Mesh):
                geom = UsdGeom.Mesh(prim)
                pts = np.array(geom.GetPointsAttr().Get(), dtype=np.float64)
                counts = np.array(geom.GetFaceVertexCountsAttr().Get())
                idx = np.array(geom.GetFaceVertexIndicesAttr().Get())
                xf = np.array(
                    UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(
                        Usd.TimeCode.Default()
                    )
                )
                pts = pts @ xf[:3, :3] + xf[3, :3]
                parts.append(trimesh.Trimesh(pts, _triangulate(counts, idx)))

    mesh = trimesh.util.concatenate(parts) if len(parts) > 1 else parts[0]
    mesh.apply_scale(meters_per_unit * 1000.0)  # -> millimetres
    return mesh


def _triangulate(counts: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """Fan-triangulate mixed polygon faces."""
    faces, i = [], 0
    for c in counts:
        for k in range(1, c - 1):
            faces.append((idx[i], idx[i + k], idx[i + k + 1]))
        i += c
    return np.array(faces)


# ---------------------------------------------------------------- analyze

@dataclass
class MeshReport:
    vertices: int = 0
    faces: int = 0
    components: int = 0
    watertight: bool = False
    boundary_edges: int = 0
    bbox_mm: list[float] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def analyze(mesh: trimesh.Trimesh) -> MeshReport:
    r = MeshReport(
        vertices=len(mesh.vertices),
        faces=len(mesh.faces),
        components=mesh.body_count,
        watertight=mesh.is_watertight,
        boundary_edges=int((trimesh.grouping.group_rows(
            mesh.edges_sorted, require_count=1)).shape[0]),
        bbox_mm=[round(float(x), 2) for x in mesh.extents],
    )
    if not r.watertight:
        r.notes.append(f"not watertight ({r.boundary_edges} boundary edges) — not printable as-is")
    if r.components > 1:
        r.notes.append(f"{r.components} disconnected pieces — floaters likely")
    if max(mesh.extents) < 5:
        r.notes.append("object smaller than 5mm — units may be wrong")
    return r


# ---------------------------------------------------------------- repair (skeleton)

def repair(mesh: trimesh.Trimesh) -> tuple[trimesh.Trimesh, list[str]]:
    """Minimal v0 repair: drop floaters, merge/clean, fill what trimesh can."""
    actions = []

    bodies = mesh.split(only_watertight=False)
    if len(bodies) > 1:
        keep = max(bodies, key=lambda b: len(b.faces))
        dropped = len(bodies) - 1
        mesh = keep
        actions.append(f"kept largest component, dropped {dropped} floater(s)")

    before = len(mesh.faces)
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.merge_vertices()
    if len(mesh.faces) != before:
        actions.append(f"removed {before - len(mesh.faces)} degenerate faces")

    if not mesh.is_watertight:
        trimesh.repair.fill_holes(mesh)
        actions.append(
            "filled small holes (trimesh) — "
            + ("now watertight" if mesh.is_watertight
               else "LARGE OPENINGS REMAIN (open bottom?) — needs v1 hole closing")
        )

    trimesh.repair.fix_normals(mesh)
    actions.append("normals unified")
    return mesh, actions


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--outdir", type=Path, default=None)
    args = ap.parse_args()

    outdir = args.outdir or args.input.parent / "scanfix_out"
    outdir.mkdir(parents=True, exist_ok=True)
    stem = args.input.stem.replace(" ", "_")

    print(f"[load]    {args.input.name}")
    mesh = load_mesh(args.input)

    print("[analyze] before:")
    before = analyze(mesh)
    for line in json.dumps(asdict(before), indent=2).splitlines():
        print("   " + line)

    print("[repair]")
    mesh, actions = repair(mesh)
    for a in actions:
        print(f"   - {a}")

    after = analyze(mesh)
    print(f"[analyze] after: watertight={after.watertight} "
          f"faces={after.faces} boundary_edges={after.boundary_edges}")

    stl_path = outdir / f"{stem}_print.stl"
    mesh.export(stl_path)
    report = {
        "input": str(args.input),
        "before": asdict(before),
        "repair_actions": actions,
        "after": asdict(after),
        "printable": after.watertight,
        "output_stl_mm": str(stl_path),
    }
    report_path = outdir / f"{stem}_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"[export]  {stl_path.name} ({stl_path.stat().st_size // 1024} KB)")
    print(f"[report]  {report_path.name}  printable={report['printable']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
