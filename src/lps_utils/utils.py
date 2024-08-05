"""
Utility Module

This module provides utility functions for general proposes.
"""
import random
import numpy as np

def set_seed():
    """ Set random seed for reproducibility. """
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
