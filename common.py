import subprocess

import solid
import solid.objects

from enum import IntFlag, auto
from pathlib import Path

from solid.objects import projection, offset
from solid.utils import down

# SEGMENTS = 64
SEGMENTS = 32

PLY_THICKNESS = 3

KERF = 0.2

KEY_BOARD_STANDOFF = 9

MIL = 2.54

LEN = 0
DEPTH = 1
HEIGHT = 2


class Face(IntFlag):
    FRONT = auto()
    BACK = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()
    # ALL = FRONT | BACK | LEFT | RIGHT | TOP | BOTTOM

    @classmethod
    def all(cls):
        return cls.FRONT | cls.BACK | cls.LEFT | cls.RIGHT | cls.TOP | cls.BOTTOM


def make_filleted_cube(size, r=0, faces=Face.all()):

    size = {LEN: size[0], DEPTH: size[1], HEIGHT: size[2]}
    center_size = {}

    for key in size:
        center_size[key] = size[key]

    center_affects = {
        Face.FRONT: DEPTH,
        Face.BACK: DEPTH,
        Face.LEFT: LEN,
        Face.RIGHT: LEN,
        Face.TOP: HEIGHT,
        Face.BOTTOM: HEIGHT,
    }

    round_depths = {}

    for face in Face:
        if face in faces:
            round_depths[face] = r
            center_size[center_affects[face]] -= r
        else:
            round_depths[face] = 0

    start_corners = {Face.FRONT: DEPTH, Face.LEFT: LEN, Face.BOTTOM: HEIGHT}

    start_coord = {}

    for face in start_corners:
        if face in faces:
            start_coord[start_corners[face]] = r
        else:
            start_coord[start_corners[face]] = 0

    assembly = solid.objects.union()
    assembly.add(
        solid.objects.translate([0, start_coord[DEPTH], start_coord[HEIGHT]])(
            solid.objects.cube([size[LEN], center_size[DEPTH], center_size[HEIGHT]])
        )
    )
    assembly.add(
        solid.objects.translate([start_coord[LEN], 0, start_coord[HEIGHT]])(
            solid.objects.cube([center_size[LEN], size[DEPTH], center_size[HEIGHT]])
        )
    )
    assembly.add(
        solid.objects.translate([start_coord[LEN], start_coord[DEPTH], 0])(
            solid.objects.cube([center_size[LEN], center_size[DEPTH], size[HEIGHT]])
        )
    )

    # now handle spheres at the 4 corners.

    r_ends = {
        LEN: size[LEN] - r,
        DEPTH: size[DEPTH] - r,
        HEIGHT: size[HEIGHT] - r,
    }

    corners = [
        (Face.FRONT | Face.LEFT | Face.BOTTOM, [r, r, r]),
        (Face.FRONT | Face.RIGHT | Face.BOTTOM, [r_ends[LEN], r, r]),
        (Face.FRONT | Face.LEFT | Face.TOP, [r, r, r_ends[HEIGHT]]),
        (
            Face.FRONT | Face.RIGHT | Face.TOP,
            [r_ends[LEN], r, r_ends[HEIGHT]],
        ),
        (Face.BACK | Face.LEFT | Face.BOTTOM, [r, r_ends[DEPTH], r]),
        (
            Face.BACK | Face.RIGHT | Face.BOTTOM,
            [r_ends[LEN], r_ends[DEPTH], r],
        ),
        (
            Face.BACK | Face.LEFT | Face.TOP,
            [r, r_ends[DEPTH], r_ends[HEIGHT]],
        ),
        (
            Face.BACK | Face.RIGHT | Face.TOP,
            [r_ends[LEN], r_ends[DEPTH], r_ends[HEIGHT]],
        ),
    ]

    for corner_faces, coords in corners:
        if corner_faces & faces == corner_faces:
            assembly.add(solid.objects.translate(coords)(solid.objects.sphere(r=r)))

    edges = [
        (
            Face.FRONT | Face.BOTTOM,
            Face.LEFT,
            [0, 90, 0],
            [r, r, r],
            [0, r, r],
            center_size[LEN],
        ),
        (
            Face.FRONT | Face.TOP,
            Face.LEFT,
            [0, 90, 0],
            [r, r, r_ends[HEIGHT]],
            [0, r, r_ends[HEIGHT]],
            center_size[LEN],
        ),
        (
            Face.BACK | Face.BOTTOM,
            Face.LEFT,
            [0, 90, 0],
            [r, r_ends[DEPTH], r],
            [0, r_ends[DEPTH], r],
            center_size[LEN],
        ),
        (
            Face.BACK | Face.TOP,
            Face.LEFT,
            [0, 90, 0],
            [r, r_ends[DEPTH], r_ends[HEIGHT]],
            [0, r_ends[DEPTH], r_ends[HEIGHT]],
            center_size[LEN],
        ),
        (
            Face.LEFT | Face.BOTTOM,
            Face.FRONT,
            [0, 90, 90],
            [r, r, r],
            [r, 0, r],
            center_size[DEPTH],
        ),
        (
            Face.LEFT | Face.TOP,
            Face.FRONT,
            [0, 90, 90],
            [r, r, r_ends[HEIGHT]],
            [r, 0, r_ends[HEIGHT]],
            center_size[DEPTH],
        ),
        (
            Face.RIGHT | Face.BOTTOM,
            Face.FRONT,
            [0, 90, 90],
            [r_ends[LEN], r, r],
            [r_ends[LEN], 0, r],
            center_size[DEPTH],
        ),
        (
            Face.RIGHT | Face.TOP,
            Face.FRONT,
            [0, 90, 90],
            [r_ends[LEN], r, r_ends[HEIGHT]],
            [r_ends[LEN], 0, r_ends[HEIGHT]],
            center_size[DEPTH],
        ),
        (
            Face.LEFT | Face.FRONT,
            Face.BOTTOM,
            [0, 0, 0],
            [r, r, r],
            [r, r, 0],
            center_size[HEIGHT],
        ),
        (
            Face.LEFT | Face.BACK,
            Face.BOTTOM,
            [0, 0, 0],
            [r, r_ends[DEPTH], r],
            [r, r_ends[DEPTH], 0],
            center_size[HEIGHT],
        ),
        (
            Face.RIGHT | Face.FRONT,
            Face.BOTTOM,
            [0, 0, 0],
            [r_ends[LEN], r, r],
            [r_ends[LEN], r, 0],
            center_size[HEIGHT],
        ),
        (
            Face.RIGHT | Face.BACK,
            Face.BOTTOM,
            [0, 0, 0],
            [r_ends[LEN], r_ends[DEPTH], r],
            [r_ends[LEN], r_ends[DEPTH], 0],
            center_size[HEIGHT],
        ),
    ]

    for edge_faces, inset_face, rot, inset_coords, coords, h in edges:
        if edge_faces & faces == edge_faces:
            trans_coords = coords
            if inset_face & faces == inset_face:
                trans_coords = inset_coords
            assembly.add(
                solid.objects.translate(trans_coords)(
                    solid.objects.rotate(rot)(solid.objects.cylinder(r=r, h=h))
                )
            )

    return assembly


def to_layer(val):
    return (val / PLY_THICKNESS) * PLY_THICKNESS


def make_rel_to_abs(list_):
    ret = []
    for idx, val in enumerate(list_):
        if idx != 0:
            val += ret[idx - 1]
        ret.append(val)
    return ret


def render_to_stl(assembly, name):
    solid.scad_render_to_file(
        assembly,
        f"{name}.scad",
        file_header=f"$fn = {SEGMENTS};",
        include_orig_code=True,
    )
    subprocess.run(["openscad", f"{name}.scad", "-o", f"{name}.stl"])


def render_to_dxfs(assembly, name):

    proj_offset = PLY_THICKNESS / 2
    idx = 1

    out_dir = Path.cwd() / f"{name}_dxfs"
    out_dir.mkdir(exist_ok=True)

    while True:
        projection_assembly = solid.objects.offset(r=KERF / 2)(
            solid.objects.projection(cut=True)(down(proj_offset)(assembly))
        )
        scad_file = out_dir / f"{name}_{idx}.scad"
        dxf_file = out_dir / f"{name}_{idx}.dxf"

        solid.scad_render_to_file(
            projection_assembly,
            scad_file,
            file_header=f"$fn = {SEGMENTS};",
            include_orig_code=True,
        )

        result = subprocess.run(["openscad", scad_file, "-o", dxf_file])

        if result.returncode != 0:
            break

        proj_offset += PLY_THICKNESS
        idx += 1
