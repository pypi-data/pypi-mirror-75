#!/bin/sh

MAJOR_MINOR="2.10"

pip install --user antsibull
git clone git@github.com:ansible-community/ansible-build-data
mkdir built
antsibull-build build-single 2.10.0a7 --build-file ansible-build-data/${MAJOR_MINOR}/acd-${MAJOR_MINOR}.build --dest-dir built

#pip install twine
#twine upload built/ansible-2.10.0a7.tar.gz