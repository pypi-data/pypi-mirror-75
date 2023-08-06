"""test cases for segmentation_transform_utils functions"""

import unittest

import numpy as np

import pycellfit.segmentation_transform_utils


class TestUtils(unittest.TestCase):
    """
        This class contains test cases for the functions in pycellfit/segmentation_tranform_utils.py
    """

    def test_fill_region(self):
        # Case 1: interior region
        array = np.array([(1, 1, 1, 1, 1, 1, 1, 1),
                          (1, 1, 1, 1, 1, 1, 0, 0),
                          (1, 0, 0, 1, 1, 0, 1, 1),
                          (1, 2, 2, 2, 2, 0, 1, 0),
                          (1, 1, 1, 2, 2, 0, 1, 0),
                          (1, 1, 1, 2, 2, 2, 2, 0),
                          (1, 1, 1, 1, 1, 2, 1, 1),
                          (1, 1, 1, 1, 1, 2, 2, 1)])
        pycellfit.segmentation_transform_utils.fill_region(array, (4, 4), 3)
        expected_result = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1, 1, 0, 0],
                                    [1, 0, 0, 1, 1, 0, 1, 1],
                                    [1, 3, 3, 3, 3, 0, 1, 0],
                                    [1, 1, 1, 3, 3, 0, 1, 0],
                                    [1, 1, 1, 3, 3, 3, 3, 0],
                                    [1, 1, 1, 1, 1, 3, 1, 1],
                                    [1, 1, 1, 1, 1, 3, 3, 1]])

        self.assertIsNone(np.testing.assert_array_equal(array, expected_result))

        # Case 2: corner region
        array = np.array([[0, 0, 1, 1],
                          [1, 1, 1, 1],
                          [2, 2, 2, 3]])
        pycellfit.segmentation_transform_utils.fill_region(array, (0, 0), 2)
        expected_result = np.array([[2, 2, 1, 1],
                                    [1, 1, 1, 1],
                                    [2, 2, 2, 3]])
        self.assertIsNone(np.testing.assert_array_equal(array, expected_result))

        # Case 3: single pixel region
        array = np.array([[0, 1, 1, 1],
                          [1, 1, 1, 1],
                          [2, 2, 2, 3]])
        pycellfit.segmentation_transform_utils.fill_region(array, (0, 0), 2)
        expected_result = np.array([[2, 1, 1, 1],
                                    [1, 1, 1, 1],
                                    [2, 2, 2, 3]])
        self.assertIsNone(np.testing.assert_array_equal(array, expected_result))


class PadWith(unittest.TestCase):
    def test_pad_outer(self):
        a = np.zeros((2, 2))
        padded_array = np.pad(a, 1, pycellfit.segmentation_transform_utils.pad_with)

        # Test 1: outer edge is -1
        self.assertEqual(padded_array[0, 0], -1)

    def test_pad_inner(self):
        a = np.zeros((2, 2))
        padded_array = np.pad(a, 1, pycellfit.segmentation_transform_utils.pad_with)

        # Test 2: inner array is not changed
        self.assertEqual(padded_array[1, 1], 0)


if __name__ == "__main__":
    unittest.main()
