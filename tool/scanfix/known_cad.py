"""Three known-CAD parts with recorded true dimensions, built from primitives with exact
booleans (manifold3d). These are the ground truth for the synthetic DEV items."""

from __future__ import annotations

import numpy as np
import trimesh


def _box(extents, translate=(0, 0, 0)):
    b = trimesh.creation.box(extents=extents)
    b.apply_translation(translate)
    return b


def _cyl(radius, height, translate=(0, 0, 0), axis="z"):
    c = trimesh.creation.cylinder(radius=radius, height=height, sections=96)
    if axis == "x":
        c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    elif axis == "y":
        c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    c.apply_translation(translate)
    return c


def l_bracket() -> tuple[trimesh.Trimesh, dict]:
    """60×40×3 mm base, 40×40×3 mm upright, two Ø5 mm holes in the base at 20 mm pitch."""
    base = _box((60, 40, 3), (0, 0, 1.5))
    upright = _box((3, 40, 40), (-28.5, 0, 20))
    body = trimesh.boolean.union([base, upright], engine="manifold")
    holes = [_cyl(2.5, 10, (x, 0, 1.5)) for x in (10, 30)]
    part = trimesh.boolean.difference([body] + holes, engine="manifold")
    truth = {"name": "l_bracket", "class": "prismatic",
             "dims_mm": {"base_length": 60, "width": 40, "thickness": 3, "upright_height": 40,
                         "hole_diameter": 5, "hole_pitch": 20},
             "bbox_mm": [60, 40, 40]}
    return part, truth


def flange() -> tuple[trimesh.Trimesh, dict]:
    """Ø70×8 mm disc, Ø30 mm bore, four Ø6.5 mm bolt holes on a Ø55 mm circle."""
    disc = _cyl(35, 8)
    bore = _cyl(15, 20)
    bolts = [_cyl(3.25, 20, (27.5 * np.cos(a), 27.5 * np.sin(a), 0))
             for a in np.radians([0, 90, 180, 270])]
    part = trimesh.boolean.difference([disc, bore] + bolts, engine="manifold")
    truth = {"name": "flange", "class": "prismatic",
             "dims_mm": {"outer_diameter": 70, "thickness": 8, "bore_diameter": 30,
                         "bolt_hole_diameter": 6.5, "bolt_circle_diameter": 55},
             "bbox_mm": [70, 70, 8]}
    return part, truth


def pocket_block() -> tuple[trimesh.Trimesh, dict]:
    """50×30×20 mm block with a 30×15×10 mm pocket from the top and a Ø8 mm through-hole (X)."""
    block = _box((50, 30, 20), (0, 0, 10))
    pocket = _box((30, 15, 10.01), (0, 0, 15))
    hole = _cyl(4, 60, (0, 0, 6), axis="x")
    part = trimesh.boolean.difference([block, pocket, hole], engine="manifold")
    truth = {"name": "pocket_block", "class": "prismatic",
             "dims_mm": {"length": 50, "width": 30, "height": 20, "pocket": [30, 15, 10],
                         "through_hole_diameter": 8},
             "bbox_mm": [50, 30, 20]}
    return part, truth


ALL = [l_bracket, flange, pocket_block]
