CC=gcc

tests.bin: spherical.o sphericalpy.o tests.c
	${CC} -o tests.bin -lm tests.c spherical.o -Wall -I/usr/include/python2.7 -lpython2.7 -L/usr/include/python2.7

spherical.o: spherical.c
	${CC} -c -lm spherical.c -Wall -I/usr/include/python2.7 -lpython2.7 -L/usr/include/python2.7

sphericalpy.o: sphericalpy.c
	${CC} -c -lm sphericalpy.c -Wall -I/usr/include/python2.7 -lpython2.7 -L/usr/include/python2.7

test: tests.bin
	./tests.bin

python:
	python setup.py build

install: python
	python setup.py install

clean:
	rm -rf build spherical.o tests.bin
