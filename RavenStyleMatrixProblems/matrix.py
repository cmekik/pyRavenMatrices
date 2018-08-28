'''This module provides a class for representing key matrix properties.'''

from typing import Tuple

class MatrixStructure(object):
    '''
    A structure representing the basic properties of a matrix.

    Represents matrix size, number of alternatives, and cell aspect ratio.
    '''

    def __init__(
        self, 
        size : int = 3, 
        num_alternatives : int = 8, 
        aspect_ratio : Tuple[float, float] = (1., 1.)
    ) -> None:

        self.size = size
        self.num_alternatives = num_alternatives
        self.aspect_ratio = aspect_ratio