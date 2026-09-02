"""Loading and exporting meshes. USDZ (Apple Object Capture) plus anything trimesh reads."""

from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

import numpy as np
import trimesh

SUPPORTED = {".usdz", ".stl", ".obj", ".ply", ".3mf", ".glb", ".gltf", ".off"}


def load_mesh(path: Path) -> tuple[trimesh.Trimesh, list[str]]:
    """Return (mesh in millimetres, notes). Multi-body files are concatenated."""
    notes: list[str] = []
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError(f"unsupported input type {suffix}; supported: {sorted(SUPPORTED)}")

    if suffix == ".usdz":
        mesh, mpu = _load_usdz(path)
        notes.append(f"USDZ metersPerUnit={mpu:g} → scaled to mm")
        return mesh, notes

    loaded = trimesh.load(path, force="mesh", process=False)
    if isinstance(loaded, trimesh.Scene):
        geoms = [g for g in loaded.dump() if isinstance(g, trimesh.Trimesh)]
        if not geoms:
            raise ValueError("no mesh geometry in file")
        loaded = trimesh.util.concatenate(geoms)
        notes.append(f"scene with {len(geoms)} geometries concatenated")
    mesh = trimesh.Trimesh(np.asarray(loaded.vertices, dtype=np.float64),
                           np.asarray(loaded.faces, dtype=np.int64), process=False)
    # STL stores every triangle with its own copies of the vertices; merging exact
    # duplicates is a format necessity, not a repair, so it happens at load.
    v0 = len(mesh.vertices)
    mesh.merge_vertices()
    if len(mesh.vertices) != v0:
        notes.append(f"merged {v0 - len(mesh.vertices)} duplicate vertices (file format stores unshared triangles)")

    # Units: STL/OBJ/PLY carry none. Assume mm; flag if implausible (checked in analyze).
    if suffix in {".glb", ".gltf"}:
        # glTF is metres by spec.
        mesh.apply_scale(1000.0)
        notes.append("glTF is metres by spec → scaled ×1000 to mm")
    return mesh, notes


def _load_usdz(path: Path) -> tuple[trimesh.Trimesh, float]:
    from pxr import Usd, UsdGeom  # usd-core

    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(path) as z:
            z.extractall(td)
        usd_files = sorted(Path(td).rglob("*.usd*"))
        if not usd_files:
            raise ValueError("no USD layer inside USDZ")
        stage = Usd.Stage.Open(str(usd_files[0]))
        mpu = UsdGeom.GetStageMetersPerUnit(stage) or 1.0
        parts = []
        for prim in stage.Traverse():
            if prim.IsA(UsdGeom.Mesh):
                geom = UsdGeom.Mesh(prim)
                pts = np.array(geom.GetPointsAttr().Get(), dtype=np.float64)
                counts = np.array(geom.GetFaceVertexCountsAttr().Get())
                idx = np.array(geom.GetFaceVertexIndicesAttr().Get())
                xf = np.array(UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(
                    Usd.TimeCode.Default()))
                pts = pts @ xf[:3, :3] + xf[3, :3]
                parts.append(trimesh.Trimesh(pts, _triangulate(counts, idx), process=False))
    if not parts:
        raise ValueError("USDZ contains no Mesh prims")
    mesh = trimesh.util.concatenate(parts) if len(parts) > 1 else parts[0]
    mesh.apply_scale(mpu * 1000.0)
    return mesh, mpu


def _triangulate(counts: np.ndarray, idx: np.ndarray) -> np.ndarray:
    faces, i = [], 0
    for c in counts:
        for k in range(1, int(c) - 1):
            faces.append((idx[i], idx[i + k], idx[i + k + 1]))
        i += int(c)
    return np.asarray(faces, dtype=np.int64)


def export_mesh(mesh: trimesh.Trimesh, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(path)
    return path
