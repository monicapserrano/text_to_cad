#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Directory containing .deb files
DEBIAN_FILES_DIR="./debian_files"

# Check if the directory exists
if [ -d "$DEBIAN_FILES_DIR" ]; then
    # Iterate over each .deb file in the directory
    for DEB_FILE in "$DEBIAN_FILES_DIR"/*.deb; do
        # Extract the package name from the .deb file
        PACKAGE_NAME=$(dpkg-deb --info "$DEB_FILE" | grep 'Package:' | awk '{print $2}')

        # Uninstall the package
        echo "Uninstalling $PACKAGE_NAME..."
        sudo dpkg --remove "$PACKAGE_NAME"
    done

    echo "All packages from $DEBIAN_FILES_DIR have been uninstalled."
else
    echo "Directory $DEBIAN_FILES_DIR does not exist."
fi
