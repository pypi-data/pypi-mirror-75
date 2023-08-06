"""
    Module contain base class and common methods for model wrappers
"""

from abc import abstractmethod
import numpy as np

class BaseModelWrapper():
    """
        Base class for model wrappers
    """
    def __init__(self):
        pass

    @abstractmethod
    def predict(self, data: np.array) -> dict:
        """ Make model predict on data

        Parameters
        ----------
        data : np.array
            Data sample or batch of samples

        Returns
        -------
        dict
            Models' predict
        """
        return None
