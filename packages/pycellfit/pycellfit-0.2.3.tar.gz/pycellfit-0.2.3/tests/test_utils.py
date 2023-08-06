"""
    This file contains test cases for pycellfit/utils.py file
"""

import unittest

import pycellfit


class TestUtils(unittest.TestCase):
    """
        This class contains test cases for the functions in pycellfit/utils.py
    """

    def test_read_segmented_image(self):
        array = pycellfit.utils.read_segmented_image('tests/images/hex.tif')

        # Case 1
        self.assertEqual(array[0, 0], 0)


if __name__ == "__main__":
    unittest.main()
