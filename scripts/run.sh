#!/bin/bash

# Ensure the run directory exists
mkdir -p build/run
cd build/run

# Check if the main.py file exists
if [ ! -f ../../main/main.py ]; then
    echo "Error: main.py not found in ../../main/"
    echo "Please ensure the file exists and try again."
    exit 1
fi

# Run the Python script and pass all arguments
echo "Running main.py with arguments: $@"
python ../../main/main.py "$@"

# Check if the script executed successfully
if [ $? -eq 0 ]; then
    echo "Script executed successfully."
else
    echo "Error: Script execution failed."
    exit 1
fi