#!/bin/bash

mkdir -p build
cd build

# Build the package
python ../setup.py sdist bdist_wheel

# Use pip to install the package in editable mode
# and redirect both stdout and stderr to install.log
echo "Installing the package in editable mode..."
pip install -e .. > install.log 2>&1

# Check if the installation was successful
if [ $? -eq 0 ]; then
    echo "Installation successful. Check install.log for details."
else
    echo "Installation failed. Check install.log for details."
fi

rm -rf ../main.egg-info
