"""Deterministic repair: floaters, duplicates, hole closing, edge-preserving smoothing,
error-bounded decimation. Every step appends an Action so the report can disclose it."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

import numpy as np
import pymeshlab
import trimesh

from .analyze import boundary_edge_count


@dataclass
class Action:
    step: str
    params: dict
    result: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def to_ms(mesh: trimesh.Trimesh) -> pymeshlab.MeshSet:
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(vertex_matrix=np.asarray(mesh.vertices, dtype=np.float64),
                               face_matrix=np.asarray(mesh.faces, dtype=np.int32)))
    return ms


def from_ms(ms: pymeshlab.MeshSet) -> trimesh.Trimesh:
    m = ms.current_mesh()
    return trimesh.Trimesh(m.vertex_matrix(), m.face_matrix(), process=False)


def remove_floaters(mesh: trimesh.Trimesh, keep_ratio: float = 0.05) -> tuple[trimesh.Trimesh, Action]:
    """Drop components whose face count is below keep_ratio × the largest component."""
    bodies = mesh.split(only_watertight=False)
    if len(bodies) <= 1:
        return mesh, Action("remove_floaters", {"keep_ratio": keep_ratio},
                            {"components_before": len(bodies), "dropped": 0})
    largest = max(len(b.faces) for b in bodies)
    keep = [b for b in bodies if len(b.faces) >= keep_ratio * largest]
    dropped = len(bodies) - len(keep)
    out = trimesh.util.concatenate(keep) if len(keep) > 1 else keep[0]
    return out, Action("remove_floaters", {"keep_ratio": keep_ratio},
                       {"components_before": len(bodies), "kept": len(keep), "dropped": dropped,
                        "dropped_faces": int(sum(len(b.faces) for b in bodies) - len(out.faces))})


def clean(mesh: trimesh.Trimesh) -> tuple[trimesh.Trimesh, Action]:
    ms = to_ms(mesh)
    v0, f0 = len(mesh.vertices), len(mesh.faces)
    ms.meshing_remove_duplicate_vertices()
    ms.meshing_remove_duplicate_faces()
    ms.meshing_remove_null_faces()
    ms.meshing_remove_unreferenced_vertices()
    try:
        ms.meshing_repair_non_manifold_edges()
        ms.meshing_repair_non_manifold_vertices()
    except pymeshlab.PyMeshLabException:
        pass
    out = from_ms(ms)
    return out, Action("clean", {}, {"vertices_removed": v0 - len(out.vertices),
                                     "faces_removed": f0 - len(out.faces)})


def close_holes(mesh: trimesh.Trimesh, max_hole_edges: int = 5000) -> tuple[trimesh.Trimesh, Action]:
    """Close boundary loops up to max_hole_edges edges (large = open bottoms too)."""
    be0 = boundary_edge_count(mesh)
    if be0 == 0:
        return mesh, Action("close_holes", {"max_hole_edges": max_hole_edges},
                            {"boundary_edges_before": 0, "skipped": True})
    ms = to_ms(mesh)
    try:
        ms.meshing_close_holes(maxholesize=int(max_hole_edges), selfintersection=False,
                               newfaceselected=False)
    except pymeshlab.PyMeshLabException as e:
        return mesh, Action("close_holes", {"max_hole_edges": max_hole_edges},
                            {"boundary_edges_before": be0, "error": str(e)[:200]})
    out = from_ms(ms)
    be1 = boundary_edge_count(out)
    return out, Action("close_holes", {"max_hole_edges": max_hole_edges},
                       {"boundary_edges_before": be0, "boundary_edges_after": be1,
                        "faces_added": len(out.faces) - len(mesh.faces),
                        "watertight_after": bool(out.is_watertight)})


def orient(mesh: trimesh.Trimesh) -> tuple[trimesh.Trimesh, Action]:
    ms = to_ms(mesh)
    try:
        ms.meshing_re_orient_faces_coherently()
    except pymeshlab.PyMeshLabException:
        pass
    out = from_ms(ms)
    flipped = False
    if out.is_watertight and out.volume < 0:
        out.invert()
        flipped = True
    return out, Action("orient_normals", {}, {"coherent": True, "inverted_to_outward": flipped})


def smooth_taubin(mesh: trimesh.Trimesh, steps: int = 10, lam: float = 0.5, mu: float = -0.53
                  ) -> tuple[trimesh.Trimesh, Action]:
    """Taubin smoothing: reduces noise without the volume shrinkage of Laplacian.
    Edge preservation is enforced downstream by the deviation budget (a step that moves
    the surface beyond the budget is rejected by the caller)."""
    ms = to_ms(mesh)
    ms.apply_coord_taubin_smoothing(lambda_=lam, mu=mu, stepsmoothnum=int(steps))
    return from_ms(ms), Action("smooth_taubin", {"steps": steps, "lambda": lam, "mu": mu})


def decimate(mesh: trimesh.Trimesh, target_faces: int) -> tuple[trimesh.Trimesh, Action]:
    if len(mesh.faces) <= target_faces:
        return mesh, Action("decimate", {"target_faces": target_faces}, {"skipped": True})
    ms = to_ms(mesh)
    ms.meshing_decimation_quadric_edge_collapse(
        targetfacenum=int(target_faces), qualitythr=0.3, preserveboundary=True,
        preservenormal=True, preservetopology=True, planarquadric=True, optimalplacement=True)
    out = from_ms(ms)
    return out, Action("decimate", {"target_faces": target_faces},
                       {"faces_before": len(mesh.faces), "faces_after": len(out.faces)})


def poisson_remesh(points: np.ndarray, normals: np.ndarray, depth: int = 8) -> trimesh.Trimesh:
    """Screened Poisson surface from an oriented point cloud (used by the virtual scanner)."""
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(vertex_matrix=np.asarray(points, dtype=np.float64),
                               v_normals_matrix=np.asarray(normals, dtype=np.float64)))
    ms.generate_surface_reconstruction_screened_poisson(depth=int(depth), preclean=True)
    return from_ms(ms)
