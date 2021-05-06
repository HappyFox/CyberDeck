#! /usr/bin/env python3

# autocmd BufWritePost core.py !python core.py

import logging
import math


import solid.objects

import common

from solid.objects import cylinder, sphere, cube, translate, difference
from solid.utils import up, right, forward, left, back, down

from common import PLY_THICKNESS


CASE_DEPTH = 300
CASE_WIDTH = 400
CASE_LAYERS = 40

CORNER_RADIUS = 30
HOLE_RADIUS = 10


HOLES_X = (CASE_WIDTH / 2) - CORNER_RADIUS
HOLES_Y = (CASE_DEPTH / 2) - CORNER_RADIUS


class CaseBuilder:
    def __init__(self):
        self.corner_radius = 30
        self.wall_thickness = self.corner_radius
        self.hole_radius = 10
        self.shelf_thickness = 15

        self.width = None
        self.depth = None
        self.height = None

        self._hole_x = None
        self._hole_y = None

        self.width_mid_posts = False
        self.depth_mid_posts = False

        self.hole_overshoot = 0.2

        self.shelves = []

    def _calc_holes(self):
        self._hole_x = (self.width / 2) - self.corner_radius
        self._hole_y = (self.depth / 2) - self.corner_radius

    def _get_offsets(self):
        offsets = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

        if self.width_mid_posts:
            offsets = offsets + [(0, 1), (0, -1)]

        if self.depth_mid_posts:
            offsets = offsets + [(1, 0), (-1, 0)]

        return offsets

    def get_shelves_height(self):
        heights = []

        for shelf in self.shelves:
            shelf_height = common.to_layer(self.height * shelf)
            heights.append(shelf_height)

        return heights

    def build_posts(self):
        case = []

        self._calc_holes()

        offsets = self._get_offsets()

        for x_mult, y_mult in offsets:
            case += translate([self._hole_x * x_mult, self._hole_y * y_mult, 0])(
                cylinder(r=self.corner_radius, h=self.height)
            )
        return case

    def build_walls(self):
        case = []

        wall_width = self.width / 2 - self.corner_radius
        wall_depth = self.depth / 2 - self.corner_radius

        wall_x_pos = self.width / 2 - self.wall_thickness / 2
        wall_y_pos = self.depth / 2 - self.wall_thickness / 2

        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for x_off, y_off in offsets:
            trans = [x_off * wall_x_pos, y_off * wall_y_pos, self.height / 2]

            coords = [self.wall_thickness, wall_depth * 2, self.height]
            if y_off:
                coords = [wall_width * 2, self.wall_thickness, self.height]

            case += translate(trans)(cube(coords, center=True))

        shelf_heights = self.get_shelves_height()

        # shelf_x_pos = self.width / 2 - self.wall_thickness - self.shelf_thickness / 2
        # shelf_y_pos = self.depth / 2 - self.wall_thickness - self.shelf_thickness / 2

        for shelf in shelf_heights:

            case += translate([0, 0, shelf])(
                cube([wall_width * 2, self.depth - 0.1, PLY_THICKNESS], center=True),
                cube([self.width - 0.1, wall_depth * 2, PLY_THICKNESS], center=True),
            )

        """ for partial shelves
        for shelf in shelf_heights:
            for x_off, y_off in offsets:
                trans = [shelf_x_pos * x_off, shelf_y_pos * y_off, shelf]
                coords = [self.shelf_thickness, wall_depth * 2, PLY_THICKNESS]

                if y_off:
                    coords = [wall_width * 2, self.shelf_thickness, PLY_THICKNESS]

                case += translate(trans)(
                    cube(
                        coords,
                        center=True,
                    )
                )
            """

        return case

    def build_holes(self):
        case = []
        offsets = self._get_offsets()

        for x_mult, y_mult in offsets:
            case += translate(
                [self._hole_x * x_mult, self._hole_y * y_mult, -self.hole_overshoot]
            )(
                cylinder(r=self.hole_radius, h=self.height + (self.hole_overshoot * 2)),
            )

        return case

    def build_shelf_holes(self):
        if not self.shelves:
            return []

        offsets = []

    def build(self):
        case = self.build_posts()
        case += self.build_walls()
        case -= self.build_holes()

        return case


def assembly():
    # case = cube([CASE_LEN, CASE_DEPTH, PLY_THICKNESS * CASE_LAYERS])

    case = CaseBuilder()
    case.width = CASE_WIDTH
    case.depth = CASE_DEPTH
    case.height = CASE_LAYERS * PLY_THICKNESS

    case.wall_thickness = 15
    case.shelf_thickness = 45

    case.width_mid_posts = True
    case.depth_mid_posts = True

    case.shelves = [0.5]

    return case.build()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    common.render_to_stl(assembly(), "case_core")
    # common.render_to_dxfs(assembly(), "case_core")
