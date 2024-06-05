"""
Filename: freecad_tools.py
Author: Monica Perez Serrano

Description: This file includes functions to generate freecad 3D objects.

"""

from text_to_cad_common.geometric_primitives import (
    Parameters,
    SupportedShapes,
    Translation,
    RotationEuler,
)
from dataclasses import dataclass
import logging as log
from typing import Optional, List
from tempfile import NamedTemporaryFile

# Import FreeCAD modules
# https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Topological_data_scripting.md
from sys import path as syspath

syspath.append("/usr/lib/freecad-python3/lib")
import FreeCAD as App


@dataclass
class Object3D:
    """Represents a 3D object to be included in a FreeCAD file."""

    name: SupportedShapes
    parameters: Parameters
    translation: Translation
    rotation: RotationEuler


def instantiate_class(class_name: str, *args, **kwargs):
    """Instantiates a class dynamically based on the provided class_name string."""
    cls = globals()[class_name.capitalize()]
    return cls(*args, **kwargs)


def generate_freecad_file(objects: List[Object3D], output_file: Optional[str]) -> str:
    """
    Generates a FreeCAD file (.fcstd) containing 3D objects.

    Args:
        objects (List[Object3D]): A list of Object3D instances representing the 3D objects to be included.
        output_file (Optional[str]): The path where the generated FreeCAD file will be saved.
            If not provided, a temporary file will be created.

    Returns:
        str: The path to the generated FreeCAD file.
    """
    if output_file is None:
        output_file = NamedTemporaryFile(suffix=".fcstd", delete=False).name

    doc = App.newDocument()
    i = 0
    for obj in objects:
        i += 1
        instantiate_class(str(obj.name), i, obj.parameters)
    try:
        doc.saveAs(output_file)
        log.info(
            f"[generate_freecad_file] Document saved successfully to: {output_file}"
        )
        App.closeDocument(doc.Name)
    except Exception as e:
        log.error(f"[generate_freecad_file] Error saving document: {e}")

    return output_file
