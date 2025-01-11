#!/bin/bash
# ==============================================================================
# Script Name: run_script.sh
# Description: Build automation script for Gmail wipe out project
# Author: Alex
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
    echo "Build completed successfullyes"
else
    echo "Build failed"
    exit 1
fi
