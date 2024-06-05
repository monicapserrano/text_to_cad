"""
Filename: generate_sphere_data.py
Author: Monica Perez Serrano

Description: Script to generate training data for the model.

"""
import json
import random

from text_to_cad_common.geometric_primitives import SupportedShapes


# Define sizes and their qualitative descriptions
sizes = ["small", "medium", "large"]
size_to_range = {
    "small": (1, 3),
    "medium": (4, 6),
    "large": (7, 10)
}

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

for _ in range(1000000):
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
    cad_parameters = [SupportedShapes.SPHERE.value, radius, 0.0]
    
    dataset.append({
        "shape": "sphere",
        "description": description,
        "cad_parameters": cad_parameters
    })

# Save to JSON file
with open('sphere_dataset.json', 'w') as f:
    json.dump(dataset, f, indent=4)