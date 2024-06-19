#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: generate_box_and_cube_data.py
Author: Monica Perez Serrano

Description: Script to generate training data for the model.

"""
import argparse
import json
import random

from text_to_cad_common.geometric_primitives import SupportedShapes
from text_to_cad_common.parameter_tools import Parameters

# TODO(@monicapserrano) Abstract common functions

parser = argparse.ArgumentParser()
optional = parser.add_argument_group("optional arguments")

optional.add_argument(
    "--num-datapoints",
    required=False,
    default=1000000,
    type=int,
    help="Number of data entries generated.",
)
args = parser.parse_args()
assert args.num_datapoints > 0, "Cannot generate a negative number of datapoints."

# Define sizes and their qualitative descriptions
sizes = ["small", "medium", "large"]
size_to_range = {"small": (1, 10), "medium": (11, 50), "large": (51, 100)}

# Different ways to say "length", "width", and "height"
length_terms = ["length"]
width_terms = ["width"]
height_terms = ["height"]


# Function to generate random parameters for a box
def generate_random_box_parameters(size):
    size_range = size_to_range[size]
    length = random.uniform(*size_range)
    width = random.uniform(*size_range)
    height = random.uniform(*size_range)
    return length, width, height


# Function to generate random parameters for a cube
def generate_random_cube_parameters(size):
    size_range = size_to_range[size]
    side = random.uniform(*size_range)
    return side, side, side


# Function to create a qualitative description
def create_qualitative_description(size, shape, length_term, width_term, height_term):
    return f"A {size} {shape} with a {length_term}, {width_term}, and {height_term}."


# Function to create a quantitative description for a box
def create_quantitative_box_description(
    length, length_term, width, width_term, height, height_term
):
    return (f"A box with a {length_term} of {length:.2f} units, a {width_term} of "
            f"{width:.2f} units, and a {height_term} of {height:.2f} units.")


# Function to create a quantitative description for a cube
def create_quantitative_cube_description(side, length_term, width_term, height_term):
    return f"A cube with a {length_term}, {width_term}, and {height_term} of {side:.2f} units."


# Generate dataset
dataset = []

for _ in range(args.num_datapoints):
    size = random.choice(sizes)
    shape = random.choice(["box", "cube"])
    if shape == "box":
        length, width, height = generate_random_box_parameters(size)
        length_term = random.choice(length_terms)
        width_term = random.choice(width_terms)
        height_term = random.choice(height_terms)

        if random.random() < 0.5:
            # Create qualitative description
            description = create_qualitative_description(
                size, shape, length_term, width_term, height_term
            )
        else:
            # Create quantitative description
            description = create_quantitative_box_description(
                length, length_term, width, width_term, height, height_term
            )

        # Store CAD parameters
        cad_parameters = Parameters(
            shape=SupportedShapes.BOX, length=length, width=width, height=height
        )
    else:  # shape == "cube"
        side = generate_random_cube_parameters(size)[0]
        length_term = random.choice(length_terms)
        width_term = random.choice(width_terms)
        height_term = random.choice(height_terms)

        if random.random() < 0.5:
            # Create qualitative description
            description = create_qualitative_description(
                size, shape, length_term, width_term, height_term
            )
        else:
            # Create quantitative description
            description = create_quantitative_cube_description(
                side, length_term, width_term, height_term
            )

        # Store CAD parameters
        cad_parameters = Parameters(
            shape=SupportedShapes.CUBE, length=side, width=side, height=side
        )

    dataset.append(
        {
            "shape": str(shape),
            "description": description,
            "cad_parameters": cad_parameters.to_list(),
        }
    )

# Save to JSON file
with open("box_and_cube_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)
