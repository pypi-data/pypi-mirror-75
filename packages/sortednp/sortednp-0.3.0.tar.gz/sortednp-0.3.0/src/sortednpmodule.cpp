// Copyright (C) 2016-2020, Frank Sauerburger
// C++ implementation of the sortednp module

#include "sortednpmodule.h"

// #define CHECK_ARRAY_BOUNDS

template <typename T>
inline T array_get(PyArrayObject* array, npy_intp index, npy_intp length) {
  #ifdef CHECK_ARRAY_BOUNDS
  if (index >= length) {
    // Causes also a python system error, but ok for debugging
    PyErr_SetString(PyExc_RuntimeError, "Array access outside array bounds");
  }
  #endif
  return static_cast<T>(PyArray_GETPTR1(array, index));
}


/**
 * Internal helper method.
 *
 * Calculate the intersection for the given arrays and the given type. The
 * method returns the pointer to the newly created output array. The first
 * parameter is used to call the templated function.
 */
template <typename T>
PyObject* intersect(PyArrayObject *a_array, PyArrayObject *b_array,
    method_t search_method, int indices, intersect_dup_t dup_treatment) {
  // Since the size of the intersection array can not be known in advance we
  // need to create an array of at least the size of the smaller array.
  npy_intp len_a = PyArray_DIMS(a_array)[0];
  npy_intp len_b = PyArray_DIMS(b_array)[0];
  npy_intp new_dim[1] = {len_a < len_b ? len_a : len_b};  // min
  if (dup_treatment == I_KEEP_MAX_N) {
    // Take the larger number, with this duplicate treatment, the intersection
    // can grow up to the sum of both
    new_dim[0] = len_a + len_b;
  }


  // Select the search function now and not during each look iteration.
  bool (*search_func)(T, PyArrayObject*, npy_intp*, const npy_intp&) = NULL;
  switch (search_method) {
    case SIMPLE:
      search_func = &simple_search;
      break;
    case BINARY:
      search_func = &binary_search;
      break;
    case GALLOPPING:
      search_func = &galloping_search;
      break;
  }

  // Creating the new array sets the reference counter to 1 and passes the
  // ownership of the returned reference to the caller. The method steals the
  // type descriptor, which is why we have to increment its count before
  // calling the method.
  PyArray_Descr* type = PyArray_DESCR(a_array);
  Py_INCREF(type);

  PyObject *out;
  out = PyArray_SimpleNewFromDescr(1, new_dim, type);
  if (out == NULL) {
    // Probably a memory error occurred.
    return NULL;
  }
  PyArrayObject *out_array = reinterpret_cast<PyArrayObject*>(out);

  PyObject *indices_a = NULL;
  PyObject *indices_b = NULL;
  PyArrayObject *indices_a_array = NULL;
  PyArrayObject *indices_b_array = NULL;
  if (indices != 0) {
    indices_a = PyArray_SimpleNew(1, new_dim, NPY_INTP);
    if (indices_a == NULL) {
      // Probably a memory error occurred.
      Py_XDECREF(out);

      // Save to exit, intermediate objects deleted.
      return NULL;
    }
    indices_a_array = reinterpret_cast<PyArrayObject*>(indices_a);

    indices_b = PyArray_SimpleNew(1, new_dim, NPY_INTP);
    if (indices_b == NULL) {
      // Probably a memory error occurred.
      Py_XDECREF(out);
      Py_XDECREF(indices_a);

      // Save to exit, intermediate objects deleted.
      return NULL;
    }
    indices_b_array = reinterpret_cast<PyArrayObject*>(indices_b);
  }

  npy_intp i_a = 0;
  npy_intp i_b = 0;
  npy_intp i_o = 0;

  T prev = 0;
  bool has_prev = false;

  // Actual computation of the intersection.
  while (i_a < len_a && i_b < len_b) {
    T v_a = *(array_get<T*>(a_array, i_a, len_a));
    T v_b = *(array_get<T*>(b_array, i_b, len_b));

    if (v_a < v_b) {
      bool exit = search_func(v_b, a_array, &i_a, len_a);
      if (exit) { break; }
      v_a = *(array_get<T*>(a_array, i_a, len_a));
    } else if (v_b < v_a) {
      bool exit = search_func(v_a, b_array, &i_b, len_b);
      if (exit) { break; }
      v_b = *(array_get<T*>(b_array, i_b, len_b));
    }

    if (v_a == v_b) {
      // Skip if I_DROP and a duplicate
      if (dup_treatment != I_DROP || v_a != prev || !has_prev) {
        T *t = array_get<T*>(out_array, i_o, new_dim[0]);
        *t = v_a;
        if (indices != 0) {
          npy_intp *t_a =
            array_get<npy_intp*>(indices_a_array, i_o, new_dim[0]);
          npy_intp *t_b =
            array_get<npy_intp*>(indices_b_array, i_o, new_dim[0]);

          *t_a = i_a;
          *t_b = i_b;
        }
        i_o++;
      }

      i_a++;
      i_b++;

      prev = v_a;
      has_prev = true;

      if (dup_treatment == I_KEEP_MAX_N) {
        if (i_a < len_a && i_b < len_b) {
          v_a = *(array_get<T*>(a_array, i_a, len_a));
          v_b = *(array_get<T*>(b_array, i_b, len_b));

          // if one still duplicate other not
          //   -> go back for other
          if (v_a == prev && v_b != prev) {
            i_b--;
          } else if (v_a != prev && v_b == prev) {
            i_a--;
          }
        } else if (i_a < len_a) {
          // b reached its end
          v_a = *(array_get<T*>(a_array, i_a, len_a));
          if (v_a == prev) {
            i_b--;
          }
        } else if (i_b < len_b) {
          // a reached its end
          v_b = *(array_get<T*>(b_array, i_b, len_b));
          if (v_b == prev) {
            i_a--;
          }
        }
      }
    }
  }

  // Resize the array after intersect operation.
  new_dim[0] = i_o;
  PyArray_Dims dims;
  dims.ptr = new_dim;
  dims.len = 1;
  PyArray_Resize(out_array, &dims, 0, NPY_CORDER);

  if (indices == 0) {
    return out;
  } else {
    PyArray_Resize(indices_a_array, &dims, 0, NPY_CORDER);
    PyArray_Resize(indices_b_array, &dims, 0, NPY_CORDER);

    PyObject* tuple =  Py_BuildValue("O(OO)", out, indices_a, indices_b);
    // The tuple holds the references to the arrays, we can release them
    Py_XDECREF(out);
    Py_XDECREF(indices_a);
    Py_XDECREF(indices_b);

    return tuple;
  }
}

/*
 * The sortednp_intersect function expects exactly two references to sorted
 * arrays as positional arguments. The function borrows the references. The
 * return value is a reference to a new sorted numpy array containing only
 * elements common in both arrays. The ownership of the returned reference is
 * passed to the caller.
 */
PyObject *sortednp_intersect(PyObject *self, PyObject *args, PyObject *kwds) {
  // References to the arguments are borrowed. Counter should not be
  // incremented since input arrays are not stored.

  PyObject *a = NULL;
  PyObject *b = NULL;
  int indices = 0;  // Default is to ignore the indices
  int algorithm = -1;
  int duplicates = -1;

  // Prepare keyword strings
  char s_a[] = "a";
  char s_b[] = "b";
  char s_indices[] = "indices";
  char s_algorithm[] = "algorithm";
  char s_duplicates[] = "duplicates";
  char * kwlist[] = {s_a, s_b, s_indices, s_algorithm, s_duplicates, NULL};

  // PyArg_ParseTuple returns borrowed references. This is fine, the input
  // arrays are not stored.
  if (!PyArg_ParseTupleAndKeywords(args, kwds, "O!O!|pii", kwlist,
      &PyArray_Type, &a, &PyArray_Type, &b, &indices, &algorithm,
      &duplicates)) {
    // Reference counters have not been changed.
    return NULL;
  }

  // PyArray_FROM_OF borrows the reference for in the input array. The method
  // might return a new object or the same object again if it matches
  // NPY_ARRAY_CARRAY_RO. We own a reference of the returned object. If this is
  // a new object, we own the single reference. If the returned object is the
  // initial object, its reference count is incremented. In any case, we need
  // decrement the counter once we are done with the object. See issue 22.
  a = PyArray_FROM_OF(a, NPY_ARRAY_CARRAY_RO);
  b = PyArray_FROM_OF(b, NPY_ARRAY_CARRAY_RO);


  if (a == NULL || b == NULL) {
    Py_XDECREF(a);
    Py_XDECREF(b);
    // Reference counter of internal arrays have been fixed. It is safe to exit.
    return NULL;
  }

  // Some methods need a PyObject* other nee a PyArrayObject*.
  PyArrayObject *a_array = reinterpret_cast<PyArrayObject*>(a);
  PyArrayObject *b_array = reinterpret_cast<PyArrayObject*>(b);

  if (PyArray_NDIM(a_array) != 1 || PyArray_NDIM(b_array) != 1) {
    PyErr_SetString(PyExc_ValueError,
      "Arguments can not be multi-dimensional.");

    Py_XDECREF(a);
    Py_XDECREF(b);
    // Reference counter of internal arrays have been fixed. It is safe to exit.
    return NULL;
  }

  if (PyArray_TYPE(a_array) != PyArray_TYPE(b_array)) {
    PyErr_SetString(PyExc_ValueError,
      "Arguments must have the same data type.");

    Py_XDECREF(a);
    Py_XDECREF(b);
    // Reference counter of internal arrays have been fixed. It is safe to exit.
    return NULL;
  }

  // Parse algorithm argument
  method_t search_method;
  switch (algorithm) {
    case 1:
      search_method = SIMPLE;
      break;
    case 2:
      search_method = BINARY;
      break;
    case -1:  // default value
    case 3:
      search_method = GALLOPPING;
      break;
    default:
      PyErr_SetString(PyExc_ValueError,
        "Invalid search algorithm.");

      Py_XDECREF(a);
      Py_XDECREF(b);
      // Reference counter of internal arrays have been fixed.
      // It is safe to exit.
      return NULL;
  }

  // Parse duplicates argument
  intersect_dup_t dup_treatment;
  switch (duplicates) {
    case 4:
      dup_treatment = I_DROP;
      break;
    case -1:  // default value
    case 5:
      dup_treatment = I_KEEP_MIN_N;
      break;
    case 7:
      dup_treatment = I_KEEP_MAX_N;
      break;

    default:
      PyErr_SetString(PyExc_ValueError,
        "Invalid duplicate treatment.");

      Py_XDECREF(a);
      Py_XDECREF(b);
      // Reference counter of internal arrays have been fixed.
      // It is safe to exit.
      return NULL;
  }


  PyObject *out;

  // Differentiate between different data types.
  switch (PyArray_TYPE(a_array)) {
    case NPY_INT8:
      out = intersect<int8_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_INT16:
      out = intersect<int16_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_INT32:
      out = intersect<int32_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_INT64:
      out = intersect<int64_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_UINT8:
      out = intersect<uint8_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_UINT16:
      out = intersect<uint16_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_UINT32:
      out = intersect<uint32_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_UINT64:
      out = intersect<uint64_t>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_FLOAT32:
      out = intersect<float>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    case NPY_FLOAT64:
      out = intersect<double>(a_array, b_array, search_method, indices,
        dup_treatment);
      break;
    default:
      PyErr_SetString(PyExc_ValueError, "Data type not supported.");

      Py_XDECREF(a);
      Py_XDECREF(b);
      // Reference counter of internal arrays have been fixed.
      // It is safe to exit.
      return NULL;
  }

  Py_XDECREF(a);
  Py_XDECREF(b);
  // Reference counter of internal arrays have been fixed. It is safe to exit.

  // Passes ownership of the returned reference to the  caller.
  return out;
}

/**
 * Internal helper method.
 *
 * Calculate the union for the given arrays and the given type. The
 * method returns the pointer to the newly created output array. The first
 * parameter is used to call the templated function.
 */
template <typename T>
PyObject* merge(PyArrayObject *a_array, PyArrayObject *b_array, int indices,
    merge_dup_t dup_treatment) {
  // Since the size of the merged array can not be known in advance we
  // need to create an array of at least the size of the concatenation of both
  // arrays.
  npy_intp len_a = PyArray_DIMS(a_array)[0];
  npy_intp len_b = PyArray_DIMS(b_array)[0];
  npy_intp new_dim[1] = {len_a + len_b};

  // Creating the new array sets the reference counter to 1 and passes the
  // ownership of the returned reference to the caller. The method steals the
  // type descriptor, which is why we have to increment its count before
  // calling the method.
  PyArray_Descr* type = PyArray_DESCR(a_array);
  Py_INCREF(type);
  PyObject *out = NULL;
  out = PyArray_SimpleNewFromDescr(1, new_dim, type);
  if (out == NULL) {
    // Probably a memory error occurred.
    return NULL;
  }
  PyArrayObject* out_array = reinterpret_cast<PyArrayObject*>(out);

  PyObject *indices_a = NULL;
  PyObject *indices_b = NULL;
  PyArrayObject *indices_a_array = NULL;
  PyArrayObject *indices_b_array = NULL;
  if (indices != 0) {
    indices_a = PyArray_SimpleNew(1, &len_a, NPY_INTP);
    if (indices_a == NULL) {
      // Probably a memory error occurred.
      Py_XDECREF(out);

      // Save to exit, intermediate objects deleted.
      return NULL;
    }
    indices_a_array = reinterpret_cast<PyArrayObject*>(indices_a);

    indices_b = PyArray_SimpleNew(1, &len_b, NPY_INTP);
    if (indices_b == NULL) {
      // Probably a memory error occurred.
      Py_XDECREF(out);
      Py_XDECREF(indices_a);

      // Save to exit, intermediate objects deleted.
      return NULL;
    }
    indices_b_array = reinterpret_cast<PyArrayObject*>(indices_b);
  }

  npy_intp i_a = 0;
  npy_intp i_b = 0;
  npy_intp i_o = 0;

  T prev = 0;
  T prev_a = 0;
  T prev_b = 0;

  bool has_prev = false;
  bool has_prev_a = false;
  bool has_prev_b = false;

  // Actually merging the arrays.
  while (i_a < len_a && i_b < len_b) {
    T v_a = *(array_get<T*>(a_array, i_a, len_a));
    T v_b = *(array_get<T*>(b_array, i_b, len_b));

    T *t = array_get<T*>(out_array, i_o, new_dim[0]);

    if (dup_treatment == M_DROP && has_prev) {
      if (v_a == prev) {
        if (indices != 0) {
          npy_intp *t_a = array_get<npy_intp*>(indices_a_array, i_a, len_a);
          *t_a = i_o - 1;
        }
        i_a++;
        continue;
      }
      if (v_b == prev) {
        if (indices != 0) {
          npy_intp *t_b = array_get<npy_intp*>(indices_b_array, i_b, len_b);
          *t_b = i_o - 1;
        }
        i_b++;
        continue;
      }
    }
    if (dup_treatment == M_DROP_IN_INPUT) {
      if (v_a == prev_a && has_prev_a) {
        if (indices != 0) {
          npy_intp *t_a = array_get<npy_intp*>(indices_a_array, i_a, len_a);
          *t_a = i_o - 1;
        }
        i_a++;
        continue;
      }
      if (v_b == prev_b && has_prev_b) {
        if (indices != 0) {
          npy_intp *t_b = array_get<npy_intp*>(indices_b_array, i_b, len_b);
          *t_b = i_o - 1;
        }
        i_b++;
        continue;
      }
    }

    if (v_a <= v_b) {
      *t = v_a;
      if (indices != 0) {
        npy_intp *t_a = array_get<npy_intp*>(indices_a_array, i_a, len_a);
        *t_a = i_o;
      }

      i_a++;
      i_o++;
      prev_a = v_a;
      prev = v_a;
      has_prev_a = true;
      has_prev = true;
    } else {
      *t = v_b;
      if (indices != 0) {
        npy_intp *t_b = array_get<npy_intp*>(indices_b_array, i_b, len_b);
        *t_b = i_o;
      }

      i_b++;
      i_o++;
      prev_b = v_b;
      prev = v_b;
      has_prev_b = true;
      has_prev = true;
    }
  }

  // If the end of one of the two arrays has been reached in the above loop,
  // we need to copy all the elements left the array to the output.
  while (i_a < len_a) {
    T v_a = *(array_get<T*>(a_array, i_a, len_a));

    if ((dup_treatment == M_DROP && v_a == prev && has_prev) ||
        (dup_treatment == M_DROP_IN_INPUT && v_a == prev_a && has_prev_a)) {
      if (indices != 0) {
        npy_intp *t_a = array_get<npy_intp*>(indices_a_array, i_a, len_a);
        *t_a = i_o - 1;
      }
      i_a++;
      continue;
    }

    T *t = array_get<T*>(out_array, i_o, new_dim[0]);
    *t = v_a;
    prev_a = v_a;
    prev = v_a;
    has_prev_a = true;
    has_prev = true;
    if (indices != 0) {
      npy_intp *t_a = array_get<npy_intp*>(indices_a_array, i_a, len_a);
      *t_a = i_o;
    }


    i_a++;
    i_o++;
  }

  while (i_b < len_b) {
    T v_b = *(array_get<T*>(b_array, i_b, len_b));

    if ((dup_treatment == M_DROP && v_b == prev && has_prev) ||
        (dup_treatment == M_DROP_IN_INPUT && v_b == prev_b && has_prev_b)) {
      if (indices != 0) {
        npy_intp *t_b = array_get<npy_intp*>(indices_b_array, i_b, len_b);
        *t_b = i_o - 1;
      }
      i_b++;
      continue;
    }

    T *t = array_get<T*>(out_array, i_o, new_dim[0]);
    *t = v_b;
    has_prev_b = true;
    has_prev = true;
    prev_b = v_b;
    prev = v_b;
    if (indices != 0) {
      npy_intp *t_b = array_get<npy_intp*>(indices_b_array, i_b, len_b);
      *t_b = i_o;
    }

    i_b++;
    i_o++;
  }


  // Resize the array after merge operation.
  new_dim[0] = i_o;
  PyArray_Dims dims;
  dims.ptr = new_dim;
  dims.len = 1;
  PyArray_Resize(out_array, &dims, 0, NPY_CORDER);

  if (indices == 0) {
    return out;
  } else {
    new_dim[0] = i_a;
    dims.ptr = new_dim;
    dims.len = 1;
    PyArray_Resize(indices_a_array, &dims, 0, NPY_CORDER);

    new_dim[0] = i_b;
    dims.ptr = new_dim;
    dims.len = 1;
    PyArray_Resize(indices_b_array, &dims, 0, NPY_CORDER);

    PyObject* tuple =  Py_BuildValue("O(OO)", out, indices_a, indices_b);

    // The tuple holds the references to the arrays, we can release them
    Py_XDECREF(out);
    Py_XDECREF(indices_a);
    Py_XDECREF(indices_b);

    return tuple;
  }
}

/*
 * The sortednp_merge function expects exactly two references to sorted
 * arrays as positional arguments. The function borrows the references. The
 * return value is a reference to a new sorted numpy array containing all
 * elements of the input arrays. The ownership of the returned reference is
 * passed to the caller.
 */
PyObject *sortednp_merge(PyObject *self, PyObject *args, PyObject *kwds) {
  // References to the arguments are borrowed. Counter should not be
  // incremented since input arrays are not stored.

  PyObject *a = NULL;
  PyObject *b = NULL;
  int indices = 0;  // Default is to ignore the indices
  int duplicates = -1;

  // Prepare keyword strings
  char s_a[] = "a";
  char s_b[] = "b";
  char s_indices[] = "indices";
  char s_duplicates[] = "duplicates";
  char * kwlist[] = {s_a, s_b, s_indices, s_duplicates, NULL};

  // PyArg_ParseTuple returns borrowed references. This is fine, the input
  // arrays are not stored.
  if (!PyArg_ParseTupleAndKeywords(args, kwds, "O!O!|pi", kwlist,
      &PyArray_Type, &a, &PyArray_Type, &b, &indices, &duplicates)) {
    // Reference counters have not been changed.
    return NULL;
  }

  // PyArray_FROM_OF borrows the reference for in the input array. The method
  // might return a new object or the same object again if it matches
  // NPY_ARRAY_CARRAY_RO. We own a reference of the returned object. If this is
  // a new object, we own the single reference. If the returned object is the
  // initial object, its reference count is incremented. In any case, we need
  // decrement the counter once we are done with the object. See issue 22.
  a = PyArray_FROM_OF(a, NPY_ARRAY_CARRAY_RO);
  b = PyArray_FROM_OF(b, NPY_ARRAY_CARRAY_RO);

  if (a == NULL || b == NULL) {
    Py_XDECREF(a);
    Py_XDECREF(b);
    // Reference counter of internal arrays have been fixed. It is safe to exit.
    return NULL;
  }

  // Some methods need a PyObject* other nee a PyArrayObject*.
  PyArrayObject *a_array = reinterpret_cast<PyArrayObject*>(a);
  PyArrayObject *b_array = reinterpret_cast<PyArrayObject*>(b);


  if (PyArray_NDIM(a_array) != 1 || PyArray_NDIM(b_array) != 1) {
    PyErr_SetString(PyExc_ValueError,
      "Arguments can not be multi-dimensional.");
    Py_XDECREF(a);
    Py_XDECREF(b);
    // Reference counter of internal arrays have been fixed. It is safe to exit.
    return NULL;
  }

  if (PyArray_TYPE(a_array) != PyArray_TYPE(b_array)) {
    PyErr_SetString(PyExc_ValueError,
      "Arguments must have the same data type.");
    Py_XDECREF(a);
    Py_XDECREF(b);
    // Reference counter of internal arrays have been fixed. It is safe to exit.
    return NULL;
  }

  // Parse duplicates argument
  merge_dup_t dup_treatment;
  switch (duplicates) {
    case 4:
      dup_treatment = M_DROP;
      break;
    case 6:
      dup_treatment = M_DROP_IN_INPUT;
      break;
    case -1:  // default value
    case 8:
      dup_treatment = M_KEEP;
      break;

    default:
      PyErr_SetString(PyExc_ValueError,
        "Invalid duplicate treatment.");

      Py_XDECREF(a);
      Py_XDECREF(b);
      // Reference counter of internal arrays have been fixed.
      // It is safe to exit.
      return NULL;
  }

  PyObject* out = NULL;

  // Differentiate between different data types.
  switch (PyArray_TYPE(a_array)) {
    case NPY_INT8:
      out = merge<int8_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_INT16:
      out = merge<int16_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_INT32:
      out = merge<int32_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_INT64:
      out = merge<int64_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_UINT8:
      out = merge<uint8_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_UINT16:
      out = merge<uint16_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_UINT32:
      out = merge<uint32_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_UINT64:
      out = merge<uint64_t>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_FLOAT32:
      out = merge<float>(a_array, b_array, indices, dup_treatment);
      break;
    case NPY_FLOAT64:
      out = merge<double>(a_array, b_array, indices, dup_treatment);
      break;
    default:
      PyErr_SetString(PyExc_ValueError, "Data type not supported.");
      Py_XDECREF(a);
      Py_XDECREF(b);
      // Reference counter of internal arrays have been fixed.
      // It is safe to exit.
      return NULL;
  }

  Py_XDECREF(a);
  Py_XDECREF(b);
  // Reference counter of internal arrays have been fixed. It is safe to exit.

  // Passes ownership of the returned reference to the  caller.
  return out;
}

PyMethodDef SortedNpMethods[] = {
  {"merge",  (PyCFunction) sortednp_merge, METH_VARARGS | METH_KEYWORDS,
    "Merge two sorted numpy arrays. If the optional argument indices is "
    "True, the mothod will\r\n return a tpule of the format "
    "(merged_array, (indices_array_a, indices_array_b))."
  },
  {"intersect",  (PyCFunction) sortednp_intersect, METH_VARARGS | METH_KEYWORDS,
    "Intersect two sorted numpy arrays. If the optional argument indices is "
    "True, the method will\r\n return a tuple of the format "
    "(intersection_array, (indices_array_a, indices_array_b))."
  },
  {NULL, NULL, 0, NULL}  // Sentinel
};

// Define module itself.
struct PyModuleDef sortednpmodule = {
  PyModuleDef_HEAD_INIT,
  "sortednp._internal",  // Name of the module
  NULL,  // Module docstring
  -1,  // The module keeps state in global variables.
  SortedNpMethods
};

// Init method
PyMODINIT_FUNC PyInit__internal(void) {
  import_array();
  return PyModule_Create(&sortednpmodule);
}
