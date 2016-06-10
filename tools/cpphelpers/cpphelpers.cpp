#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <limits>
#include <cmath>
#include <string>

#include "cpphelpers.h"

std::vector<int> file2histogram(const char* filename, const int pos, const double start, const double stop, const double step){

    double energy, pow;
    std::string line;
    std::ifstream infile(filename);
    int idx, n = (stop-start)/step;
    std::vector<int> bins(n, 0);

    // skip header
    while (infile.peek() == '#')
	infile.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    while (!infile.eof()){
	std::getline(infile, line);
	
	for(int i=0; i<pos; ++i){
	    infile.ignore(std::numeric_limits<std::streamsize>::max(), '\t');
	}
	infile >> pow;
        infile.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

	if (float(pow) == 0)
	    continue;

	energy = log10(float(pow)) + 18.0;

	idx = round( (energy - start)/step );
	if (idx < 0)
	    continue;

	bins[idx]++;
    }
    infile.close();

    return bins;
}

int main(int argc, char** argv){

    int pos = std::stoi(argv[2]);
    double start, stop, step;
    std::vector<int> bins;
    
    start = 15;
    stop = 20.51;
    step = 0.1;

    bins = file2histogram(argv[1], pos, start, stop, step);

    for (int &i : bins){
        std::cout << i << " ";
    }

    return 0;
}
