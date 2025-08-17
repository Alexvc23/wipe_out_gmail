#!/bin/bash
# ==============================================================================
# Author: Alex
# Script: run_script.sh
# Description: Automates the Docker-based build process for the Gmail wipe-out application
#
# This script performs the following operations:
# 1. Enables debug mode with set -x
# 2. Checks if Docker is running and starts it if needed
# 3. Changes to the project directory
# 4. Verifies the presence of a Makefile
# 5. Executes the make command
# 6. Shuts down Docker after successful build
#
# Dependencies:
#   - Docker Desktop for macOS
#   - osascript (macOS)
#   - make
#
# Usage: ./run_script.sh
#
# Exit codes:
#   0 - Success
#   1 - Error (Docker start failure, directory change failure, missing Makefile, or build failure)
#
# Author: Alex
# Path: /Users/alex/Documents/programing/python/wipe_out_gmail/run_script.sh
# ==============================================================================

set -x
echo "Debugging the script..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Starting Docker..."
    # For macOS
    open -a Docker
    # Wait for Docker to start (max 30 seconds)
    for i in {1..30}; do
        if docker info > /dev/null 2>&1; then
            echo "Docker is now running"
            break
        fi
        echo "Waiting for Docker to start..."
        sleep 1
        if [ $i -eq 30 ]; then
            echo "Error: Docker failed to start"
            exit 1
        fi
    done
fi

# Set the working directory
cd /Users/alex/brige-projects/programing/python/wipe_out_gmail || { echo "Error: Failed to change directory"; exit 1; }

# Check if Makefile exists
if [ ! -f "Makefile" ]; then
    echo "Error: Makefile not found in current directory"
    exit 1
fi

# Run make
make up

# Check if make command was successful
if [ $? -eq 0 ]; then
    echo "Build completed successfully"
    echo "Will shutdown Docker in 30 seconds..."
    sleep 30
    osascript -e 'quit app "Docker Desktop"'
else
    echo "Build failed"
    exit 1
fi
