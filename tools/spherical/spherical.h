#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>

#ifndef M_PI
#define M_PI acos(-1.0)
#endif

typedef long long int bigint;
typedef unsigned long long int bigposint;

static PyObject * spherical_factorial(PyObject *self, PyObject *args);
static PyObject * spherical_shortfactorial(PyObject *self, PyObject *args);
static PyObject * spherical_AssociatedLegendreP(PyObject *self, PyObject *args);
static PyObject * spherical_SphericalHarmonics(PyObject *self, PyObject *args);
static PyObject * spherical_C(PyObject *self, PyObject *args);

PyMODINIT_FUNC initspherical(void);

bigint factorial(int);
double shortfactorial(int, int);
double AssociatedLegendreP(int l, int m, double x);
double complex SphericalHarmonics(int l, int m, double theta, double phi);
double complex a(int l, int m, double * theta, double * phi);
double C(int l, double * theta, double * phi);
