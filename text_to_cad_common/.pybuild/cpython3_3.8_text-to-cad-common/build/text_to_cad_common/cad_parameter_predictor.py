"""
Filename: cad_parameter_predictor.py
Author: Monica Perez Serrano

Description: CADParameterPredictor class used by the network model.

"""

import torch.nn as nn
from torch import Tensor

class CADParameterPredictor(nn.Module):
    """
    A neural network model for predicting CAD parameters from input data.

    This model consists of two fully connected (linear) layers with ReLU activation 
    in between. It takes an input tensor, processes it through the layers, and outputs 
    a tensor representing the predicted CAD parameters.

    Attributes:
        fc1 (nn.Linear): The first fully connected layer.
        relu (nn.ReLU): The ReLU activation function.
        fc2 (nn.Linear): The second fully connected layer.

    Methods:
        forward(x: Tensor) -> Tensor:
            Defines the forward pass of the model. Takes an input tensor `x` and 
            returns the output tensor after processing through the network.
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        """
        Initializes the CADParameterPredictor model.

        Args:
            input_dim (int): The number of input features.
            hidden_dim (int): The number of features in the hidden layer.
            output_dim (int): The number of output features (predicted CAD parameters).
        """
        super(CADParameterPredictor, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: Tensor) -> Tensor:
        """
        Defines the forward pass of the model.

        Args:
            x (Tensor): The input tensor.

        Returns:
            Tensor: The output tensor after being processed by the network.
        """
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
