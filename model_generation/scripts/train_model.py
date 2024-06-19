#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
Filename: train_model.py
Author: Monica Perez Serrano

Description: This script generates a model to predict the shape and CAD 
             parameters given a text input.

"""

import argparse
import json
import logging as log
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import yaml

from text_to_cad_common.cad_parameter_predictor import CADParameterPredictor
from text_to_cad_common.common import (
    evaluate,
    preprocess_description,
    train,
    split_string,
)
from text_to_cad_common.parameter_tools import from_list_to_parameter, convert_params


if __name__ == "__main__":
    """
    Main function for training the CAD parameter predictor model.
    """
    logger = log.getLogger()
    logger.setLevel(log.DEBUG)
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "--datasets-dir",
        required=True,
        type=str,
        help="Directory with all datasets to train the model.",
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
        help="File to save the vectorizer.",
    )

    optional.add_argument(
        "--config-file",
        required=False,
        type=str,
        default="config.yaml",
        help="File to save the model configuration.",
    )
    optional.add_argument(
        "--num-epochs",
        required=False,
        type=int,
        default=5,
        help="Number of iterations/epochs.",
    )
    optional.add_argument(
        "--batch-size",
        required=False,
        type=int,
        default=32,
        help="Batch size for model training.",
    )
    optional.add_argument(
        "--hidden-dimension",
        required=False,
        type=int,
        default=128,
        help="Hidden dimension for the model.",
    )
    optional.add_argument(
        "--retrain",
        required=False,
        action='store_true',
        help="Flag to indicate retraining with additional data.",
    )

    args = parser.parse_args()

    assert Path(
        args.datasets_dir
    ).exists(), (
        f"[train_model] The dataset directory {args.datasets_dir} does not exist."
    )

    # Load dataset
    log.debug("[train_model] Loading datasets")
    dataset: List[Dict[str, Any]] = []
    for file_path in Path(args.datasets_dir).iterdir():
        if file_path.is_file():
            with open(file_path, "r") as f:
                dataset += json.load(f)
                log.debug(
                    f"[train_model] Loaded data from {file_path}. Current data entries: {len(dataset)}"
                )

    assert (
        len(dataset) > 0
    ), f"[train_model] The input dataset from {args.datasets_dir} to train the model is empty!"

    processed_dataset: List[Dict[str, Any]] = []
    for entry in dataset:
        new_params = from_list_to_parameter(
            shape=entry["shape"], parameters=entry["cad_parameters"]
        ).to_list()
        processed_entry = entry.copy()
        processed_entry["cad_parameters"] = new_params
        processed_dataset.append(processed_entry)

    # Create a DataFrame
    log.debug("[train_model] Creating the database")
    df = pd.DataFrame(processed_dataset)

    # Split DataFrame into train and test sets
    train_df, test_df = train_test_split(df, test_size=0.2)

    y_train_params = convert_params(train_df["cad_parameters"])
    y_test_params = convert_params(test_df["cad_parameters"])

    # Determine the length of cad_parameters
    param_length = len(y_train_params[0])

    # TODO: Check that all parameters have the same length

    # Convert to numpy arrays
    y_train_params = np.array(y_train_params, dtype=np.float32)
    y_test_params = np.array(y_test_params, dtype=np.float32)

    # Apply preprocessing to the descriptions
    train_df["processed_description"] = train_df["description"].apply(
        preprocess_description
    )
    test_df["processed_description"] = test_df["description"].apply(
        preprocess_description
    )

    if args.retrain and Path(args.vectorizer_file).exists():
        with open(args.vectorizer_file, "rb") as f:
            vectorizer = pickle.load(f)
    else:
        vectorizer = CountVectorizer(tokenizer=split_string, lowercase=True)
        vectorizer.fit(train_df["processed_description"])

    # Preprocess text data
    X_train = vectorizer.fit_transform(train_df["processed_description"])
    X_test = vectorizer.transform(test_df["processed_description"])

    with open(args.vectorizer_file, "wb") as f:
        pickle.dump(vectorizer, f)
    log.info(f"[train_model] Vectorizer saved to {args.vectorizer_file}")

    # Convert to PyTorch sparse tensors
    def to_sparse_tensor(sparse_matrix):
        coo = sparse_matrix.tocoo()
        values = coo.data
        indices = np.vstack((coo.row, coo.col))
        i = torch.tensor(indices, dtype=torch.int64)
        v = torch.tensor(values, dtype=torch.float32)
        shape = coo.shape
        return torch.sparse.FloatTensor(i, v, torch.Size(shape))

    X_train = to_sparse_tensor(X_train).to_dense()
    X_test = to_sparse_tensor(X_test).to_dense()
    y_train_params = torch.tensor(y_train_params, dtype=torch.float32)
    y_test_params = torch.tensor(y_test_params, dtype=torch.float32)

    # Model parameters
    input_dim = X_train.shape[1]
    hidden_dim = args.hidden_dimension
    output_dim = param_length  # Predicting the maximum number of parameters

    log.info(
        f"Model dimensions: INPUT DIM - {input_dim}, HIDDEN_DIM - {hidden_dim}, OUTPUT DIM - {output_dim}."
    )

    # Instantiate the model
    model_predictor = CADParameterPredictor(input_dim, hidden_dim, output_dim)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model_predictor.to(device)

    if args.retrain and Path(args.model_file).exists():
        model.load_state_dict(torch.load(args.model_file))
        log.info(f"[train_model] Model loaded from {args.model_file}")


    # Define optimizer and loss function
    optimizer = optim.Adam(model.parameters())
    criterion = nn.MSELoss()

    # Training loop
    n_epochs = args.num_epochs
    batch_size = args.batch_size

    for epoch in range(n_epochs):
        train_loss = train(
            model, X_train, y_train_params, optimizer, criterion, device, batch_size
        )
        valid_loss = evaluate(model, X_test, y_test_params, criterion, batch_size)

        log.info(
            f"[train_model] Epoch: {epoch+1:02}, Train Loss: {train_loss:.3f}, Val. Loss: {valid_loss:.3f}"
        )

    # Save the parameters to a YAML file
    with open(args.config_file, "w") as file:
        params = {
            "input_dim": input_dim,
            "hidden_dim": hidden_dim,
            "output_dim": output_dim,
        }
        yaml.dump(params, file)

    # Save the trained model
    torch.save(model.state_dict(), args.model_file)
    log.info(f"[train_model] Model saved to {args.model_file}")
