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
    echo $4
    ./configure --prefix=$CRPROPA_DIR $4
	make
	make install

}

function pip_install {
	pip install $1
}

# SWIG install
SWIG_FILE="swig-3.0.7.tar.gz"
SWIG_URL="http://prdownloads.sourceforge.net/swig/$SWIG_FILE"
SWIG_BUILD=$CRPROPA_DIR"/swig_build"
SWIG_OPTIONS=""

download_install $SWIG_FILE $SWIG_URL $SWIG_BUILD $SWIG_OPTIONS

# FFTW3 install
FFTW_FILE="fftw-3.3.4.tar.gz"
FFTW_URL="http://www.fftw.org/$FFTW_FILE"
FFTW_BUILD=$CRPROPA_DIR"/fftw_build"
FFTW_OPTIONS="--enable-float --enable-shared CFLAGS=-fPIC"

download_install $FFTW_FILE $FFTW_URL $FFTW_BUILD "$FFTW_OPTIONS"

# muparser install
MUPARS_FILE="v2.2.5.tar.gz"
MUPARS_URL="https://github.com/beltoforion/muparser/archive/$MUPARS_FILE"
MUPARS_BUILD=$CRPROPA_DIR"/muparser_build"
MUPARS_OPTIONS=""

download_install $MUPARS_FILE $MUPARS_URL $MUPARS_BUILD $MUPARS_OPTIONS

# numpy
pip_install numpy
