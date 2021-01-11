import subprocess

import solid

SEGMENTS = 64

PLY_THICKNESS = 3
KEY_BOARD_STANDOFF = 9


def render_to_stl(assembly, name):
    solid.scad_render_to_file(
        assembly,
        f"{name}.scad",
        file_header=f"$fn = {SEGMENTS};",
        include_orig_code=True,
    )
    subprocess.run(["openscad", "stand.scad", "-o", f"{name}.stl"])
