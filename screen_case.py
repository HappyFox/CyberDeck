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


MOUNT_DIAM = 4.564
DEPTH_FOR_MOUNT = 9

WALL_THICKNESS = 5  # Wall Thickness

SCREEN_WIDTH = 74.8
SCREEN_HEIGHT = 140.4
SCREEN_CORNER_R = 4

POCKET_SIZE = 36

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

BUTTON_POS = (-0.55, -46.80)
BUTTON_SIZE = 2.5
BUTTON_GUIDE_HEIGHT = 30

MOUNT_HOLE_SIZE_R = 1.5


HDMI_LEN = 23
HDMI_WIDTH = 16
HDMI_DEPTH = 9


USB_WIDTH = 12.2
USB_LEN = 16.5
USB_HEIGHT = 10.60


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
    return (offset(r=WALL_THICKNESS)(screen_out_line()),)


def hdmi_cutout():
    rect = square([HDMI_WIDTH, HDMI_LEN])
    return linear_extrude(HDMI_DEPTH)(rect)


def usb_cutout():
    rect = square([USB_WIDTH, USB_LEN])
    return linear_extrude(USB_HEIGHT)(rect)


def assembly():
    case_radius = SCREEN_CORNER_R + WALL_THICKNESS
    floor_add = DEPTH_FOR_MOUNT - case_radius

    case = linear_extrude(POCKET_SIZE + floor_add)(
        difference()(
            case_out_line(),
            screen_out_line(),
        )
    )

    coordinates = get_corner_pivots()

    print(f"CASE RADIUS : {case_radius}")
    spheres = []
    for coord in coordinates:
        spheres.append(translate(coord)(sphere(case_radius)))

    case += solid.objects.hull()(spheres) - linear_extrude(case_radius + 1)(
        case_out_line()
    )

    floor_add = DEPTH_FOR_MOUNT - case_radius
    print(f"Need to have depth of {DEPTH_FOR_MOUNT}, adding {floor_add}")

    case += linear_extrude(floor_add)(case_out_line())

    mount_holes = []

    for x, y in SCREEN_MOUNTS:
        hole = translate([x, y])(
            translate([0, 0, -50])(cylinder(r=MOUNT_HOLE_SIZE_R, h=CASE_DEPTH + 600)),
            translate([0, 0, -case_radius - 6])(
                cylinder(r=MOUNT_HOLE_SIZE_R * 2, h=case_radius)
            ),
        )
        mount_holes.append(hole)

    hole = translate([0, 0, -50])(cylinder(r=MOUNT_DIAM, h=CASE_DEPTH + 600))
    mount_holes.append(hole)

    hole = translate([BUTTON_POS[0], BUTTON_POS[1]])(
        cylinder(r=BUTTON_SIZE * 2, h=BUTTON_GUIDE_HEIGHT),
    )

    # case += hole

    hole = translate([BUTTON_POS[0], BUTTON_POS[1]])(
        translate([0, 0 - 50])(cylinder(r=BUTTON_SIZE, h=CASE_DEPTH + 600)),
    )
    mount_holes.append(hole)

    case = solid.objects.difference()(case, *mount_holes)

    hdmi_move = (((SCREEN_HEIGHT / 2) + WALL_THICKNESS) - HDMI_LEN) + 0.1
    case = solid.objects.difference()(case, translate([-5, hdmi_move])(hdmi_cutout()))

    usb_move = (((SCREEN_HEIGHT / 2) + WALL_THICKNESS) - USB_LEN) + 0.1
    case = solid.objects.difference()(
        case, translate([-(10 + HDMI_WIDTH), usb_move])(usb_cutout())
    )

    return translate([0, 0, case_radius])(case)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # common.render_to_stl(hdmi_cutout(), "display_case")
    common.render_to_stl(assembly(), "display_case")
    # common.render_to_dxfs(assembly(), "display_case")
