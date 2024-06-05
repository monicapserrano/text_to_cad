"""
Filename: parameter_tools.py
Author: Monica Perez Serrano

Description: Common functions used by the different packages regarding shape parameters.

"""

from typing import List, Any
from text_to_cad_common.geometric_primitives import (
    Parameters,
    SupportedShapes,
    Translation,
    RotationEuler,
)
from generative_cad.freecad_tools import Object3D


def from_list_to_parameter(shape: str, parameters: List[float]) -> Parameters:
    """
    Convert a list of parameters into a Parameters object based on the shape type.

    Args:
        shape (str): The shape type as a string.
        parameters (List[float]): List of numerical parameters for the shape.

    Returns:
        Parameters: The corresponding Parameters object.
    """
    p = {
        "length": 0,
        "width": 1,
        "height": 2,
        "radius": 3,
        "radius1": 4,
        "radius2": 5,
        "pitch": 5,
        "angle": 7,
    }
    if shape == str(SupportedShapes.PLANE):
        return Parameters(
            shape=SupportedShapes[shape.upper()],
            length=parameters[p["length"]],
            width=parameters[p["width"]],
        )
    elif shape == str(SupportedShapes.CUBE) or shape == str(SupportedShapes.BOX):
        return Parameters(
            shape=SupportedShapes[shape.upper()],
            length=parameters[p["length"]],
            width=parameters[p["width"]],
            height=parameters[p["height"]],
        )
    elif shape == str(SupportedShapes.CYLINDER):
        return Parameters(
            shape=SupportedShapes[shape.upper()],
            radius=parameters[p["radius"]],
            height=parameters[p["height"]],
        )
    elif shape == str(SupportedShapes.CONE):
        return Parameters(
            shape=SupportedShapes[shape.upper()],
            radius1=parameters[p["radius1"]],
            radius2=parameters[p["radius2"]],
            height=parameters[p["height"]],
        )
    elif shape == str(SupportedShapes.SPHERE):
        return Parameters(
            shape=SupportedShapes[shape.upper()], radius=parameters[p["radius"]]
        )
    elif shape == str(SupportedShapes.TORUS):
        return Parameters(
            shape=SupportedShapes[shape.upper()],
            radius1=parameters[p["radius1"]],
            radius2=parameters[p["radius2"]],
        )
    elif shape == str(SupportedShapes.HELIX):
        return Parameters(
            shape=SupportedShapes[shape.upper()],
            pitch=parameters[p["pitch"]],
            height=parameters[p["height"]],
            radius=parameters[p["radius"]],
            angle=parameters[p["angle"]],
        )
    elif shape == str(SupportedShapes.CIRCLE):
        return Parameters(
            shape=SupportedShapes[shape.upper()], radius=parameters[p["radius"]]
        )
    elif shape == str(SupportedShapes.POLYGON):
        return Parameters(shape=SupportedShapes[shape.upper()])
    else:
        raise ValueError(f"Unsupported shape type: {shape}")


def from_model_output_to_object(
    shape_prediction_vector: List[float], pose_prediction_vector: List[float]
) -> Object3D:
    """
    Convert model prediction vectors to an Object3D.

    Args:
        shape_prediction_vector (List[float]): Prediction vector for the shape parameters.
        pose_prediction_vector (List[float]): Prediction vector for the pose parameters.

    Returns:
        Object3D: The generated Object3D.
    """
    assert (
        len(shape_prediction_vector) > 0
    ), "The shape prediction vector needs to be larger than 0."
    assert (
        len(pose_prediction_vector) > 0
    ), "The pose prediction vector needs to be larger than 0."

    return Object3D(
        name=SupportedShapes(shape_prediction_vector[0]),
        parameters=shape_prediction_vector[1:],
        translation=Translation(
            x=pose_prediction_vector[0],
            y=pose_prediction_vector[1],
            z=pose_prediction_vector[2],
        ),
        rotation=RotationEuler(
            x_rad=pose_prediction_vector[3],
            y_rad=pose_prediction_vector[4],
            z_rad=pose_prediction_vector[5],
        ),
    )


def convert_params(params: List[Any]) -> List[List[float]]:
    """
    Convert a list of parameters to a consistent numerical format.

    Args:
        params (List[Any]): The parameters to convert.

    Returns:
        List[List[float]]: The converted parameters.
    """
    return [list(map(float, param)) for param in params]
