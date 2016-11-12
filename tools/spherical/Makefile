CC=gcc
DEBUG="-g"

all: spherical.o tests.c
	${CC} -o tests.bin -lm tests.c spherical.o -Wall -I/usr/include/python2.7 -lpython2.7 -L/usr/include/python2.7

spherical.o: spherical.c
	${CC} -c -lm spherical.c -Wall -I/usr/include/python2.7 -lpython2.7 -L/usr/include/python2.7

test:
	./tests.bin

python:
	python setup.py build

clean:
	rm spherical.o tests.bin
