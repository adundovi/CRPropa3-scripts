
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>

#ifndef M_PI
#define M_PI acos(-1.0)
#endif

typedef long long int bigint;
typedef unsigned long long int bigposint;

bigint factorial(int);
double shortfactorial(int, int);
double AssociatedLegendreP(int l, int m, double x);
double complex SphericalHarmonics(int l, int m, double theta, double phi);
double complex a(int l, int m, double * theta, double * phi);
double C(int l, double * theta, double * phi);
