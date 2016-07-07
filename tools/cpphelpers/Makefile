CXX=g++
CXXFLAGS=-O2 -fPIC
FILENAME=cpphelpers
PYTHONHEADER=/usr/include/python2.6/

all:
	swig -c++ -python -builtin $(FILENAME).i
	$(CXX) $(CXXFLAGS) -c $(FILENAME).cpp
	$(CXX) $(CXXFLAGS) -c $(FILENAME)_wrap.cxx -I $(PYTHONHEADER) -lpython2.6
	$(CXX) $(CXXFLAGS) -shared $(FILENAME).o $(FILENAME)_wrap.cxx -o _$(FILENAME).so -I $(PYTHONHEADER) -lpython2.6
clean:
	@rm -f *.so *.o *_wrap.cxx $(FILENAME).py *.pyc
