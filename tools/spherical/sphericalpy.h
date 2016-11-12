#include <Python.h>
#include "spherical.h"

static PyObject * spherical_factorial(PyObject *self, PyObject *args);
static PyObject * spherical_shortfactorial(PyObject *self, PyObject *args);
static PyObject * spherical_AssociatedLegendreP(PyObject *self, PyObject *args);
static PyObject * spherical_SphericalHarmonics(PyObject *self, PyObject *args);
static PyObject * spherical_C(PyObject *self, PyObject *args);

PyMODINIT_FUNC initspherical(void);
