#! /usr/bin/env python3

# autocmd BufWritePost keyboard_case.py !python keyboard_case.py

import logging

import solid
import solid.objects
import solid.utils

import common

from common import Face

from solid import objects
from solid.objects import cube, sphere, union, translate, cylinder


SCREEN_HEIGHT = 74.76
SCREEN_WIDTH = 140.4
SCREEN_CORNER_R = 4

CASE_WALL = 10
CASE_DEPTH = 40
CASE_CORNER_R = 8

DOUBLE_WALL = CASE_WALL * 2

SCREEN_MOUNTS = [(9.661, 10.581), (53.67, 10.697), (9.458, 129.465), (68.506, 117.619)]

MOUNT_HOLE_SIZE_R = 3


def assembly():

    case = common.make_filleted_cube(
        [SCREEN_HEIGHT + DOUBLE_WALL, SCREEN_WIDTH + DOUBLE_WALL, CASE_DEPTH],
        r=CASE_CORNER_R,
        faces=Face.FRONT | Face.BACK | Face.LEFT | Face.RIGHT | Face.TOP,
    )
    case -= translate([CASE_WALL, CASE_WALL, -0.01])(
        common.make_filleted_cube(
            [SCREEN_HEIGHT, SCREEN_WIDTH, CASE_DEPTH - CASE_WALL],
            r=SCREEN_CORNER_R,
            faces=Face.FRONT | Face.BACK | Face.LEFT | Face.RIGHT | Face.TOP,
        )
    )

    mount_holes = []
    for x, y in SCREEN_MOUNTS:
        hole = translate([x + CASE_WALL, y + CASE_WALL, 0])(
            cylinder(r=MOUNT_HOLE_SIZE_R, h=CASE_DEPTH + 10)
        )
        mount_holes.append(hole)

    case = solid.objects.difference()(case, *mount_holes)
    # case = solid.objects.union()(case, *mount_holes)

    return case


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    common.render_to_stl(assembly(), "display_case")
    # common.render_to_dxfs(assembly(), "display_case")
