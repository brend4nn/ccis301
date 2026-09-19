#!/bin/bash
# Setup script for Grade System project

# Exit on error
set -e

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install the package
pip install -e .

# Verify installation
python -c "import grade_system; print('Grade System package installed successfully')"

# Run tests
pytest tests/

# Verify new commands
echo "Testing new CLI commands..."
grade-system add-student TestStudent 90,85
grade-system update-student TestStudent 95,90
grade-system add-course Math "Alice:90,Bob:85"
grade-system delete-course Math
grade-system export-summary summary.txt

echo "Project setup complete. Run 'source venv/bin/activate' to activate the virtual environment."