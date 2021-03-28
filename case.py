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
CASE_HEIGHT = 500
ROUNDING_HEIGHT = 50


def assembly():

    return common.make_filleted_cube(
        [CASE_LEN, CASE_DEPTH, CASE_HEIGHT],
        r=ROUNDING_HEIGHT,
        faces=Face.FRONT | Face.BACK | Face.LEFT | Face.RIGHT | Face.BOTTOM,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    common.render_to_stl(assembly(), "case")
    # common.render_to_dxfs(assembly(), "case")
