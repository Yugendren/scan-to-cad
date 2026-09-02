#!/usr/bin/env python3
"""Prototype experiment: phone scan vs independent reference scans of the same object.

For the DualSense: load the Apple Object Capture scan and the downloaded reference
scans, decimate the heavy ones, align every reference to the phone scan (rigid ICP,
then ICP with scale to expose scale error), and report:
  - bounding boxes vs Sony's spec (160 x 106 x 66 mm sorted)
  - phone-vs-reference deviation (median / p95 / max) after rigid alignment
  - the scale factor that best fits each reference (phone scale error)
  - reference-vs-reference deviation (how much the references agree = consensus quality)
Outputs devset/reference/compare.json, compare.md, and per-pair deviation PNGs.
Single run; a couple of minutes on the Mac at most (decimation dominates).
"""

import json
import time
from pathlib import Path

import numpy as np
import trimesh

from scanfix.repair import decimate

root = Path(__file__).resolve().parents[1]
ref_dir = root / "devset" / "reference"
phone_path = root / "devset" / "inputs" / "dualsense_controller.usdz"
SPEC = np.array([160.0, 106.0, 66.0])  # Sony blog, sorted descending

from scanfix.io import load_mesh


def load(path: Path, target_faces=150_000) -> trimesh.Trimesh:
    m, _ = load_mesh(path)
    m = max(m.split(only_watertight=False), key=lambda b: len(b.faces)) if m.body_count > 1 else m
    if len(m.faces) > target_faces:
        m, _ = decimate(m, target_faces)
    return m


def bbox_vs_spec(m):
    ext = np.sort(m.extents)[::-1]
    return ext.round(2).tolist(), (ext - SPEC).round(2).tolist()


def deviation(a: trimesh.Trimesh, b: trimesh.Trimesh, n=20000, seed=0):
    """Distance from points on a to surface b (mm)."""
    pts, _ = trimesh.sample.sample_surface(a, n, seed=seed)
    _, d, _ = trimesh.proximity.closest_point(b, pts)
    d = np.asarray(d)
    return pts, d


def summarize(d):
    return {"median_mm": round(float(np.median(d)), 3), "p95_mm": round(float(np.percentile(d, 95)), 3),
            "max_mm": round(float(d.max()), 3), "frac_over_0p5mm": round(float((d > 0.5).mean()), 3),
            "frac_over_1mm": round(float((d > 1.0).mean()), 3)}


def align(moving: trimesh.Trimesh, fixed: trimesh.Trimesh, scale: bool):
    T, cost = trimesh.registration.mesh_other(moving, fixed, samples=1500, scale=scale,
                                              icp_first=10, icp_final=60)
    out = moving.copy(); out.apply_transform(T)
    s = float(np.cbrt(abs(np.linalg.det(T[:3, :3]))))
    return out, T, cost, s


def heatmap_png(pts, d, path: Path, title: str, vmax=2.0):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (i, j, lab) in zip(axes, [(0, 1, "top (XY)"), (0, 2, "front (XZ)"), (1, 2, "side (YZ)")]):
        sc = ax.scatter(pts[:, i], pts[:, j], c=np.clip(d, 0, vmax), s=1, cmap="viridis", vmin=0, vmax=vmax)
        ax.set_aspect("equal"); ax.set_title(lab); ax.set_xlabel("mm"); ax.set_ylabel("mm")
    fig.colorbar(sc, ax=axes, label="deviation mm (clipped)")
    fig.suptitle(title)
    fig.savefig(path, dpi=110, bbox_inches="tight"); plt.close(fig)


def main():
    t0 = time.time()
    phone = load(phone_path)
    refs = {
        "kabliga": ref_dir / "kabliga_ps5_scan.stl",
        "v3design": ref_dir / "v3design_dualsense_original.stl",
        "printables1508424": ref_dir / "printables1508424_dualsense_scan.3mf",
    }
    meshes = {k: load(p) for k, p in refs.items()}
    report = {"spec_sorted_mm": SPEC.tolist(), "phone": {}, "references": {}, "phone_vs_reference": {},
              "reference_vs_reference": {}, "notes": []}
    ext, err = bbox_vs_spec(phone)
    report["phone"] = {"faces": len(phone.faces), "bbox_sorted_mm": ext, "bbox_minus_spec_mm": err}
    for k, m in meshes.items():
        ext, err = bbox_vs_spec(m)
        report["references"][k] = {"faces": len(m.faces), "bbox_sorted_mm": ext, "bbox_minus_spec_mm": err,
                                   "watertight": bool(m.is_watertight)}

    # phone vs each reference: rigid alignment (no scale) → deviation; then with scale → scale factor
    aligned = {}
    for k, m in meshes.items():
        rig, T, cost, _ = align(m, phone, scale=False)
        pts, d = deviation(phone, rig)           # phone surface → reference
        pts_r, d_r = deviation(rig, phone)       # reference surface → phone
        _, Ts, cost_s, s = align(m, phone, scale=True)
        report["phone_vs_reference"][k] = {
            "rigid_icp_cost": round(float(cost), 4),
            "phone_to_ref": summarize(d), "ref_to_phone": summarize(d_r),
            "best_fit_scale_ref_to_phone": round(s, 4),
            "implied_phone_scale_error_pct": round((1 / s - 1) * 100, 2),
        }
        aligned[k] = rig
        heatmap_png(pts, d, ref_dir / f"dev_phone_vs_{k}.png", f"phone scan deviation vs {k} (rigid ICP)")

    # reference vs reference (consensus): align each to kabliga
    base = aligned["kabliga"]
    for k, m in aligned.items():
        if k == "kabliga":
            continue
        rig, T, cost, _ = align(m, base, scale=False)
        pts, d = deviation(base, rig)
        report["reference_vs_reference"][f"kabliga_vs_{k}"] = {"rigid_icp_cost": round(float(cost), 4), **summarize(d)}
        heatmap_png(pts, d, ref_dir / f"dev_kabliga_vs_{k}.png", f"reference agreement: kabliga vs {k}")
        rig.export(ref_dir / f"{k}_aligned_to_kabliga.stl")
    base.export(ref_dir / "kabliga_aligned_to_phone.stl")

    report["runtime_s"] = round(time.time() - t0, 1)
    (ref_dir / "compare.json").write_text(json.dumps(report, indent=2))
    lines = [f"# DualSense: phone scan vs reference scans ({report['runtime_s']} s)\n",
             f"Spec (sorted): {SPEC.tolist()} mm\n",
             f"Phone scan bbox: {report['phone']['bbox_sorted_mm']} (minus spec: {report['phone']['bbox_minus_spec_mm']})\n"]
    for k, r in report["references"].items():
        lines.append(f"- ref {k}: {r['faces']} faces, bbox {r['bbox_sorted_mm']} (minus spec {r['bbox_minus_spec_mm']}), watertight={r['watertight']}")
    lines.append("\n## Phone vs reference (rigid alignment, mm)")
    for k, r in report["phone_vs_reference"].items():
        p = r["phone_to_ref"]
        lines.append(f"- vs {k}: median {p['median_mm']}, p95 {p['p95_mm']}, max {p['max_mm']}, "
                     f">0.5mm {p['frac_over_0p5mm']*100:.0f}%, >1mm {p['frac_over_1mm']*100:.0f}%; "
                     f"best-fit scale {r['best_fit_scale_ref_to_phone']} → phone scale error {r['implied_phone_scale_error_pct']}%")
    lines.append("\n## Reference vs reference (consensus quality, mm)")
    for k, r in report["reference_vs_reference"].items():
        lines.append(f"- {k}: median {r['median_mm']}, p95 {r['p95_mm']}, max {r['max_mm']}, >0.5mm {r['frac_over_0p5mm']*100:.0f}%")
    (ref_dir / "compare.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
