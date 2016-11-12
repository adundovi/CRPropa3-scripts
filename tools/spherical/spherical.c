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

bigint factorial(int n){
	// max 20!
	// for more look: https://en.wikipedia.org/wiki/GNU_Multiple_Precision_Arithmetic_Library
	int i;
	bigint product = 1;

	if (n == 0)
		return 1;
	for (i=1; i<=n; ++i){
		product *= i;
	}
    	return product;
}

static PyObject * spherical_shortfactorial(PyObject *self, PyObject *args){
    int first, second;
    double result;

    if (!PyArg_ParseTuple(args, "ii", &first, &second))
        return NULL;
    result = shortfactorial(first, second);
    return Py_BuildValue("d", result);
}

double shortfactorial(int first, int second){
	bigint product = 1;
	int i;
	int smaller = first <= second ? first : second;
	int bigger = first >= second ? first : second;

	for (i=smaller+1; i<=bigger; ++i){
		product *= i;
	}

	return first <= second ? 1./product : product;
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
    return Py_BuildValue("D", pyresult);
}

double AssociatedLegendreP(int l, int m, double x){
	if (m < 0)
		// inverse for negative m
		return pow(-1, m)*shortfactorial(l+m, l-m)*AssociatedLegendreP(l, -1*m, x);
	if (l < m)
		return 0;
	if (l == 0 && m == 0)
		return 1;
	if (l == 1 && m == 0)
		return x;
	if (l == 1 && m == 1)
		return -sqrt(1-x*x);
	if (l == 2 && m == 1)
		return -3*x*sqrt(1-x*x);
	if (l == 2 && m == 0)
		return (3*x*x-1)/2;
	if (l == 2 && m == 2)
		return 3*(1-x*x);
	if (l == m)
		return -(2*(l-1)+1)*sqrt(1-x*x)*AssociatedLegendreP(l-1, m-1, x);
	
	// based on a recurrence formula:
	// {\frac {1}{\sqrt {1-x^{2}}}}P_{\ell }^{m}(x) =
	// {\frac {-1}{2m}}\left[P_{\ell -1}^{m+1}(x)+(\ell +m-1)(\ell +m)P_{\ell -1}^{m-1}(x)\right]
	return AssociatedLegendreP(l-2, m, x) -
	       (2*(l-1)+1)*sqrt(1-x*x)*AssociatedLegendreP(l-1, m-1, x);
}

double complex SphericalHarmonics(int l, int m, double theta, double phi){
	double norm;

	norm = sqrt((2*l+1)/(4*M_PI)*factorial(l-m)/factorial(l+m));

	return norm*AssociatedLegendreP(l, m, cos(theta))*(cos(m*phi) + I*sin(m*phi));
}

double complex a(int l, int m, double * theta, double * phi){
	int i;
	int N;
	double complex sum = 0;

	N = (int)theta[0];

	for (i=1; i<=N; ++i){
		sum += conj(SphericalHarmonics(l, m, theta[i], phi[i]));
	}

	return sum/N;
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

double C(int l, double theta[], double phi[]){
	int m;
	double sum = 0;
	double complex a_lm;

	for (m=-l; m<=l; ++m){
		a_lm = a(l, m, theta, phi);
		sum += creal(conj(a_lm)*a_lm);
	}

	return sum/(2*l+1);
}
