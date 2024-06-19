#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: generate_torus_data.py
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

# Different ways to say "major radius" and "minor radius"
major_radius_terms = ["major radius", "outer radius"]
minor_radius_terms = ["minor radius", "inner radius"]

# Function to generate random parameters
def generate_random_parameters(size):
    size_range = size_to_range[size]
    major_radius = random.uniform(*size_range)
    minor_radius = random.uniform(1, major_radius - 0.1)  # Ensuring minor_radius < major_radius
    return major_radius, minor_radius

# Function to create a qualitative description
def create_qualitative_description(size, major_radius_term, minor_radius_term):
    return f"A {size} torus with a {major_radius_term} and a {minor_radius_term}."

# Function to create a quantitative description
def create_quantitative_description(major_radius, major_radius_term, minor_radius, minor_radius_term):
    return f"A torus with a {major_radius_term} of {major_radius:.2f} units and a {minor_radius_term} of {minor_radius:.2f} units."

# Generate dataset
dataset = []

for _ in range(args.num_datapoints):
    size = random.choice(sizes)
    major_radius, minor_radius = generate_random_parameters(size)
    major_radius_term = random.choice(major_radius_terms)
    minor_radius_term = random.choice(minor_radius_terms)

    if random.random() < 0.5:
        # Create qualitative description
        description = create_qualitative_description(size, major_radius_term, minor_radius_term)
    else:
        # Create quantitative description
        description = create_quantitative_description(
            major_radius, major_radius_term, minor_radius, minor_radius_term
        )

    # Always store CAD parameters in terms of major radius and minor radius
    cad_parameters = Parameters(
        shape=SupportedShapes.TORUS, radius1=major_radius, radius2=minor_radius
    )

    dataset.append(
        {
            "shape": "torus",
            "description": description,
            "cad_parameters": cad_parameters.to_list(),
        }
    )

# Save to JSON file
with open("torus_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)
