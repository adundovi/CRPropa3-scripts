#!/bin/bash

if [ -n "$1" ]; then
        CRPROPA_DIR=$1;
else
        echo "Missing CRPropa dir"
        exit;
fi

function download_install {
	mkdir -p $3
	wget --no-clobber $2 --directory-prefix=$CRPROPA_DIR
	tar xvf "$CRPROPA_DIR/$1" --strip 1 -C $3

	cd $3
	./configure --prefix=$CRPROPA_DIR $4
	make
	make install

}

function pip_install {
	pip install $1
}

# SWIG install

SWIG_FILE="swig-3.0.5.tar.gz"
SWIG_URL="http://prdownloads.sourceforge.net/swig/$SWIG_FILE"
SWIG_BUILD=$CRPROPA_DIR"/swig_build"
SWIG_OPTIONS=""

download_install $SWIG_FILE $SWIG_URL $SWIG_BUILD $SWIG_OPTIONS

# FFTW3 install

FFTW_FILE="fftw-3.3.4.tar.gz"
FFTW_URL="http://www.fftw.org/$FFTW_FILE"
FFTW_BUILD=$CRPROPA_DIR"/fftw_build"
FFTW_OPTIONS="--enable-float --enable-shared --with-pic"

download_install $FFTW_FILE $FFTW_URL $FFTW_BUILD $FFTW_OPTIONS

pip_install numpy
