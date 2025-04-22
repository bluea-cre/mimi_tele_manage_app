#!/bin/bash

mkdir -p build
cd build

# Prompt user for actions
echo "Select actions to perform (you can select multiple options):"
echo "1. Install the package in editable mode"
echo "2. Build executable with terminal"
echo "3. Build executable without terminal"
read -p "Enter your choices (e.g., 1 2 3): " choices

# Loop through user choices
for choice in $choices; do
    case $choice in
        1)
            # Install the package in editable mode
            echo "Installing the package in editable mode..."
            pip install -e .. > install.log 2>&1

            # Check if the installation was successful
            if [ $? -eq 0 ]; then
                echo "Installation successful. Check install.log for details."
            else
                echo "Installation failed. Check install.log for details."
            fi
            rm -rf ../main.egg-info
            ;;
        2)
            # Use pyinstaller to create an executable with terminal
            echo "Building executable with terminal..."
            pyinstaller --onefile ../main/main.py --distpath ./bin/with_terminal --name main

            # Check if the executable was created successfully
            if [ $? -eq 0 ]; then
                echo "Executable run with terminal created successfully."
            else
                echo "Failed to create executable run with terminal."
            fi
            ;;
        3)
            # Use pyinstaller to create an executable without terminal
            echo "Building executable without terminal..."
            pyinstaller --onefile --noconsole --strip ../main/main.py --distpath ./bin/without_terminal --name main

            # Check if the executable was created successfully
            if [ $? -eq 0 ]; then
                echo "Executable run without terminal created successfully."
            else
                echo "Failed to create executable run without terminal."
            fi
            ;;
        *)
            echo "Invalid choice: $choice"
            ;;
    esac
done