"""Printability: wall thickness by inward ray casting, orientation suggestion, explicit
(logged) thickening. Never changes geometry unless the caller asked for --thicken."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

import numpy as np
import trimesh


@dataclass
class ThicknessReport:
    samples: int
    min_mm: float
    p05_mm: float
    median_mm: float
    below_min_wall_frac: float
    below_nozzle2x_frac: float
    min_wall_mm: float
    nozzle2x_mm: float
    thin_region_count: int
    thin_regions: list[dict] = field(default_factory=list)
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OrientationReport:
    suggested: str
    rotation_deg: list[float]
    overhang_area_frac: float
    base_contact_area_mm2: float
    candidates: list[dict] = field(default_factory=list)
    reasoning: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def wall_thickness(mesh: trimesh.Trimesh, nozzle: float, min_wall: float,
                   samples: int = 3000, seed: int = 0) -> ThicknessReport:
    """Cast a ray inward from sampled surface points; distance to the next surface hit
    is the local thickness. Sampling-based: a min over 3000 samples is an estimate."""
    if not len(mesh.faces):
        return ThicknessReport(0, 0, 0, 0, 0, 0, min_wall, 2 * nozzle, 0, "empty mesh")
    rng = np.random.default_rng(seed)
    pts, fidx = trimesh.sample.sample_surface(mesh, samples, seed=seed)
    normals = mesh.face_normals[fidx]
    # nudge inside to avoid self-hit, cast along -normal
    origins = pts - normals * 1e-3
    dirs = -normals
    intersector = mesh.ray
    locs, ray_ids, tri_ids = intersector.intersects_location(origins, dirs, multiple_hits=True)
    thick = np.full(samples, np.nan)
    if len(ray_ids):
        d = np.linalg.norm(locs - origins[ray_ids], axis=1)
        # At a sharp corner the inward ray immediately hits the neighbouring face; that is
        # not a wall. Skip hits on faces sharing a vertex with the sample's own face.
        src_faces = mesh.faces[fidx[ray_ids]]
        hit_faces = mesh.faces[tri_ids]
        shares = np.array([len(set(a) & set(b)) > 0 for a, b in zip(src_faces, hit_faces)])
        d = d[~shares]; ray_ids = ray_ids[~shares]
        order = np.lexsort((d, ray_ids))  # first (nearest) genuine hit per ray
        ray_ids, d = ray_ids[order], d[order]
        first = np.concatenate(([True], ray_ids[1:] != ray_ids[:-1]))
        thick[ray_ids[first]] = d[first]
    valid = thick[~np.isnan(thick)]
    if len(valid) == 0:
        return ThicknessReport(samples, 0, 0, 0, 0, 0, min_wall, 2 * nozzle, 0,
                               "no inward hits — mesh may be open or single-sided")
    # ignore hits that are far larger than the object (ray escaped through a hole)
    valid = valid[valid <= np.max(mesh.extents)]
    n2 = 2 * nozzle
    below_min = float((valid < min_wall).mean())
    below_n2 = float((valid < n2).mean())
    # thin regions: cluster thin sample points spatially and report where they are
    mask = (~np.isnan(thick)) & (thick < max(min_wall, n2))
    thin_pts = pts[mask]
    thin_val = thick[mask]
    regions, where = 0, []
    if len(thin_pts):
        from scipy.cluster.hierarchy import fcluster, linkage
        sub, subv = thin_pts[:1500], thin_val[:1500]
        if len(sub) > 1:
            labels = fcluster(linkage(sub, method="single"), t=max(mesh.extents) * 0.05, criterion="distance")
        else:
            labels = np.ones(1, dtype=int)
        regions = int(labels.max())
        for lab in np.unique(labels):
            m = labels == lab
            where.append({"center_mm": [round(float(x), 1) for x in sub[m].mean(axis=0)],
                          "samples": int(m.sum()), "min_mm": round(float(subv[m].min()), 3)})
        where.sort(key=lambda r: -r["samples"])
    return ThicknessReport(
        samples=samples, min_mm=round(float(valid.min()), 3),
        p05_mm=round(float(np.percentile(valid, 5)), 3),
        median_mm=round(float(np.median(valid)), 3),
        below_min_wall_frac=round(below_min, 4), below_nozzle2x_frac=round(below_n2, 4),
        min_wall_mm=min_wall, nozzle2x_mm=n2, thin_region_count=regions, thin_regions=where[:10],
        note="sampling-based estimate (3000 inward rays); flags are fractions of surface samples; "
             "thin_regions lists where the thin samples cluster (largest first)")


def suggest_orientation(mesh: trimesh.Trimesh, overhang_deg: float = 45.0) -> OrientationReport:
    """Try the six axis-aligned 'down' directions; score = overhang area (faces facing
    down steeper than overhang_deg) minus a small bonus for base contact area."""
    cands = {
        "+Z up (as-is)": np.array([0, 0, 1.0]), "-Z up (flip)": np.array([0, 0, -1.0]),
        "+X up": np.array([1.0, 0, 0]), "-X up": np.array([-1.0, 0, 0]),
        "+Y up": np.array([0, 1.0, 0]), "-Y up": np.array([0, -1.0, 0]),
    }
    n = mesh.face_normals
    a = mesh.area_faces
    total = float(a.sum())
    cos_thr = np.cos(np.radians(90 - overhang_deg))  # normal pointing down more than 45° from horizontal
    rows = []
    for name, up in cands.items():
        down = -up
        facing_down = n @ down  # 1 = straight down
        overhang = float(a[facing_down > cos_thr].sum())
        # base contact: faces nearly straight down within 1% of extent from the lowest point
        heights = mesh.triangles_center @ up
        lowest = heights.min()
        base = float(a[(facing_down > 0.98) & (heights < lowest + 0.01 * np.ptp(heights))].sum())
        rows.append({"orientation": name, "up": up.tolist(), "overhang_area_frac": overhang / total,
                     "base_contact_mm2": base})
    best = min(rows, key=lambda r: r["overhang_area_frac"] - 0.05 * (r["base_contact_mm2"] / total))
    up = np.array(best["up"])
    # rotation that maps chosen 'up' to +Z, expressed as Euler for the report
    rot = trimesh.geometry.align_vectors(up, [0, 0, 1.0])
    euler = trimesh.transformations.euler_from_matrix(rot)
    return OrientationReport(
        suggested=best["orientation"], rotation_deg=[round(float(np.degrees(e)), 1) for e in euler],
        overhang_area_frac=round(best["overhang_area_frac"], 4),
        base_contact_area_mm2=round(best["base_contact_mm2"], 2),
        candidates=[{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in rows],
        reasoning=f"minimum overhang area (>{overhang_deg:g}° from vertical) among six axis-aligned "
                  f"orientations, with a small bonus for flat base contact; supports may still be needed")


def thicken(mesh: trimesh.Trimesh, offset_mm: float) -> tuple[trimesh.Trimesh, dict]:
    """EXPERIMENTAL explicit thickening: move vertices outward along vertex normals.
    Correct only for gently curved shells; concave regions may self-intersect.
    Always logged; never applied unless the user passes --thicken."""
    v = mesh.vertices + mesh.vertex_normals * offset_mm
    out = trimesh.Trimesh(v, mesh.faces, process=False)
    return out, {"step": "thicken_vertex_normal_offset", "offset_mm": offset_mm,
                 "experimental": True, "watertight_after": bool(out.is_watertight),
                 "warning": "vertex-normal offset; may self-intersect in concave regions"}
