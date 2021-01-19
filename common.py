import subprocess

import solid
import solid.objects

from pathlib import Path

from solid.objects import projection, offset
from solid.utils import down

# SEGMENTS = 64
SEGMENTS = 32

PLY_THICKNESS = 3

KERF = 0.2

KEY_BOARD_STANDOFF = 9

MIL = 2.54


def make_rel_to_abs(list_):
    ret = []
    for idx, val in enumerate(list_):
        if idx != 0:
            val += ret[idx - 1]
        ret.append(val)
    return ret


def render_to_stl(assembly, name):
    solid.scad_render_to_file(
        assembly,
        f"{name}.scad",
        file_header=f"$fn = {SEGMENTS};",
        include_orig_code=True,
    )
    subprocess.run(["openscad", f"{name}.scad", "-o", f"{name}.stl"])


def render_to_dxfs(assembly, name):

    proj_offset = PLY_THICKNESS / 2
    idx = 1

    out_dir = Path.cwd() / f"{name}_dxfs"
    out_dir.mkdir(exist_ok=True)

    while True:
        projection_assembly = solid.objects.offset(r=KERF / 2)(
            solid.objects.projection(cut=True)(down(proj_offset)(assembly))
        )
        scad_file = out_dir / f"{name}_{idx}.scad"
        dxf_file = out_dir / f"{name}_{idx}.dxf"

        solid.scad_render_to_file(
            projection_assembly,
            scad_file,
            file_header=f"$fn = {SEGMENTS};",
            include_orig_code=True,
        )

        result = subprocess.run(["openscad", scad_file, "-o", dxf_file])

        if result.returncode != 0:
            break

        proj_offset += PLY_THICKNESS
        idx += 1
