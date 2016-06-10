CXX=g++
FILENAME=cpphelpers

all:
	swig -c++ -python -builtin $(FILENAME).i
	${CXX} -O2 -fPIC -c $(FILENAME).cpp
	${CXX} -O2 -fPIC -c $(FILENAME)_wrap.cxx -I /home/andy/.virtualenvs/crpropa/include/python2.7/ 
	${CXX} -fPIC -shared $(FILENAME).o $(FILENAME)_wrap.cxx -o _$(FILENAME).so -I /home/andy/.virtualenvs/crpropa/include/python2.7/
clean:
	@rm -f *.so *.o *_wrap.cxx $(FILENAME).py *.pyc
