#include "spherical.h"

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
	// \sqrt{1-x^2}P_\ell^m(x) = \frac1{2\ell+1} \left[ - P_{\ell+1}^{m+1}(x) + P_{\ell-1}^{m+1}(x) \right]
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
