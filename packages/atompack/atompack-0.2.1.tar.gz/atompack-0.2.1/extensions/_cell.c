#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>
#include "util.h"

static PyObject *py_cell_contains(PyObject *self, PyObject *args);

static PyMethodDef method_def[] = {
    {"cell_contains", py_cell_contains, METH_VARARGS, "Returns True if point is within cell."},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "_cell",
    "Module `_cell` provides optimized C functions which operate on a 3x3 matrix representation of a prallelepiped cell.",
    -1,
    method_def,
};

PyMODINIT_FUNC PyInit__cell(void)
{
    PyObject *module = PyModule_Create(&module_def);
    if (module == NULL)
    {
        return NULL;
    }
    return module;
}

// Populates an array with the vertices of a cell.
void _vertices(double cell[3][3], double out[8][3])
{
    double origin[3] = {0.0, 0.0, 0.0};
    double x[3] = {cell[0][0], cell[0][1], cell[0][2]};
    double y[3] = {cell[1][0], cell[1][1], cell[1][2]};
    double z[3] = {cell[2][0], cell[2][1], cell[2][2]};
    double xy[3] = {
        cell[0][0] + cell[1][0],
        cell[0][1] + cell[1][1],
        cell[0][2] + cell[1][2],
    };
    double xz[3] = {
        cell[0][0] + cell[2][0],
        cell[0][1] + cell[2][1],
        cell[0][2] + cell[2][2],
    };
    double yz[3] = {
        cell[1][0] + cell[2][0],
        cell[1][1] + cell[2][1],
        cell[1][2] + cell[2][2],
    };
    double xyz[3] = {
        cell[0][0] + cell[1][0] + cell[2][0],
        cell[0][1] + cell[1][1] + cell[2][1],
        cell[0][2] + cell[1][2] + cell[2][2],
    };
    for (int i = 0; i < 3; i++)
    {
        out[0][i] = origin[i];
        out[1][i] = x[i];
        out[2][i] = y[i];
        out[3][i] = z[i];
        out[4][i] = xy[i];
        out[5][i] = xz[i];
        out[6][i] = yz[i];
        out[7][i] = xyz[i];
    }
}

// Populates an array with the faces of a cell represented as an array of 3 coplanar points.
void _faces(double cell[3][3], double out[6][3][3])
{
    double verts[8][3];
    _vertices(cell, verts);
    for (int i = 0; i < 3; i++)
    {
        // lower xy
        out[0][0][i] = verts[4][i];
        out[0][1][i] = verts[1][i];
        out[0][2][i] = verts[2][i];
        // upper xy
        out[1][0][i] = verts[7][i];
        out[1][1][i] = verts[6][i];
        out[1][2][i] = verts[5][i];
        // rear xz
        out[2][0][i] = verts[5][i];
        out[2][1][i] = verts[3][i];
        out[2][2][i] = verts[1][i];
        // front xz
        out[3][0][i] = verts[2][i];
        out[3][1][i] = verts[6][i];
        out[3][2][i] = verts[4][i];
        // left yz
        out[4][0][i] = verts[6][i];
        out[4][1][i] = verts[2][i];
        out[4][2][i] = verts[3][i];
        // right yz
        out[5][0][i] = verts[1][i];
        out[5][1][i] = verts[4][i];
        out[5][2][i] = verts[5][i];
    }
}

// Populates an array with the vector normal to each face on the cell.
void _normals(double cell[3][3], double out[6][3])
{
    double d;
    double a[3], b[3], n[3];
    double faces[6][3][3];
    _faces(cell, faces);
    for (int i = 0; i < 6; i++)
    {
        sub(faces[i][1], faces[i][0], a);
        sub(faces[i][2], faces[i][0], b);
        cross(a, b, n);
        d = norm(n);
        div_scalar(n, d, out[i]);
    }
}

int cell_contains(double cell[3][3], double position[3], double tolerance)
{
    double faces[6][3][3];
    _faces(cell, faces);
    double normals[6][3];
    _normals(cell, normals);
    double p2f[3], reduced_normal[3];
    double d, p2f_norm;

    for (int i = 0; i < 6; i++)
    {
        sub(faces[i][0], position, p2f);
        p2f_norm = norm(p2f);
        div_scalar(normals[i], p2f_norm, reduced_normal);
        d = dot(p2f, reduced_normal);
        if (d < -tolerance)
        {
            return 0; // false
        }
    }
    return 1; // true
}

static PyObject *py_cell_contains(PyObject *self, PyObject *args)
{
    PyArrayObject *py_cell;
    double(*cell)[3];
    PyArrayObject *py_position;
    double(*position);
    double tolerance;

    if (!PyArg_ParseTuple(args, "OOd", &py_cell, &py_position, &tolerance))
    {
        return NULL;
    }

    cell = (double(*)[3])PyArray_DATA(py_cell);
    position = (double(*))PyArray_DATA(py_position);

    if (cell_contains(cell, position, tolerance))
    {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}