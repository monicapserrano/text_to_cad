#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: generate_helix_data.py
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

# Different ways to say "pitch", "height", "radius", and "angle"
pitch_terms = ["pitch"]
height_terms = ["height"]
radius_terms = ["radius"]
angle_terms = ["angle"]

# Function to generate random parameters
def generate_random_parameters(size):
    size_range = size_to_range[size]
    pitch = random.uniform(*size_range)
    height = random.uniform(*size_range)
    radius = random.uniform(*size_range)
    angle = random.uniform(0, 360)  # Angle in degrees
    return pitch, height, radius, angle

# Function to create a qualitative description
def create_qualitative_description(size, pitch_term, height_term, radius_term, angle_term):
    return f"A {size} helix with a {pitch_term}, {height_term}, {radius_term}, and {angle_term}."

# Function to create a quantitative description
def create_quantitative_description(pitch, pitch_term, height, height_term, radius, radius_term, angle, angle_term):
    return f"A helix with a {pitch_term} of {pitch:.2f} units, a {height_term} of {height:.2f} units, a {radius_term} of {radius:.2f} units, and an {angle_term} of {angle:.2f} degrees."

# Generate dataset
dataset = []

for _ in range(args.num_datapoints):
    size = random.choice(sizes)
    pitch, height, radius, angle = generate_random_parameters(size)
    pitch_term = random.choice(pitch_terms)
    height_term = random.choice(height_terms)
    radius_term = random.choice(radius_terms)
    angle_term = random.choice(angle_terms)

    if random.random() < 0.5:
        # Create qualitative description
        description = create_qualitative_description(size, pitch_term, height_term, radius_term, angle_term)
    else:
        # Create quantitative description
        description = create_quantitative_description(
            pitch, pitch_term, height, height_term, radius, radius_term, angle, angle_term
        )

    # Always store CAD parameters in terms of pitch, height, radius, and angle
    cad_parameters = Parameters(
        shape=SupportedShapes.HELIX, pitch=pitch, height=height, radius=radius, angle=angle
    )

    dataset.append(
        {
            "shape": "helix",
            "description": description,
            "cad_parameters": cad_parameters.to_list(),
        }
    )

# Save to JSON file
with open("helix_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)
