'''This module provides a class for representing key matrix properties.'''

from typing import Tuple


class CellStructure(object):
    '''
    A structure representing the basic properties of a matrix cell.

    Represents cell height and width.
    '''

    def __init__(self, name : str, width : int, height : int) -> None:

        self.name = name
        self.width = width
        self.height = height


class MatrixStructure(object):
    '''
    A structure representing the basic properties of a matrix.

    Represents matrix size, number of alternatives, and cell structure.
    '''

    def __init__(
        self, 
        cell_height : int,
        cell_width : int,
        size : int = 3, 
        num_alternatives : int = 8, 
    ) -> None:

        self.size = size
        self.num_alternatives = num_alternatives
        self.cell_height = cell_height
        self.cell_width = cell_width