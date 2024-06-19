#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: generate_cylinder_data.py
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

# Different ways to say "radius"
radius_terms = ["radius", "diameter"]

# Different ways to say "height" or "tall"
height_terms = ["height", "tall"]


# Function to generate random parameters
def generate_random_parameters(size):
    radius_range = size_to_range[size]
    radius = random.uniform(*radius_range)
    height = random.uniform(*radius_range)
    return radius, height


# Function to create a qualitative description
def create_qualitative_description(size, radius_term, height_term):
    return f"A {size} cylinder with a {radius_term} and {height_term}."


# Function to create a quantitative description
def create_quantitative_description(radius, radius_term, height, height_term):
    if radius_term == "diameter":
        radius = radius * 2  # Convert radius to diameter
    return f"A cylinder with a {radius_term} of {radius:.2f} units and {height_term} of {height:.2f} units."


# Generate dataset
dataset = []

for _ in range(args.num_datapoints):
    size = random.choice(sizes)
    radius, height = generate_random_parameters(size)
    radius_term = random.choice(radius_terms)
    height_term = random.choice(height_terms)

    if random.random() < 0.5:
        # Create qualitative description
        description = create_qualitative_description(size, radius_term, height_term)
    else:
        # Create quantitative description
        description = create_quantitative_description(
            radius, radius_term, height, height_term
        )

    # Always store CAD parameters in terms of radius and height
    cad_parameters = Parameters(
        shape=SupportedShapes.CYLINDER, radius=radius, height=height
    )

    dataset.append(
        {
            "shape": "cylinder",
            "description": description,
            "cad_parameters": cad_parameters.to_list(),
        }
    )

# Save to JSON file
with open("cylinder_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)
