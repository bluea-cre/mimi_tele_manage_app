#!/bin/bash

echo "Cleaning project..."

# Remove build artifacts
echo "Removing build/ directory..."
rm -rf build/

echo "Removing dist/ directory..."
rm -rf dist/

echo "Removing *.egg-info directories..."
rm -rf *.egg-info
rm -rf */*.egg-info

# Remove Python cache files
echo "Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Removing *.pyc and *.pyo files..."
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

echo "Project cleaned successfully!"