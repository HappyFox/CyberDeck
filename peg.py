#! /usr/bin/env python3

# autocmd BufWritePost peg.py !python peg.py

import solid
import solid.objects

import common

from solid import scad_render_to_file
from solid.objects import cylinder, sphere
from solid.utils import up


from common import PLY_THICKNESS, KEY_BOARD_STANDOFF


BASE_DIA = 10
BASE_HEIGHT = PLY_THICKNESS

CONE_BASE_DIA = 4.2
CONE_BASE_RAI = CONE_BASE_DIA / 2
CONE_TOP_DIA = 3.5
CONE_TOP_RAI = CONE_TOP_DIA / 2


def _make_base(add=0):
    return cylinder(r=BASE_DIA / 2, h=BASE_HEIGHT + add)


def make_hole():
    return _make_base(add=0.1)


def assembly():
    peg = _make_base()

    peg += up(BASE_HEIGHT)(
        cylinder(
            r1=CONE_BASE_DIA / 2,
            r2=CONE_TOP_DIA / 2,
            h=KEY_BOARD_STANDOFF - CONE_TOP_RAI,
        )
    )

    peg += up(BASE_HEIGHT + (KEY_BOARD_STANDOFF - CONE_TOP_RAI))(sphere(CONE_TOP_RAI))

    return peg


if __name__ == "__main__":
    common.render_to_stl(assembly(), "peg")
