#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: run_text_to_cad.py
Author: Monica Perez Serrano

Description: This script generates a CAD part based on a text description using a trained neural network model.

Usage:
    python run_text_to_cad.py --text-input "A small cylinder" --output-file output.fcstd

Arguments:
    --text-input: The text description to generate a CAD part (e.g., "A small cylinder").
    --output-file: The name of the CAD file that will be generated.
    --model-file: The path to the trained model (default: model.pth).
    --vectorizer-file: The path to the vectorizer used for text preprocessing (default: vectorizer.pkl).
    --config-file: The path to the YAML file with model dimensions, which should match the ones used during training (default: config_file.yaml).
"""

import argparse
import logging as log
import torch
from pathlib import Path
import pickle
import subprocess
import yaml

from generative_cad.freecad_tools import generate_freecad_file
from text_to_cad_common.cad_parameter_predictor import CADParameterPredictor
from text_to_cad_common.common import predict, split_string
from text_to_cad_common.parameter_tools import from_model_output_to_object


if __name__ == "__main__":
    logger = log.getLogger()
    logger.setLevel(log.DEBUG)
    log.info("[run_text_to_cad] Starting...")

    parser = argparse.ArgumentParser()
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    required.add_argument(
        "--text-input",
        required=True,
        type=str,
        help="Text to generate a CAD part (E.g. A small cylinder).",
    )

    required.add_argument(
        "--output-file",
        required=True,
        type=str,
        help="Name of the CAD file that will be generated.",
    )
    optional.add_argument(
        "--model-file",
        required=False,
        default="model.pth",
        type=str,
        help="Trained model.",
    )

    optional.add_argument(
        "--vectorizer-file",
        required=False,
        type=str,
        default="vectorizer.pkl",
        help="Vectorizer used for text preprocessing.",
    )

    optional.add_argument(
        "--config-file",
        required=False,
        type=str,
        default="config_file.yaml",
        help="YAML file with model dimensions, which "
        "should match the ones used during training.",
    )

    args = parser.parse_args()

    # Check that the model and vectorizer files exist
    assert Path(args.model_file).exists(), (
        f"[run_text_to_cad] The model file {args.model_file} does not exist."
    )
    assert Path(args.vectorizer_file).exists(), (
        f"[run_text_to_cad] The vectorizer file {args.vectorizer_file} does not exist."
    )
    assert Path(args.config_file).exists(), (
        f"[run_text_to_cad] The config file {args.config_file} does not exist."
    )

    # Load configuration from YAML file
    with open(args.config_file, "r") as file:
        config = yaml.safe_load(file)
        input_dim = config["input_dim"]
        hidden_dim = config["hidden_dim"]
        output_dim = config["output_dim"]

    model = CADParameterPredictor(input_dim, hidden_dim, output_dim)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(args.model_file, map_location=device))
    model.to(device)
    model.eval()

    with open(args.vectorizer_file, "rb") as f:
        vectorizer = pickle.load(f)

    shape_prediction_params = predict(model, args.text_input, vectorizer, device)[0]
    log.info(f"[run_text_to_cad] Predicted CAD shape parameters: {shape_prediction_params}")
    log.info(f"[run_text_to_cad] Translation and Rotation are not yet supported.")
    pose_prediction_vector = [0] * 6

    # Call CAD generation
    # Currently it is only supported to generate one object at a time with no rotation nor translation
    generate_freecad_file(
        objects=[
            from_model_output_to_object(shape_prediction_params, pose_prediction_vector)
        ],
        output_file=args.output_file,
    )
    log.info(
        f"[run_text_to_cad] Finished! You can now open the {args.output_file} in FreeCAD. "
        "Remember to click on the object + Space Bar to make it visible."
    )

    subprocess.run(["freecad", args.output_file], check=True)
