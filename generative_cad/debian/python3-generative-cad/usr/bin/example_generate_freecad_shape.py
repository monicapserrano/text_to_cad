#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: example_generate_freecad_shape.py
Author: Monica Perez Serrano

Description: This script generates a freecad file containing a 3D shapes.

"""

from sys import path as syspath

syspath.append("/usr/lib/freecad-python3/lib")

import FreeCAD as App
import FreeCADGui as Gui
import Part

from text_to_cad_common.geometric_primitives import (Plane)
from text_to_cad_common.geometric_primitives import (
    Translation,
    RotationEuler,
)
if __name__ == "__main__":

    # Example parameters (you can replace this with your actual parameters)
    degius = 1.0
    height = 2.0

    # Create a cylinder
    cylinder = Part.makeCylinder(degius, height)

    # Create a box
    box = Part.makeBox(100.0, 100.0, 100.0)  # Example dimensions: 1.0 x 1.0 x 1.0

    # Translate the box to a position where it intersects with the cylinder
    box.translate((0.5, 0.5, height / 2))

    # Fuse operation to combine the shapes
    result = cylinder.fuse(box)

    # Convert the result to a FreeCAD solid
    solid = Part.Solid(result)

    # Create a FreeCAD document
    doc = App.newDocument()

    # Add the solid to the document
    obj = doc.addObject("Part::Feature", "Result")
    obj.Shape = result
    print(f"Object Type {type(obj)}")

    p1 = App.Vector(10, 0, 0)
    p2 = App.Vector(0, 10, 0)
    p3 = App.Vector(-10, 0, 0)
    arc = Part.Arc(p1, p2, p3)
    obj = doc.addObject("Part::Feature", "Arc")
    obj.Shape = arc.toShape()
    # obj.Visibility = True

    doc.recompute()
    Plane(name="plane", width=100, length=50).add_to_doc(
        doc=doc, translation=Translation(100, 10, 10), rotation=RotationEuler(45, 0, 0)
    )

    # Check if the solid was successfully added to the document
    if obj.Shape.isNull():
        print("Error: Failed to create solid")
    else:
        print("Solid created successfully")

    # Save the document to a file (optional)
    file_path = "output_model.fcstd"
    try:
        doc.saveAs(file_path)
        print("Document saved successfully to:", file_path)
        FreeCAD.closeDocument(doc.Name)
    except Exception as e:
        print("Error saving document:", e)

    # Show the FreeCAD GUI (optional)
    Gui.showMainWindow()
    # Gui.setWorkbench("PartWorkbench")
    Gui.activateWorkbench("PartWorkbench")
