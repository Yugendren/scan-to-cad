"""Minimal virtual scanner: known CAD mesh → scan-like corruption with structured artifacts.

Layers (each toggleable): multi-view raycast depth → per-ray depth noise → grazing-angle
dropout + random hole patches → per-view registration jitter → Poisson refusion (rounds
sharp edges, bridges gaps) → trim refused surface far from samples (leaves holes).
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
import trimesh

from .repair import poisson_remesh


@dataclass
class ScannerConfig:
    views: int = 14
    rays_per_view: int = 40000
    depth_noise_mm: float = 0.08
    grazing_dropout_deg: float = 70.0
    hole_patches: int = 3
    hole_radius_frac: float = 0.06
    registration_jitter_mm: float = 0.15
    registration_jitter_deg: float = 0.3
    poisson_depth: int = 8
    trim_distance_factor: float = 3.0
    seed: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def _fibonacci_sphere(n: int) -> np.ndarray:
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)], axis=1)


def virtual_scan(mesh: trimesh.Trimesh, cfg: ScannerConfig) -> tuple[trimesh.Trimesh, dict]:
    rng = np.random.default_rng(cfg.seed)
    center = mesh.bounding_box.centroid
    radius = float(np.linalg.norm(mesh.extents)) * 1.2
    dirs = _fibonacci_sphere(cfg.views)
    # skip views from directly below (object sits on a table): drop the lowest 20%
    dirs = dirs[dirs[:, 2] > -0.6]
    all_pts, all_nrm = [], []
    stats = {"views": int(len(dirs)), "hits": 0, "dropped_grazing": 0, "dropped_holes": 0}
    for d in dirs:
        eye = center + d * radius
        # random ray directions inside a cone toward the object
        u = rng.normal(size=(cfg.rays_per_view, 3))
        u /= np.linalg.norm(u, axis=1, keepdims=True)
        targets = center + u * (np.max(mesh.extents) * 0.55)
        rd = targets - eye
        rd /= np.linalg.norm(rd, axis=1, keepdims=True)
        locs, ray_ids, tri = mesh.ray.intersects_location(np.tile(eye, (len(rd), 1)), rd,
                                                          multiple_hits=False)
        if not len(ray_ids):
            continue
        n = mesh.face_normals[tri]
        view_dir = rd[ray_ids]
        cosang = np.abs((n * view_dir).sum(axis=1))
        keep = cosang > np.cos(np.radians(cfg.grazing_dropout_deg))
        stats["dropped_grazing"] += int((~keep).sum())
        locs, n, view_dir = locs[keep], n[keep], view_dir[keep]
        # depth noise along the ray, larger at grazing angles
        sigma = cfg.depth_noise_mm * (1 + (1 - cosang[keep]))
        locs = locs + view_dir * rng.normal(0, 1, len(locs))[:, None] * sigma[:, None]
        # registration jitter per view
        rot = trimesh.transformations.rotation_matrix(
            np.radians(rng.normal(0, cfg.registration_jitter_deg)), rng.normal(size=3))
        locs = trimesh.transform_points(locs, rot) + rng.normal(0, cfg.registration_jitter_mm, 3)
        n = trimesh.transform_points(n, rot, translate=False)
        all_pts.append(locs)
        all_nrm.append(n)
        stats["hits"] += int(len(locs))
    pts = np.vstack(all_pts)
    nrm = np.vstack(all_nrm)
    # hole patches: delete all points within a radius of a few random surface points
    r = cfg.hole_radius_frac * np.max(mesh.extents)
    for _ in range(cfg.hole_patches):
        c = pts[rng.integers(len(pts))]
        m = np.linalg.norm(pts - c, axis=1) > r
        stats["dropped_holes"] += int((~m).sum())
        pts, nrm = pts[m], nrm[m]
    # refuse into a surface (this is what rounds edges and bridges gaps)
    fused = poisson_remesh(pts, -nrm if False else nrm, depth=cfg.poisson_depth)
    # trim faces far from any sample (Poisson invents surface across holes)
    from scipy.spatial import cKDTree
    tree = cKDTree(pts)
    spacing = float(np.median(tree.query(pts[: 5000], k=2)[0][:, 1]))
    dist, _ = tree.query(fused.triangles_center)
    keep_faces = dist < cfg.trim_distance_factor * max(spacing, cfg.depth_noise_mm)
    fused.update_faces(keep_faces)
    fused.remove_unreferenced_vertices()
    stats.update({"points": int(len(pts)), "faces_out": int(len(fused.faces)),
                  "sample_spacing_mm": round(spacing, 4), "config": cfg.to_dict()})
    return fused, stats
