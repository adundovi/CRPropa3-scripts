#include "sphericalpy.h"
#include "spherical.h"

static PyMethodDef SHMethods[] = {
    {"shortfactorial",  spherical_shortfactorial, METH_VARARGS,
     "Calculate factorial(first)/factorial(second)."},
    {"factorial",  spherical_factorial, METH_VARARGS,
     "Calculate factorial."},
    {"SphericalHarmonics",  spherical_SphericalHarmonics, METH_VARARGS,
     "Calculate SphericalHarmonics."},
    {"AssociatedLegendreP",  spherical_AssociatedLegendreP, METH_VARARGS,
     "Calculate AssociatedLegendreP."},
    {"C",  spherical_C, METH_VARARGS,
     "Calculate angular power spectrum."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initspherical(void){
    (void) Py_InitModule("spherical", SHMethods);
}

static PyObject * spherical_factorial(PyObject *self, PyObject *args){
    int n;
    bigint result;

    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
    result = factorial(n);
    return Py_BuildValue("l", result);
}


static PyObject * spherical_shortfactorial(PyObject *self, PyObject *args){
    int first, second;
    double result;

    if (!PyArg_ParseTuple(args, "ii", &first, &second))
        return NULL;
    result = shortfactorial(first, second);
    return Py_BuildValue("d", result);
}


static PyObject * spherical_AssociatedLegendreP(PyObject *self, PyObject *args){
    int l, m;
    double x;
    double result;

    if (!PyArg_ParseTuple(args, "iid", &l, &m, &x))
        return NULL;
    result = AssociatedLegendreP(l, m, x);
    return Py_BuildValue("d", result);
}

static PyObject * spherical_SphericalHarmonics(PyObject *self, PyObject *args){
    int l, m;
    double theta, phi;
    double complex result;
    Py_complex pyresult;

    if (!PyArg_ParseTuple(args, "iidd", &l, &m, &theta, &phi))
        return NULL;
    
    result = SphericalHarmonics(l, m, theta, phi);
    pyresult.real = creal(result);
    pyresult.imag = cimag(result);
    return PyComplex_FromCComplex(pyresult);
}

static PyObject * spherical_C(PyObject *self, PyObject *args){
	int i;
 	int numThetaElements;
 	int numPhiElements;
	PyObject * thetaObj;
	PyObject * phiObj;
	double * ptr_theta;
	double * ptr_phi;

	int l;
	double result;

	if (!PyArg_ParseTuple(args, "iO!O!", &l, &PyList_Type, &thetaObj, &PyList_Type, &phiObj))
		return NULL;

	numThetaElements = PyList_Size(thetaObj);
	numPhiElements = PyList_Size(phiObj);

	if (numThetaElements != numPhiElements)
		return NULL;

	ptr_theta = (double *)malloc((numThetaElements+1)*sizeof(double));
	ptr_phi = (double *)malloc((numPhiElements+1)*sizeof(double));

	ptr_theta[0] = numThetaElements;
	ptr_phi[0] = numPhiElements;

	for (i=0; i<numThetaElements; ++i){
		ptr_theta[i+1] = PyFloat_AsDouble(PyList_GetItem(thetaObj, i));
		ptr_phi[i+1] = PyFloat_AsDouble(PyList_GetItem(phiObj, i));
	}

	result = C(l, ptr_theta, ptr_phi);

	free(ptr_theta);
	free(ptr_phi);
	Py_DECREF(thetaObj);
	Py_DECREF(phiObj);	

	return Py_BuildValue("d", result);
}
