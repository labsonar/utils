"""
Utility Module

This module provides utility functions for general proposes.
"""
import random
import os
import numpy as np

def set_seed():
    """ Set random seed for reproducibility. """
    seed = 42
    random.seed(seed)
    np.random.seed(seed)


def find_files(current_directory='.', extension = ".wav"):
    wav_files = []

    for root, _, files in os.walk(current_directory):
        for file in files:
            if file.endswith(extension):
                wav_files.append(os.path.join(root, file))

    return wav_files