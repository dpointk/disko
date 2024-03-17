#!/bin/bash

# cd "/home/$USER/Desktop/Disko/feature-1/code" || exit

# Create the db
db_create() {
    python3 db_create.py
    if [ $? -ne 0 ]; then
        exit 1
    fi
    sleep 2
    echo "Database created!"
}

# Create the statistics
statistics() {
    echo "Calculating statistics..."
    python3 statistics.py
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

# Add the clusters to db
clusters() {
    echo "Scanning for clusters..."
    python3 clusters.py
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

# Delete the db
cleanup() {
    echo "Cleaning up..."
    sudo rm -rf "/home/$USER/Desktop/Disko/src/__pycache__/" 
    sudo rm -rf "/home/$USER/Desktop/Disko/src/disko/__pycache__/"
    sudo rm -rf image_data.db
    sleep 2
    echo "Cleaned up!" 
}

# main
if [ "$1" == "-d" ]; then
    cleanup
    exit 0
fi

db_create
clusters
statistics
