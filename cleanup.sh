#!/bin/bash

# Delete the db
cleanup() {
    echo "Cleaning up..."
    sudo rm -rf "/home/$USER/Desktop/disko/src/__pycache__/" 
    sudo rm -rf "/home/$USER/Desktop/disko/src/disko/__pycache__/"
    sudo rm -rf "/home/$USER/Desktop/disko/src/mvc/__pycache__/"
    sudo rm -rf image_data.db
    sleep 1
    echo "Cleaned up!" 
}

# main
cleanup
