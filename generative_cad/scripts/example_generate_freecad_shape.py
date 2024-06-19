#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: example_generate_freecad_shape.py
Author: Monica Perez Serrano

Description: This script generates a freecad file containing a 3D shapes.

"""

from sys import path as syspath

syspath.append("/usr/lib/freecad-python3/lib")

import subprocess
from typing import List

from text_to_cad_common.geometric_primitives import (
    SupportedShapes,
    Parameters,
    Translation,
    RotationEuler,
)
from generative_cad.freecad_tools import generate_freecad_file, Object3D

if __name__ == "__main__":
    name: SupportedShapes
    parameters: Parameters
    translation: Translation
    rotation: RotationEuler

    sphere = Object3D(
        name=SupportedShapes.SPHERE,
        parameters=Parameters(shape=SupportedShapes.SPHERE, radius=1),
        translation=Translation(x=0, y=2, z=2),
        rotation=RotationEuler(x_rad=0, y_rad=0, z_rad=0),
    )
    torus = Object3D(
        name=SupportedShapes.TORUS,
        parameters=Parameters(shape=SupportedShapes.TORUS, radius1=0.1, radius2=10),
        translation=Translation(x=-1, y=0, z=1),
        rotation=RotationEuler(x_rad=1.57, y_rad=0, z_rad=0),
    )
    objects: List[Object3D] = [sphere, torus]
    freecad_file_name = "example_freecad_shape.fcstd"
    generate_freecad_file(objects=objects, output_file=freecad_file_name)
    subprocess.run(["freecad", freecad_file_name], check=True)
