#!/bin/bash

if [ -n "$1" ]; then
        CRPROPA_DIR=$1;
else
        echo "Missing CRPropa dir"
	exit;
fi

CRPROPA_BUILD=$CRPROPA_DIR"/crpropa3_build"

mkdir -p $CRPROPA_BUILD"/build"
cd $CRPROPA_BUILD"/build"

CMAKE_PREFIX_PATH=$CRPROPA_DIR cmake -DCMAKE_INSTALL_PREFIX=$CRPROPA_DIR ..

make 
make install

