"""Mesh statistics and the noise-envelope estimate used to gate every geometric decision."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

import numpy as np
import trimesh


@dataclass
class MeshStats:
    vertices: int
    faces: int
    components: int
    watertight: bool
    boundary_edges: int
    nonmanifold_edges: int
    bbox_mm: list[float]
    surface_area_mm2: float
    volume_mm3: float | None
    mean_edge_mm: float
    noise_envelope_mm: float
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def boundary_edge_count(mesh: trimesh.Trimesh) -> int:
    if len(mesh.faces) == 0:
        return 0
    groups = trimesh.grouping.group_rows(mesh.edges_sorted, require_count=1)
    return int(len(groups))


def nonmanifold_edge_count(mesh: trimesh.Trimesh) -> int:
    if len(mesh.faces) == 0:
        return 0
    _, counts = np.unique(mesh.edges_sorted, axis=0, return_counts=True)
    return int((counts > 2).sum())


def estimate_noise_envelope(mesh: trimesh.Trimesh, samples: int = 4000, k: int = 12,
                            seed: int = 0) -> float:
    """Local roughness: RMS distance of vertices from a plane fit to their k nearest
    neighbours, taken at the 95th percentile. Sharp edges inflate it slightly, so this
    is a conservative (larger) budget for flat-region snapping. Units: mm."""
    v = mesh.vertices
    if len(v) < k + 1:
        return 0.0
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(v), size=min(samples, len(v)), replace=False)
    from scipy.spatial import cKDTree
    tree = cKDTree(v)
    _, nn = tree.query(v[pick], k=k + 1)
    resid = np.empty(len(pick))
    for i, ids in enumerate(nn):
        p = v[ids]
        c = p.mean(axis=0)
        q = p - c
        # smallest singular vector = plane normal
        _, s, vt = np.linalg.svd(q, full_matrices=False)
        n = vt[-1]
        d = q @ n
        resid[i] = np.sqrt(np.mean(d * d))
    return float(np.percentile(resid, 95))


def analyze(mesh: trimesh.Trimesh) -> MeshStats:
    notes: list[str] = []
    watertight = bool(mesh.is_watertight) if len(mesh.faces) else False
    be = boundary_edge_count(mesh)
    nme = nonmanifold_edge_count(mesh)
    extents = [round(float(x), 3) for x in (mesh.extents if len(mesh.vertices) else [0, 0, 0])]
    vol = float(mesh.volume) if watertight else None
    edge_len = float(mesh.edges_unique_length.mean()) if len(mesh.faces) else 0.0
    noise = estimate_noise_envelope(mesh)

    if not watertight:
        notes.append(f"not watertight: {be} boundary edges — not printable as-is")
    if nme:
        notes.append(f"{nme} non-manifold edges")
    comps = mesh.body_count if len(mesh.faces) else 0
    if comps > 1:
        notes.append(f"{comps} disconnected pieces — floaters likely")
    mx = max(extents) if extents else 0
    if mx and mx < 5:
        notes.append(f"largest extent {mx} mm — suspiciously small; units may be metres/inches")
    if mx > 1000:
        notes.append(f"largest extent {mx} mm — suspiciously large; units may be wrong")

    return MeshStats(
        vertices=int(len(mesh.vertices)), faces=int(len(mesh.faces)), components=int(comps),
        watertight=watertight, boundary_edges=be, nonmanifold_edges=nme, bbox_mm=extents,
        surface_area_mm2=round(float(mesh.area), 2) if len(mesh.faces) else 0.0,
        volume_mm3=round(vol, 2) if vol is not None else None,
        mean_edge_mm=round(edge_len, 4), noise_envelope_mm=round(noise, 4), notes=notes,
    )
