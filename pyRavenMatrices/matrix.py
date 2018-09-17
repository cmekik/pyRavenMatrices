'''This module provides a class for representing key matrix properties.'''

from typing import Tuple


class CellStructure(object):
    """Specifies basic properties of a matrix cell."""

    def __init__(
        self, 
        cell_id: str, 
        width: int, 
        height: int, 
        horizontal_margin: int = 0,
        vertical_margin: int = 0
    ) -> None:
        """
        Initialize a cell structure.

        All dimensions assumed to be in px.

        :param cell_id: Identifying information about cell (parent matrix, 
            position etc).
        :param width: Width of cell image.
        :param height: Height of cell image.
        :param horizontal_margin: Width of horizontal margin to be left from 
            edge of cell when drawing figures.
        :param vertical_margin: Width of vertical margin to be left from edge of 
            cell when drawing figures.
        """

        self.id = cell_id
        self.width = width
        self.height = height
        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin


class MatrixStructure(object):
    """Represents basic properties of a matrix."""

    def __init__(
        self,
        name : str, 
        cell_height : int,
        cell_width : int,
        size : int = 3, 
        num_alternatives : int = 8, 
    ) -> None:

        self.name = name
        self.size = size
        self.num_alternatives = num_alternatives
        self.cell_height = cell_height
        self.cell_width = cell_width