#!/bin/bash

echo "~~~~~~~~~~"
if [ "$1" == "--upgrade" ]; then
  echo "Upgrading all pip dependencies. To install without upgrading pinned versions, run without the --upgrade flag"
else
  echo "Installing all pip dependencies. To upgrade pinned versions, run with the --upgrade flag"
fi

# Make sure pip-tools is installed first
pip list | grep "pip-tools"
if [ $? == 1 ]; then
  pip install pip-tools
fi

# shellcheck disable=SC2034
export CUSTOM_COMPILE_COMMAND="./pip-install.sh"

echo
echo "~~~~~~~~~~"
echo "Updating requirements.txt"
pip-compile requirements.in "$@"

echo
echo "~~~~~~~~~~"
echo "Installing all dependencies"
pip-sync requirements.txt
