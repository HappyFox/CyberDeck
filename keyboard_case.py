#! /usr/bin/env python3

# autocmd BufWritePost keyboard_case.py !python keyboard_case.py

import logging


import solid.objects

import common

from solid.objects import cylinder, sphere, cube, translate
from solid.utils import up, right, forward

from common import PLY_THICKNESS, KEY_BOARD_STANDOFF

import peg
import rear_stand


KEY_BOARD_LEN = 431
KEY_BOARD_DEPTH = 128

CASE_WALL = 40

CASE_LEN = KEY_BOARD_LEN  # + CASE_WALL
CASE_DEPTH = KEY_BOARD_DEPTH  # + CASE_WALL


def get_peg_positions(z_delta):
    # yes I did record the x positions inverse to the way openscad does it.

    # Y postions
    # ys = [40.6, 38]

    # ys = common.make_rel_to_abs(ys)

    ys = [40.6, 78.6]

    logging.info(f"the Y coords {ys}")

    # X positions
    # xs = [57.5, 45, 89, 76, 53, 62]
    # xs = [57.5, 102.5, 191.5, 267.5, 320.5, 382.5]

    # Guess 1: 0, +3, +2,
    # xs = [57.5, 105.5, 193.5, 267.5, 320.5, 382.5]

    # Guess 1: 0, +3, +2,
    xs = [58.5, 105.5, 191.5, 267.5, 320.5, 382.5]
    # xs = common.make_rel_to_abs(xs)

    logging.info(f"the X coords {xs}")

    holes = []
    for x in xs:
        for y in ys:
            holes.append(translate((x, y, z_delta))(peg.make_hole()))

    # add that rando middle hole.

    holes.append(translate((154, 60, z_delta))(peg.make_hole()))

    # return solid.objects.union()(*holes)
    return holes


def assembly():
    case = cube([CASE_LEN, CASE_DEPTH, PLY_THICKNESS * 2])
    # case -= up(PLY_THICKNESS)(get_peg_positions())
    rear_peg = translate((216, 101.6, PLY_THICKNESS))(rear_stand.get_hole())
    case = solid.objects.difference()(case, rear_peg, *get_peg_positions(PLY_THICKNESS))

    return case


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    common.render_to_stl(assembly(), "keyboard_case")
    common.render_to_dxfs(assembly(), "keyboard_case")
