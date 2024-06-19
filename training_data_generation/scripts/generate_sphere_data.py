#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: generate_sphere_data.py
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

# Function to generate random parameters
def generate_random_parameters(size):
    radius_range = size_to_range[size]
    radius = random.uniform(*radius_range)
    return radius

# Function to create a qualitative description
def create_qualitative_description(size, radius_term):
    return f"A {size} sphere with a {radius_term}."

# Function to create a quantitative description
def create_quantitative_description(radius, radius_term):
    if radius_term == "diameter":
        radius = radius * 2  # Convert radius to diameter
    return f"A sphere with a {radius_term} of {radius:.2f} units."

# Generate dataset
dataset = []

for _ in range(args.num_datapoints):
    size = random.choice(sizes)
    radius = generate_random_parameters(size)
    radius_term = random.choice(radius_terms)
    
    if random.random() < 0.5:
        # Create qualitative description
        description = create_qualitative_description(size, radius_term)
    else:
        # Create quantitative description
        description = create_quantitative_description(radius, radius_term)
    
    # Always store CAD parameters in terms of radius
    cad_parameters = Parameters(shape=SupportedShapes.SPHERE, radius=radius)
    
    dataset.append({
        "shape": "sphere",
        "description": description,
        "cad_parameters": cad_parameters.to_list()
    })

# Save to JSON file
with open('sphere_dataset.json', 'w') as f:
    json.dump(dataset, f, indent=4)