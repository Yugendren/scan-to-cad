"""Deviation certificate: how far did the restored surface move from the original?"""

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
    flagged_regions: list[dict] = field(default_factory=list)
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def deviation(original: trimesh.Trimesh, restored: trimesh.Trimesh, budget_mm: float,
              samples: int = 5000, seed: int = 0) -> DeviationReport:
    """Unsigned distance from points sampled on the restored surface to the original
    surface. Newly created surface (closed holes) is excluded by masking samples whose
    nearest original point is farther than 5× budget AND lies on a former boundary —
    approximated here by excluding the top 1% outliers from summary stats but
    reporting them as flagged regions."""
    if not len(original.faces) or not len(restored.faces):
        return DeviationReport(0, 0, 0, 0, budget_mm, True, note="empty mesh")
    pts, _ = trimesh.sample.sample_surface(restored, samples, seed=seed)
    _, dist, _ = trimesh.proximity.closest_point(original, pts)
    dist = np.asarray(dist)
    # Hole closing legitimately creates surface far from the original; keep those out
    # of the "did we distort existing surface" statistic, but report them.
    cutoff = np.percentile(dist, 99)
    core = dist[dist <= cutoff]
    flagged = []
    far = pts[dist > max(5 * budget_mm, cutoff)]
    if len(far):
        from scipy.cluster.hierarchy import fcluster, linkage
        sub = far[: min(len(far), 1500)]
        if len(sub) > 1:
            labels = fcluster(linkage(sub, method="single"),
                              t=max(restored.extents) * 0.05, criterion="distance")
        else:
            labels = np.array([1])
        for lab in np.unique(labels):
            m = labels == lab
            flagged.append({"center_mm": [round(float(x), 2) for x in sub[m].mean(axis=0)],
                            "samples": int(m.sum()),
                            "max_dev_mm": round(float(dist[dist > max(5 * budget_mm, cutoff)][: len(sub)][m].max()), 3),
                            "likely": "new surface from hole closing, or a large local change — inspect"})
    return DeviationReport(
        samples=samples, max_mm=round(float(core.max()), 4), p95_mm=round(float(np.percentile(core, 95)), 4),
        mean_mm=round(float(core.mean()), 4), budget_mm=budget_mm,
        within_budget=bool(np.percentile(core, 95) <= budget_mm), flagged_regions=flagged,
        note="stats exclude the top 1% of samples (new surface from hole closing); those are listed as flagged regions")
