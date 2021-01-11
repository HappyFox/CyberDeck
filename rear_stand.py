#! /usr/bin/env python3

# autocmd BufWritePost rear_stand.py !python rear_stand.py


import common

from solid.objects import cylinder, sphere
from solid.utils import up

from common import PLY_THICKNESS, KEY_BOARD_STANDOFF

OUT_RAD = 4.5
INNER_RAD = 2.5
NUB_HEIGHT = 1.65

STAND_RAD = 20 / 2


def assembly():
    stand = cylinder(r=STAND_RAD, h=PLY_THICKNESS)

    stand += up(PLY_THICKNESS)(cylinder(r=OUT_RAD, h=KEY_BOARD_STANDOFF))

    stand += up(PLY_THICKNESS + KEY_BOARD_STANDOFF)(cylinder(r=INNER_RAD, h=NUB_HEIGHT))

    return stand


if __name__ == "__main__":
    common.render_to_stl(assembly(), "stand")
