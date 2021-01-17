#! /usr/bin/env python3

# autocmd BufWritePost rear_stand.py !python rear_stand.py


import common

from solid.objects import cylinder, sphere, cube
from solid.utils import up, right, forward

from common import PLY_THICKNESS, KEY_BOARD_STANDOFF

import peg


def assembly():
    case = cube([100, 200, PLY_THICKNESS * 2])
    case -= forward(10)(right(20)(up(PLY_THICKNESS)(peg.assembly())))

    return case


if __name__ == "__main__":
    common.render_to_stl(assembly(), "keyboard_case")
