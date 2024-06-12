"""
Filename: common.py
Author: Monica Perez Serrano

Description: Functions used by the different packages contained in the text_to_cad repo.

"""

import re
import torch
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def preprocess_description(description: str) -> str:
    """
    Preprocesses a CAD description by extracting numerical values and relevant keywords.

    Args:
        description (str): The input CAD description as a string.

    Returns:
        str: A combined representation of numerical values and keywords extracted from the description.
    """
    # Extract numerical values
    numerical_values = re.findall(r"\d+\.?\d*", description)
    numerical_values = [float(num) for num in numerical_values]

    # Extract relevant keywords
    keywords = re.findall(
        r"\b(plane|box|cylinder|cone|sphere|ellipsoid|torus|prism|"
        r"wedge|helix|spiral|circle|ellipse|point|line|polygon|radius|"
        r"height|tall|diameter|width|length|units|angle|degrees|radians|"
        r"pitch)\b",
        description.lower(),
    )

    # Create a combined representation (numerical values + keywords)
    combined = " ".join(keywords) + " " + " ".join(map(str, numerical_values))

    return combined


def train(
    model: torch.nn.Module,
    X_train: torch.Tensor,
    y_train_params: torch.Tensor,
    optimizer: torch.optim.Optimizer,
    criterion: torch.nn.Module,
    device: torch.device,
    batch_size: int = 32,
) -> float:
    """
    Trains the model for one epoch.

    Args:
        model (torch.nn.Module): The neural network model to train.
        X_train (torch.Tensor): Training data features.
        y_train_params (torch.Tensor): Training data labels.
        optimizer (torch.optim.Optimizer): Optimizer for the model.
        criterion (torch.nn.Module): Loss function.
        batch_size (int, optional): Batch size for training. Defaults to 32.

    Returns:
        float: The average loss over the epoch.
    """
    model.train()
    epoch_loss = 0
    num_batches = len(X_train) // batch_size

    for i in range(num_batches):
        optimizer.zero_grad()
        start_idx = i * batch_size
        end_idx = start_idx + batch_size

        X_batch = X_train[start_idx:end_idx].to(device)
        y_params_batch = y_train_params[start_idx:end_idx].to(device)

        params_pred = model(X_batch)
        loss = criterion(params_pred, y_params_batch)

        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    return epoch_loss / num_batches


def evaluate(
    model: torch.nn.Module,
    X_test: torch.Tensor,
    y_test_params: torch.Tensor,
    criterion: torch.nn.Module,
    batch_size: int = 32,
) -> float:
    """
    Evaluates the model on the test data.

    Args:
        model (torch.nn.Module): The neural network model to evaluate.
        X_test (torch.Tensor): Test data features.
        y_test_params (torch.Tensor): Test data labels.
        criterion (torch.nn.Module): Loss function.
        batch_size (int, optional): Batch size for evaluation. Defaults to 32.

    Returns:
        float: The average loss over the evaluation.
    """
    model.eval()
    epoch_loss = 0
    num_batches = len(X_test) // batch_size

    with torch.no_grad():
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = start_idx + batch_size

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            X_batch = X_test[start_idx:end_idx].to(device)
            y_params_batch = y_test_params[start_idx:end_idx].to(device)

            params_pred = model(X_batch)
            loss = criterion(params_pred, y_params_batch)

            epoch_loss += loss.item()

    return epoch_loss / num_batches


def predict(
    model: torch.nn.Module,
    description: str,
    vectorizer: CountVectorizer,
    device: torch.device,
) -> np.ndarray:
    """
    Makes a prediction for CAD parameters based on the input description.

    Args:
        model (torch.nn.Module): The trained neural network model.
        description (str): The input CAD description as a string.
        vectorizer (CountVectorizer): The vectorizer used for text preprocessing.
        device (torch.device): The device to run the model on (CPU or GPU).

    Returns:
        np.ndarray: The predicted CAD parameters.
    """
    processed_description = preprocess_description(description)
    indexed = vectorizer.transform([processed_description]).toarray()
    tensor = torch.tensor(indexed, dtype=torch.float32).to(device)

    with torch.no_grad():
        params_pred = model(tensor)

    return abs(params_pred.cpu().numpy())

def split_string(input: str) -> str:
    return input.split()
