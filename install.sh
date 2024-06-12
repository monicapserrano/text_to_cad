#!/bin/bash

# Exit immediately if any command fails
set -e

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Set the source directory containing the package directories
SOURCE_DIR="."

# Set the target directory where .deb files will be stored
TARGET_DIR="./debian_files"

# Ensure the target directory exists
mkdir -p "$TARGET_DIR"

# Iterate over each subdirectory in the source directory
for PACKAGE_DIR in "$SOURCE_DIR"/*; do
    echo $PACKAGE_DIR;
    if [ -d "$PACKAGE_DIR" ]; then
        # Skip the target directory
        if [ "$PACKAGE_DIR" == "$TARGET_DIR" ]; then
            continue
        fi

        echo "Building package in $PACKAGE_DIR"

        # Change to the package directory
        cd "$PACKAGE_DIR"

        # Build the package
        dpkg-buildpackage -us -uc -b

        # Move the .deb files to the target directory
        mv ../*.deb "../$TARGET_DIR"

        # Move back to the source directory
        cd ..
    fi
done

echo "All packages have been built and stored in $TARGET_DIR"

# Install all .deb files in the target directory
cd "$TARGET_DIR"
sudo dpkg -i *.deb

echo "All .deb files have been installed"
