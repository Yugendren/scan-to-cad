"""Deviation certificate: how far did the restored surface move from the original?

Two directions, reported separately because they answer different questions:
- original → restored ("distortion"): sample the ORIGINAL surface (after floater
  removal), measure distance to the restored surface. This is the budgeted statistic:
  did we move surface that existed? New surface from hole closing cannot inflate it.
- restored → original ("added surface"): sample the RESTORED surface, measure distance
  to the original. Samples far from any original surface are new geometry (closed
  holes, bridged gaps). Reported as a fraction and as flagged regions, never hidden.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

import numpy as np
import trimesh


@dataclass
class DeviationReport:
    samples: int
    max_mm: float
    p95_mm: float
    mean_mm: float
    budget_mm: float
    within_budget: bool
    added_surface_frac: float
    added_surface_threshold_mm: float
    flagged_regions: list[dict] = field(default_factory=list)
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _clusters(points: np.ndarray, extent: float, cap: int = 1500):
    from scipy.cluster.hierarchy import fcluster, linkage
    sub = points[:cap]
    if len(sub) < 2:
        return sub, np.ones(len(sub), dtype=int)
    labels = fcluster(linkage(sub, method="single"), t=extent * 0.05, criterion="distance")
    return sub, labels


def deviation(original: trimesh.Trimesh, restored: trimesh.Trimesh, budget_mm: float,
              samples: int = 5000, seed: int = 0) -> DeviationReport:
    if not len(original.faces) or not len(restored.faces):
        return DeviationReport(0, 0, 0, 0, budget_mm, True, 0.0, 0.0, note="empty mesh")

    # distortion: original → restored
    pts_o, _ = trimesh.sample.sample_surface(original, samples, seed=seed)
    _, d_o, _ = trimesh.proximity.closest_point(restored, pts_o)
    d_o = np.asarray(d_o)

    # added surface: restored → original
    pts_r, _ = trimesh.sample.sample_surface(restored, samples, seed=seed + 1)
    _, d_r, _ = trimesh.proximity.closest_point(original, pts_r)
    d_r = np.asarray(d_r)
    thr = max(5 * budget_mm, 1.0)
    added = d_r > thr
    flagged = []
    if added.any():
        sub, labels = _clusters(pts_r[added], float(max(restored.extents)))
        dsub = d_r[added][: len(sub)]
        for lab in np.unique(labels):
            m = labels == lab
            flagged.append({"center_mm": [round(float(x), 2) for x in sub[m].mean(axis=0)],
                            "samples": int(m.sum()), "max_dev_mm": round(float(dsub[m].max()), 3),
                            "likely": "new surface (closed hole / bridged gap) — not present in the original"})

    return DeviationReport(
        samples=samples, max_mm=round(float(d_o.max()), 4), p95_mm=round(float(np.percentile(d_o, 95)), 4),
        mean_mm=round(float(d_o.mean()), 4), budget_mm=budget_mm,
        within_budget=bool(np.percentile(d_o, 95) <= budget_mm),
        added_surface_frac=round(float(added.mean()), 4), added_surface_threshold_mm=thr,
        flagged_regions=flagged,
        note="max/p95/mean = distance from the original surface (floaters removed) to the restored "
             "surface; added_surface_frac = share of the restored surface farther than the threshold "
             "from any original surface (new geometry), listed as flagged regions")
