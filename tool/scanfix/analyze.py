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


def is_cad_like(mesh: trimesh.Trimesh, min_area_frac: float = 0.25) -> bool:
    """CAD-exported meshes have exactly coplanar adjacent triangles (flat faces made of
    a few large triangles). Scans essentially never do. If ≥ min_area_frac of the area
    lies in exactly-coplanar facets, treat the mesh as noise-free."""
    if len(mesh.faces) == 0:
        return False
    try:
        facets = mesh.facets  # groups of adjacent, exactly coplanar faces
    except Exception:
        return False
    if len(facets) == 0:
        return False
    area = sum(float(mesh.area_faces[f].sum()) for f in facets)
    return area / float(mesh.area) >= min_area_frac


def estimate_noise_envelope(mesh: trimesh.Trimesh, samples: int = 4000, k: int = 12,
                            seed: int = 0) -> float:
    """Typical local roughness: median over sampled vertices of the RMS distance of the
    k nearest neighbours from their best-fit plane. The median (not a high percentile)
    keeps sharp edges and curvature from masquerading as noise; CAD-like meshes are
    reported as 0. Units: mm."""
    if is_cad_like(mesh):
        return 0.0
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
        _, s, vt = np.linalg.svd(q, full_matrices=False)  # smallest singular vector = normal
        d = q @ vt[-1]
        resid[i] = np.sqrt(np.mean(d * d))
    return float(np.median(resid))


def analyze(mesh: trimesh.Trimesh) -> MeshStats:
    notes: list[str] = []
    watertight = bool(mesh.is_watertight) if len(mesh.faces) else False
    be = boundary_edge_count(mesh)
    nme = nonmanifold_edge_count(mesh)
    extents = [round(float(x), 3) for x in (mesh.extents if len(mesh.vertices) else [0, 0, 0])]
    vol = float(mesh.volume) if watertight else None
    edge_len = float(mesh.edges_unique_length.mean()) if len(mesh.faces) else 0.0
    noise = estimate_noise_envelope(mesh)
    if noise == 0.0 and len(mesh.faces) and is_cad_like(mesh):
        notes.append("CAD-like mesh (exactly coplanar facets) — treated as noise-free")

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
