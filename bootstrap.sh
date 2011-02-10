#!/bin/bash

# Creates a new virtualenv with no site package
virtualenv --no-site-packages --distribute . &&
# Activates the newly created virtualenv
source ./bin/activate &&
# Installs the requirements to the new virtualenv
if [ -f ./requirements.txt ]; then
	pip install -r ./requirements.txt 
fi
