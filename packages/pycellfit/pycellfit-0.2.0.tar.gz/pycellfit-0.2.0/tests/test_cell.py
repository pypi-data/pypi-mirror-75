"""
    This file contains test cases for pycellfit/cell.py file
"""

import unittest

from pycellfit.cell import Cell


class TestUtils(unittest.TestCase):
    """
        This class contains test cases for the functions describing the cell class
    """

    def test_constructor_and_label(self):
        # Case 1: first cell should have label of 0
        cell_0 = Cell(0)
        self.assertEqual(cell_0.label, 0)

        # Case 2: subsequent cell labels should auto-increment
        cell_1 = Cell(1)
        self.assertEqual(cell_1.label, 1)

    def test_eq(self):
        cell_0 = Cell(0)
        cell_1 = Cell(0)
        s = {cell_0, cell_1}
        self.assertEqual(len(s), 1)

    def test_add_remove_cells(self):
        s = set()
        s.add(Cell(0))
        self.assertEqual(len(s), 1)
        s.remove(Cell(0))
        self.assertEqual(len(s), 0)

    def test_add_edge_point_to_cell_in_set(self):
        s = set()
        s.add(Cell(0))
        for cell in s:
            if cell.label == 0:
                cell.add_edge_point((0, 1), 1)

        for cell in s:
            if cell.label == 0:
                self.assertEqual(cell.number_of_edge_points, 1)

if __name__ == "__main__":
    unittest.main()
