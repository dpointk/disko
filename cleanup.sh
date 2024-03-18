#!/bin/bash

# Delete the db
cleanup() {
    echo "Cleaning up..."
    sudo rm -rf "./src/__pycache__/" 
    sudo rm -rf "./src/disko/__pycache__/"
    sudo rm -rf "./src/mvc/__pycache__/"
    sudo rm -rf image_data.db
    sleep 1
    echo "Cleaned up!" 
}

# main
cleanup
