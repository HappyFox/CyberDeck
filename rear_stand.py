import subprocess

from solid import scad_render_to_file
from solid.objects import cylinder, sphere
from solid.utils import up

from common import PLY_THICKNESS, KEY_BOARD_STANDOFF, SEGMENTS

OUT_RAD = 10
INNER_RAD = 5
NUB_HEIGHT = 2

STAND_RAD = 15


def assembly():
    stand = cylinder(r=STAND_RAD, h=PLY_THICKNESS)

    stand += up(PLY_THICKNESS)(cylinder(r=OUT_RAD, h=KEY_BOARD_STANDOFF))

    stand += up(PLY_THICKNESS + KEY_BOARD_STANDOFF)(cylinder(r=INNER_RAD, h=NUB_HEIGHT))

    return stand


if __name__ == "__main__":
    a = assembly()
    scad_render_to_file(
        a, "stand.scad", file_header=f"$fn = {SEGMENTS};", include_orig_code=True
    )
    subprocess.run(["openscad", "stand.scad", "-o", "stand.stl"])
