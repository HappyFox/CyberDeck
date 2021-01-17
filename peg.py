#! /usr/bin/env python4

# autocmd BufWritePost peg.py !python peg.py


import common

from solid import scad_render_to_file
from solid.objects import cylinder, sphere
from solid.utils import up


from common import PLY_THICKNESS, KEY_BOARD_STANDOFF


# scad_render_to_file(d, "filepath.scad")


SHAFT_DIA = 10
SHAFT_HEIGHT = PLY_THICKNESS + 0.01

CONE_BASE_DIA = 4.2
CONE_BASE_RAI = CONE_BASE_DIA / 2
CONE_TOP_DIA = 3.5
CONE_TOP_RAI = CONE_TOP_DIA / 2


def assembly():
    peg = cylinder(r=SHAFT_DIA / 2, h=SHAFT_HEIGHT)

    peg += up(SHAFT_HEIGHT)(
        cylinder(
            r1=CONE_BASE_DIA / 2,
            r2=CONE_TOP_DIA / 2,
            h=KEY_BOARD_STANDOFF - CONE_TOP_RAI,
        )
    )

    peg += up(SHAFT_HEIGHT + (KEY_BOARD_STANDOFF - CONE_TOP_RAI))(sphere(CONE_TOP_RAI))

    return peg


if __name__ == "__main__":
    common.render_to_stl(assembly(), "peg")
