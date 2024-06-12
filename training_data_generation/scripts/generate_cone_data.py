#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: generate_cone_data.py
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

# Different ways to say "base radius" and "top radius"
base_radius_terms = ["base radius", "base diameter"]
top_radius_terms = ["top radius", "top diameter"]
height_terms = ["height"]

# Function to generate random parameters
def generate_random_parameters(size):
    size_range = size_to_range[size]
    base_radius = random.uniform(*size_range)
    top_radius = random.uniform(0.1, base_radius)  # Ensuring top_radius < base_radius
    height = random.uniform(*size_range)
    return base_radius, top_radius, height

# Function to create a qualitative description
def create_qualitative_description(size, base_radius_term, top_radius_term, height_term):
    return f"A {size} cone with a {base_radius_term}, {top_radius_term}, and {height_term}."

# Function to create a quantitative description
def create_quantitative_description(base_radius, base_radius_term, top_radius, top_radius_term, height, height_term):
    if base_radius_term == "base diameter":
        base_radius = base_radius * 2  # Convert base radius to diameter
    if top_radius_term == "top diameter":
        top_radius = top_radius * 2  # Convert top radius to diameter
    return f"A cone with a {base_radius_term} of {base_radius:.2f} units, a {top_radius_term} of {top_radius:.2f} units, and a {height_term} of {height:.2f} units."

# Generate dataset
dataset = []

for _ in range(args.num_datapoints):
    size = random.choice(sizes)
    base_radius, top_radius, height = generate_random_parameters(size)
    base_radius_term = random.choice(base_radius_terms)
    top_radius_term = random.choice(top_radius_terms)
    height_term = random.choice(height_terms)

    if random.random() < 0.5:
        # Create qualitative description
        description = create_qualitative_description(size, base_radius_term, top_radius_term, height_term)
    else:
        # Create quantitative description
        description = create_quantitative_description(
            base_radius, base_radius_term, top_radius, top_radius_term, height, height_term
        )

    # Always store CAD parameters in terms of base radius, top radius, and height
    cad_parameters = Parameters(
        shape=SupportedShapes.CONE, radius1=base_radius, radius2=top_radius, height=height
    )

    dataset.append(
        {
            "shape": "cone",
            "description": description,
            "cad_parameters": cad_parameters.to_list(),
        }
    )

# Save to JSON file
with open("cone_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)
