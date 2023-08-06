#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <float.h>
#include <numpy/arrayobject.h>
#include "util.h"

static PyObject *py_pbc_nearest_neighbor(PyObject *self, PyObject *args);

static PyMethodDef method_def[] = {
    {"pbc_nearest_neighbor", py_pbc_nearest_neighbor, METH_VARARGS, "Returns the distance from and index of the nearest neighbor."},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "_pbc",
    "Module `_pbc` provides optimized C functions for operations with periodic boundary conditions.",
    -1,
    method_def,
};

PyMODINIT_FUNC PyInit__pbc(void)
{
    PyObject *module = PyModule_Create(&module_def);
    if (module == NULL)
    {
        return NULL;
    }
    return module;
}

size_t pbc_nearest_neighbor(double position[3], double positions[][3], size_t length, double cell[3][3], int pbc[3], double *out)
{
    double pbc_bounds[3];
    for (int i = 0; i < 3; i++)
    {
        if (pbc[i])
        {
            pbc_bounds[i] = norm(cell[i]) / 2.0;
        }
        else
        {
            pbc_bounds[i] = norm(cell[i]);
        }
    }

    double pbc_position[3];
    for (int i = 0; i < 3; i++)
    {
        if (position[i] > pbc_bounds[i])
        {
            pbc_position[i] = position[i] - pbc_bounds[i];
        }
        else
        {
            pbc_position[i] = position[i];
        }
    }

    double pbc_neighbor_position[3];
    double distance = DBL_MAX;
    double tmp_distance;
    size_t index = 0;

    for (size_t i = 0; i < length; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (positions[i][j] > pbc_bounds[j])
            {
                pbc_neighbor_position[j] = positions[i][j] - pbc_bounds[j];
            }
            else
            {
                pbc_neighbor_position[j] = positions[i][j];
            }
        }
        tmp_distance = euclidean(pbc_position, pbc_neighbor_position);
        if (tmp_distance < distance)
        {
            distance = tmp_distance;
            index = i;
        }
    }
    *out = distance;
    return index;
}

static PyObject *py_pbc_nearest_neighbor(PyObject *self, PyObject *args)
{
    PyArrayObject *py_position;
    double(*position);
    PyArrayObject *py_positions;
    double(*positions)[3];
    PyArrayObject *py_cell;
    double(*cell)[3];
    PyObject *py_pbc;
    int pbc[3];

    if (!PyArg_ParseTuple(args, "OOOO", &py_position, &py_positions, &py_cell, &py_pbc))
    {
        return NULL;
    }

    position = (double(*))PyArray_DATA(py_position);
    size_t length = PyArray_DIM(py_positions, 0);
    positions = (double(*)[3])PyArray_DATA(py_positions);
    cell = (double(*)[3])PyArray_DATA(py_cell);

    if (!PyTuple_Check(py_pbc))
    {
        return NULL;
    }
    for (int i = 0; i < 3; i++)
    {
        if (PyObject_IsTrue(PyTuple_GET_ITEM(py_pbc, i)))
        {
            pbc[i] = 1;
        }
        else
        {
            pbc[i] = 0;
        }
    }

    double distance = 0;
    size_t index = 0;
    index = pbc_nearest_neighbor(position, positions, length, cell, pbc, &distance);
    PyObject *res = PyTuple_New(2);
    PyTuple_SET_ITEM(res, 0, PyFloat_FromDouble(distance));
    PyTuple_SET_ITEM(res, 1, PyLong_FromSize_t(index));
    return res;
}