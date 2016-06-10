%module cpphelpers

%include "std_vector.i"
%include "cpphelpers.h"

%{
#include "cpphelpers.h"
%}

namespace std {
        %template(vectori) vector<int>;
}

