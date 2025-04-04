#!/bin/bash
set -eaux

SCRIPT_DIR=$(realpath $(dirname "$0"))

# Make sure pip-tools is installed first
pip list | grep "pip-tools"
if [ $? == 1 ]; then
  pip install pip-tools
fi

cd $SCRIPT_DIR/../

echo
echo "~~~~~~~~~~"
echo "Updating requirements.txt"
pip-compile -v -o requirements.txt pyproject.toml

echo
echo "~~~~~~~~~~"
echo "Updating requirements-google.txt"
pip-compile -v --extra google -o requirements-google.txt pyproject.toml
