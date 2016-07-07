#!/bin/bash

# Setup python virtualenv without root privileges

if [ -n "$1" ]; then
	VIRTENV_DIR=$1;
else
	VIRTENV_DIR=$HOME"/python_virtenv";
fi


function install_virtualenv_old {
	# Old way of installing virtualenv	

	VIRTPY_URL="http://peak.telecommunity.com/dist/virtual-python.py"
	EZSETUP_URL="http://peak.telecommunity.com/dist/ez_setup.py"

	BOOTSTRAP_DIR=$HOME"/.bootstrap_virtenv"

	SYS_PYTHON=`which python2.7`
	WGET="`which wget`"
	export PYTHONPATH=$BOOTSTRAP_DIR"/lib/python2.6/site-packages"

	# Prepare bootstrap dir
	mkdir -p $BOOTSTRAP_DIR

	# Download and install virtual-python, easy_install and virtualenv
	$WGET --directory-prefix=$BOOTSTRAP_DIR $VIRTPY_URL $EZSETUP_URL
	$SYS_PYTHON $BOOTSTRAP_DIR"/virtual-python.py" --prefix=$BOOTSTRAP_DIR --no-site-packages
	$BOOTSTRAP_DIR"/bin/python" $BOOTSTRAP_DIR"/ez_setup.py" --prefix=$BOOTSTRAP_DIR setuptools
	$BOOTSTRAP_DIR"/bin/easy_install" --prefix=$BOOTSTRAP_DIR virtualenv

	VIRTENV=$BOOTSTRAP_DIR"/bin/virtualenv"

	# setup new virtualenv
	VIRTENV=$BOOTSTRAP_DIR"/bin/virtualenv"
	$VIRTENV $VIRTENV_DIR --no-site-packages

        # remove bootstrap directory
        rm -rf $BOOTSTRAP_DIR
}

function install_virtualenv_new {
	# New way of installing virtualenv (recommanded)

	BOOTSTRAP_DIR=$HOME"/.bootstrap_virtenv"
	VIRTENV_URL="https://github.com/pypa/virtualenv/archive/15.0.2.zip"
    VIRTENV_DIR=$1

	WGET="`which wget`"
	UNZIP="`which unzip`"
    SYS_PYTHON=`which python2.7`

	$WGET --directory-prefix=$BOOTSTRAP_DIR $VIRTENV_URL 
	$UNZIP -o $BOOTSTRAP_DIR"/15.0.2.zip" -d $BOOTSTRAP_DIR
	
	# setup new virtualenv
	VIRTENV=$BOOTSTRAP_DIR"/virtualenv-15.0.2/virtualenv.py"
	$SYS_PYTHON $VIRTENV $VIRTENV_DIR --no-site-packages

	# remove bootstrap directory
	#rm -rf $BOOTSTRAP_DIR
}

if ! [ -d "$VIRTENV_DIR" ]; then
    mkdir $VIRTENV_DIR
    install_virtualenv_new $VIRTENV_DIR
fi


