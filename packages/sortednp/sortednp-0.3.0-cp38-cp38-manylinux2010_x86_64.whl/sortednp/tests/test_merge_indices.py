
from abc import ABCMeta, abstractmethod
import sys
import weakref
import unittest
import numpy as np

import sortednp as snp

class MergeBase(metaclass=ABCMeta):
    """
    Define general test cases for the merge method. Sub-classes need to
    implement have to overwrite the dtype method.
    """

    def assertListAlmostEqual(self, a, b, *args, **kwds):
        """
        Check that the given lists are almost equal.
        """
        for A, B in zip(a, b):
            self.assertAlmostEqual(A, B, *args, **kwds)

    def test_assertListAlmostEqual_pass(self):
        """
        Check that assertListAlmostEqual raises no exception, if the given
        values are almost equal.
        """
        a = [0, 1, 2 + 1e-9, 10]
        b = [0, 1, 2       , 10]

        self.assertListAlmostEqual(a, b)

    def test_assertListAlmostEqual_fail(self):
        """
        Check that assertListAlmostEqual raises an exception, if the given
        values differ.
        """
        a = [0, 1, 2 + 1e-3, 10]
        b = [0, 1, 2       , 10]

        self.assertRaises(AssertionError, self.assertListAlmostEqual, a, b)
                
    @abstractmethod
    def get_dtype(self):
        """
        Returns the numpy data type, which should be used for all tests.
        """
        pass
    

    def test_simple(self):
        """
        Check that merging two non-empty arrays returns the union of the two
        arrays.
        """
        a = np.array([1, 3, 7], dtype=self.get_dtype())
        b = np.array([2, 5, 6], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, indices=True)
        self.assertEqual(list(m), [1, 2, 3, 5, 6, 7])
        self.assertEqual(m.dtype, self.get_dtype())

        self.assertEqual(list(i_a), [0, 2, 5])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [1, 3, 4])
        self.assertEqual(i_b.dtype, "intp")

    def test_separated(self):
        """
        Check that merging two non-empty arrays returns the union of the two
        arrays if all element in on array are greater than all elements in the
        other. This tests the copy parts of the implementation.
        """
        a = np.array([1, 3, 7], dtype=self.get_dtype())
        b = np.array([9, 10, 16], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, indices=True)
        self.assertEqual(list(m), [1, 3, 7, 9, 10, 16])
        self.assertEqual(m.dtype, self.get_dtype())

        self.assertEqual(list(i_a), [0, 1, 2])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [3, 4, 5])
        self.assertEqual(i_b.dtype, "intp")

    def test_empty_single(self):
        """
        Check that merging two arrays returns a copy of the first one if
        the other is empty.
        """
        a = np.array([1, 3, 7], dtype=self.get_dtype())
        b = np.array([], dtype=self.get_dtype())

        # a and b
        m, (i_a, i_b) = snp.merge(a, b, indices=True)
        self.assertEqual(list(m), [1, 3, 7])
        self.assertEqual(list(a), [1, 3, 7])
        self.assertEqual(m.dtype, self.get_dtype())
        m[0] = 0
        self.assertEqual(list(a), [1, 3, 7])

        self.assertEqual(list(i_a), [0, 1, 2])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [])
        self.assertEqual(i_b.dtype, "intp")

        # b and a
        m, (i_a, i_b) = snp.merge(b, a, indices=True)
        self.assertEqual(list(m), [1, 3, 7])
        self.assertEqual(list(a), [1, 3, 7])
        self.assertEqual(m.dtype, self.get_dtype())
        m[0] = 0
        self.assertEqual(list(a), [1, 3, 7])

        self.assertEqual(list(i_a), [])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [0, 1, 2])
        self.assertEqual(i_b.dtype, "intp")


    def test_empty_both(self):
        """
        Check that merging two empty arrays returns an empty array.
        """
        a = np.array([], dtype=self.get_dtype())
        b = np.array([], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, indices=True)
        self.assertEqual(list(m), [])
        self.assertEqual(len(m), 0)
        self.assertEqual(m.dtype, self.get_dtype())

        self.assertEqual(list(i_a), [])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [])
        self.assertEqual(i_b.dtype, "intp")


    def test_identical(self):
        """
        Check that merging two identical arrays returns each element twice.
        """
        a = np.array([1, 3, 7], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, a, indices=True)
        self.assertEqual(list(m), [1, 1, 3, 3, 7, 7])
        self.assertEqual(m.dtype, self.get_dtype())

        self.assertEqual(list(i_a), [0, 2, 4])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [1, 3, 5])
        self.assertEqual(i_b.dtype, "intp")

    def test_duplicates_same(self):
        """
        Check that duplications in a single array are passed to the result.
        """
        a = np.array([1, 3, 3, 7], dtype=self.get_dtype())
        b = np.array([2, 5, 6], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, indices=True)
        self.assertEqual(list(m), [1, 2, 3, 3, 5, 6, 7])
        self.assertEqual(m.dtype, self.get_dtype())

        self.assertEqual(list(i_a), [0, 2, 3, 6])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [1, 4, 5])
        self.assertEqual(i_b.dtype, "intp")

    def test_duplicates_other(self):
        """
        Check that duplications in the other array are passed to the result.
        """
        a = np.array([1, 3, 7], dtype=self.get_dtype())
        b = np.array([2, 3, 5, 6], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, indices=True)
        self.assertEqual(list(m), [1, 2, 3, 3, 5, 6, 7])
        self.assertEqual(m.dtype, self.get_dtype())

        self.assertEqual(list(i_a), [0, 2, 6])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [1, 3, 4, 5])
        self.assertEqual(i_b.dtype, "intp")

    def test_duplicates_both(self):
        """
        Check that duplications in a single and the other array are both passed to
        the result.
        """
        a = np.array([1, 3, 3, 7], dtype=self.get_dtype())
        b = np.array([2, 3, 5, 6], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, indices=True)
        self.assertEqual(list(m), [1, 2, 3, 3, 3, 5, 6, 7])
        self.assertEqual(m.dtype, self.get_dtype())
        
        self.assertEqual(list(i_a), [0, 2, 3, 7])
        self.assertEqual(i_a.dtype, "intp")
        self.assertEqual(list(i_b), [1, 4, 5, 6])
        self.assertEqual(i_b.dtype, "intp")

    def test_raise_multi_dim(self):
        """
        Check that passing in a multi dimensional array raises an exception.
        """
        a = np.zeros((10, 2), dtype=self.get_dtype())
        b = np.array([2, 3, 5, 6], dtype=self.get_dtype())

        self.assertRaises(ValueError, snp.merge, a, b, indices=True)
        self.assertRaises(ValueError, snp.merge, b, a, indices=True)
        self.assertRaises(ValueError, snp.merge, a, a, indices=True)
        
    def test_raise_non_array(self):
        """
        Check that passing in a non-numpy-array raises an exception.
        """
        b = np.array([2, 3, 5, 6], dtype=self.get_dtype())

        self.assertRaises(TypeError, snp.merge, 3, b, indices=True)
        self.assertRaises(TypeError, snp.merge, b, 2, indices=True)
        self.assertRaises(TypeError, snp.merge, 3, "a", indices=True)
        
    def test_reference_counting_principle(self):
        """
        Check that the reference counting works as expected with standard
        numpy arrays.
        """

        # Create inputs
        a = np.arange(10, dtype=self.get_dtype()) * 3
        b = np.arange(10, dtype=self.get_dtype()) * 2 + 5

        # Check ref count for input. Numpy arrays have two references.
        self.assertEqual(sys.getrefcount(a), 2)
        self.assertEqual(sys.getrefcount(b), 2)

        # Create weak refs for inputs
        weak_a = weakref.ref(a)
        weak_b = weakref.ref(b)

        self.assertEqual(sys.getrefcount(a), 2)
        self.assertEqual(sys.getrefcount(b), 2)
        self.assertIsNotNone(weak_a())
        self.assertIsNotNone(weak_b())

        # Delete a
        del a
        self.assertEqual(sys.getrefcount(b), 2)
        self.assertIsNone(weak_a())
        self.assertIsNotNone(weak_b())

        # Delete b
        del b
        self.assertIsNone(weak_a())
        self.assertIsNone(weak_b())

    def test_reference_counting(self):
        """
        Check that the reference counting is done correctly.
        """
        # Create inputs
        a = np.arange(10, dtype=self.get_dtype()) * 3
        b = np.arange(10, dtype=self.get_dtype()) * 2 + 5

        # Check ref count for input. Numpy arrays have two references.
        self.assertEqual(sys.getrefcount(a), 2)
        self.assertEqual(sys.getrefcount(b), 2)

        # Create weak refs for inputs
        weak_a = weakref.ref(a)
        weak_b = weakref.ref(b)

        self.assertEqual(sys.getrefcount(a), 2)
        self.assertEqual(sys.getrefcount(b), 2)
        self.assertIsNotNone(weak_a())
        self.assertIsNotNone(weak_b())

        ## Intersect
        i, (i_a, i_b) = snp.merge(a, b, indices=True)

        self.assertEqual(sys.getrefcount(a), 2)
        self.assertEqual(sys.getrefcount(b), 2)
        self.assertEqual(sys.getrefcount(i), 2)
        self.assertEqual(sys.getrefcount(i_a), 2)
        self.assertEqual(sys.getrefcount(i_b), 2)

        # Create weakrefs
        weak_i = weakref.ref(i)
        weak_i_a = weakref.ref(i_a)
        weak_i_b = weakref.ref(i_b)
        self.assertEqual(sys.getrefcount(a), 2)
        self.assertEqual(sys.getrefcount(b), 2)
        self.assertEqual(sys.getrefcount(i), 2)
        self.assertEqual(sys.getrefcount(i_a), 2)
        self.assertEqual(sys.getrefcount(i_b), 2)
        self.assertIsNotNone(weak_a())
        self.assertIsNotNone(weak_b())
        self.assertIsNotNone(weak_i())
        self.assertIsNotNone(weak_i_a())
        self.assertIsNotNone(weak_i_b())

        # Delete a
        del a
        self.assertEqual(sys.getrefcount(b), 2)
        self.assertEqual(sys.getrefcount(i), 2)
        self.assertEqual(sys.getrefcount(i_a), 2)
        self.assertEqual(sys.getrefcount(i_b), 2)
        self.assertIsNone(weak_a())
        self.assertIsNotNone(weak_b())
        self.assertIsNotNone(weak_i())
        self.assertIsNotNone(weak_i_a())
        self.assertIsNotNone(weak_i_b())

        # Delete b
        del b
        self.assertEqual(sys.getrefcount(i), 2)
        self.assertEqual(sys.getrefcount(i_a), 2)
        self.assertEqual(sys.getrefcount(i_b), 2)
        self.assertIsNone(weak_a())
        self.assertIsNone(weak_b())
        self.assertIsNotNone(weak_i())
        self.assertIsNotNone(weak_i_a())
        self.assertIsNotNone(weak_i_b())

        # Delete i
        del i
        self.assertEqual(sys.getrefcount(i_a), 2)
        self.assertEqual(sys.getrefcount(i_b), 2)
        self.assertIsNone(weak_a())
        self.assertIsNone(weak_b())
        self.assertIsNone(weak_i())
        self.assertIsNotNone(weak_i_a())
        self.assertIsNotNone(weak_i_b())

        # Delete i_a
        del i_a
        self.assertEqual(sys.getrefcount(i_b), 2)
        self.assertIsNone(weak_a())
        self.assertIsNone(weak_b())
        self.assertIsNone(weak_i())
        self.assertIsNone(weak_i_a())
        self.assertIsNotNone(weak_i_b())

        # Delete i_b
        del i_b
        self.assertIsNone(weak_a())
        self.assertIsNone(weak_b())
        self.assertIsNone(weak_i())
        self.assertIsNone(weak_i_a())
        self.assertIsNone(weak_i_b())

    def test_both_dup_w_DROP(self):
        """Check arrays with duplicates in both and DROP treatment."""
        a = np.array([1, 7, 7, 10], dtype=self.get_dtype())
        b = np.array([5, 7, 7, 7, 21], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, duplicates=snp.DROP, indices=True)
        self.assertEqual(list(m), [1, 5, 7, 10, 21])
        self.assertEqual(list(i_a), [0, 2, 2, 3])
        self.assertEqual(list(i_b), [1, 2, 2, 2, 4])

    def test_both_dup_w_DROP_IN_INPUT(self):
        """Check arrays with duplicates in both and DROP_IN_INPUT treatment."""
        a = np.array([1, 7, 7, 10], dtype=self.get_dtype())
        b = np.array([5, 7, 7, 7, 21], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, duplicates=snp.DROP_IN_INPUT,
                                  indices=True)
        self.assertEqual(list(m), [1, 5, 7, 7, 10, 21])
        self.assertEqual(list(i_a), [0, 2, 2, 4])
        self.assertEqual(list(i_b), [1, 3, 3, 3, 5])

    def test_both_dup_w_KEEP(self):
        """Check arrays with duplicates in both and KEEP treatment."""
        a = np.array([1, 7, 7, 10], dtype=self.get_dtype())
        b = np.array([5, 7, 7, 7, 21], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, duplicates=snp.KEEP, indices=True)
        self.assertEqual(list(m), [1, 5, 7, 7, 7, 7, 7, 10, 21])
        self.assertEqual(list(i_a), [0, 2, 3, 7])
        self.assertEqual(list(i_b), [1, 4, 5, 6, 8])

    def test_dub_single_w_DROP(self):
        """Check merging duplicated with an empty array and DROP"""
        a = np.array([1, 2, 7, 7, 7, 9], dtype=self.get_dtype())
        b = np.array([], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, duplicates=snp.DROP, indices=True)
        self.assertEqual(list(m), [1, 2, 7, 9])
        self.assertEqual(list(i_a), [0, 1, 2, 2, 2, 3])
        self.assertEqual(list(i_b), [])

        m, (i_b, i_a) = snp.merge(b, a, duplicates=snp.DROP, indices=True)
        self.assertEqual(list(m), [1, 2, 7, 9])
        self.assertEqual(list(i_a), [0, 1, 2, 2, 2, 3])
        self.assertEqual(list(i_b), [])

    def test_dub_single_w_DROP_IN_INPUT(self):
        """Check merging duplicated with an empty array and DROP_IN_INPUT"""
        a = np.array([1, 2, 7, 7, 7, 9], dtype=self.get_dtype())
        b = np.array([], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, duplicates=snp.DROP_IN_INPUT,
                                  indices=True)
        self.assertEqual(list(m), [1, 2, 7, 9])
        self.assertEqual(list(i_a), [0, 1, 2, 2, 2, 3])
        self.assertEqual(list(i_b), [])

        m, (i_b, i_a) = snp.merge(b, a, duplicates=snp.DROP_IN_INPUT,
                                  indices=True)
        self.assertEqual(list(m), [1, 2, 7, 9])
        self.assertEqual(list(i_a), [0, 1, 2, 2, 2, 3])
        self.assertEqual(list(i_b), [])

    def test_dub_single_w_KEEP(self):
        """Check merging duplicated with an empty array and KEEP"""
        a = np.array([1, 2, 7, 7, 7, 9], dtype=self.get_dtype())
        b = np.array([], dtype=self.get_dtype())

        m, (i_a, i_b) = snp.merge(a, b, duplicates=snp.KEEP, indices=True)
        self.assertEqual(list(m), [1, 2, 7, 7, 7, 9])
        self.assertEqual(list(i_a), [0, 1, 2, 3, 4, 5])
        self.assertEqual(list(i_b), [])

        m, (i_b, i_a) = snp.merge(b, a, duplicates=snp.KEEP, indices=True)
        self.assertEqual(list(m), [1, 2, 7, 7, 7, 9])
        self.assertEqual(list(i_a), [0, 1, 2, 3, 4, 5])
        self.assertEqual(list(i_b), [])


class MergeTestCase_Double(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'float64'

class MergeTestCase_Float(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'float32'

class MergeTestCase_Int8(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'int8'

class MergeTestCase_Int16(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'int16'

class MergeTestCase_Int32(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'int32'

class MergeTestCase_Int64(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'int64'
        self.assertEqual(m.dtype, self.get_dtype())
 
class MergeTestCase_UInt8(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'uint8'

class MergeTestCase_UInt16(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'uint16'

class MergeTestCase_UInt32(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'uint32'

class MergeTestCase_UInt64(MergeBase, unittest.TestCase):
    def get_dtype(self):
        return 'uint64'
