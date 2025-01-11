# Your script logic
#!/bin/bash
# ==============================================================================
# Script Name: run_script.sh
# Description: Build automation script for Gmail wipe out project
# Author: Alex
# ==============================================================================
#
# This script performs the following operations:
# 1. Enables debug mode for shell script execution
# 2. Changes to the project directory
# 3. Verifies the existence of a Makefile
# 4. Executes the make command to build the project
# 5. Validates the build process success
#
# Exit codes:
#   0 - Success
#   1 - Failed to change directory
#   1 - Makefile not found
#   1 - Build process failed
#
# Usage: ./run_script.sh
# ==============================================================================

set -x
echo "Debugging the script..."
# Set the working directory
cd /Users/alex/Documents/programing/python/wipe_out_gmail || { echo "Error: Failed to change directory"; exit 1; }

# Check if Makefile exists
if [ ! -f "Makefile" ]; then
    echo "Error: Makefile not found in current directory"
    exit 1
fi

# Run make
make

# Check if make command was successful
if [ $? -eq 0 ]; then
    echo "Build completed successfully"
else
    echo "Build failed"
    exit 1
fi
