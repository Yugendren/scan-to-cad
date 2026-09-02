"""Idealization, prismatic class only: find near-planar regions and flatten a region
ONLY IF the post-flatten vertex deviation stays inside the deviation budget.

Every accept and every refusal is logged with numbers. Vertices shared between
regions (edges/corners) are never moved — conservative by design.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

import numpy as np
import trimesh


@dataclass
class RegionDecision:
    region_id: int
    faces: int
    area_mm2: float
    max_dev_mm: float
    p95_dev_mm: float
    budget_mm: float
    accepted: bool
    reason: str
    vertices_moved: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class IdealizeResult:
    enabled: bool
    mesh_class: str
    budget_mm: float
    regions_found: int
    accepted: int
    refused: int
    decisions: list[RegionDecision] = field(default_factory=list)
    note: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["decisions"] = [x.to_dict() for x in self.decisions]
        return d


def grow_planar_regions(mesh: trimesh.Trimesh, angle_deg: float = 6.0, min_faces: int = 30,
                        min_area_frac: float = 0.005):
    """Region growing over face adjacency: a face joins a region if its normal is within
    angle_deg of the region's running mean normal. A region is kept if it has at least
    min_faces faces OR at least min_area_frac of the total area — the area rule matters
    for clean CAD meshes, where a whole flat face can be two large triangles."""
    n = mesh.face_normals
    adj = mesh.face_adjacency
    nf = len(mesh.faces)
    neighbors = [[] for _ in range(nf)]
    for a, b in adj:
        neighbors[a].append(b)
        neighbors[b].append(a)
    cos_thr = np.cos(np.radians(angle_deg))
    label = -np.ones(nf, dtype=np.int64)
    regions = []
    total_area = float(mesh.area_faces.sum())
    # seed from largest faces first: flat areas have larger, more regular triangles
    order = np.argsort(-mesh.area_faces)
    for seed in order:
        if label[seed] != -1:
            continue
        rid = len(regions)
        members = [seed]
        label[seed] = rid
        mean = n[seed].copy()
        stack = [seed]
        while stack:
            f = stack.pop()
            for g in neighbors[f]:
                if label[g] != -1:
                    continue
                if n[g] @ mean >= cos_thr:
                    label[g] = rid
                    members.append(g)
                    stack.append(g)
                    mean = mean + (n[g] - mean) / len(members)
                    mean /= np.linalg.norm(mean)
        members = np.asarray(members)
        area = float(mesh.area_faces[members].sum())
        if len(members) >= min_faces or area >= min_area_frac * total_area:
            regions.append(members)
        else:
            label[members] = -2  # too small; leave unlabelled
    return regions


def fit_plane(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    c = points.mean(axis=0)
    _, _, vt = np.linalg.svd(points - c, full_matrices=False)
    return c, vt[-1]


def planar_area_fraction(mesh: trimesh.Trimesh, fit_tol_mm: float, angle_deg: float = 6.0,
                         min_faces: int = 30) -> tuple[float, int]:
    """Share of surface area in regions that are TRULY planar: grown by normal
    similarity, then kept only if the p95 residual of their vertices from a fitted
    plane is within fit_tol_mm. Curved strips that region growing happens to merge
    fail the residual test, so organic meshes score low. Returns (fraction, count)."""
    regions = grow_planar_regions(mesh, angle_deg=angle_deg, min_faces=min_faces)
    total = float(mesh.area)
    if not regions or total == 0:
        return 0.0, 0
    v = mesh.vertices
    planar_area, count = 0.0, 0
    for fr in regions:
        vids = np.unique(mesh.faces[fr].ravel())
        c, n = fit_plane(v[vids])
        d = np.abs((v[vids] - c) @ n)
        if np.percentile(d, 95) <= fit_tol_mm:
            planar_area += float(mesh.area_faces[fr].sum())
            count += 1
    return planar_area / total, count


def idealize(mesh: trimesh.Trimesh, mesh_class: str, budget_mm: float,
             enabled: bool = True, angle_deg: float = 6.0, min_faces: int = 30,
             min_area_frac: float = 0.005) -> tuple[trimesh.Trimesh, IdealizeResult]:
    if not enabled:
        return mesh, IdealizeResult(False, mesh_class, budget_mm, 0, 0, 0, note="disabled by flag")
    if mesh_class != "prismatic":
        return mesh, IdealizeResult(False, mesh_class, budget_mm, 0, 0, 0,
                                    note=f"class '{mesh_class}': organic/mixed surfaces are never snapped")

    regions = grow_planar_regions(mesh, angle_deg=angle_deg, min_faces=min_faces)
    total_area = float(mesh.area)
    v = mesh.vertices.copy()
    faces = mesh.faces
    # a vertex is "interior" to a region if every incident face belongs to that region
    face_region = -np.ones(len(faces), dtype=np.int64)
    for rid, fr in enumerate(regions):
        face_region[fr] = rid
    vert_regions: list[set] = [set() for _ in range(len(v))]
    for fi, f in enumerate(faces):
        for vi in f:
            vert_regions[vi].add(int(face_region[fi]))

    decisions: list[RegionDecision] = []
    accepted = 0
    for rid, fr in enumerate(regions):
        area = float(mesh.area_faces[fr].sum())
        if area < min_area_frac * total_area:
            continue
        vids = np.unique(faces[fr].ravel())
        c, nrm = fit_plane(v[vids])
        d = (v[vids] - c) @ nrm
        max_dev, p95 = float(np.abs(d).max()), float(np.percentile(np.abs(d), 95))
        interior = np.array([vi for vi in vids if vert_regions[vi] == {rid}], dtype=np.int64)
        if p95 <= budget_mm and max_dev <= 3 * budget_mm and len(interior) > 0:
            v[interior] -= np.outer((v[interior] - c) @ nrm, nrm)
            accepted += 1
            decisions.append(RegionDecision(rid, len(fr), round(area, 2), round(max_dev, 4),
                                            round(p95, 4), budget_mm, True,
                                            "p95 within budget and max within 3× budget",
                                            int(len(interior))))
        else:
            why = ("p95 deviation exceeds budget" if p95 > budget_mm else
                   "max deviation exceeds 3× budget" if max_dev > 3 * budget_mm else
                   "no interior vertices to move")
            decisions.append(RegionDecision(rid, len(fr), round(area, 2), round(max_dev, 4),
                                            round(p95, 4), budget_mm, False, why))

    out = trimesh.Trimesh(v, faces, process=False)
    res = IdealizeResult(True, mesh_class, budget_mm, len(decisions), accepted,
                         len(decisions) - accepted, decisions,
                         note="only vertices fully interior to an accepted region are moved; "
                              "edges and corners are left in place")
    return out, res
