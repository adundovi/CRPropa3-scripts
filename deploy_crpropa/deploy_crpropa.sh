#!/bin/bash

# pretty output
SCRIPT_DIR=`dirname $0`
source $SCRIPT_DIR"/cli_output.sh"


# custom or default path
if [ -n "$1" ]; then
        CRPROPA_DIR=$1;
else
        CRPROPA_DIR=$HOME"/.virtualenvs/crpropa"
fi

announce "Deploy CRPropa3 to $CRPROPA_DIR"

step "Setup python virtualenv"
	$SCRIPT_DIR"/setup_virtualenv.sh" $CRPROPA_DIR > /dev/null 2>&1
verify

step "Activate virtualenv"
	source $CRPROPA_DIR"/bin/activate"
verify

CRPROPA_BUILD=$CRPROPA_DIR"/crpropa3_build"
if [ -d $CRPROPA_BUILD ]; then
    step "Remove old CRPropa build directory"
    rm -rf $CRPROPA_BUILD
    verify
fi

step "Getting CRPropa3 from GitHub"
	CRPROPA_GIT="https://github.com/CRPropa/CRPropa3.git"

	quiet_git() {
	    GIT="`which git`"
	    stdout="gitout"
	    stderr="giterr"

	    if ! $GIT "$@" </dev/null >$stdout 2>$stderr; then
	        cat $stderr >&2
	        rm -f $stdout $stderr
	        Exit 1
	    fi
	
	    rm -f $stdout $stderr
	}

	quiet_git clone $CRPROPA_GIT $CRPROPA_BUILD
	#git reset --hard $CUSTOM_VER
verify

step "Compile and install dependencies: SWIG, FFTW3, numpy"
	$SCRIPT_DIR"/install_deps.sh" $CRPROPA_DIR > /dev/null 2>&1
verify

step "Compile and install CRPropa3"
	$SCRIPT_DIR"/install_crpropa.sh" $CRPROPA_DIR > /dev/null 2>&1
verify

step "Add CRPropa to virtualenv path"
	echo "export LD_LIBRARY_PATH=$CRPROPA_DIR/lib:\$LD_LIBRARY_PATH" >> $CRPROPA_DIR"/bin/activate"
verify

echo
echo "To enter in python's virtualenv with CRPropa support run:"
echo "source $CRPROPA_DIR/bin/activate"

