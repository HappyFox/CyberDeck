#! /usr/bin/env python3

# autocmd BufWritePost keyboard_case.py !python keyboard_case.py

import logging

import solid
import solid.objects
import solid.utils

import common

from common import Face

from solid import objects
from solid.objects import cube, sphere, union, translate

CASE_LEN = 1000
CASE_DEPTH = 250
CASE_HEIGHT = 150
ROUNDING_HEIGHT = 50


CENTER_DEPTH = CASE_DEPTH - (2 * ROUNDING_HEIGHT)
CENTER_LEN = CASE_LEN - (2 * ROUNDING_HEIGHT)
CENTER_HEIGHT = CASE_HEIGHT - ROUNDING_HEIGHT

FRONT_ROUND = ROUNDING_HEIGHT
BACK_ROUND = ROUNDING_HEIGHT + CENTER_DEPTH

LEFT_ROUND = ROUNDING_HEIGHT
RIGHT_ROUND = ROUNDING_HEIGHT + CENTER_LEN
UP_ROUND = ROUNDING_HEIGHT


def round_corner():
    return objects.union()(
        objects.sphere(r=ROUNDING_HEIGHT),
        objects.cylinder(r=ROUNDING_HEIGHT, h=ROUNDING_HEIGHT),
    )


def assembly():
    """case = union()
    case.add(
        objects.translate([0, FRONT_ROUND, UP_ROUND])(
            objects.cube(
                [
                    CASE_LEN,
                    CENTER_DEPTH,
                    CENTER_HEIGHT,
                ]
            )
        )
    )
    case.add(
        objects.translate([LEFT_ROUND, 0, UP_ROUND])(
            objects.cube(
                [
                    CENTER_LEN,
                    CASE_DEPTH,
                    CENTER_HEIGHT,
                ]
            )
        )
    )
    case.add(
        objects.translate([ROUNDING_HEIGHT, ROUNDING_HEIGHT, 0])(
            objects.cube(
                [
                    CASE_LEN - (2 * ROUNDING_HEIGHT),
                    CASE_DEPTH - (2 * ROUNDING_HEIGHT),
                    CASE_HEIGHT,
                ]
            )
        )
    )
    front_left_corner = round_corner()
    front_left_corner.add(
        objects.rotate([-90, 0, 0])(objects.cylinder(r=ROUNDING_HEIGHT, h=CENTER_DEPTH))
    )
    front_left_corner.add(
        objects.rotate([0, 90, 0])(objects.cylinder(r=ROUNDING_HEIGHT, h=CENTER_LEN))
    )

    case.add(
        objects.translate([ROUNDING_HEIGHT, ROUNDING_HEIGHT, ROUNDING_HEIGHT])(
            front_left_corner
        )
    )"""

    return common.make_filted_cube(
        [CASE_LEN, CASE_DEPTH, CASE_HEIGHT],
        r=ROUNDING_HEIGHT,
        faces=Face.FRONT | Face.BACK | Face.LEFT | Face.RIGHT | Face.BOTTOM,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    common.render_to_stl(assembly(), "case")
    # common.render_to_dxfs(assembly(), "case")
