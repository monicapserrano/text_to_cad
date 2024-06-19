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
rm -f "$SOURCE_DIR"/*.buildinfo
rm -f "$SOURCE_DIR"/*.changes
rm -f "$SOURCE_DIR"/*.deb

# Set the target directory where .deb files are stored
TARGET_DIR="./debian_files"

# Ensure the target directory exists
echo "Cleaning $TARGET_DIR" containing .deb files
if [ -d "$TARGET_DIR" ]; then
    rm -rf "$TARGET_DIR"

else
    echo "$TARGET_DIR does not exist, skipping .deb files cleanup"
fi

# Iterate over each subdirectory in the source directory
for PACKAGE_DIR in "$SOURCE_DIR"/*; do
    if [ -d "$PACKAGE_DIR" ]; then
        # Skip the target directory
        if [ "$PACKAGE_DIR" == "$TARGET_DIR" ]; then
            continue
        fi

        echo "Cleaning build files in $PACKAGE_DIR"

        # Change to the package directory
        cd "$PACKAGE_DIR"

        # Remove build artifacts
        rm -rf build
        rm -rf .pybuild
        rm -rf python/*.egg-info

        DEBIAN_DIR="debian"

        # Files to keep
        KEEP_FILES=("changelog" "control" "copyright" "rules")

        # Convert array to a pattern for the find command
        KEEP_PATTERN=$(printf "! -name %s " "${KEEP_FILES[@]}")

        # Remove all files and directories inside DEBIAN_DIR except for the specified files
        find "$DEBIAN_DIR" -mindepth 1 -maxdepth 1 $KEEP_PATTERN -exec rm -rf {} +

        # Move back to the source directory
        cd ..
    fi
done

echo "All build files have been cleaned."
