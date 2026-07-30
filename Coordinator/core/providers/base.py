"""
AIOS Provider Base Class

Every provider inside AIOS must inherit
from this class.

Version 1
"""

from abc import ABC
from abc import abstractmethod


class Provider(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs):

        """
        Executes the provider.

        Every provider determines
        what execute() means.

        Search:
            execute(query)

        OCR:
            execute(image)

        Vision:
            execute(image)

        Translation:
            execute(text)
        """

        pass