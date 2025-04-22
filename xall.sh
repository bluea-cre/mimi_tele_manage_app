#!/bin/bash

echo "Cleaning all untracked files and directories..."

# Dry run to show what will be removed
echo "Performing a dry run to show untracked files and directories:"
git clean -ndx

# Confirm with the user before proceeding
read -p "Do you want to proceed with cleaning these files? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborting clean operation."
    exit 0
fi

# Clean all untracked files and directories
echo "Cleaning untracked files and directories..."
git clean -fdx

echo "Cleanup complete!"