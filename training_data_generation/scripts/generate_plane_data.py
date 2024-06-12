#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: generate_plane_data.py
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

# Define sizes and their qualitative descriptions
sizes = ["small", "medium", "large"]
size_to_range = {"small": (1, 10), "medium": (11, 50), "large": (51, 100)}

# Different ways to say "width"
width_terms = ["width"]

# Different ways to say "height"
height_terms = ["height"]


# Function to generate random parameters
def generate_random_parameters(size):
    size_range = size_to_range[size]
    width = random.uniform(*size_range)
    height = random.uniform(*size_range)
    return width, height


# Function to create a qualitative description
def create_qualitative_description(size, width_term, height_term):
    return f"A {size} plane with a {width_term} and {height_term}."


# Function to create a quantitative description
def create_quantitative_description(width, width_term, height, height_term):
    return f"A plane with a {width_term} of {width:.2f} units and {height_term} of {height:.2f} units."


# Generate dataset
dataset = []

for _ in range(args.num_datapoints):
    size = random.choice(sizes)
    width, height = generate_random_parameters(size)
    width_term = random.choice(width_terms)
    height_term = random.choice(height_terms)

    if random.random() < 0.5:
        # Create qualitative description
        description = create_qualitative_description(size, width_term, height_term)
    else:
        # Create quantitative description
        description = create_quantitative_description(
            width, width_term, height, height_term
        )

    # Always store CAD parameters in terms of width and height
    cad_parameters = Parameters(
        shape=SupportedShapes.PLANE, width=width, height=height
    )

    dataset.append(
        {
            "shape": "plane",
            "description": description,
            "cad_parameters": cad_parameters.to_list(),
        }
    )

# Save to JSON file
with open("plane_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)
