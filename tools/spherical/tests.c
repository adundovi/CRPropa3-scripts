#include "spherical.h"
#include <stdio.h>
#include <math.h>
#include <complex.h>

#define TRUE 1
#define FALSE 0

int check(double returned_value, double expected_value){
	if((fabs(returned_value - expected_value) > 1E-7)){
		printf("\tFAILED\n");
		printf("\t\tReturned value: %f, Expected value: %f\n", returned_value, expected_value);
		//exit(0);
		return FALSE;
	}
	return TRUE;
}

int main(){

	int l, m;
	double var_x, var_y, sum;
	double theta[] = {1, 0.1}; // 0, 0};
	double phi[] = {1, 0}; //, 0, 0};

	printf("(1) Test factorial\n");

	check(factorial(0), 1);
	check(factorial(1), 1);
	check(factorial(10), 3628800);
	check(factorial(15), 1307674368000);
	check(factorial(18), 6402373705728000ULL);
	l = 10, m = 5;
	check(shortfactorial(l-m, l+m), factorial(l-m)/factorial(l+m));
	
	printf("(2) Test AssociatedLegenderP\n");

	for(var_x=-1.0; var_x<=1.0; var_x+=0.1){
		check(AssociatedLegendreP(0,0,var_x), 1.0);
		check(AssociatedLegendreP(1,0,var_x), var_x);
		check(AssociatedLegendreP(1,1,var_x), -1*pow((1-pow(var_x,2)),0.5));
		check(AssociatedLegendreP(4,4,var_x), 105*pow(1-var_x*var_x,2));
		check(AssociatedLegendreP(4,1,var_x), (-5.)/2*(7*pow(var_x,3) - 3*var_x)*sqrt(1-var_x*var_x));
		check(AssociatedLegendreP(4,-1,var_x), -1./20*AssociatedLegendreP(4,1,var_x));
		check(AssociatedLegendreP(4,-1,var_x), -1./20*(-5)/2*(7*pow(var_x,3) - 3*var_x)*pow(1-var_x*var_x,0.5));
		//check(AssociatedLegendreP(15,15,var_x), -6190283353629375*pow(1-var_x*var_x, 15/2.));
	}
	
	printf("(3) Test SphericalHarmonics\n");

	for(var_x=0; var_x <= M_PI; var_x+=0.5)
		for(var_y=0; var_y <=2*M_PI; var_y+=0.5){
			check(creal(SphericalHarmonics(0, 0, var_x, var_y)), 1/2.*sqrt(1/M_PI));
			check(creal(SphericalHarmonics(1, -1, var_x, var_y)), creal(1/2.*sqrt(3./(2*M_PI))*sin(var_x)*cexp(-I*var_y)));
			check(creal(SphericalHarmonics(2, 0, var_x, var_y)), 1/4.*sqrt(5/M_PI)*(3*cos(var_x)*cos(var_x)-1));
			check(cimag(SphericalHarmonics(5, -4, var_x, var_y)), cimag(3/16.*sqrt(385/(2*M_PI))*pow(sin(var_x),4)*cos(var_x)*cexp(-4*I*var_y)));
			check(cimag(SphericalHarmonics(7, 7, var_x, var_y)), cimag(-3/64.*sqrt(715/(2*M_PI))*pow(sin(var_x),7)*cexp(7*I*var_y)));
			check(creal(SphericalHarmonics(10, 9, var_x, var_y)), creal(-1/512.*sqrt(4849845/(M_PI))*pow(sin(var_x),9)*cos(var_x)*cexp(9*I*var_y)));
			//check(creal(SphericalHarmonics(15,15, var_x, var_y)), creal(-3/16384.*sqrt(33393355/M_PI)*pow(sin(var_x),15)*exp(15*I*var_y)));
		}
	
	// completness
	for(l=0;l<11;++l){
		for(var_x=0; var_x <= M_PI; var_x+=0.1)
			for(var_y=0; var_y <=2*M_PI; var_y+=0.1){
				sum = 0;
				for(m=-l; m<=l; ++m){
					sum += conj(SphericalHarmonics(l, m, var_x, var_y))*SphericalHarmonics(l, m, var_x, var_y);
				}
				if(!check(sum, (2*l+1)/(4*M_PI))){
					printf("%d", l);
				};
			}
	}

	printf("(4) Test Coefficients of Harmonics expansion\n");

	check(creal(a(10, 5, theta, phi)), -0.00033704);

	printf("(5) Test power spectrum expansion\n");
	
	check(C(5, theta, phi), 0.0795775);
	check(C(9, theta, phi), 0.0795775);

	return 0;
}

