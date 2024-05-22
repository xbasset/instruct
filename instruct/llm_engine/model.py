from abc import ABC, abstractmethod
import json
import logging
import os

logging.basicConfig(level=logging.ERROR)


class Model(ABC):
    """
    Abstract base class for Model implementations.
    """

    @abstractmethod
    def __init__(self, model_conf):
        """
        Initializes the model object.

        Args:
            model_conf (dict): The configuration for the model.
        """
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def invoke(self, messages, temperature, max_tokens):
        """
        Perform a Model chat completion.

        Args:
            messages (list): List of messages.
            temperature (float): Temperature parameter for generating responses.
            max_tokens (int): Maximum number of tokens in the generated response.

        Returns:
            None
        """
        pass

    @abstractmethod
    def invoke_from_pt(self, pt, temperature, max_tokens):
        """
        Perform a Model chat completion using the provided PT.

        Args:
            pt (PT): The PT object.
            temperature (float): Temperature parameter for generating responses.
            max_tokens (int): Maximum number of tokens in the generated response.

        Returns:
            None
        """
        pass

    @abstractmethod
    def chatCompletion(self, *args, **kwargs):
        """
        Abstract method that should be implemented to handle chat completions. The parameters for each subclass that
        implements this method may vary, hence the use of *args and **kwargs to accept any number of arguments.
        """
        pass
