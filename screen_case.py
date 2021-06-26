#! /usr/bin/env python3

# autocmd BufWritePost keyboard_case.py !python keyboard_case.py

import logging

import solid
import solid.objects
import solid.utils

import common

from common import Face

from solid import objects
from solid.objects import (
    cube,
    sphere,
    union,
    translate,
    cylinder,
    linear_extrude,
    difference,
    offset,
    square,
    hull,
)


WALL_THICKNESS = 5  # Wall Thickness

SCREEN_WIDTH = 74.76
SCREEN_HEIGHT = 140.4
SCREEN_CORNER_R = 4

POCKET_SIZE = 50

CASE_DEPTH = 40


SCREEN_MOUNTS = [
    (16.75, 61.83),
    (-30.65, 62.00),
    (23.75, 39.75),
    (-25.22, 39.91),
    (23.83, -18.16),
    (-25.40, -17.95),
    (31.71, -48.21),
    (-31.00, -60.08),
]

MOUNT_HOLE_SIZE_R = 3


def get_corner_pivots():
    offset_reduction = SCREEN_CORNER_R * 2
    width = (SCREEN_WIDTH - offset_reduction) / 2
    height = (SCREEN_HEIGHT - offset_reduction) / 2

    coords = [
        (-width, -height),
        (width, -height),
        (-width, height),
        (width, height),
    ]
    return coords


def screen_out_line():
    offset_reduction = SCREEN_CORNER_R * 2
    square_size = [SCREEN_WIDTH - offset_reduction, SCREEN_HEIGHT - offset_reduction]
    return offset(r=SCREEN_CORNER_R)(square(square_size, center=True))

def case_out_line():
    return offset(r=WALL_THICKNESS)(screen_out_line()),


def assembly():
    case = linear_extrude(POCKET_SIZE)(
        difference()(
            case_out_line()
            screen_out_line(),
        )
    )

    coordinates = get_corner_pivots()

    spheres = []
    for coord in coordinates:
        spheres.append(translate(coord)(sphere(SCREEN_CORNER_R + WALL_THICKNESS)))

    case += solid.objects.hull()(spheres)

    mount_holes = []
    for x, y in SCREEN_MOUNTS:
        hole = translate([x, y, -50])(cylinder(r=MOUNT_HOLE_SIZE_R, h=CASE_DEPTH + 600))
        mount_holes.append(hole)

    case = solid.objects.difference()(case, *mount_holes)
    return case


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    common.render_to_stl(assembly(), "display_case")
    # common.render_to_dxfs(assembly(), "display_case")
